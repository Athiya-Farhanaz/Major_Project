import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import time
import os
import sys
import json
import psutil
from datetime import datetime

# Add the project root directory to the python path to resolve imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import (
    MODEL_PATH, PREPROCESSOR_PATH, BASELINE_TRAIN_SIZE,
    SIMULATION_TICK_RATE, DRIFT_WINDOW_SIZE, DRIFT_ALPHA
)
from src.data_generator import NetworkTrafficSimulator
from src.preprocessor import NetworkPreprocessor
from src.model import AnomalyDetector
from src.drift_detector import ConceptDriftDetector
from src.xai_engine import NetworkXAI

# Set page configuration
st.set_page_config(
    page_title="Real-Time XAI Network Anomaly Detector",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- Helper Functions -----------------

def initialize_models_if_needed():
    """Generates baseline data and trains initial models if they don't exist."""
    if not os.path.exists(MODEL_PATH) or not os.path.exists(PREPROCESSOR_PATH):
        with st.spinner("Training baseline anomaly detection models. Please wait..."):
            sim = NetworkTrafficSimulator(random_state=42)
            df_baseline = sim.generate_baseline(BASELINE_TRAIN_SIZE)
            
            preprocessor = NetworkPreprocessor()
            X_train = preprocessor.fit_transform(df_baseline)
            preprocessor.save()
            
            detector = AnomalyDetector()
            detector.fit(X_train)
            detector.save()
            st.success("Baseline models successfully trained!")
            time.sleep(1)

def retrain_model_on_drift():
    """Retrains the model using the current window buffer as new normal baseline."""
    st.session_state.is_retraining = True
    
    recent_flows_df = pd.DataFrame(st.session_state.flow_history)
    # Security filter: retrain ONLY on traffic classified as normal by the model
    # to prevent poisoning from active attacks during baseline adaptation.
    normal_flows = recent_flows_df[recent_flows_df['pred_anomaly'] == 0]
    
    if len(normal_flows) < 200:
        normal_flows = st.session_state.simulator.generate_baseline(500)
    
    X_train_new = st.session_state.preprocessor.fit_transform(normal_flows)
    st.session_state.preprocessor.save()
    
    st.session_state.detector.fit(X_train_new)
    st.session_state.detector.save()
    
    bg_samples = X_train_new[:min(len(X_train_new), 150)]
    st.session_state.xai = NetworkXAI(
        st.session_state.detector,
        st.session_state.preprocessor,
        bg_samples
    )
    
    st.session_state.drift_detector.reset_reference(normal_flows)
    
    retrain_time = datetime.now().strftime("%H:%M:%S")
    st.session_state.retrain_events.append(f"Model retrained at {retrain_time} (Adaptive realignment)")
    st.session_state.is_retraining = False

# ----------------- Session State Initialization -----------------

initialize_models_if_needed()

if 'simulator' not in st.session_state:
    st.session_state.simulator = NetworkTrafficSimulator(random_state=42)
    st.session_state.preprocessor = NetworkPreprocessor.load()
    st.session_state.detector = AnomalyDetector.load()
    
    df_baseline = st.session_state.simulator.generate_baseline(150)
    X_bg = st.session_state.preprocessor.transform(df_baseline)
    st.session_state.xai = NetworkXAI(st.session_state.detector, st.session_state.preprocessor, X_bg)
    
    st.session_state.drift_detector = ConceptDriftDetector(df_baseline)
    
    st.session_state.flow_history = []
    st.session_state.anomalies = []
    st.session_state.drift_alerts = []
    st.session_state.retrain_events = []
    st.session_state.p_values_history = {feat: [] for feat in st.session_state.drift_detector.features_to_monitor}
    st.session_state.p_values_history['step'] = []
    st.session_state.scores_history = []
    st.session_state.predict_latencies = []
    st.session_state.shap_latencies = []
    st.session_state.stream_active = False
    st.session_state.is_retraining = False
    st.session_state.step = 0
    st.session_state.forced_attack = None

# ----------------- Sidebar resources monitoring -----------------

st.sidebar.header("Simulation Control Panel")

# Streaming state
if st.session_state.stream_active:
    btn_label = "Pause Live Stream"
else:
    btn_label = "Start Live Stream"

if st.sidebar.button(btn_label, use_container_width=True):
    st.session_state.stream_active = not st.session_state.stream_active
    st.rerun()

tick_rate = st.sidebar.slider("Stream Speed (Seconds/Flow)", 0.05, 2.0, SIMULATION_TICK_RATE)

st.sidebar.markdown("---")
st.sidebar.header("Traffic Disturbance Controls")

drift_sim = st.sidebar.checkbox("Simulate Concept Drift (VPN/WFH Shift)")
st.session_state.simulator.set_drift(drift_sim)

auto_retrain = st.sidebar.checkbox("Auto-Retrain Model on Drift", value=True)

# Force anomaly buttons
st.sidebar.subheader("Inject Simulated Attacks")
c1, c2 = st.sidebar.columns(2)
if c1.button("SYN Flood", use_container_width=True):
    st.session_state.forced_attack = "syn_flood"
if c2.button("Brute Force", use_container_width=True):
    st.session_state.forced_attack = "brute_force"

c3, c4 = st.sidebar.columns(2)
if c3.button("Data Exfiltration", use_container_width=True):
    st.session_state.forced_attack = "data_exfiltration"
if c4.button("Port Scan", use_container_width=True):
    st.session_state.forced_attack = "port_scan"

st.sidebar.markdown("---")
st.sidebar.header("System Actions")
if st.sidebar.button("Retrain Model Manually", use_container_width=True):
    with st.spinner("Retraining model..."):
        retrain_model_on_drift()
    st.sidebar.success("Retrained successfully!")

if st.sidebar.button("Reset Entire System", use_container_width=True):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# Real Resource Monitoring
st.sidebar.markdown("---")
st.sidebar.header("Application Resources")
try:
    process = psutil.Process(os.getpid())
    cpu_percent = psutil.cpu_percent()
    memory_mb = process.memory_info().rss / (1024 * 1024)
    st.sidebar.metric("Process CPU Usage", f"{cpu_percent:.1f}%")
    st.sidebar.metric("Process Memory Allocation", f"{memory_mb:.1f} MB")
except Exception:
    st.sidebar.info("Resource metrics unavailable on this system configuration.")

# ----------------- Dashboard Main Layout -----------------

st.title("🛡️ Real-Time Adaptive & Explainable Network Anomaly Detection")

# Core framing: Streaming Anomaly Explanation + Drift-Triggered Adaptive Retraining
st.markdown(
    """
    > **Core Technical Novelty:** This system features a hybrid pipeline combining 
    > **(1) real-time streaming anomaly explanations** via local Shapley feature attribution (SHAP) and 
    > **(2) drift-triggered adaptive model retraining** using Kolmogorov-Smirnov statistical tests. 
    > Unlike static detection models, this system continuously detects, explains, and self-corrects in response to shifting network distributions.
    """
)

# Tabs
tab1, tab2 = st.tabs(["⚡ Real-Time Streaming Detection & XAI", "📊 Offline Validation & Benchmarks (UNSW-NB15)"])

# ----------------- Tab 1: Real-Time Stream -----------------
with tab1:
    # Row 1: KPI Metrics
    kpi_placeholder = st.empty()

    # Row 2: Live Charts
    chart_col1, chart_col2 = st.columns([2, 1])
    with chart_col1:
        st.subheader("Live Traffic Anomaly Score Window")
        score_plot_placeholder = st.empty()
    with chart_col2:
        st.subheader("Traffic Composition")
        comp_plot_placeholder = st.empty()

    # Row 3: Alert Console & XAI Panel
    st.markdown("---")
    alert_col, xai_col = st.columns([1, 1])

    with alert_col:
        st.subheader("⚠️ Anomalous Flow Alert Console")
        alert_console_placeholder = st.empty()

    with xai_col:
        st.subheader("🔍 Explainable AI (SHAP) Insights")
        xai_placeholder = st.empty()

    # Row 4: Concept Drift Monitor
    st.markdown("---")
    drift_col1, drift_col2 = st.columns([2, 1])
    with drift_col1:
        st.subheader("📈 Statistical Drift Tracking (p-values)")
        drift_plot_placeholder = st.empty()
    with drift_col2:
        st.subheader("⚙️ System Event Log")
        log_placeholder = st.empty()

# ----------------- Tab 2: Offline Validation (UNSW-NB15) -----------------
with tab2:
    st.header("Offline Performance Validation on UNSW-NB15 Dataset")
    st.write(
        "To evaluate our unsupervised anomaly detection approach in a static, real-world setting, "
        "we run offline validation benchmarks against the modern **UNSW-NB15** cybersecurity dataset. "
        "The evaluation trains the Isolation Forest using pure normal network flows, sets the threshold at the 98th "
        "percentile of training scores, and evaluates against a balanced test set containing mixed normal and attack traffic."
    )

    metrics_path = os.path.join("data", "offline_metrics.json")
    if os.path.exists(metrics_path):
        with open(metrics_path, "r") as f:
            offline_metrics = json.load(f)
            
        # Extract individual model metrics
        if_metrics = offline_metrics["isolation_forest"]
        ocsvm_metrics = offline_metrics["one_class_svm"]
            
        # Display KPIs for our chosen model (Isolation Forest)
        mc1, mc2, mc3, mc4, mc5 = st.columns(5)
        mc1.metric("ROC-AUC Score", f"{if_metrics['roc_auc']:.4f}")
        mc2.metric("Accuracy", f"{if_metrics['accuracy'] * 100:.2f}%")
        mc3.metric("Precision", f"{if_metrics['precision'] * 100:.2f}%")
        mc4.metric("Recall", f"{if_metrics['recall'] * 100:.2f}%")
        mc5.metric("F1-Score", f"{if_metrics['f1_score']:.4f}")
        
        # Display Comparative Table
        st.subheader("Unsupervised Model Performance Comparison")
        st.write(
            "The comparison highlights the efficiency and accuracy tradeoffs between models. "
            "Isolation Forest maintains higher ROC-AUC and scales linear-logarithmically on the full training set. "
            "One-Class SVM is constrained by $O(N^3)$ computational scaling, necessitating downsampling for training."
        )
        comparison_data = {
            "Performance Metric": ["ROC-AUC", "Accuracy", "Precision", "Recall", "F1-Score", "Training Time"],
            "Isolation Forest (Full Set - Chosen)": [
                f"{if_metrics['roc_auc']:.4f}",
                f"{if_metrics['accuracy'] * 100:.2f}%",
                f"{if_metrics['precision'] * 100:.2f}%",
                f"{if_metrics['recall'] * 100:.2f}%",
                f"{if_metrics['f1_score']:.4f}",
                f"{if_metrics['train_time']:.3f}s"
            ],
            "One-Class SVM (Sampled 5,000)": [
                f"{ocsvm_metrics['roc_auc']:.4f}",
                f"{ocsvm_metrics['accuracy'] * 100:.2f}%",
                f"{ocsvm_metrics['precision'] * 100:.2f}%",
                f"{ocsvm_metrics['recall'] * 100:.2f}%",
                f"{ocsvm_metrics['f1_score']:.4f}",
                f"{ocsvm_metrics['train_time']:.3f}s"
            ]
        }
        st.table(pd.DataFrame(comparison_data))
        
        # Display Details and Confusion Matrix
        col_m1, col_m2 = st.columns([1, 1])
        with col_m1:
            st.subheader("Confusion Matrix (Isolation Forest)")
            cm = if_metrics["confusion_matrix"]
            z = [[cm["tn"], cm["fp"]], [cm["fn"], cm["tp"]]]
            x = ["Predicted Normal", "Predicted Attack"]
            y = ["Actual Normal", "Actual Attack"]
            fig_cm = px.imshow(
                z, x=x, y=y,
                labels=dict(x="Predicted Label", y="Actual Label", color="Count"),
                color_continuous_scale="Blues",
                text_auto=True
            )
            fig_cm.update_layout(margin=dict(l=20, r=20, t=10, b=20), height=300)
            st.plotly_chart(fig_cm, use_container_width=True)
            
        with col_m2:
            st.subheader("Evaluation Set Details")
            st.write(f"**Dataset Source:** UNSW-NB15 Partitioned Testing Set")
            st.write(f"**Baseline Normal Training Flows:** 29,600 records")
            st.write(f"**Mixed Evaluation Flows:** 14,800 records (balanced)")
            st.write(f"**Evaluated At:** `{offline_metrics['evaluated_at']}`")
            
            # Show attack categories count
            st.write("**Traffic Categories Evaluated:**")
            cat_df = pd.DataFrame(
                list(offline_metrics["attack_categories"].items()),
                columns=["Traffic Class", "Record Count"]
            )
            st.dataframe(cat_df, use_container_width=True, hide_index=True)
    else:
        st.warning(
            "Offline validation metrics have not been generated yet. "
            "Please run `python -m src.offline_validation` to download the UNSW-NB15 dataset "
            "and compute offline validation metrics."
        )

# ----------------- Streaming Execution Loop -----------------

if st.session_state.stream_active:
    st.session_state.step += 1
    
    # 1. Generate traffic flow
    force_attack = st.session_state.forced_attack
    st.session_state.forced_attack = None  # Reset trigger
    
    raw_flow = st.session_state.simulator.generate_single_flow(force_anomaly_type=force_attack)
    st.session_state.flow_history.append(raw_flow)
    
    # Limit flow history size
    if len(st.session_state.flow_history) > 400:
        st.session_state.flow_history.pop(0)

    # 2. Run Inference with Latency Timers
    t_start = time.perf_counter()
    df_single = pd.DataFrame([raw_flow])
    X_single = st.session_state.preprocessor.transform(df_single)
    is_anomaly, score = st.session_state.detector.predict(X_single)
    predict_latency_ms = (time.perf_counter() - t_start) * 1000
    st.session_state.predict_latencies.append(predict_latency_ms)
    if len(st.session_state.predict_latencies) > 200:
        st.session_state.predict_latencies.pop(0)
    
    raw_flow['anomaly_score'] = float(score[0])
    raw_flow['pred_anomaly'] = int(is_anomaly[0])
    raw_flow['timestamp'] = datetime.now().strftime("%H:%M:%S")
    raw_flow['predict_latency_ms'] = predict_latency_ms
    
    st.session_state.scores_history.append(float(score[0]))
    if len(st.session_state.scores_history) > 100:
        st.session_state.scores_history.pop(0)

    # 3. Add to anomalies if flagged
    if is_anomaly[0] == 1:
        t_shap_start = time.perf_counter()
        # Calculate SHAP explanation immediately
        explanation = st.session_state.xai.explain_instance(raw_flow, X_single)
        shap_latency_ms = (time.perf_counter() - t_shap_start) * 1000
        st.session_state.shap_latencies.append(shap_latency_ms)
        if len(st.session_state.shap_latencies) > 100:
            st.session_state.shap_latencies.pop(0)
            
        anomaly_alert = {
            "index": len(st.session_state.anomalies),
            "timestamp": raw_flow['timestamp'],
            "score": raw_flow['anomaly_score'],
            "protocol": raw_flow['protocol_type'],
            "service": raw_flow['service'],
            "src_bytes": raw_flow['src_bytes'],
            "dst_bytes": raw_flow['dst_bytes'],
            "label": raw_flow['label'],
            "explanation": explanation,
            "raw_record": raw_flow,
            "predict_latency_ms": predict_latency_ms,
            "shap_latency_ms": shap_latency_ms
        }
        st.session_state.anomalies.append(anomaly_alert)
        if len(st.session_state.anomalies) > 50:
            st.session_state.anomalies.pop(0)

    # 4. Concept Drift Detection
    drift_detected, p_values = st.session_state.drift_detector.update(raw_flow)
    
    # Log p-values
    st.session_state.p_values_history['step'].append(st.session_state.step)
    for feat in st.session_state.drift_detector.features_to_monitor:
        st.session_state.p_values_history[feat].append(p_values.get(feat, 1.0))
        
    if len(st.session_state.p_values_history['step']) > 150:
        st.session_state.p_values_history['step'].pop(0)
        for feat in st.session_state.drift_detector.features_to_monitor:
            st.session_state.p_values_history[feat].pop(0)

    # 5. Handle Drift Alert & Auto Retrain
    if drift_detected:
        alert_time = datetime.now().strftime("%H:%M:%S")
        st.session_state.drift_alerts.append(f"Concept Drift detected at {alert_time}!")
        if len(st.session_state.drift_alerts) > 10:
            st.session_state.drift_alerts.pop(0)
            
        if auto_retrain and not st.session_state.is_retraining:
            retrain_model_on_drift()


# ----------------- UI Drawing Routine (Tab 1 Elements Only) -----------------

if st.session_state.flow_history:
    df_hist = pd.DataFrame(st.session_state.flow_history)
    total_processed = len(df_hist)
    pred_anomaly_rate = df_hist['pred_anomaly'].mean() * 100
    
    gt_anomalies = df_hist['is_anomaly'].values
    pred_anomalies = df_hist['pred_anomaly'].values
    
    correct = (gt_anomalies == pred_anomalies).sum()
    accuracy = (correct / total_processed) * 100 if total_processed > 0 else 100.0
else:
    total_processed = 0
    pred_anomaly_rate = 0.0
    accuracy = 100.0

current_phase_name = st.session_state.simulator.current_phase
phase_color = "red" if "Drift" in current_phase_name else "green"

# Compute median latencies
if st.session_state.predict_latencies:
    median_pred_lat = np.median(st.session_state.predict_latencies)
else:
    median_pred_lat = 0.0

if st.session_state.shap_latencies:
    median_shap_lat = np.median(st.session_state.shap_latencies)
else:
    median_shap_lat = 0.0

with kpi_placeholder.container():
    c1_1, c1_2, c1_3, c1_4 = st.columns(4)
    c1_1.metric("Flows Processed (Session)", f"{total_processed}")
    c1_2.metric("Detected Anomaly Rate", f"{pred_anomaly_rate:.2f}%")
    c1_3.metric("System Accuracy (vs Ground Truth)", f"{accuracy:.1f}%")
    
    drift_alert_state = "⚠️ DRIFT ALERT" if st.session_state.drift_alerts else "✅ STABLE"
    c1_4.markdown(f"**Traffic Phase:** <span style='color:{phase_color};font-weight:bold'>{current_phase_name}</span>", unsafe_allow_html=True)
    c1_4.markdown(f"**Drift Status:** {drift_alert_state}")
    c1_4.markdown(f"**Anomaly Threshold:** `{st.session_state.detector.threshold:.4f}`")
    
    # Latency and performance telemetry row
    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    c2_1, c2_2, c2_3, c2_4 = st.columns(4)
    c2_1.metric("Median Inference Latency", f"{median_pred_lat:.2f} ms")
    c2_2.metric("Median SHAP Explanation", f"{median_shap_lat:.1f} ms" if median_shap_lat > 0 else "N/A")
    c2_3.write("")  # Spacer
    c2_4.write("")  # Spacer


# Draw Anomaly Score Chart
if st.session_state.scores_history:
    scores = st.session_state.scores_history
    steps = list(range(max(0, st.session_state.step - len(scores)), st.session_state.step))
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=steps, y=scores,
        mode='lines',
        name='Anomaly Score',
        line=dict(color='#1f77b4', width=2)
    ))
    fig.add_hline(
        y=st.session_state.detector.threshold,
        line_dash="dash",
        line_color="red",
        annotation_text="Anomaly Threshold",
        annotation_position="top left"
    )
    fig.update_layout(
        margin=dict(l=20, r=20, t=10, b=20),
        height=260,
        xaxis_title="Step Number",
        yaxis_title="Isolation Forest Score",
        yaxis=dict(range=[0.25, 0.85]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    score_plot_placeholder.plotly_chart(fig, use_container_width=True)
else:
    score_plot_placeholder.info("Waiting for data stream to begin...")


# Draw Protocol Composition Chart
if st.session_state.flow_history:
    df_hist = pd.DataFrame(st.session_state.flow_history)
    proto_counts = df_hist['protocol_type'].value_counts().reset_index()
    proto_counts.columns = ['Protocol', 'Count']
    
    fig = px.bar(
        proto_counts, x='Protocol', y='Count',
        color='Protocol',
        color_discrete_map={'tcp': '#636EFA', 'udp': '#EF553B', 'icmp': '#00CC96'}
    )
    fig.update_layout(
        margin=dict(l=20, r=20, t=10, b=20),
        height=260,
        showlegend=False
    )
    comp_plot_placeholder.plotly_chart(fig, use_container_width=True)
else:
    comp_plot_placeholder.info("No composition data yet.")


# Draw Alert Console
with alert_console_placeholder.container():
    if st.session_state.anomalies:
        anom_list = st.session_state.anomalies[::-1]
        
        options = [
            f"ID {a['index']} | Time: {a['timestamp']} | Score: {a['score']:.3f} | Attack: {a['label']}"
            for a in anom_list
        ]
        
        selected_option = st.selectbox(
            "Select an anomaly alert below to inspect its Explainable AI (SHAP) details:",
            options=options,
            key="anomaly_selector"
        )
        
        selected_id = int(selected_option.split(" | ")[0].replace("ID ", ""))
        selected_anomaly = next(a for a in st.session_state.anomalies if a['index'] == selected_id)
        st.session_state.selected_anomaly = selected_anomaly
        
        table_data = []
        for a in anom_list[:10]:
            table_data.append({
                "ID": a['index'],
                "Timestamp": a['timestamp'],
                "Score": f"{a['score']:.3f}",
                "Protocol": a['protocol'],
                "Service": a['service'],
                "Bytes Sent": a['src_bytes'],
                "Bytes Rcvd": a['dst_bytes'],
                "Threat Label": a['label']
            })
        st.dataframe(pd.DataFrame(table_data), use_container_width=True, hide_index=True)
    else:
        st.info("No anomalies detected yet. Use 'Traffic Disturbance Controls' in the sidebar to inject attacks!")
        st.session_state.selected_anomaly = None


# Draw XAI Panel
with xai_placeholder.container():
    if 'selected_anomaly' in st.session_state and st.session_state.selected_anomaly is not None:
        anomaly = st.session_state.selected_anomaly
        explanation = anomaly['explanation']
        raw_rec = anomaly['raw_record']
        
        mc1, mc2, mc3 = st.columns(3)
        mc1.metric("Anomaly Score", f"{anomaly['score']:.3f}")
        mc2.metric("Ground Truth Label", anomaly['label'])
        mc3.metric("Timestamp", anomaly['timestamp'])
        
        grouped_shap = explanation['grouped_shap_values']
        sorted_shap = sorted(grouped_shap.items(), key=lambda x: abs(x[1]), reverse=True)
        plot_features = [x[0] for x in sorted_shap[:7]]
        plot_values = [x[1] for x in sorted_shap[:7]]
        
        colors = ['#EF553B' if val > 0 else '#636EFA' for val in plot_values]
        
        fig = go.Figure(go.Bar(
            x=plot_values,
            y=plot_features,
            orientation='h',
            marker_color=colors
        ))
        
        fig.update_layout(
            yaxis=dict(autorange="reversed"),
            title="Feature Contributions to Anomaly Decision (Shapley Values)",
            xaxis_title="Anomaly Contribution Strength",
            margin=dict(l=20, r=20, t=30, b=20),
            height=250
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("#### Natural Language Explanation")
        st.markdown(explanation['explanation_text'])
        
        with st.expander("Show Raw Connection Details"):
            st.json(raw_rec)
    else:
        st.info("Please start the stream and select an anomaly from the left panel to inspect explainable AI insights.")


# Draw Concept Drift P-Values Chart
if st.session_state.p_values_history['step']:
    hist_p = st.session_state.p_values_history
    steps = hist_p['step']
    
    fig = go.Figure()
    for feat in st.session_state.drift_detector.features_to_monitor:
        fig.add_trace(go.Scatter(
            x=steps, y=hist_p[feat],
            mode='lines',
            name=feat
        ))
        
    fig.add_hline(
        y=DRIFT_ALPHA,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Drift Threshold (alpha={DRIFT_ALPHA})",
        annotation_position="bottom left"
    )
    
    fig.update_layout(
        margin=dict(l=20, r=20, t=10, b=20),
        height=220,
        xaxis_title="Step Number",
        yaxis_title="KS-test p-value",
        yaxis=dict(type='log', range=[-10, 0]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    drift_plot_placeholder.plotly_chart(fig, use_container_width=True)
else:
    drift_plot_placeholder.info("Concept drift monitoring will activate once the window buffers are full.")


# Draw Event Log Console
with log_placeholder.container():
    st.markdown("##### System Alerts & Logs")
    logs = []
    
    for a in st.session_state.drift_alerts:
        logs.append(f"🚩 **Drift Alert:** {a}")
        
    for e in st.session_state.retrain_events:
        logs.append(f"🔄 **Retrain:** {e}")
        
    if not logs:
        st.write("System operating normally. No alerts or maintenance events logged.")
    else:
        for log in logs[::-1][:10]:
            st.markdown(log)

# Auto-refresh mechanism
if st.session_state.stream_active:
    time.sleep(tick_rate)
    st.rerun()
