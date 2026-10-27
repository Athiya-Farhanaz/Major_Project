import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle
import numpy as np

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUTPUT_DIR, exist_ok=True)

FONT_FAMILY = "DejaVu Sans"
COLOR_PRIMARY = "#1A365D"     # Deep corporate navy
COLOR_SECONDARY = "#2B6CB0"   # Classic slate blue
COLOR_ACCENT = "#C53030"      # Crimson / Red alert
COLOR_GREEN = "#276749"       # Deep green
COLOR_BOX_FILL = "#EDF2F7"    # Soft grey-blue
COLOR_ACTOR = "#E2E8F0"
COLOR_NOTE = "#FEFCBF"
COLOR_LINE = "#2D3748"

def draw_header(ax, title, subtitle):
    ax.text(0.5, 0.965, title, ha='center', va='center', fontsize=24, fontweight='bold',
            color=COLOR_PRIMARY, fontname=FONT_FAMILY, transform=ax.transAxes)
    ax.text(0.5, 0.932, subtitle, ha='center', va='center', fontsize=13.5, fontstyle='italic',
            color='#4A5568', fontname=FONT_FAMILY, transform=ax.transAxes)
    ax.plot([0.08, 0.92], [0.910, 0.910], color='#CBD5E0', lw=2.0, transform=ax.transAxes)

# ==========================================
# 1. USE CASE DIAGRAM
# ==========================================
def generate_use_case_diagram():
    fig, ax = plt.subplots(figsize=(18, 13), dpi=300)
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 13)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    draw_header(ax, "UML Use Case Diagram", "Dynamic Real-Time Network Anomaly Detection & Explainable AI System")

    sys_rect = FancyBboxPatch((4.3, 0.5), 9.4, 10.5, boxstyle="round,pad=0.25",
                              facecolor="#F7FAFC", edgecolor=COLOR_PRIMARY, linewidth=2.4)
    ax.add_patch(sys_rect)
    ax.text(9.0, 10.6, "System Boundary: Real-Time XAI Intrusion Detection System", ha='center', va='center',
            fontsize=14.5, fontweight='bold', color=COLOR_PRIMARY)

    def draw_actor(x, y, name, role):
        head = Circle((x, y + 0.75), 0.38, facecolor=COLOR_ACTOR, edgecolor=COLOR_PRIMARY, lw=2.2)
        ax.add_patch(head)
        ax.plot([x, x], [y + 0.37, y - 0.45], color=COLOR_PRIMARY, lw=2.6)
        ax.plot([x - 0.55, x + 0.55], [y + 0.05, y + 0.05], color=COLOR_PRIMARY, lw=2.6)
        ax.plot([x, x - 0.45], [y - 0.45, y - 1.25], color=COLOR_PRIMARY, lw=2.6)
        ax.plot([x, x + 0.45], [y - 0.45, y - 1.25], color=COLOR_PRIMARY, lw=2.6)
        ax.text(x, y - 1.55, name, ha='center', va='top', fontsize=12.5, fontweight='bold', color=COLOR_PRIMARY)
        ax.text(x, y - 2.25, role, ha='center', va='top', fontsize=10.5, fontstyle='italic', color="#718096")

    draw_actor(2.0, 6.0, "Security Analyst\n/ Administrator", "Primary Actor\n(Monitoring & Control)")
    draw_actor(16.0, 6.0, "Network Gateway\n/ Traffic Stream", "Automated Actor\n(Telemetry Source)")

    use_cases = [
        (9.0, 9.7, "UC1: Configure & Start Live Network Stream", "#EBF8FF"),
        (9.0, 8.4, "UC2: Simulate Cyber Threats & Traffic Shifts\n(SYN Flood, Brute Force, Exfiltration, VPN Drift)", "#FFF5F5"),
        (9.0, 7.1, "UC3: Inspect Real-Time Telemetry & Latencies\n(Inference Speed < 2ms, SHAP Overhead ~100ms)", "#F0FFF4"),
        (9.0, 5.7, "UC4: Unsupervised Anomaly Detection\n(Online Isolation Forest & Dynamic Percentile)", "#EBF8FF"),
        (9.0, 4.3, "UC5: Explain Anomaly with Explainable AI\n(TreeSHAP Local Attributions & Natural Language)", "#FEFCBF"),
        (9.0, 2.9, "UC6: Monitor Statistical Concept Drift\n(Bonferroni-Corrected 2-Sample KS-Tests, p < 0.002)", "#F0FFF4"),
        (9.0, 1.5, "UC7: Trigger Adaptive Retraining\n(Anti-Poisoning Clean Normal Buffer Filter)", "#FFF5F5"),
    ]

    uc_lefts, uc_rights = {}, {}
    for idx, (ux, uy, utext, ucolor) in enumerate(use_cases):
        box_w, box_h = 7.8, 1.05
        uc_box = FancyBboxPatch((ux - box_w/2, uy - box_h/2), box_w, box_h, boxstyle="round,pad=0.2",
                                facecolor=ucolor, edgecolor=COLOR_PRIMARY, lw=1.8)
        ax.add_patch(uc_box)
        ax.text(ux, uy, utext, ha='center', va='center', fontsize=11.2, fontweight='bold', color=COLOR_PRIMARY)
        uc_lefts[idx + 1] = (ux - box_w/2 - 0.25, uy)
        uc_rights[idx + 1] = (ux + box_w/2 + 0.25, uy)

    analyst_pt = (2.6, 6.0)
    for uc_idx in [1, 2, 3, 5, 7]:
        ax.annotate("", xy=uc_lefts[uc_idx], xytext=analyst_pt,
                    arrowprops=dict(arrowstyle="-", color=COLOR_LINE, lw=1.8))

    engine_pt = (15.4, 6.0)
    for uc_idx in [1, 4, 6, 7]:
        ax.annotate("", xy=uc_rights[uc_idx], xytext=engine_pt,
                    arrowprops=dict(arrowstyle="-", color=COLOR_LINE, lw=1.8))

    ax.annotate("«include»\n(upon anomaly detection)", xy=(9.0, 5.0), xytext=(9.0, 5.0),
                ha='center', va='center', fontsize=10.5, color=COLOR_ACCENT, fontweight='bold',
                backgroundcolor="white")
    ax.plot([9.0, 9.0], [5.2, 4.8], color=COLOR_ACCENT, lw=1.6, linestyle='--')

    ax.annotate("«extend»\n[if drift p < 0.002]", xy=(9.0, 2.2), xytext=(9.0, 2.2),
                ha='center', va='center', fontsize=10.5, color=COLOR_GREEN, fontweight='bold',
                backgroundcolor="white")
    ax.plot([9.0, 9.0], [2.4, 2.0], color=COLOR_GREEN, lw=1.6, linestyle='--')

    plt.tight_layout()
    filepath = os.path.join(OUTPUT_DIR, "use_case_diagram.png")
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {filepath}")

# ==========================================
# 2. CLASS DIAGRAM
# ==========================================
def generate_class_diagram():
    fig, ax = plt.subplots(figsize=(22, 14), dpi=300)
    ax.set_xlim(0, 22)
    ax.set_ylim(0, 14)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    draw_header(ax, "UML Class Diagram", "System Architecture, Classes, Attributes, Operations & Structural Relationships")

    def draw_uml_class(x, y, w, h, class_name, stereotype, attributes, methods, fill_color="#F7FAFC"):
        rect = FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0",
                              facecolor=fill_color, edgecolor=COLOR_PRIMARY, lw=2.0)
        ax.add_patch(rect)
        header_h = 1.05
        head_rect = Rectangle((x, y + h - header_h), w, header_h, facecolor=COLOR_PRIMARY, edgecolor=COLOR_PRIMARY, lw=2.0)
        ax.add_patch(head_rect)
        if stereotype:
            ax.text(x + w/2, y + h - 0.30, f"«{stereotype}»", ha='center', va='center', fontsize=10.5, color="#E2E8F0")
            ax.text(x + w/2, y + h - 0.72, class_name, ha='center', va='center', fontsize=13.5, fontweight='bold', color="white")
        else:
            ax.text(x + w/2, y + h - 0.55, class_name, ha='center', va='center', fontsize=14, fontweight='bold', color="white")

        attr_step = 0.35
        attr_h = len(attributes) * attr_step + 0.32
        line_y = y + h - header_h - attr_h
        ax.plot([x, x + w], [line_y, line_y], color=COLOR_PRIMARY, lw=1.4)

        curr_y = y + h - header_h - 0.28
        for attr in attributes:
            ax.text(x + 0.22, curr_y, attr, ha='left', va='top', fontsize=10.5, color="#1A202C", fontfamily="monospace")
            curr_y -= attr_step

        curr_y = line_y - 0.26
        for m in methods:
            ax.text(x + 0.22, curr_y, m, ha='left', va='top', fontsize=10.5, color="#1A202C", fontfamily="monospace")
            curr_y -= attr_step

    sim_attrs = [
        "- rng: np.random.RandomState",
        "- drift_active: bool = False",
        "- current_phase: str",
        "- step_counter: int = 0"
    ]
    sim_methods = [
        "+ set_drift(active: bool): void",
        "+ generate_single_flow(force: str): dict",
        "- _generate_normal(): dict",
        "- _generate_anomaly(type: str): dict",
        "+ generate_baseline(n: int): DataFrame"
    ]
    draw_uml_class(0.8, 7.3, 5.8, 4.9, "NetworkTrafficSimulator", "Entity / Generator", sim_attrs, sim_methods)

    prep_attrs = [
        "- preprocessor: ColumnTransformer",
        "- feature_names: List[str]",
        "- is_fitted: bool = False"
    ]
    prep_methods = [
        "+ fit(df: DataFrame): void",
        "+ transform(df: DataFrame): ndarray",
        "+ fit_transform(df: DataFrame): ndarray",
        "+ get_feature_names(): List[str]",
        "+ save(filepath: str): void",
        "+ load(filepath: str): Preprocessor"
    ]
    draw_uml_class(8.1, 7.3, 5.8, 4.9, "NetworkPreprocessor", "Component / Pipeline", prep_attrs, prep_methods)

    det_attrs = [
        "- model: IsolationForest",
        "- threshold: float = 0.55",
        "- is_trained: bool = False",
        "- contamination: float = 0.01"
    ]
    det_methods = [
        "+ fit(X_train: ndarray): void",
        "+ get_anomaly_score(X): ndarray",
        "+ predict(X): Tuple[ndarray, ndarray]",
        "+ save(filepath: str): void",
        "+ load(filepath: str): Detector"
    ]
    draw_uml_class(15.4, 7.3, 5.8, 4.9, "AnomalyDetector", "ML Model / Engine", det_attrs, det_methods)

    drift_attrs = [
        "- window_size: int = 250",
        "- alpha: float = 0.01",
        "- features_to_monitor: List[str]",
        "- reference_data: Dict[str, ndarray]",
        "- window_buffer: Dict[str, List]",
        "- last_p_values: Dict[str, float]"
    ]
    drift_methods = [
        "+ update(record: dict): Tuple[bool, dict]",
        "- _check_bonferroni(p_vals): bool",
        "+ reset_reference(new_df): void"
    ]
    draw_uml_class(0.8, 1.2, 5.8, 5.3, "ConceptDriftDetector", "Statistical Monitor", drift_attrs, drift_methods)

    xai_attrs = [
        "- detector: AnomalyDetector",
        "- preprocessor: NetworkPreprocessor",
        "- explainer: shap.TreeExplainer",
        "- feature_names: List[str]"
    ]
    xai_methods = [
        "+ explain_instance(raw, X): dict",
        "- _group_categorical_contributions(): dict",
        "- _get_feature_interpretation(f, v): str"
    ]
    draw_uml_class(8.1, 1.2, 5.8, 5.3, "NetworkXAI", "Explainable AI Engine", xai_attrs, xai_methods)

    dash_attrs = [
        "- simulator: NetworkTrafficSimulator",
        "- preprocessor: NetworkPreprocessor",
        "- detector: AnomalyDetector",
        "- drift_detector: ConceptDriftDetector",
        "- xai: NetworkXAI",
        "- stream_active: bool = False"
    ]
    dash_methods = [
        "+ initialize_models_if_needed(): void",
        "+ retrain_model_on_drift(): void",
        "+ render_live_telemetry_tab(): void",
        "+ render_unsw_validation_tab(): void"
    ]
    draw_uml_class(15.4, 1.2, 5.8, 5.3, "StreamlitDashboardController", "UI / Controller", dash_attrs, dash_methods)

    def draw_assoc(x1, y1, x2, y2, label=""):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color=COLOR_PRIMARY, lw=2.0))
        if label:
            mx, my = (x1 + x2)/2, (y1 + y2)/2 + 0.16
            ax.text(mx, my, label, fontsize=11.2, color=COLOR_PRIMARY, fontweight='bold',
                    ha='center', va='bottom', backgroundcolor='white')

    draw_assoc(6.6, 9.7, 8.1, 9.7, "raw flow dict")
    draw_assoc(13.9, 9.7, 15.4, 9.7, "scaled vector X")
    draw_assoc(15.4, 8.2, 13.9, 5.8, "explains model")
    draw_assoc(11.0, 7.3, 11.0, 6.5, "extracts names")
    draw_assoc(18.3, 6.5, 18.3, 7.3, "orchestrates")
    draw_assoc(15.4, 3.8, 13.9, 3.8, "queries local SHAP")
    draw_assoc(8.1, 3.8, 6.6, 3.8, "updates buffer")

    plt.tight_layout()
    filepath = os.path.join(OUTPUT_DIR, "class_diagram.png")
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {filepath}")

# ==========================================
# 3. SEQUENCE DIAGRAM
# ==========================================
def generate_sequence_diagram():
    fig, ax = plt.subplots(figsize=(20, 14), dpi=300)
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 14)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    draw_header(ax, "UML Sequence Diagram", "Synchronous Message Sequence: Ingestion, Anomaly Scoring, SHAP Attribution & Drift Adaptation")

    lifelines = [
        (1.8, "Security Analyst\n(Client UI)", "#EBF8FF"),
        (4.6, "Dashboard\n(Controller)", "#EDF2F7"),
        (7.5, "Traffic\nSimulator", "#FFF5F5"),
        (10.4, "Preprocessor\nPipeline", "#F0FFF4"),
        (13.3, "IsolationForest\n(Detector)", "#EBF8FF"),
        (16.1, "NetworkXAI\n(SHAP Engine)", "#FEFCBF"),
        (18.6, "DriftDetector\n(KS Monitor)", "#F0FFF4")
    ]

    top_y = 11.4
    bot_y = 0.8

    for lx, lname, lcolor in lifelines:
        box = FancyBboxPatch((lx - 1.25, top_y - 0.55), 2.5, 1.1, boxstyle="round,pad=0.15",
                             facecolor=lcolor, edgecolor=COLOR_PRIMARY, lw=1.8)
        ax.add_patch(box)
        ax.text(lx, top_y, lname, ha='center', va='center', fontsize=11.5, fontweight='bold', color=COLOR_PRIMARY)
        ax.plot([lx, lx], [top_y - 0.65, bot_y], color="#A0AEC0", linestyle='--', lw=1.4)

    messages = [
        (10.4, 1.8, 4.6, "1: Click 'Start Live Stream'", False, False),
        (9.8, 4.6, 7.5, "2: generate_single_flow()", False, False),
        (9.2, 7.5, 4.6, "3: return raw_flow record", True, True),
        (8.5, 4.6, 10.4, "4: transform(raw_flow)", False, False),
        (7.9, 10.4, 4.6, "5: return X_scaled vector", True, True),
        (7.2, 4.6, 13.3, "6: predict(X_scaled) [Timer Started]", False, False),
        (6.6, 13.3, 4.6, "7: return (pred_anomaly, anomaly_score) [Lat: ~1.2ms]", True, True),
        (5.9, 4.6, 16.1, "8: [if anomaly] explain_instance(raw, X) [Timer Started]", False, False),
        (5.3, 16.1, 4.6, "9: return Shapley values & NLP summary [Lat: ~95ms]", True, True),
        (4.6, 4.6, 18.6, "10: update(raw_flow) [sliding window N=250]", False, False),
        (4.0, 18.6, 4.6, "11: return (drift_detected, feature_p_values)", True, True),
        (3.3, 4.6, 13.3, "12: [if drift: p < 0.002] retrain_model_on_drift(clean_buffer)", False, False),
        (2.7, 13.3, 4.6, "13: Isolation Forest refit & dynamic threshold recalibrated", True, True),
        (2.0, 4.6, 18.6, "14: reset_reference(clean_buffer)", False, False),
        (1.3, 4.6, 1.8, "15: Update HUD KPIs, Latency gauges & Plotly charts", True, False),
    ]

    for y, fx, tx, text, is_ret, is_dash in messages:
        ls = '--' if is_dash else '-'
        col = COLOR_ACCENT if "[if" in text else COLOR_PRIMARY
        ax.annotate("", xy=(tx, y), xytext=(fx, y),
                    arrowprops=dict(arrowstyle="->", color=col, lw=1.6, linestyle=ls))
        mid_x = (fx + tx) / 2
        ax.text(mid_x, y + 0.14, text, ha='center', va='bottom', fontsize=10.8, fontweight='bold', color=col,
                backgroundcolor="white")

    activations = [
        (4.6, 10.5, 1.2),
        (7.5, 9.9, 9.1),
        (10.4, 8.6, 7.8),
        (13.3, 7.3, 6.5),
        (16.1, 6.0, 5.2),
        (18.6, 4.7, 3.9),
        (13.3, 3.4, 2.6)
    ]
    for ax_x, ay1, ay2 in activations:
        act_box = Rectangle((ax_x - 0.15, ay2), 0.30, ay1 - ay2, facecolor="#CBD5E0", edgecolor=COLOR_PRIMARY, lw=1.2)
        ax.add_patch(act_box)

    plt.tight_layout()
    filepath = os.path.join(OUTPUT_DIR, "sequence_diagram.png")
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {filepath}")

# ==========================================
# 4. ACTIVITY DIAGRAM (FLOWCHART WORKFLOW)
# ==========================================
def generate_activity_diagram():
    fig, ax = plt.subplots(figsize=(18, 16), dpi=300)
    ax.set_xlim(0, 18)
    ax.set_ylim(-0.5, 15.5)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    draw_header(ax, "UML Activity Diagram", "Operational Workflow: Streaming Decision Tree, Local Explanations & Adaptive Realignment")

    def draw_action(x, y, w, h, text, fill="#EDF2F7"):
        box = FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.2",
                             facecolor=fill, edgecolor=COLOR_PRIMARY, lw=2.0)
        ax.add_patch(box)
        ax.text(x, y, text, ha='center', va='center', fontsize=11.5, fontweight='bold', color=COLOR_PRIMARY)

    def draw_decision(x, y, w, h, label=""):
        pts = [[x, y + h/2], [x + w/2, y], [x, y - h/2], [x - w/2, y]]
        poly = patches.Polygon(pts, closed=True, facecolor="#FEFCBF", edgecolor=COLOR_PRIMARY, lw=2.0)
        ax.add_patch(poly)
        if label:
            ax.text(x, y, label, ha='center', va='center', fontsize=11.0, fontweight='bold', color=COLOR_PRIMARY)

    # Initial state
    start_c = Circle((9.0, 13.8), 0.28, facecolor=COLOR_PRIMARY, edgecolor=COLOR_PRIMARY)
    ax.add_patch(start_c)
    ax.text(9.0, 14.25, "Stream Initialized", ha='center', va='center', fontsize=12.5, fontweight='bold', color=COLOR_PRIMARY)

    ax.annotate("", xy=(9.0, 13.15), xytext=(9.0, 13.52), arrowprops=dict(arrowstyle="->", lw=1.8, color=COLOR_PRIMARY))

    # Step 1: Ingestion
    draw_action(9.0, 12.7, 6.8, 0.85, "Ingest / Generate Network Flow Record")
    ax.annotate("", xy=(9.0, 11.85), xytext=(9.0, 12.28), arrowprops=dict(arrowstyle="->", lw=1.8, color=COLOR_PRIMARY))

    # Step 2: Preprocess
    draw_action(9.0, 11.4, 6.8, 0.85, "Preprocess, Encode Categoricals & Scale Features")
    ax.annotate("", xy=(9.0, 10.55), xytext=(9.0, 10.98), arrowprops=dict(arrowstyle="->", lw=1.8, color=COLOR_PRIMARY))

    # Step 3: Isolation Forest
    draw_action(9.0, 10.1, 6.8, 0.85, "Isolation Forest Path Evaluation [Measure Inference Latency]")
    ax.annotate("", xy=(9.0, 9.2), xytext=(9.0, 9.68), arrowprops=dict(arrowstyle="->", lw=1.8, color=COLOR_PRIMARY))

    # Decision 1: Anomaly?
    draw_decision(9.0, 8.6, 3.0, 1.15, "Anomaly Score >\nThreshold?")

    # Yes branch -> Right -> SHAP explanation
    ax.annotate("Yes [Anomaly]", xy=(12.8, 8.6), xytext=(10.5, 8.6),
                arrowprops=dict(arrowstyle="->", lw=1.8, color=COLOR_ACCENT),
                fontsize=11.2, fontweight='bold', color=COLOR_ACCENT, ha='center', va='bottom')
    draw_action(14.8, 8.6, 4.4, 1.1, "Compute TreeSHAP Attributions\n& Plain-English Explanation", fill="#FFF5F5")
    ax.annotate("", xy=(14.8, 7.55), xytext=(14.8, 8.05), arrowprops=dict(arrowstyle="->", lw=1.8, color=COLOR_ACCENT))
    draw_action(14.8, 7.1, 4.4, 0.85, "Register High-Priority Alert", fill="#FFF5F5")

    # No branch -> Straight down
    ax.annotate("No [Normal]", xy=(9.0, 7.55), xytext=(9.0, 8.02),
                arrowprops=dict(arrowstyle="->", lw=1.8, color=COLOR_GREEN),
                fontsize=11.2, fontweight='bold', color=COLOR_GREEN, ha='left', va='center')

    # Merge point
    draw_action(9.0, 7.1, 6.8, 0.85, "Update Sliding Feature Buffers (Window N=250)")
    # Connect right branch back
    ax.annotate("", xy=(12.4, 7.1), xytext=(12.6, 7.1), arrowprops=dict(arrowstyle="->", lw=1.8, color=COLOR_PRIMARY))

    ax.annotate("", xy=(9.0, 6.15), xytext=(9.0, 6.68), arrowprops=dict(arrowstyle="->", lw=1.8, color=COLOR_PRIMARY))

    # Decision 2: Window full?
    draw_decision(9.0, 5.5, 3.0, 1.15, "Buffer Full &\nCheck Tick?")

    # Yes branch -> Straight down
    ax.annotate("Yes", xy=(9.0, 4.25), xytext=(9.0, 4.92),
                arrowprops=dict(arrowstyle="->", lw=1.8, color=COLOR_PRIMARY),
                fontsize=11.2, fontweight='bold', color=COLOR_PRIMARY, ha='left', va='center')

    draw_action(9.0, 3.8, 6.8, 0.85, "Execute 2-Sample KS-Test with Bonferroni Rule")
    ax.annotate("", xy=(9.0, 2.95), xytext=(9.0, 3.38), arrowprops=dict(arrowstyle="->", lw=1.8, color=COLOR_PRIMARY))

    # Decision 3: Drift?
    draw_decision(9.0, 2.3, 3.0, 1.15, "Drift Detected\n(p < 0.002)?")

    # Yes branch -> Retrain
    ax.annotate("Yes", xy=(12.6, 2.3), xytext=(10.5, 2.3),
                arrowprops=dict(arrowstyle="->", lw=1.8, color=COLOR_ACCENT),
                fontsize=11.2, fontweight='bold', color=COLOR_ACCENT, ha='center', va='bottom')
    draw_action(14.8, 2.3, 4.4, 1.05, "Filter Clean Normal Buffer\n& Retrain Isolation Forest", fill="#FFF5F5")

    # Connect retrain to UI
    ax.annotate("", xy=(12.5, 0.8), xytext=(14.8, 1.78), arrowprops=dict(arrowstyle="->", lw=1.8, color=COLOR_PRIMARY))

    # No branch from Buffer Full -> Bypass straight to UI
    ax.plot([7.5, 3.0, 3.0, 5.6], [5.5, 5.5, 0.8, 0.8], color=COLOR_PRIMARY, lw=1.8)
    ax.annotate("", xy=(5.8, 0.8), xytext=(5.6, 0.8), arrowprops=dict(arrowstyle="->", lw=1.8, color=COLOR_PRIMARY))
    ax.text(3.3, 5.7, "No", fontsize=11.2, fontweight='bold', color=COLOR_PRIMARY)

    # No branch from Drift -> UI
    ax.annotate("", xy=(9.0, 1.25), xytext=(9.0, 1.72),
                arrowprops=dict(arrowstyle="->", lw=1.8, color=COLOR_GREEN))
    ax.text(9.15, 1.5, "No", fontsize=11.2, fontweight='bold', color=COLOR_GREEN, ha='left', va='center')

    # UI Rendering
    draw_action(9.0, 0.8, 6.8, 0.82, "Render Real-Time Dashboard & Update KPI Gauges", fill="#F0FFF4")

    # Clean outer loopback from bottom up to top
    ax.plot([5.6, 1.0], [0.8, 0.8], color=COLOR_PRIMARY, lw=1.8)
    ax.plot([1.0, 1.0], [0.8, 12.7], color=COLOR_PRIMARY, lw=1.8)
    ax.annotate("Next Stream Tick", xy=(5.6, 12.7), xytext=(1.0, 12.7),
                arrowprops=dict(arrowstyle="->", lw=1.8, color=COLOR_PRIMARY),
                fontsize=11.8, fontweight='bold', color=COLOR_PRIMARY, ha='center', va='bottom')

    plt.tight_layout()
    filepath = os.path.join(OUTPUT_DIR, "activity_diagram.png")
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {filepath}")

# ==========================================
# 5. COMPONENT DIAGRAM (LAYERED ARCHITECTURE)
# ==========================================
def generate_component_diagram():
    fig, ax = plt.subplots(figsize=(19, 14), dpi=300)
    ax.set_xlim(0, 19)
    ax.set_ylim(0, 14)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    draw_header(ax, "UML Component Diagram", "System Packages, Layered Subsystems, Interfaces & Data Contracts")

    def draw_component(x, y, w, h, name, description, fill="#EDF2F7"):
        rect = FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0",
                              facecolor=fill, edgecolor=COLOR_PRIMARY, lw=2.0)
        ax.add_patch(rect)
        tab1 = Rectangle((x - 0.32, y + h - 0.75), 0.64, 0.30, facecolor="white", edgecolor=COLOR_PRIMARY, lw=1.6)
        tab2 = Rectangle((x - 0.32, y + h - 1.35), 0.64, 0.30, facecolor="white", edgecolor=COLOR_PRIMARY, lw=1.6)
        ax.add_patch(tab1)
        ax.add_patch(tab2)
        ax.text(x + w - 0.25, y + h - 0.28, "«component»", ha='right', va='top', fontsize=10.5, color="#718096", fontstyle='italic')
        ax.text(x + w/2, y + h/2 + 0.22, name, ha='center', va='center', fontsize=13.5, fontweight='bold', color=COLOR_PRIMARY)
        ax.text(x + w/2, y + h/2 - 0.38, description, ha='center', va='center', fontsize=10.5, color="#2D3748")

    # Layer 1: Presentation & Orchestration (Top)
    draw_component(0.8, 8.8, 8.0, 2.4, "Web Presentation Layer\n(src/dashboard.py)", "Streamlit Interface, Session State, Real-time Plotly Gauges & Latency HUD")
    draw_component(10.0, 8.8, 8.2, 2.4, "Traffic Simulation & Streaming Gateway\n(src/data_generator.py)", "Normal Baseline Profiler, Cyber Attack Synthesizer & VPN Concept Drift Engine")

    # Layer 2: Preprocessing & Analytics (Middle)
    draw_component(0.8, 4.8, 5.4, 2.4, "Preprocessing Pipeline\n(src/preprocessor.py)", "ColumnTransformer, StandardScaler\n& OneHotEncoder")
    draw_component(6.8, 4.8, 5.4, 2.4, "Isolation Forest Engine\n(src/model.py)", "Unsupervised Tree Scoring\n& Dynamic 99th %tile Threshold Gate")
    draw_component(12.8, 4.8, 5.4, 2.4, "Explainable AI Engine\n(src/xai_engine.py)", "TreeSHAP Local Attributions\n& Natural Language Generator")

    # Layer 3: Drift Monitoring & Offline Validation & Persistence (Bottom)
    draw_component(0.8, 0.8, 5.4, 2.4, "Statistical Drift Monitor\n(src/drift_detector.py)", "Sliding Window Buffer (N=250)\n& Bonferroni KS-Test Gateway")
    draw_component(6.8, 0.8, 5.4, 2.4, "Offline Benchmark Suite\n(src/offline_validation.py)", "UNSW-NB15 Partition Evaluator\n(Isolation Forest vs OC-SVM)")
    draw_component(12.8, 0.8, 5.4, 2.4, "Model & Benchmark Store\n(data/*.pkl, data/*.json)", "Serialized Isolation Forest, Pipeline Binaries\n& Comparative Offline Metrics", fill="#FEFCBF")

    def draw_dependency(x1, y1, x2, y2, label=""):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", lw=1.8, color=COLOR_PRIMARY, linestyle='--'))
        if label:
            mx, my = (x1 + x2)/2, (y1 + y2)/2 + 0.16
            ax.text(mx, my, label, fontsize=11.2, color=COLOR_PRIMARY, fontweight='bold',
                    ha='center', va='bottom', backgroundcolor='white')

    # Clean vertical and horizontal tiered connections
    draw_dependency(8.8, 10.0, 10.0, 10.0, "polls streaming flows")
    draw_dependency(3.5, 8.8, 3.5, 7.2, "raw flow dict")
    draw_dependency(6.2, 6.0, 6.8, 6.0, "scaled feature vector X")
    draw_dependency(12.2, 6.0, 12.8, 6.0, "explains anomalous instances")
    draw_dependency(3.5, 4.8, 3.5, 3.2, "tracks sliding window")
    draw_dependency(9.5, 4.8, 9.5, 3.2, "validates baseline")
    draw_dependency(12.2, 2.0, 12.8, 2.0, "logs metrics")
    draw_dependency(12.2, 5.0, 12.8, 3.2, "loads/persists models")

    plt.tight_layout()
    filepath = os.path.join(OUTPUT_DIR, "component_diagram.png")
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {filepath}")

# ==========================================
# 6. STATE MACHINE DIAGRAM (CIRCULAR LIFECYCLE)
# ==========================================
def generate_state_machine_diagram():
    fig, ax = plt.subplots(figsize=(18, 13), dpi=300)
    ax.set_xlim(0, 18)
    ax.set_ylim(-0.8, 13.0)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    draw_header(ax, "UML State Machine Diagram", "Lifecycle State Transitions of the Self-Adaptive Intrusion Detection System")

    def draw_state(x, y, w, h, name, activities=[], fill="#EDF2F7"):
        box = FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.25",
                             facecolor=fill, edgecolor=COLOR_PRIMARY, lw=2.0)
        ax.add_patch(box)
        header_y = y + h/2 - 0.40
        ax.text(x, header_y, name, ha='center', va='center', fontsize=13.5, fontweight='bold', color=COLOR_PRIMARY)
        if activities:
            ax.plot([x - w/2, x + w/2], [header_y - 0.30, header_y - 0.30], color=COLOR_PRIMARY, lw=1.2)
            curr_y = header_y - 0.62
            for act in activities:
                ax.text(x - w/2 + 0.30, curr_y, act, ha='left', va='center', fontsize=10.5, color="#2D3748", fontfamily="monospace")
                curr_y -= 0.34

    # Initial state
    start_c = Circle((1.4, 9.6), 0.26, facecolor=COLOR_PRIMARY, edgecolor=COLOR_PRIMARY)
    ax.add_patch(start_c)
    ax.annotate("", xy=(2.6, 9.6), xytext=(1.75, 9.6), arrowprops=dict(arrowstyle="->", lw=1.8, color=COLOR_PRIMARY))
    ax.text(2.15, 9.95, "launch", fontsize=11.2, fontweight='bold', color=COLOR_PRIMARY, ha='center')

    # States
    draw_state(5.2, 9.6, 4.8, 2.2, "INITIALIZING", [
        "entry / check_dependencies()",
        "do / fit_baseline_models()",
        "exit / load_preprocessor_&_IF()"
    ])

    draw_state(13.2, 9.6, 5.6, 2.5, "NORMAL_MONITORING", [
        "entry / stream_active = True",
        "do / predict(flow) [log latency]",
        "do / update_sliding_buffer()",
        "exit / log_telemetry()"
    ], fill="#F0FFF4")

    draw_state(13.2, 4.6, 5.6, 2.5, "ANOMALY_EXPLAINING", [
        "entry / flag_alert(score)",
        "do / compute_tree_shap(flow)",
        "do / synthesize_nlp_explanation()",
        "exit / push_alert_console()"
    ], fill="#FFF5F5")

    draw_state(5.2, 4.6, 5.2, 2.5, "DRIFT_ANALYSIS", [
        "entry / window_buffer_full",
        "do / run_2sample_ks_test()",
        "do / apply_bonferroni(alpha=0.002)",
        "exit / log_drift_pvalues()"
    ], fill="#FEFCBF")

    draw_state(5.2, 0.8, 5.6, 2.2, "ADAPTIVE_RETRAINING", [
        "entry / filter_clean_normal_flows()",
        "do / refit_isolation_forest()",
        "do / reset_dynamic_threshold()",
        "exit / reset_ks_reference()"
    ], fill="#EBF8FF")

    # Transitions without intersecting any box
    # 1. Init -> Normal Monitoring
    ax.annotate("", xy=(10.4, 9.6), xytext=(7.6, 9.6), arrowprops=dict(arrowstyle="->", lw=1.8, color=COLOR_PRIMARY))
    ax.text(9.0, 9.85, "models_ready", fontsize=11.2, color=COLOR_PRIMARY, fontweight='bold', ha='center', va='bottom')

    # 2. Normal -> Anomaly
    ax.annotate("", xy=(13.2, 5.85), xytext=(13.2, 8.35),
                arrowprops=dict(arrowstyle="->", lw=1.8, color=COLOR_ACCENT))
    ax.text(13.35, 7.1, "score > threshold\n[threat identified]", fontsize=11.0, color=COLOR_ACCENT,
                fontweight='bold', ha='left', va='center')

    # 3. Anomaly -> Normal (return loop on the right)
    ax.annotate("", xy=(16.0, 8.35), xytext=(16.0, 5.85),
                arrowprops=dict(arrowstyle="->", lw=1.8, color=COLOR_PRIMARY, connectionstyle="arc3,rad=-0.25"))
    ax.text(16.7, 7.1, "explanation_logged\n[resume]", fontsize=11.0, color=COLOR_PRIMARY,
            fontweight='bold', ha='left', va='center')

    # 4. Normal -> Drift Analysis
    ax.plot([10.4, 8.4, 8.4, 7.8], [8.5, 8.5, 4.6, 4.6], color=COLOR_PRIMARY, lw=1.8)
    ax.annotate("", xy=(7.8, 4.6), xytext=(8.0, 4.6), arrowprops=dict(arrowstyle="->", lw=1.8, color=COLOR_PRIMARY))
    ax.text(8.55, 6.5, "buffer_full\n[eval_tick]", fontsize=11.0, color=COLOR_PRIMARY,
            fontweight='bold', ha='left', va='center')

    # 5. Drift -> Retraining
    ax.annotate("", xy=(5.2, 1.9), xytext=(5.2, 3.35),
                arrowprops=dict(arrowstyle="->", lw=1.8, color=COLOR_ACCENT))
    ax.text(5.35, 2.6, "drift_detected\n[p < 0.002]", fontsize=11.0, color=COLOR_ACCENT,
            fontweight='bold', ha='left', va='center')

    # 6. Retraining -> Normal Monitoring (Clean route in gap between columns)
    ax.plot([8.0, 9.2, 9.2, 10.4], [0.8, 0.8, 8.8, 8.8], color=COLOR_GREEN, lw=1.8)
    ax.annotate("", xy=(10.4, 8.8), xytext=(10.1, 8.8),
                arrowprops=dict(arrowstyle="->", lw=1.8, color=COLOR_GREEN))
    ax.text(9.2, 2.5, "model_adapted\n[baseline realigned]", fontsize=11.2, color=COLOR_GREEN,
            fontweight='bold', ha='center', va='center', backgroundcolor='white')

    plt.tight_layout()
    filepath = os.path.join(OUTPUT_DIR, "state_machine_diagram.png")
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {filepath}")

# ==========================================
# 7. DEPLOYMENT DIAGRAM
# ==========================================
def generate_deployment_diagram():
    fig, ax = plt.subplots(figsize=(18, 14), dpi=300)
    ax.set_xlim(0, 18)
    ax.set_ylim(0, 14)
    ax.axis('off')
    fig.patch.set_facecolor('white')

    draw_header(ax, "UML Deployment Diagram", "Physical Hardware Nodes, Execution Environments & Deployed Software Artifacts")

    def draw_3d_node(x, y, w, h, name, stereotype="device", fill="#F7FAFC"):
        depth = 0.50
        front = Rectangle((x, y), w, h, facecolor=fill, edgecolor=COLOR_PRIMARY, lw=2.0)
        ax.add_patch(front)
        top_pts = [[x, y + h], [x + depth, y + h + depth], [x + w + depth, y + h + depth], [x + w, y + h]]
        top_poly = patches.Polygon(top_pts, closed=True, facecolor="#E2E8F0", edgecolor=COLOR_PRIMARY, lw=2.0)
        ax.add_patch(top_poly)
        side_pts = [[x + w, y], [x + w + depth, y + depth], [x + w + depth, y + h + depth], [x + w, y + h]]
        side_poly = patches.Polygon(side_pts, closed=True, facecolor="#CBD5E0", edgecolor=COLOR_PRIMARY, lw=2.0)
        ax.add_patch(side_poly)

        ax.text(x + w/2, y + h - 0.40, f"«{stereotype}»", ha='center', va='center', fontsize=11.2, color="#718096", fontstyle='italic')
        ax.text(x + w/2, y + h - 0.85, name, ha='center', va='center', fontsize=14.0, fontweight='bold', color=COLOR_PRIMARY)

    def draw_artifact(x, y, w, h, title, sub):
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.12", facecolor="white", edgecolor=COLOR_PRIMARY, lw=1.4)
        ax.add_patch(box)
        ax.text(x + w/2, y + h/2 + 0.16, f"«artifact» {title}", ha='center', va='center', fontsize=11.5, fontweight='bold', color=COLOR_PRIMARY)
        ax.text(x + w/2, y + h/2 - 0.20, sub, ha='center', va='center', fontsize=10.0, color="#718096")

    # Node 1: Client Machine
    draw_3d_node(0.8, 6.2, 5.8, 5.5, "Client Workstation\n(Admin Device)", "execution environment")
    draw_artifact(1.2, 8.4, 5.0, 0.85, "Web Browser Engine", "Google Chrome / Edge / Firefox")
    draw_artifact(1.2, 7.1, 5.0, 0.85, "Plotly Visualization Engine", "WebGL / HTML5 Interactive Telemetry")

    # Node 2: Server / ML Compute Node
    draw_3d_node(9.0, 4.5, 8.2, 7.2, "Application & ML Compute Node\n(Host Server)", "execution environment")
    draw_artifact(9.5, 9.7, 7.2, 0.82, "Python 3.9+ Runtime", "uvicorn / asyncio web server engine")
    draw_artifact(9.5, 8.6, 7.2, 0.82, "Streamlit Web Application", "dashboard.py (State Management & HUD)")
    draw_artifact(9.5, 7.5, 7.2, 0.82, "Isolation Forest Worker", "scikit-learn Anomaly Detection Engine")
    draw_artifact(9.5, 6.4, 7.2, 0.82, "TreeSHAP Attribution Engine", "shap.TreeExplainer (Exact path length)")
    draw_artifact(9.5, 5.3, 7.2, 0.82, "KS-Test Drift Monitor", "scipy.stats (Bonferroni alpha=0.002)")

    # Node 3: Storage Node
    draw_3d_node(4.2, 0.5, 8.6, 3.6, "Persistent File System\n(Disk Storage)", "database / file system", fill="#FEFCBF")
    draw_artifact(4.8, 2.1, 7.4, 0.82, "Serialized Model Binaries", "isolation_forest.pkl, preprocessor.pkl")
    draw_artifact(4.8, 1.0, 7.4, 0.82, "Validation Datasets & Metrics", "UNSW_NB15_testing-set.csv, offline_metrics.json")

    # Network Connection
    ax.plot([6.6, 9.0], [9.2, 9.2], color=COLOR_LINE, lw=2.4)
    ax.text(7.8, 9.5, "HTTP / WebSockets\n(Port :8501)", ha='center', va='bottom', fontsize=11.5, fontweight='bold', color=COLOR_PRIMARY)

    # File I/O Connection
    ax.plot([13.1, 13.1, 12.8], [4.5, 3.6, 3.6], color=COLOR_LINE, lw=2.2)
    ax.text(13.3, 4.15, " File I/O (Pickle & JSON)", ha='left', va='center', fontsize=11.0, color="#4A5568", fontweight='bold')

    plt.tight_layout()
    filepath = os.path.join(OUTPUT_DIR, "deployment_diagram.png")
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {filepath}")

def main():
    print("Regenerating all 7 UML Diagrams with larger, highly visible fonts...")
    generate_use_case_diagram()
    generate_class_diagram()
    generate_sequence_diagram()
    generate_activity_diagram()
    generate_component_diagram()
    generate_state_machine_diagram()
    generate_deployment_diagram()
    print("All 7 UML Diagrams regenerated successfully with large, visible typography!")

if __name__ == "__main__":
    main()
