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
    SIMULATION_TICK_RATE, DRIFT_WINDOW_SIZE, DRIFT_ALPHA,
    SHAP_BACKGROUND_SIZE
)
from src.data_generator import NetworkTrafficSimulator
from src.preprocessor import NetworkPreprocessor
from src.model import AnomalyDetector
from src.drift_detector import ConceptDriftDetector
from src.xai_engine import NetworkXAI

# Set page configuration
st.set_page_config(
    page_title="Real-Time XAI Network Anomaly Detection System",
    page_icon="🛡️",
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
    
    bg_samples = X_train_new[:min(len(X_train_new), SHAP_BACKGROUND_SIZE)]
    st.session_state.xai = NetworkXAI(
        st.session_state.detector,
        st.session_state.preprocessor,
        bg_samples
    )
    
    st.session_state.drift_detector.reset_reference(normal_flows)
    
    retrain_time = datetime.now().strftime("%H:%M:%S")
    log_msg = f"Model retrained at {retrain_time} (Filtered {len(recent_flows_df) - len(normal_flows)} anomalous flows)"
    st.session_state.retrain_events.append(log_msg)
    st.session_state.timeline_events.append({
        "step": st.session_state.step,
        "type": "retrain",
        "label": "Adaptive Retrain"
    })
    st.session_state.is_retraining = False

def calculate_severity(score: float, threshold: float) -> tuple:
    """Returns (severity_label, badge_color)."""
    if score >= threshold * 1.25:
        return "CRITICAL", "#FF4B4B"
    elif score >= threshold * 1.10:
        return "HIGH", "#FFA500"
    else:
        return "ELEVATED", "#FFD700"

# ----------------- Session State Initialization -----------------

initialize_models_if_needed()

if 'simulator' not in st.session_state:
    st.session_state.simulator = NetworkTrafficSimulator(random_state=42)
    st.session_state.preprocessor = NetworkPreprocessor.load()
    st.session_state.detector = AnomalyDetector.load()
    
    df_baseline = st.session_state.simulator.generate_baseline(SHAP_BACKGROUND_SIZE)
    X_bg = st.session_state.preprocessor.transform(df_baseline)
    st.session_state.xai = NetworkXAI(st.session_state.detector, st.session_state.preprocessor, X_bg)
    
    st.session_state.drift_detector = ConceptDriftDetector(df_baseline)
    
    st.session_state.flow_history = []
    st.session_state.anomalies = []
    st.session_state.drift_alerts = []
    st.session_state.retrain_events = []
    st.session_state.timeline_events = []
    st.session_state.p_values_history = {feat: [] for feat in st.session_state.drift_detector.features_to_monitor}
    st.session_state.p_values_history['step'] = []
    st.session_state.scores_history = []
    st.session_state.predict_latencies = []
    st.session_state.shap_latencies = []
    st.session_state.stream_active = False
    st.session_state.is_retraining = False
    st.session_state.step = 0
    st.session_state.forced_attack = None
    st.session_state.attack_burst = None
    st.session_state.stats = {"tp": 0, "fp": 0, "fn": 0, "tn": 0}

# ----------------- Sidebar Controls -----------------

st.sidebar.title("🛡️ SOC Operations Console")
st.sidebar.markdown("---")

# Streaming state
col_s1, col_s2 = st.sidebar.columns(2)
if st.session_state.stream_active:
    if col_s1.button("⏸️ Pause", use_container_width=True):
        st.session_state.stream_active = False
        st.rerun()
else:
    if col_s1.button("▶️ Start Stream", use_container_width=True):
        st.session_state.stream_active = True
        st.rerun()

if col_s2.button("🔄 Reset", use_container_width=True):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

tick_rate = st.sidebar.slider("Flow Rate (Sec / Flow)", 0.05, 2.0, SIMULATION_TICK_RATE, 0.05)

# Sensitivity slider
st.sidebar.subheader("🎛️ Detection Sensitivity")
sensitivity_mult = st.sidebar.slider(
    "Threshold Multiplier", 
    0.80, 1.25, 1.00, 0.05,
    help="Scales dynamic threshold (lower multiplier = more sensitive, higher = conservative)"
)
effective_threshold = st.session_state.detector.threshold * sensitivity_mult

st.sidebar.markdown("---")
st.sidebar.header("⚡ Live Threat Injection")
st.sidebar.caption("Inject sustained attack waves to test real-time detection & SHAP explanation:")

b1, b2 = st.sidebar.columns(2)
if b1.button("🌊 SYN Flood Wave", use_container_width=True):
    st.session_state.attack_burst = {"type": "syn_flood", "name": "SYN Flood Wave", "remaining": 8, "total": 8}
if b2.button("🔨 Brute Force Wave", use_container_width=True):
    st.session_state.attack_burst = {"type": "brute_force", "name": "SSH Brute Force", "remaining": 8, "total": 8}

b3, b4 = st.sidebar.columns(2)
if b3.button("📤 Data Exfil Wave", use_container_width=True):
    st.session_state.attack_burst = {"type": "data_exfiltration", "name": "Data Exfiltration", "remaining": 6, "total": 6}
if b4.button("🔎 Port Scan Sweep", use_container_width=True):
    st.session_state.attack_burst = {"type": "port_scan", "name": "Port Scan Sweep", "remaining": 8, "total": 8}

with st.sidebar.expander("Single-Shot Injections"):
    s1, s2 = st.columns(2)
    if s1.button("Single SYN", use_container_width=True):
        st.session_state.forced_attack = "syn_flood"
    if s2.button("Single Brute", use_container_width=True):
        st.session_state.forced_attack = "brute_force"

st.sidebar.markdown("---")
st.sidebar.header("🌐 Concept Drift Simulation")
drift_sim = st.sidebar.toggle("Simulate WFH / VPN Traffic Shift", value=st.session_state.simulator.drift_active)
st.session_state.simulator.set_drift(drift_sim)

auto_retrain = st.sidebar.checkbox("Autonomous Retraining on Drift", value=True)

if st.sidebar.button("Force Manual Retrain", use_container_width=True):
    with st.spinner("Executing adaptive retraining..."):
        retrain_model_on_drift()
    st.sidebar.success("Model realigned with latest baseline!")

# Resource Telemetry
st.sidebar.markdown("---")
st.sidebar.subheader("💻 System Telemetry")
try:
    process = psutil.Process(os.getpid())
    cpu_percent = psutil.cpu_percent()
    memory_mb = process.memory_info().rss / (1024 * 1024)
    r1, r2 = st.sidebar.columns(2)
    r1.metric("CPU Load", f"{cpu_percent:.1f}%")
    r2.metric("Memory", f"{memory_mb:.1f} MB")
except Exception:
    st.sidebar.caption("Hardware telemetry unavailable.")

# ----------------- Main UI Layout -----------------

st.title("🛡️ Autonomous Network Anomaly Detection with Explainable AI & Adaptive Retraining")

# Attack Wave Alert Banner
if st.session_state.attack_burst and st.session_state.attack_burst['remaining'] > 0:
    burst = st.session_state.attack_burst
    st.warning(
        f"🚨 **ACTIVE ATTACK WAVE SIMULATION:** `{burst['name']}` "
        f"— Remaining Packets: **{burst['remaining']}/{burst['total']}** | Analyzing real-time model response..."
    )

tab1, tab2, tab3 = st.tabs([
    "⚡ Real-Time Detection & XAI Console", 
    "📈 Concept Drift & Adaptability Forensics",
    "📊 Offline Benchmark (UNSW-NB15)"
])

# ----------------- Tab 1: Real-Time Stream -----------------
with tab1:
    # Top Row: SOC Telemetry Gauges
    gauge_placeholder = st.empty()
    
    # Second Row: Key Performance Indicators
    kpi_placeholder = st.empty()

    # Third Row: Real-time Timeline & Composition
    chart_col1, chart_col2 = st.columns([2, 1])
    with chart_col1:
        st.subheader("🌐 Unified Real-Time Attack & Anomaly Timeline")
        timeline_placeholder = st.empty()
    with chart_col2:
        st.subheader("📊 Traffic Distribution")
        comp_plot_placeholder = st.empty()

    # Fourth Row: Alert Console & XAI Panel
    st.markdown("---")
    alert_col, xai_col = st.columns([1, 1])

    with alert_col:
        st.subheader("⚠️ Live Security Incident Console")
        alert_console_placeholder = st.empty()

    with xai_col:
        st.subheader("🔍 Explainable AI (SHAP Waterfall Attribution)")
        xai_placeholder = st.empty()

    # Fifth Row: Incident Report Export
    st.markdown("---")
    export_placeholder = st.empty()

# ----------------- Tab 2: Concept Drift & Adaptability -----------------
with tab2:
    st.header("📈 Concept Drift & Continuous Adaptation Telemetry")
    st.write(
        "Modern network environments experience natural distribution shifts (e.g., shifts to remote work, "
        "cloud migrations, new protocols). This system employs **two-sample Kolmogorov-Smirnov (KS) tests** "
        "with **Bonferroni family-wise error rate correction** to detect genuine statistical drift while suppressing false alarms. "
        "Upon drift verification, an **anti-poisoning filter** extracts verified normal traffic to retrain the model autonomously."
    )
    
    dcol1, dcol2 = st.columns([2, 1])
    with dcol1:
        st.subheader("Statistical Drift Tracking (Per-Feature p-values)")
        drift_plot_placeholder = st.empty()
    with dcol2:
        st.subheader("🛡️ Retraining & Maintenance Audit Log")
        log_placeholder = st.empty()

# ----------------- Tab 3: Offline Validation (UNSW-NB15) -----------------
with tab3:
    st.header("📊 Benchmark Evaluation on UNSW-NB15 Cybersecurity Dataset")
    st.write(
        "To establish academic credibility, the unsupervised Isolation Forest model was evaluated against the "
        "modern **UNSW-NB15** cybersecurity benchmark and compared directly with **One-Class Support Vector Machine (OC-SVM)**."
    )

    metrics_path = os.path.join("data", "offline_metrics.json")
    if os.path.exists(metrics_path):
        with open(metrics_path, "r") as f:
            offline_metrics = json.load(f)
            
        if_metrics = offline_metrics["isolation_forest"]
        ocsvm_metrics = offline_metrics["one_class_svm"]
            
        mc1, mc2, mc3, mc4, mc5 = st.columns(5)
        mc1.metric("ROC-AUC Score", f"{if_metrics['roc_auc']:.4f}")
        mc2.metric("Accuracy", f"{if_metrics['accuracy'] * 100:.2f}%")
        mc3.metric("Precision", f"{if_metrics['precision'] * 100:.2f}%")
        mc4.metric("Recall", f"{if_metrics['recall'] * 100:.2f}%")
        mc5.metric("F1-Score", f"{if_metrics['f1_score']:.4f}")
        
        st.subheader("Algorithmic Comparison: Isolation Forest vs One-Class SVM")
        st.write(
            "Isolation Forest demonstrates superior computational scaling ($O(N \\log N)$ vs $O(N^3)$), "
            "enabling full-scale real-time inference without training-time downsampling."
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
        
        col_m1, col_m2 = st.columns([1, 1])
        with col_m1:
            st.subheader("Confusion Matrix (Isolation Forest on UNSW-NB15)")
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
            st.subheader("Dataset Details")
            st.write(f"**Source:** UNSW Sydney Cyber Research Group (UNSW-NB15)")
            st.write(f"**Baseline Normal Training Flows:** 29,600 records")
            st.write(f"**Mixed Evaluation Flows:** 14,800 records (balanced)")
            st.write(f"**Evaluated At:** `{offline_metrics['evaluated_at']}`")
            
            cat_df = pd.DataFrame(
                list(offline_metrics["attack_categories"].items()),
                columns=["Traffic Category", "Sample Count"]
            )
            st.dataframe(cat_df, use_container_width=True, hide_index=True)
    else:
        st.warning("Offline validation metrics have not been generated yet. Run `python -m src.offline_validation`.")

# ----------------- Streaming Execution Loop -----------------

if st.session_state.stream_active:
    st.session_state.step += 1
    
    # 1. Determine attack injection
    force_attack = None
    if st.session_state.attack_burst and st.session_state.attack_burst['remaining'] > 0:
        force_attack = st.session_state.attack_burst['type']
        st.session_state.attack_burst['remaining'] -= 1
        if st.session_state.attack_burst['remaining'] <= 0:
            st.session_state.attack_burst = None
    elif st.session_state.forced_attack:
        force_attack = st.session_state.forced_attack
        st.session_state.forced_attack = None  # Reset single-shot
    
    # 2. Generate traffic flow
    raw_flow = st.session_state.simulator.generate_single_flow(force_anomaly_type=force_attack)
    
    # 3. Run Inference with Latency Timing
    t_start = time.perf_counter()
    df_single = pd.DataFrame([raw_flow])
    X_single = st.session_state.preprocessor.transform(df_single)
    
    # Calculate continuous score and dynamic decision
    raw_scores = st.session_state.detector.get_anomaly_score(X_single)
    current_score = float(raw_scores[0])
    is_anomaly = int(current_score > effective_threshold)
    predict_latency_ms = (time.perf_counter() - t_start) * 1000
    
    st.session_state.predict_latencies.append(predict_latency_ms)
    if len(st.session_state.predict_latencies) > 200:
        st.session_state.predict_latencies.pop(0)
    
    raw_flow['anomaly_score'] = current_score
    raw_flow['pred_anomaly'] = is_anomaly
    raw_flow['timestamp'] = datetime.now().strftime("%H:%M:%S")
    raw_flow['step'] = st.session_state.step
    raw_flow['predict_latency_ms'] = predict_latency_ms
    
    # Update live session confusion matrix stats
    gt = raw_flow['is_anomaly']
    pred = is_anomaly
    if gt == 1 and pred == 1:
        st.session_state.stats["tp"] += 1
    elif gt == 0 and pred == 1:
        st.session_state.stats["fp"] += 1
    elif gt == 1 and pred == 0:
        st.session_state.stats["fn"] += 1
    else:
        st.session_state.stats["tn"] += 1
    
    st.session_state.flow_history.append(raw_flow)
    if len(st.session_state.flow_history) > 400:
        st.session_state.flow_history.pop(0)
    
    st.session_state.scores_history.append({
        "step": st.session_state.step,
        "score": current_score,
        "is_anomaly": is_anomaly,
        "label": raw_flow['label']
    })
    if len(st.session_state.scores_history) > 100:
        st.session_state.scores_history.pop(0)

    # 4. Compute XAI Explanation for Flagged Flows
    if is_anomaly == 1:
        t_shap_start = time.perf_counter()
        explanation = st.session_state.xai.explain_instance(raw_flow, X_single)
        shap_latency_ms = (time.perf_counter() - t_shap_start) * 1000
        
        st.session_state.shap_latencies.append(shap_latency_ms)
        if len(st.session_state.shap_latencies) > 100:
            st.session_state.shap_latencies.pop(0)
            
        severity, color = calculate_severity(current_score, effective_threshold)
        
        anomaly_alert = {
            "index": len(st.session_state.anomalies) + 1,
            "step": st.session_state.step,
            "timestamp": raw_flow['timestamp'],
            "score": current_score,
            "severity": severity,
            "color": color,
            "protocol": raw_flow['protocol_type'],
            "service": raw_flow['service'],
            "src_bytes": raw_flow['src_bytes'],
            "dst_bytes": raw_flow['dst_bytes'],
            "duration": raw_flow['duration'],
            "label": raw_flow['label'],
            "explanation": explanation,
            "raw_record": raw_flow,
            "predict_latency_ms": predict_latency_ms,
            "shap_latency_ms": shap_latency_ms
        }
        st.session_state.anomalies.append(anomaly_alert)
        st.session_state.timeline_events.append({
            "step": st.session_state.step,
            "type": "anomaly",
            "label": raw_flow['label']
        })
        if len(st.session_state.anomalies) > 80:
            st.session_state.anomalies.pop(0)

    # 5. Concept Drift Detection Update
    drift_detected, p_values = st.session_state.drift_detector.update(raw_flow)
    
    st.session_state.p_values_history['step'].append(st.session_state.step)
    for feat in st.session_state.drift_detector.features_to_monitor:
        st.session_state.p_values_history[feat].append(p_values.get(feat, 1.0))
        
    if len(st.session_state.p_values_history['step']) > 150:
        st.session_state.p_values_history['step'].pop(0)
        for feat in st.session_state.drift_detector.features_to_monitor:
            st.session_state.p_values_history[feat].pop(0)

    # 6. Handle Drift Triggers
    if drift_detected:
        alert_time = datetime.now().strftime("%H:%M:%S")
        st.session_state.drift_alerts.append(f"Statistically significant distribution drift verified at {alert_time}")
        st.session_state.timeline_events.append({
            "step": st.session_state.step,
            "type": "drift",
            "label": "Drift Detected"
        })
        if len(st.session_state.drift_alerts) > 10:
            st.session_state.drift_alerts.pop(0)
            
        if auto_retrain and not st.session_state.is_retraining:
            retrain_model_on_drift()

# ----------------- UI Rendering Routine -----------------

# 1. Render Gauges
latest_score = st.session_state.scores_history[-1]['score'] if st.session_state.scores_history else 0.45
min_p_val = 1.0
if st.session_state.p_values_history['step']:
    recent_p_vals = [st.session_state.p_values_history[f][-1] for f in st.session_state.drift_detector.features_to_monitor if st.session_state.p_values_history[f]]
    if recent_p_vals:
        min_p_val = min(recent_p_vals)

drift_risk_pct = max(0.0, min(100.0, (1.0 - min_p_val) * 100))

with gauge_placeholder.container():
    g1, g2, g3 = st.columns(3)
    
    # Anomaly Score Gauge
    fig_g1 = go.Figure(go.Indicator(
        mode="gauge+number",
        value=latest_score,
        title={'text': "Live Flow Anomaly Score"},
        gauge={
            'axis': {'range': [0.2, 0.9]},
            'bar': {'color': "#FF4B4B" if latest_score > effective_threshold else "#1f77b4"},
            'steps': [
                {'range': [0.2, effective_threshold * 0.95], 'color': "rgba(44, 160, 44, 0.2)"},
                {'range': [effective_threshold * 0.95, effective_threshold], 'color': "rgba(255, 215, 0, 0.3)"},
                {'range': [effective_threshold, 0.9], 'color': "rgba(255, 75, 75, 0.35)"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': effective_threshold
            }
        }
    ))
    fig_g1.update_layout(height=160, margin=dict(l=20, r=20, t=25, b=10))
    g1.plotly_chart(fig_g1, use_container_width=True)
    
    # Drift Risk Gauge
    fig_g2 = go.Figure(go.Indicator(
        mode="gauge+number",
        value=drift_risk_pct,
        number={'suffix': "%"},
        title={'text': "Concept Drift Risk (KS-Test)"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "#FF4B4B" if drift_risk_pct > 90 else ("#FFA500" if drift_risk_pct > 60 else "#2ca02c")},
            'steps': [
                {'range': [0, 60], 'color': "rgba(44, 160, 44, 0.2)"},
                {'range': [60, 90], 'color': "rgba(255, 165, 0, 0.2)"},
                {'range': [90, 100], 'color': "rgba(255, 75, 75, 0.3)"}
            ]
        }
    ))
    fig_g2.update_layout(height=160, margin=dict(l=20, r=20, t=25, b=10))
    g2.plotly_chart(fig_g2, use_container_width=True)
    
    # System Health & Latency Metric Gauge
    med_pred = np.median(st.session_state.predict_latencies) if st.session_state.predict_latencies else 0.8
    med_shap = np.median(st.session_state.shap_latencies) if st.session_state.shap_latencies else 0.0
    
    fig_g3 = go.Figure(go.Indicator(
        mode="number+delta",
        value=med_pred,
        number={'suffix': " ms"},
        title={'text': "Median Detection Latency"},
        delta={'reference': 5.0, 'decreasing': {'color': "green"}, 'increasing': {'color': "red"}}
    ))
    fig_g3.update_layout(height=160, margin=dict(l=20, r=20, t=25, b=10))
    g3.plotly_chart(fig_g3, use_container_width=True)

# 2. Render KPI Metrics Bar
total_processed = len(st.session_state.flow_history)
pred_anomaly_rate = (len(st.session_state.anomalies) / total_processed * 100) if total_processed > 0 else 0.0

st_stats = st.session_state.stats
tp = st_stats["tp"]
fp = st_stats["fp"]
fn = st_stats["fn"]
tn = st_stats["tn"]
session_acc = ((tp + tn) / (tp + fp + fn + tn) * 100) if (tp + fp + fn + tn) > 0 else 100.0
session_prec = (tp / (tp + fp) * 100) if (tp + fp) > 0 else 100.0
session_rec = (tp / (tp + fn) * 100) if (tp + fn) > 0 else 100.0
session_f1 = (2 * session_prec * session_rec / (session_prec + session_rec)) if (session_prec + session_rec) > 0 else 0.0

current_phase_name = st.session_state.simulator.current_phase
phase_color = "#FF4B4B" if "Drift" in current_phase_name else "#00CC96"

with kpi_placeholder.container():
    k1, k2, k3, k4, k5, k6 = st.columns(6)
    k1.metric("Flows Inspected", f"{total_processed}")
    k2.metric("Detected Threats", f"{len(st.session_state.anomalies)}")
    k3.metric("Live Accuracy", f"{session_acc:.1f}%")
    k4.metric("Live Precision", f"{session_prec:.1f}%")
    k5.metric("Live Recall", f"{session_rec:.1f}%")
    k6.metric("Active Threshold", f"{effective_threshold:.4f}")

# 3. Render Unified Timeline Plot
if st.session_state.scores_history:
    df_scores = pd.DataFrame(st.session_state.scores_history)
    
    fig_time = go.Figure()
    
    # Base Anomaly Score Stream
    fig_time.add_trace(go.Scatter(
        x=df_scores['step'],
        y=df_scores['score'],
        mode='lines',
        name='Anomaly Score',
        line=dict(color='#1f77b4', width=2)
    ))
    
    # Dynamic Threshold Line
    fig_time.add_hline(
        y=effective_threshold,
        line_dash="dash",
        line_color="red",
        annotation_text="Anomaly Decision Boundary",
        annotation_position="top left"
    )
    
    # Anomaly Spikes Highlight
    anom_points = df_scores[df_scores['score'] > effective_threshold]
    if not anom_points.empty:
        fig_time.add_trace(go.Scatter(
            x=anom_points['step'],
            y=anom_points['score'],
            mode='markers',
            name='Threat Detected',
            text=anom_points['label'],
            marker=dict(color='red', size=9, symbol='x')
        ))
    
    fig_time.update_layout(
        margin=dict(l=20, r=20, t=10, b=20),
        height=260,
        xaxis_title="Simulation Flow Index",
        yaxis_title="Score",
        yaxis=dict(range=[0.25, 0.85]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    timeline_placeholder.plotly_chart(fig_time, use_container_width=True)
else:
    timeline_placeholder.info("Click '▶️ Start Stream' in the sidebar to begin real-time traffic inspection.")

# 4. Render Traffic Composition
if st.session_state.flow_history:
    df_hist = pd.DataFrame(st.session_state.flow_history)
    proto_counts = df_hist['protocol_type'].value_counts().reset_index()
    proto_counts.columns = ['Protocol', 'Count']
    
    fig_comp = px.bar(
        proto_counts, x='Protocol', y='Count',
        color='Protocol',
        color_discrete_map={'tcp': '#636EFA', 'udp': '#EF553B', 'icmp': '#00CC96'}
    )
    fig_comp.update_layout(margin=dict(l=20, r=20, t=10, b=20), height=260, showlegend=False)
    comp_plot_placeholder.plotly_chart(fig_comp, use_container_width=True)
else:
    comp_plot_placeholder.info("Awaiting network flows...")

# 5. Render Alert Console
with alert_console_placeholder.container():
    if st.session_state.anomalies:
        anom_list = st.session_state.anomalies[::-1]
        
        options = [
            f"ID #{a['index']} | {a['timestamp']} | [{a['severity']}] {a['label']} | Score: {a['score']:.3f}"
            for a in anom_list
        ]
        
        selected_option = st.selectbox(
            "Select an incident to investigate with SHAP Explainable AI:",
            options=options,
            key="anomaly_selector"
        )
        
        selected_id = int(selected_option.split(" | ")[0].replace("ID #", ""))
        selected_anomaly = next((a for a in st.session_state.anomalies if a['index'] == selected_id), None)
        st.session_state.selected_anomaly = selected_anomaly
        
        # Incident table
        tbl = []
        for a in anom_list[:8]:
            tbl.append({
                "ID": a['index'],
                "Severity": a['severity'],
                "Time": a['timestamp'],
                "Threat Type": a['label'],
                "Score": f"{a['score']:.3f}",
                "Proto": a['protocol'].upper(),
                "Service": a['service'],
                "Bytes Sent": a['src_bytes']
            })
        st.dataframe(pd.DataFrame(tbl), use_container_width=True, hide_index=True)
    else:
        st.info("System clean. No anomalous flows detected. Inject attack waves from the sidebar to trigger alerts!")
        st.session_state.selected_anomaly = None

# 6. Render Explainable AI (SHAP Waterfall)
with xai_placeholder.container():
    if 'selected_anomaly' in st.session_state and st.session_state.selected_anomaly is not None:
        anomaly = st.session_state.selected_anomaly
        explanation = anomaly['explanation']
        raw_rec = anomaly['raw_record']
        
        # Header metrics
        m1, m2, m3 = st.columns(3)
        m1.markdown(f"**Threat:** `{anomaly['label']}`")
        m2.markdown(f"**Severity:** <span style='color:{anomaly['color']};font-weight:bold;'>{anomaly['severity']}</span>", unsafe_allow_html=True)
        m3.markdown(f"**Anomaly Score:** `{anomaly['score']:.4f}`")
        
        # Interactive SHAP Waterfall Chart
        grouped_shap = explanation['grouped_shap_values']
        sorted_shap = sorted(grouped_shap.items(), key=lambda x: abs(x[1]), reverse=True)[:6]
        
        base_val = explanation.get('base_value', 0.50)
        waterfall_x = ["Baseline Normal"]
        waterfall_y = [base_val]
        waterfall_measures = ["absolute"]
        
        for feat, val in sorted_shap:
            waterfall_x.append(f"{feat}")
            waterfall_y.append(val)
            waterfall_measures.append("relative")
            
        waterfall_x.append("Final Score")
        waterfall_y.append(None)
        waterfall_measures.append("total")
        
        fig_waterfall = go.Figure(go.Waterfall(
            orientation="v",
            measure=waterfall_measures,
            x=waterfall_x,
            textposition="outside",
            text=[f"{v:+.2f}" if v is not None else "" for v in waterfall_y],
            y=waterfall_y,
            increasing={"marker": {"color": "#FF4B4B"}},
            decreasing={"marker": {"color": "#2CA02C"}},
            totals={"marker": {"color": "#1F77B4"}},
            connector={"line": {"color": "rgb(63, 63, 63)"}}
        ))
        fig_waterfall.update_layout(
            title="Local Shapley Attribution Waterfall (How Features Drove Decision)",
            height=250,
            margin=dict(l=20, r=20, t=35, b=20),
            showlegend=False
        )
        st.plotly_chart(fig_waterfall, use_container_width=True)
        
        # Plain-English Explanation
        st.markdown("##### 📝 Plain-English Security Explanation")
        st.markdown(explanation['explanation_text'])
        
        with st.expander("🔍 Inspect Full Raw Network Flow Packet Data"):
            st.json(raw_rec)
    else:
        st.info("Select an anomaly from the Incident Console to generate instant SHAP explanations.")

# 7. Render Incident Report CSV Export
with export_placeholder.container():
    if st.session_state.anomalies:
        export_records = []
        for a in st.session_state.anomalies:
            top_factors = ", ".join([f"{item['feature']} ({item['contribution']:+.2f})" for item in a['explanation']['top_contributors'][:3]])
            export_records.append({
                "Incident_ID": a['index'],
                "Timestamp": a['timestamp'],
                "Threat_Type": a['label'],
                "Severity": a['severity'],
                "Anomaly_Score": a['score'],
                "Protocol": a['protocol'],
                "Service": a['service'],
                "Src_Bytes": a['src_bytes'],
                "Dst_Bytes": a['dst_bytes'],
                "Duration_Sec": a['duration'],
                "Inference_Latency_ms": a['predict_latency_ms'],
                "SHAP_Latency_ms": a['shap_latency_ms'],
                "Top_Contributing_Features": top_factors,
                "Plain_English_Diagnosis": a['explanation']['explanation_text'].replace("\n", " ")
            })
        df_export = pd.DataFrame(export_records)
        csv_data = df_export.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="📥 Export Full Incident Forensics Report (CSV)",
            data=csv_data,
            file_name=f"soc_incident_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )

# 8. Render Concept Drift Telemetry (Tab 2)
if st.session_state.p_values_history['step']:
    hist_p = st.session_state.p_values_history
    steps = hist_p['step']
    
    fig_drift = go.Figure()
    for feat in st.session_state.drift_detector.features_to_monitor:
        fig_drift.add_trace(go.Scatter(
            x=steps, y=hist_p[feat],
            mode='lines',
            name=feat
        ))
        
    bonferroni_threshold = DRIFT_ALPHA / len(st.session_state.drift_detector.features_to_monitor)
    fig_drift.add_hline(
        y=bonferroni_threshold,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Bonferroni Adjusted α = {bonferroni_threshold:.4f}",
        annotation_position="bottom left"
    )
    
    fig_drift.update_layout(
        margin=dict(l=20, r=20, t=10, b=20),
        height=260,
        xaxis_title="Flow Step",
        yaxis_title="p-value (Log Scale)",
        yaxis=dict(type='log', range=[-10, 0]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    drift_plot_placeholder.plotly_chart(fig_drift, use_container_width=True)
else:
    drift_plot_placeholder.info("Awaiting window buffer initialization (requires 250 records)...")

with log_placeholder.container():
    logs = []
    for a in st.session_state.drift_alerts:
        logs.append(f"🚩 **Drift:** {a}")
    for e in st.session_state.retrain_events:
        logs.append(f"🔄 **Retrain:** {e}")
    if not logs:
        st.write("No maintenance events. Baseline distributions stable.")
    else:
        for log in logs[::-1][:10]:
            st.markdown(log)

# 9. Auto-Refresh Loop for Live Streaming
if st.session_state.stream_active:
    time.sleep(tick_rate)
    st.rerun()
