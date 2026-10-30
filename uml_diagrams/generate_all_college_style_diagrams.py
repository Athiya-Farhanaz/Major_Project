import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Ellipse, Rectangle, Circle, Polygon
import numpy as np

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Exact College Style Palette (from Photo 2)
FONT_FAMILY = "DejaVu Sans"
COLOR_RED = "#B81D24"       # Deep crisp crimson/red
COLOR_YELLOW = "#FFFFE0"    # Soft light cream-yellow
COLOR_TEXT = "#000000"      # Sharp black text
COLOR_BG = "#FFFFFF"        # Pure white background
COLOR_LIGHT_RED = "#FFF5F5"
COLOR_WHITE = "#FFFFFF"

def draw_boundary(ax, width, height, title):
    """Draws the standard college template outer red boundary box and centered title."""
    rect = Rectangle((0.8, 0.5), width - 1.6, height - 1.0, linewidth=2.6,
                     edgecolor=COLOR_RED, facecolor='none')
    ax.add_patch(rect)
    ax.text(width / 2.0, height - 0.5, title,
            ha='center', va='center', fontsize=18, fontweight='bold', color=COLOR_TEXT,
            fontname=FONT_FAMILY, bbox=dict(boxstyle='square,pad=0.45', facecolor=COLOR_WHITE, edgecolor='none'))

# ==============================================================================
# 1. ARCHITECTURE DIAGRAM
# ==============================================================================
def generate_architecture_diagram():
    fig, ax = plt.subplots(figsize=(24, 15), dpi=300)
    ax.set_xlim(0, 24)
    ax.set_ylim(0, 15)
    ax.axis('off')
    fig.patch.set_facecolor(COLOR_BG)

    draw_boundary(ax, 24, 15, "Autonomous Real-Time Network Anomaly Detection System - System Architecture")

    def draw_box(x, y, w, h, title, items, title_size=12, text_size=10.5):
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.2",
                             facecolor=COLOR_YELLOW, edgecolor=COLOR_RED, linewidth=2.0)
        ax.add_patch(box)
        ax.text(x + w / 2, y + h - 0.35, title, ha='center', va='top',
                fontsize=title_size, fontweight='bold', color=COLOR_RED, fontname=FONT_FAMILY)
        ax.plot([x + 0.2, x + w - 0.2], [y + h - 0.60, y + h - 0.60], color=COLOR_RED, lw=1.4)
        line_y = y + h - 0.88
        for item in items:
            ax.text(x + 0.3, line_y, f"• {item}", ha='left', va='top',
                    fontsize=text_size, color=COLOR_TEXT, fontname=FONT_FAMILY)
            line_y -= 0.38

    def draw_arrow(x1, y1, x2, y2, label=None, dashed=False, lw=2.0):
        ls = '--' if dashed else '-'
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color=COLOR_RED, lw=lw, ls=ls, mutation_scale=16))
        if label:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(mx, my + 0.16, label, ha='center', va='bottom',
                    fontsize=9.5, fontweight='bold', color=COLOR_RED, fontname=FONT_FAMILY,
                    bbox=dict(boxstyle='round,pad=0.2', facecolor=COLOR_WHITE, edgecolor=COLOR_RED, lw=0.8))

    # Column 1: Ingestion & Simulation Tier
    c1_rect = Rectangle((1.2, 1.2), 3.8, 12.4, fill=False, edgecolor=COLOR_RED, lw=1.4, linestyle=":")
    ax.add_patch(c1_rect)
    ax.text(3.1, 13.25, "1. INGESTION TIER", ha='center', va='center', fontsize=12.5, fontweight='bold', color=COLOR_RED)
    draw_box(1.4, 8.8, 3.4, 3.8, "Network Flow Ingestion",
             ["Streaming NetFlow Source", "15 Captured Metrics", "12 Continuous Features", "3 Categorical Fields", "Zero-Packet Drop Pipe"])
    draw_box(1.4, 2.0, 3.4, 6.0, "Threat Vector Simulation",
             ["Normal Baseline Profile", "TCP SYN Flood Wave", "SSH Brute Force Wave", "Data Exfiltration Wave", "Port Reconnaissance", "Concept Drift Injection\n  (WFH/VPN Shift)"])

    # Column 2: Preprocessing Pipeline Tier
    c2_rect = Rectangle((5.6, 1.2), 3.8, 12.4, fill=False, edgecolor=COLOR_RED, lw=1.4, linestyle=":")
    ax.add_patch(c2_rect)
    ax.text(7.5, 13.25, "2. PREPROCESSING TIER", ha='center', va='center', fontsize=12.5, fontweight='bold', color=COLOR_RED)
    draw_box(5.8, 7.5, 3.4, 5.1, "Feature Pipeline",
             ["Scikit-Learn ColumnTransformer", "StandardScaler (Z-Score)", "OneHotEncoder (proto, state, serv)", "Robust Null / Inf Handling", "Preserved Feature Mapping", "Scaled Output Vector (X)"])
    draw_box(5.8, 2.0, 3.4, 4.8, "State Buffer Cache",
             ["Sliding Window Buffer (N=250)", "Historical Normal Baselines", "Real-Time Telemetry Log", "Anti-Poison Filter Buffer", "Pickle State Persistence"])

    # Column 3: Unsupervised ML Detection Tier
    c3_rect = Rectangle((10.0, 1.2), 3.8, 12.4, fill=False, edgecolor=COLOR_RED, lw=1.4, linestyle=":")
    ax.add_patch(c3_rect)
    ax.text(11.9, 13.25, "3. ML DETECTION TIER", ha='center', va='center', fontsize=12.5, fontweight='bold', color=COLOR_RED)
    draw_box(10.2, 7.5, 3.4, 5.1, "Isolation Forest Engine",
             ["100 Isolation Decision Trees", "subsample_size = 256", "Inference Latency < 2.0 ms", "contamination = 0.01", "Unsupervised Partitioning", "Continuous Anomaly Score"])
    draw_box(10.2, 2.0, 3.4, 4.8, "Decision Logic Gate",
             ["Dynamic 99th %tile Cutoff", "Real-Time Binary Classification", "Alert Priority Level", "Threat Classification Log", "Low False-Alarm Filter"])

    # Column 4: Explainable AI & Statistical Drift Tier
    c4_rect = Rectangle((14.4, 1.2), 4.2, 12.4, fill=False, edgecolor=COLOR_RED, lw=1.4, linestyle=":")
    ax.add_patch(c4_rect)
    ax.text(16.5, 13.25, "4. XAI & ADAPTIVE TIER", ha='center', va='center', fontsize=12.5, fontweight='bold', color=COLOR_RED)
    draw_box(14.6, 7.5, 3.8, 5.1, "TreeSHAP XAI Engine",
             ["TreeExplainer Tree Path Attribution", "Exact Shapley Additivity", "Feature Force & Direction", "Latency Overhead ~95 ms", "Natural Language Synthesizer", "Top-3 Driving Causes Extracted"])
    draw_box(14.6, 2.0, 3.8, 4.8, "Concept Drift & Retrain",
             ["Two-Sample KS-Test (p-value)", "Bonferroni Rule (α = 0.002)", "Anti-Poison Retraining Clean Filter", "Autonomous Model Refit", "Zero-Downtime Hot Swapping"])

    # Column 5: Presentation & SOC Tier
    c5_rect = Rectangle((19.2, 1.2), 3.8, 12.4, fill=False, edgecolor=COLOR_RED, lw=1.4, linestyle=":")
    ax.add_patch(c5_rect)
    ax.text(21.1, 13.25, "5. SOC INTERACTION TIER", ha='center', va='center', fontsize=12.5, fontweight='bold', color=COLOR_RED)
    draw_box(19.4, 7.5, 3.4, 5.1, "Security Dashboard",
             ["Streamlit Live Web Server", "Plotly Threat HUD Gauges", "SHAP Waterfall Visualizer", "Inference / XAI Latency Cards", "UNSW-NB15 Benchmark Tab", "Real-Time Packet Streamer"])
    draw_box(19.4, 2.0, 3.4, 4.8, "SOC Analyst Control",
             ["One-Click Threat Injection", "Autonomous Adaptation Toggle", "Telemetry Export (CSV/JSON)", "Alert Remediation Dispatch", "Drift Status Inspection"])

    # Inter-Tier Connectors (All Crimson Red)
    draw_arrow(4.8, 10.5, 5.8, 10.5, "Raw NetFlow")
    draw_arrow(4.8, 5.0, 5.8, 4.0, "Drift / Attack Packets")
    draw_arrow(9.2, 10.0, 10.2, 10.0, "Scaled Feature Vector (X)")
    draw_arrow(9.2, 4.4, 10.2, 4.4, "Baseline Samples")
    draw_arrow(13.6, 10.0, 14.6, 10.0, "Trigger [if Anomaly]")
    draw_arrow(13.6, 4.4, 14.6, 4.4, "Sliding Window Flows")
    draw_arrow(18.4, 10.0, 19.4, 10.0, "SHAP Local Explanation")
    draw_arrow(18.4, 4.4, 19.4, 4.4, "Drift P-Values & HUD")

    # Feedback retrain loop arrow
    ax.plot([16.5, 16.5, 11.9, 11.9], [2.0, 1.5, 1.5, 2.0], color=COLOR_RED, lw=2.0, linestyle="--")
    ax.annotate('', xy=(11.9, 2.0), xytext=(11.9, 1.5),
                arrowprops=dict(arrowstyle="-|>", color=COLOR_RED, lw=2.0, ls='--', mutation_scale=16))
    ax.text(14.2, 1.68, "Autonomous Retrain Feedback Loop (Anti-Poisoning)", ha='center', va='bottom',
            fontsize=10, fontweight='bold', color=COLOR_RED,
            bbox=dict(boxstyle='round,pad=0.2', facecolor=COLOR_WHITE, edgecolor=COLOR_RED, lw=0.8))

    filepath = os.path.join(OUTPUT_DIR, "architecture_diagram.png")
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {filepath}")

# ==============================================================================
# 2. COLLABORATION / COMMUNICATION DIAGRAM
# ==============================================================================
def generate_collaboration_diagram():
    fig, ax = plt.subplots(figsize=(24, 15), dpi=300)
    ax.set_xlim(0, 24)
    ax.set_ylim(0, 15)
    ax.axis('off')
    fig.patch.set_facecolor(COLOR_BG)

    draw_boundary(ax, 24, 15, "Autonomous Real-Time Network Anomaly Detection System - Collaboration Diagram")

    def draw_actor(x, y, label):
        head = Circle((x, y + 0.55), 0.32, facecolor='none', edgecolor=COLOR_RED, lw=2.4)
        ax.add_patch(head)
        ax.plot([x, x], [y + 0.23, y - 0.45], color=COLOR_RED, lw=2.6)
        ax.plot([x - 0.45, x + 0.45], [y - 0.05, y - 0.05], color=COLOR_RED, lw=2.6)
        ax.plot([x, x - 0.42], [y - 0.45, y - 1.15], color=COLOR_RED, lw=2.6)
        ax.plot([x, x + 0.42], [y - 0.45, y - 1.15], color=COLOR_RED, lw=2.6)
        lbl_box = Rectangle((x - 1.1, y - 1.7), 2.2, 0.48, facecolor=COLOR_YELLOW, edgecolor=COLOR_RED, lw=1.8)
        ax.add_patch(lbl_box)
        ax.text(x, y - 1.46, label, ha='center', va='center', fontsize=11, fontweight='bold', color=COLOR_TEXT)

    def draw_object(x, y, w, h, name, stereotype=None):
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.2",
                             facecolor=COLOR_YELLOW, edgecolor=COLOR_RED, lw=2.0)
        ax.add_patch(box)
        if stereotype:
            ax.text(x + w / 2, y + h - 0.38, f"«{stereotype}»", ha='center', va='center',
                    fontsize=10, color=COLOR_RED, fontstyle='italic')
            ax.text(x + w / 2, y + h / 2 - 0.15, name, ha='center', va='center',
                    fontsize=11.5, fontweight='bold', color=COLOR_TEXT)
        else:
            ax.text(x + w / 2, y + h / 2, name, ha='center', va='center',
                    fontsize=11.5, fontweight='bold', color=COLOR_TEXT)
        return (x, y, w, h)

    # Actor: Security Analyst
    draw_actor(1.8, 8.0, "Security Analyst")

    # Objects in Circular / Network Layout
    obj_dash = draw_object(5.0, 7.2, 3.8, 1.8, ":DashboardController\n(Streamlit UI)", "boundary")
    obj_sim = draw_object(10.2, 11.5, 3.8, 1.8, ":TrafficSimulator\n(NetFlow Source)", "entity")
    obj_prep = draw_object(10.2, 7.2, 3.8, 1.8, ":NetworkPreprocessor\n(Scaler/Encoder)", "control")
    obj_det = draw_object(15.6, 7.2, 3.8, 1.8, ":AnomalyDetector\n(Isolation Forest)", "control")
    obj_xai = draw_object(15.6, 11.5, 3.8, 1.8, ":NetworkXAI\n(TreeSHAP Engine)", "control")
    obj_drift = draw_object(15.6, 2.5, 3.8, 1.8, ":DriftDetector\n(KS-Test Monitor)", "control")
    obj_retrain = draw_object(10.2, 2.5, 3.8, 1.8, ":RetrainEngine\n(Anti-Poison Filter)", "control")
    obj_store = draw_object(20.4, 7.2, 2.8, 1.8, ":ModelStore\n(Pickle/JSON)", "entity")

    def draw_link(o1, o2, messages_up=[], messages_down=[]):
        x1, y1 = o1[0] + o1[2] / 2, o1[1] + o1[3] / 2
        x2, y2 = o2[0] + o2[2] / 2, o2[1] + o2[3] / 2
        ax.plot([x1, x2], [y1, y2], color=COLOR_RED, lw=1.8, zorder=1)

        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        dx, dy = x2 - x1, y2 - y1
        dist = np.hypot(dx, dy)
        if dist > 0:
            nx, ny = -dy / dist, dx / dist
        else:
            nx, ny = 0, 1

        offset = 0.32
        for idx, m in enumerate(messages_up):
            px = mx + nx * (offset + idx * 0.35)
            py = my + ny * (offset + idx * 0.35)
            ax.text(px, py, m, fontsize=9.2, fontweight='bold', color=COLOR_RED,
                    ha='center', va='center', bbox=dict(boxstyle='round,pad=0.18', facecolor=COLOR_WHITE, edgecolor=COLOR_RED, lw=0.6))

        for idx, m in enumerate(messages_down):
            px = mx - nx * (offset + idx * 0.35)
            py = my - ny * (offset + idx * 0.35)
            ax.text(px, py, m, fontsize=9.2, fontweight='bold', color=COLOR_RED,
                    ha='center', va='center', bbox=dict(boxstyle='round,pad=0.18', facecolor=COLOR_WHITE, edgecolor=COLOR_RED, lw=0.6))

    # Link Analyst -> Dashboard
    ax.plot([2.9, 5.0], [8.0, 8.1], color=COLOR_RED, lw=1.8)
    ax.text(3.95, 8.45, "1: click 'Start Stream' ➔\n8: inspect HUD gauges ➔",
            fontsize=9.2, fontweight='bold', color=COLOR_RED, ha='center', va='bottom',
            bbox=dict(boxstyle='round,pad=0.2', facecolor=COLOR_WHITE, edgecolor=COLOR_RED, lw=0.6))

    # Links between objects
    draw_link(obj_dash, obj_sim, ["2: generate_flow() ➔"], ["2.1: raw_flow record ➔"])
    draw_link(obj_dash, obj_prep, ["3: transform(raw) ➔"], ["3.1: scaled X vector ➔"])
    draw_link(obj_prep, obj_det, ["4: predict(X) ➔"], ["4.1: score & flag ➔"])
    draw_link(obj_det, obj_xai, ["5: [if anomaly] explain(X) ➔"], ["5.1: SHAP values & summary ➔"])
    draw_link(obj_det, obj_drift, ["6: update(raw) ➔"], ["6.1: drift p-values ➔"])
    draw_link(obj_drift, obj_retrain, ["7: [if drift] trigger_retrain() ➔"], ["7.1: clean buffer filtered ➔"])
    draw_link(obj_retrain, obj_det, ["7.2: refit_model() ➔"])
    draw_link(obj_det, obj_store, ["4.2: load_weights() ➔"], ["7.3: persist_model() ➔"])

    filepath = os.path.join(OUTPUT_DIR, "collaboration_diagram.png")
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {filepath}")

# ==============================================================================
# 3. SEQUENCE DIAGRAM
# ==============================================================================
def generate_sequence_diagram():
    fig, ax = plt.subplots(figsize=(24, 15), dpi=300)
    ax.set_xlim(0, 24)
    ax.set_ylim(0, 15)
    ax.axis('off')
    fig.patch.set_facecolor(COLOR_BG)

    draw_boundary(ax, 24, 15, "Autonomous Real-Time Network Anomaly Detection System - Sequence Diagram")

    lifelines = [
        (2.0, "Security Analyst\n(Client SOC)"),
        (5.2, "Dashboard Controller\n(Streamlit UI)"),
        (8.4, "Traffic Simulator\n(NetFlow Source)"),
        (11.6, "Preprocessor\n(ColumnTransformer)"),
        (14.8, "Anomaly Detector\n(Isolation Forest)"),
        (18.0, "TreeSHAP Engine\n(Explainable AI)"),
        (21.2, "Drift Monitor\n(KS-Test Engine)")
    ]

    top_y = 12.8
    bot_y = 1.0

    # Draw lifeline headers and vertical dashed red lines
    for lx, lname in lifelines:
        box = Rectangle((lx - 1.35, top_y - 0.5), 2.7, 1.1, facecolor=COLOR_YELLOW,
                        edgecolor=COLOR_RED, lw=2.0)
        ax.add_patch(box)
        ax.text(lx, top_y + 0.05, lname, ha='center', va='center', fontsize=10.5,
                fontweight='bold', color=COLOR_TEXT, fontname=FONT_FAMILY)
        ax.plot([lx, lx], [top_y - 0.55, bot_y], color=COLOR_RED, linestyle='--', lw=1.5, zorder=1)

    # Messages (y, from_x, to_x, label, is_return, is_dash)
    messages = [
        (11.4, 2.0, 5.2, "1: Click 'Start Live Stream' & Select Threat Profile", False, False),
        (10.6, 5.2, 8.4, "2: generate_single_flow() [Normal / Attack / Drift]", False, False),
        (9.8, 8.4, 5.2, "3: return raw_flow record (15 features)", True, True),
        (9.0, 5.2, 11.6, "4: transform(raw_flow) [Z-Score & One-Hot]", False, False),
        (8.2, 11.6, 5.2, "5: return scaled feature vector X", True, True),
        (7.4, 5.2, 14.8, "6: predict(X) [Timer Start: Evaluate Path Lengths]", False, False),
        (6.6, 14.8, 5.2, "7: return (anomaly_flag, score) [Latency < 2.0 ms]", True, True),
        (5.8, 5.2, 18.0, "8: [if anomaly] explain_instance(raw, X) [Timer Start]", False, False),
        (5.0, 18.0, 5.2, "9: return Shapley values & NLP summary [Latency ~95 ms]", True, True),
        (4.2, 5.2, 21.2, "10: update(raw_flow) [sliding window buffer N=250]", False, False),
        (3.4, 21.2, 5.2, "11: return (drift_detected, feature_p_values)", True, True),
        (2.6, 5.2, 14.8, "12: [if drift: p < 0.002] retrain_model(clean_normal_buffer)", False, False),
        (1.8, 14.8, 5.2, "13: model refit & dynamic 99th %tile recalibrated", True, True),
        (1.2, 5.2, 2.0, "14: render Real-Time HUD, Waterfall Plot & Latency Cards", True, False)
    ]

    for y, fx, tx, text, is_ret, is_dash in messages:
        ls = '--' if is_dash else '-'
        ax.annotate("", xy=(tx, y), xytext=(fx, y),
                    arrowprops=dict(arrowstyle="-|>", color=COLOR_RED, lw=1.8, linestyle=ls, mutation_scale=14))
        mid_x = (fx + tx) / 2
        ax.text(mid_x, y + 0.16, text, ha='center', va='bottom', fontsize=9.8,
                fontweight='bold', color=COLOR_TEXT, fontname=FONT_FAMILY,
                bbox=dict(boxstyle='round,pad=0.2', facecolor=COLOR_WHITE, edgecolor=COLOR_RED, lw=0.6))

    # Activation boxes on lifelines
    activations = [
        (5.2, 11.6, 1.2),
        (8.4, 10.7, 9.7),
        (11.6, 9.1, 8.1),
        (14.8, 7.5, 6.5),
        (18.0, 5.9, 4.9),
        (21.2, 4.3, 3.3),
        (14.8, 2.7, 1.7)
    ]
    for ax_x, ay1, ay2 in activations:
        act = Rectangle((ax_x - 0.15, ay2), 0.30, ay1 - ay2, facecolor=COLOR_YELLOW,
                        edgecolor=COLOR_RED, lw=1.5, zorder=2)
        ax.add_patch(act)

    filepath = os.path.join(OUTPUT_DIR, "sequence_diagram.png")
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {filepath}")

# ==============================================================================
# 4. COMPONENT DIAGRAM
# ==============================================================================
def generate_component_diagram():
    fig, ax = plt.subplots(figsize=(24, 15), dpi=300)
    ax.set_xlim(0, 24)
    ax.set_ylim(0, 15)
    ax.axis('off')
    fig.patch.set_facecolor(COLOR_BG)

    draw_boundary(ax, 24, 15, "Autonomous Real-Time Network Anomaly Detection System - Component Diagram")

    def draw_uml_component(x, y, w, h, name, description, stereotype="component"):
        # Base rectangle
        rect = FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0",
                              facecolor=COLOR_YELLOW, edgecolor=COLOR_RED, lw=2.2)
        ax.add_patch(rect)
        # Component icon tabs on top-left edge
        tab1 = Rectangle((x - 0.32, y + h - 0.70), 0.64, 0.28, facecolor=COLOR_WHITE, edgecolor=COLOR_RED, lw=1.6)
        tab2 = Rectangle((x - 0.32, y + h - 1.25), 0.64, 0.28, facecolor=COLOR_WHITE, edgecolor=COLOR_RED, lw=1.6)
        ax.add_patch(tab1)
        ax.add_patch(tab2)
        # Stereotype and title
        ax.text(x + w - 0.30, y + h - 0.25, f"«{stereotype}»", ha='right', va='top', fontsize=9.5, color=COLOR_RED, fontstyle='italic')
        ax.text(x + w / 2, y + h / 2 + 0.22, name, ha='center', va='center', fontsize=12.5, fontweight='bold', color=COLOR_TEXT)
        ax.text(x + w / 2, y + h / 2 - 0.38, description, ha='center', va='center', fontsize=10.0, color="#333333")

    def draw_dep(x1, y1, x2, y2, label=""):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", lw=1.8, color=COLOR_RED, linestyle='--', mutation_scale=15))
        if label:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2 + 0.16
            ax.text(mx, my, label, fontsize=9.8, color=COLOR_RED, fontweight='bold',
                    ha='center', va='bottom', bbox=dict(boxstyle='round,pad=0.2', facecolor=COLOR_WHITE, edgecolor=COLOR_RED, lw=0.6))

    # Top Row: Presentation & Simulation Subsystems
    draw_uml_component(1.5, 9.5, 9.5, 3.2, "Web Dashboard Subsystem\n(src/dashboard.py)",
                       "Streamlit HUD, Plotly Interactive Gauges,\nSession State, Real-Time Latency Cards")
    draw_uml_component(13.0, 9.5, 9.5, 3.2, "Network Simulation & Ingestion Subsystem\n(src/data_generator.py)",
                       "Normal Baseline Profile, Attack Synthesizer (SYN/Brute/Exfil),\nVPN Concept Drift Engine")

    # Middle Row: Core Machine Learning & XAI Subsystems
    draw_uml_component(1.5, 5.2, 6.4, 3.0, "Preprocessing Pipeline\n(src/preprocessor.py)",
                       "ColumnTransformer (StandardScaler &\nOneHotEncoder), Imputation")
    draw_uml_component(8.8, 5.2, 6.4, 3.0, "Isolation Forest Engine\n(src/model.py)",
                       "Unsupervised Tree Path Scoring,\nDynamic 99th %tile Cutoff")
    draw_uml_component(16.1, 5.2, 6.4, 3.0, "Explainable AI Engine\n(src/xai_engine.py)",
                       "TreeSHAP Attribution Calculator &\nNatural Language Synthesizer")

    # Bottom Row: Drift Monitoring, Retraining & Storage Subsystems
    draw_uml_component(1.5, 1.2, 6.4, 2.8, "Statistical Drift Monitor\n(src/drift_detector.py)",
                       "Sliding Window (N=250), 2-Sample KS-Test\nwith Bonferroni Correction (α=0.002)")
    draw_uml_component(8.8, 1.2, 6.4, 2.8, "Anti-Poison Retraining Engine\n(src/model.py)",
                       "Clean Normal Flow Buffer Extraction\n& Autonomous Model Re-Fitting")
    draw_uml_component(16.1, 1.2, 6.4, 2.8, "Persistence & Model Repository\n(data/*.pkl, data/*.json)",
                       "Serialized Isolation Forest, Pipeline Pickles\n& UNSW-NB15 Benchmark Metrics")

    # Dependencies
    draw_dep(11.0, 11.1, 13.0, 11.1, "polls streaming telemetry flows")
    draw_dep(5.0, 9.5, 4.7, 8.2, "passes raw flow dict")
    draw_dep(7.9, 6.7, 8.8, 6.7, "scaled feature vector X")
    draw_dep(15.2, 6.7, 16.1, 6.7, "explains anomalous instances")
    draw_dep(4.7, 5.2, 4.7, 4.0, "streams flows to sliding window")
    draw_dep(7.9, 2.6, 8.8, 2.6, "triggers retrain upon drift (p < 0.002)")
    draw_dep(12.0, 4.0, 12.0, 5.2, "hot-swaps retrained model")
    draw_dep(15.2, 2.6, 16.1, 2.6, "persists/loads model state")

    filepath = os.path.join(OUTPUT_DIR, "component_diagram.png")
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {filepath}")

# ==============================================================================
# 5. DEPLOYMENT DIAGRAM
# ==============================================================================
def generate_deployment_diagram():
    fig, ax = plt.subplots(figsize=(24, 15), dpi=300)
    ax.set_xlim(0, 24)
    ax.set_ylim(0, 15)
    ax.axis('off')
    fig.patch.set_facecolor(COLOR_BG)

    draw_boundary(ax, 24, 15, "Autonomous Real-Time Network Anomaly Detection System - Deployment Diagram")

    def draw_3d_node(x, y, w, h, name, stereotype="device", depth=0.55):
        # Front face
        front = Rectangle((x, y), w, h, facecolor=COLOR_YELLOW, edgecolor=COLOR_RED, lw=2.2)
        ax.add_patch(front)
        # Top face
        top_pts = [[x, y + h], [x + depth, y + h + depth], [x + w + depth, y + h + depth], [x + w, y + h]]
        top_poly = Polygon(top_pts, closed=True, facecolor="#FFF8DC", edgecolor=COLOR_RED, lw=2.2)
        ax.add_patch(top_poly)
        # Right face
        side_pts = [[x + w, y], [x + w + depth, y + depth], [x + w + depth, y + h + depth], [x + w, y + h]]
        side_poly = Polygon(side_pts, closed=True, facecolor="#FFE4B5", edgecolor=COLOR_RED, lw=2.2)
        ax.add_patch(side_poly)

        ax.text(x + w / 2, y + h - 0.35, f"«{stereotype}»", ha='center', va='center',
                fontsize=10.5, color=COLOR_RED, fontstyle='italic')
        ax.text(x + w / 2, y + h - 0.85, name, ha='center', va='center',
                fontsize=13.5, fontweight='bold', color=COLOR_TEXT)

    def draw_artifact(x, y, w, h, title, sub):
        box = Rectangle((x, y), w, h, facecolor=COLOR_WHITE, edgecolor=COLOR_RED, lw=1.5)
        ax.add_patch(box)
        ax.text(x + w / 2, y + h / 2 + 0.16, f"«artifact» {title}", ha='center', va='center',
                fontsize=11.0, fontweight='bold', color=COLOR_TEXT)
        ax.text(x + w / 2, y + h / 2 - 0.22, sub, ha='center', va='center',
                fontsize=9.5, color="#555555")

    # Node 1: Client SOC Workstation
    draw_3d_node(1.5, 6.2, 6.8, 6.8, "Client SOC Workstation\n(Analyst Endpoint)", "device")
    draw_artifact(2.0, 9.4, 5.8, 0.95, "Web Browser Engine", "Google Chrome / Mozilla Firefox / MS Edge")
    draw_artifact(2.0, 8.1, 5.8, 0.95, "Plotly Visualization Engine", "WebGL / HTML5 Interactive Canvas HUD")
    draw_artifact(2.0, 6.8, 5.8, 0.95, "REST / WebSocket Client", "Bidirectional Real-Time Telemetry Stream")

    # Node 2: ML Compute & Application Server
    draw_3d_node(13.2, 3.8, 9.5, 9.2, "Application & ML Compute Node\n(Host Server)", "execution environment")
    draw_artifact(13.8, 10.2, 8.3, 0.90, "Python 3.9+ Virtualenv", "Standard Scientific Python Stack")
    draw_artifact(13.8, 9.1, 8.3, 0.90, "Streamlit Server (Port :8501)", "dashboard.py (State Management & Telemetry UI)")
    draw_artifact(13.8, 8.0, 8.3, 0.90, "Isolation Forest Worker", "scikit-learn Anomaly Detection (Inference < 2ms)")
    draw_artifact(13.8, 6.9, 8.3, 0.90, "TreeSHAP Attribution Engine", "shap.TreeExplainer (Latency Overhead ~95ms)")
    draw_artifact(13.8, 5.8, 8.3, 0.90, "Two-Sample KS-Test Engine", "scipy.stats (Bonferroni-Corrected α = 0.002)")
    draw_artifact(13.8, 4.7, 8.3, 0.90, "Anti-Poison Retraining Engine", "Clean Flow Filtering & Dynamic Threshold Reset")

    # Node 3: Storage Node (Disk)
    draw_3d_node(3.5, 1.0, 8.5, 4.2, "Persistent File Storage\n(Local NVMe Disk)", "file system")
    draw_artifact(4.2, 2.7, 7.1, 0.92, "Serialized Model Binaries", "isolation_forest.pkl, preprocessor.pkl")
    draw_artifact(4.2, 1.5, 7.1, 0.92, "Validation Benchmarks & Logs", "UNSW_NB15_testing-set.csv, offline_metrics.json")

    # Physical Network Links (Red)
    ax.plot([8.3, 13.2], [9.6, 9.6], color=COLOR_RED, lw=2.4)
    ax.text(10.75, 9.95, "HTTPS / WebSockets\n(Port :8501)", ha='center', va='bottom',
            fontsize=11.0, fontweight='bold', color=COLOR_RED,
            bbox=dict(boxstyle='round,pad=0.2', facecolor=COLOR_WHITE, edgecolor=COLOR_RED, lw=0.8))

    ax.plot([14.5, 12.0], [3.8, 3.8], color=COLOR_RED, lw=2.2)
    ax.text(13.25, 3.45, "Local File I/O (Pickle & JSON)", ha='center', va='top',
            fontsize=10.5, color=COLOR_RED, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor=COLOR_WHITE, edgecolor=COLOR_RED, lw=0.8))

    filepath = os.path.join(OUTPUT_DIR, "deployment_diagram.png")
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {filepath}")

# ==============================================================================
# 6. ACTIVITY DIAGRAM
# ==============================================================================
def generate_activity_diagram():
    fig, ax = plt.subplots(figsize=(24, 16), dpi=300)
    ax.set_xlim(0, 24)
    ax.set_ylim(-0.5, 15.5)
    ax.axis('off')
    fig.patch.set_facecolor(COLOR_BG)

    draw_boundary(ax, 24, 16, "Autonomous Real-Time Network Anomaly Detection System - Activity Diagram")

    def draw_action(x, y, w, h, text):
        box = FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.25",
                             facecolor=COLOR_YELLOW, edgecolor=COLOR_RED, lw=2.0)
        ax.add_patch(box)
        ax.text(x, y, text, ha='center', va='center', fontsize=11.0, fontweight='bold',
                color=COLOR_TEXT, fontname=FONT_FAMILY, multialignment='center')

    def draw_decision(x, y, w, h, label=""):
        pts = [[x, y + h / 2], [x + w / 2, y], [x, y - h / 2], [x - w / 2, y]]
        poly = Polygon(pts, closed=True, facecolor=COLOR_YELLOW, edgecolor=COLOR_RED, lw=2.0)
        ax.add_patch(poly)
        if label:
            ax.text(x, y, label, ha='center', va='center', fontsize=10.5, fontweight='bold',
                    color=COLOR_TEXT, fontname=FONT_FAMILY, multialignment='center')

    # Initial State (Filled Red Circle)
    start_c = Circle((12.0, 14.2), 0.28, facecolor=COLOR_RED, edgecolor=COLOR_RED)
    ax.add_patch(start_c)
    ax.text(12.0, 14.65, "Start: Stream Initialized", ha='center', va='center',
            fontsize=12.0, fontweight='bold', color=COLOR_RED)
    ax.annotate("", xy=(12.0, 13.55), xytext=(12.0, 13.92),
                arrowprops=dict(arrowstyle="-|>", lw=2.0, color=COLOR_RED, mutation_scale=15))

    # Step 1: Ingest
    draw_action(12.0, 13.1, 8.0, 0.85, "Ingest / Synthesize NetFlow Record (15 Features)")
    ax.annotate("", xy=(12.0, 12.25), xytext=(12.0, 12.68),
                arrowprops=dict(arrowstyle="-|>", lw=2.0, color=COLOR_RED, mutation_scale=15))

    # Step 2: Preprocess
    draw_action(12.0, 11.8, 8.0, 0.85, "Preprocess: Z-Score Scaling & One-Hot Encoding")
    ax.annotate("", xy=(12.0, 10.95), xytext=(12.0, 11.38),
                arrowprops=dict(arrowstyle="-|>", lw=2.0, color=COLOR_RED, mutation_scale=15))

    # Step 3: Isolation Forest
    draw_action(12.0, 10.5, 8.0, 0.85, "Isolation Forest Path Evaluation [Measure Latency < 2ms]")
    ax.annotate("", xy=(12.0, 9.60), xytext=(12.0, 10.08),
                arrowprops=dict(arrowstyle="-|>", lw=2.0, color=COLOR_RED, mutation_scale=15))

    # Decision 1: Anomaly?
    draw_decision(12.0, 9.0, 3.8, 1.2, "Anomaly Score >\nThreshold?")

    # Yes Branch -> Right -> SHAP explanation
    ax.annotate("Yes [Threat Detected]", xy=(16.8, 9.0), xytext=(13.9, 9.0),
                arrowprops=dict(arrowstyle="-|>", lw=2.0, color=COLOR_RED, mutation_scale=15),
                fontsize=10.5, fontweight='bold', color=COLOR_RED, ha='center', va='bottom')
    draw_action(19.2, 9.0, 4.6, 1.1, "Compute TreeSHAP Attributions\n& Plain-English Explanation")
    ax.annotate("", xy=(19.2, 7.95), xytext=(19.2, 8.45),
                arrowprops=dict(arrowstyle="-|>", lw=2.0, color=COLOR_RED, mutation_scale=15))
    draw_action(19.2, 7.5, 4.6, 0.85, "Dispatch High-Priority Threat Alert")

    # No Branch -> Straight down
    ax.annotate("No [Normal]", xy=(12.0, 7.95), xytext=(12.0, 8.40),
                arrowprops=dict(arrowstyle="-|>", lw=2.0, color=COLOR_RED, mutation_scale=15),
                fontsize=10.5, fontweight='bold', color=COLOR_RED, ha='left', va='center')

    # Merge Point
    draw_action(12.0, 7.5, 8.0, 0.85, "Update Sliding Feature Buffers (Window N=250)")
    # Connect threat alert back to buffer
    ax.annotate("", xy=(16.0, 7.5), xytext=(16.9, 7.5),
                arrowprops=dict(arrowstyle="-|>", lw=2.0, color=COLOR_RED, mutation_scale=15))

    ax.annotate("", xy=(12.0, 6.55), xytext=(12.0, 7.08),
                arrowprops=dict(arrowstyle="-|>", lw=2.0, color=COLOR_RED, mutation_scale=15))

    # Decision 2: Buffer Full?
    draw_decision(12.0, 5.9, 3.8, 1.2, "Buffer Full (N=250)\n& Check Tick?")

    # Yes branch -> KS-Test
    ax.annotate("Yes", xy=(12.0, 4.65), xytext=(12.0, 5.30),
                arrowprops=dict(arrowstyle="-|>", lw=2.0, color=COLOR_RED, mutation_scale=15),
                fontsize=10.5, fontweight='bold', color=COLOR_RED, ha='left', va='center')
    draw_action(12.0, 4.2, 8.0, 0.85, "Execute 2-Sample KS-Test with Bonferroni Rule (α = 0.002)")
    ax.annotate("", xy=(12.0, 3.30), xytext=(12.0, 3.78),
                arrowprops=dict(arrowstyle="-|>", lw=2.0, color=COLOR_RED, mutation_scale=15))

    # Decision 3: Drift Detected?
    draw_decision(12.0, 2.7, 3.8, 1.2, "Drift Detected\n(p < 0.002)?")

    # Yes branch -> Retrain
    ax.annotate("Yes [Concept Drift]", xy=(16.8, 2.7), xytext=(13.9, 2.7),
                arrowprops=dict(arrowstyle="-|>", lw=2.0, color=COLOR_RED, mutation_scale=15),
                fontsize=10.5, fontweight='bold', color=COLOR_RED, ha='center', va='bottom')
    draw_action(19.2, 2.7, 4.6, 1.1, "Filter Clean Normal Buffer &\nRetrain Isolation Forest Engine")

    # Retrain connects to HUD
    ax.annotate("", xy=(16.0, 1.2), xytext=(19.2, 2.15),
                arrowprops=dict(arrowstyle="-|>", lw=2.0, color=COLOR_RED, mutation_scale=15))

    # No branch from Buffer Full -> Bypass straight down to HUD
    ax.plot([10.1, 4.0, 4.0, 8.0], [5.9, 5.9, 1.2, 1.2], color=COLOR_RED, lw=1.8)
    ax.annotate("", xy=(8.0, 1.2), xytext=(7.8, 1.2),
                arrowprops=dict(arrowstyle="-|>", lw=2.0, color=COLOR_RED, mutation_scale=15))
    ax.text(4.2, 6.1, "No", fontsize=10.5, fontweight='bold', color=COLOR_RED)

    # No branch from Drift -> HUD
    ax.annotate("", xy=(12.0, 1.65), xytext=(12.0, 2.10),
                arrowprops=dict(arrowstyle="-|>", lw=2.0, color=COLOR_RED, mutation_scale=15))
    ax.text(12.15, 1.88, "No", fontsize=10.5, fontweight='bold', color=COLOR_RED, ha='left', va='center')

    # HUD Rendering
    draw_action(12.0, 1.2, 8.0, 0.85, "Render Real-Time Dashboard & Update KPI HUD Gauges")

    # Loop back to next stream tick
    ax.plot([8.0, 2.0], [1.2, 1.2], color=COLOR_RED, lw=1.8)
    ax.plot([2.0, 2.0], [1.2, 13.1], color=COLOR_RED, lw=1.8)
    ax.annotate("Next Stream Packet Tick", xy=(8.0, 13.1), xytext=(2.0, 13.1),
                arrowprops=dict(arrowstyle="-|>", lw=2.0, color=COLOR_RED, mutation_scale=15),
                fontsize=11.5, fontweight='bold', color=COLOR_RED, ha='center', va='bottom')

    filepath = os.path.join(OUTPUT_DIR, "activity_diagram.png")
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {filepath}")

# ==============================================================================
# 7. CLASS DIAGRAM
# ==============================================================================
def generate_class_diagram():
    fig, ax = plt.subplots(figsize=(24, 15), dpi=300)
    ax.set_xlim(0, 24)
    ax.set_ylim(0, 15)
    ax.axis('off')
    fig.patch.set_facecolor(COLOR_BG)

    draw_boundary(ax, 24, 15, "Autonomous Real-Time Network Anomaly Detection System - Class Diagram")

    def draw_uml_class(x, y, w, h, class_name, stereotype, attributes, methods):
        # Outer box
        rect = FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0",
                              facecolor=COLOR_YELLOW, edgecolor=COLOR_RED, lw=2.0)
        ax.add_patch(rect)
        # Class Header box (Red background with white text)
        header_h = 1.05
        head_rect = Rectangle((x, y + h - header_h), w, header_h, facecolor=COLOR_RED, edgecolor=COLOR_RED, lw=2.0)
        ax.add_patch(head_rect)
        if stereotype:
            ax.text(x + w / 2, y + h - 0.30, f"«{stereotype}»", ha='center', va='center', fontsize=9.5, color="#FFE4E1")
            ax.text(x + w / 2, y + h - 0.72, class_name, ha='center', va='center', fontsize=12.5, fontweight='bold', color=COLOR_WHITE)
        else:
            ax.text(x + w / 2, y + h - 0.55, class_name, ha='center', va='center', fontsize=13.5, fontweight='bold', color=COLOR_WHITE)

        attr_step = 0.33
        attr_h = len(attributes) * attr_step + 0.30
        line_y = y + h - header_h - attr_h
        ax.plot([x, x + w], [line_y, line_y], color=COLOR_RED, lw=1.4)

        curr_y = y + h - header_h - 0.28
        for attr in attributes:
            ax.text(x + 0.22, curr_y, attr, ha='left', va='top', fontsize=9.8, color=COLOR_TEXT, fontfamily="monospace")
            curr_y -= attr_step

        curr_y = line_y - 0.24
        for m in methods:
            ax.text(x + 0.22, curr_y, m, ha='left', va='top', fontsize=9.8, color=COLOR_TEXT, fontfamily="monospace")
            curr_y -= attr_step

    # Row 1: Generator, Preprocessor, Detector
    sim_attrs = ["- rng: np.random.RandomState", "- drift_active: bool = False", "- current_phase: str", "- step_counter: int = 0"]
    sim_methods = ["+ set_drift(active: bool): void", "+ generate_single_flow(force: str): dict", "- _generate_normal(): dict", "- _generate_anomaly(type: str): dict", "+ generate_baseline(n: int): DataFrame"]
    draw_uml_class(1.2, 7.8, 6.6, 5.2, "NetworkTrafficSimulator", "Entity / Generator", sim_attrs, sim_methods)

    prep_attrs = ["- preprocessor: ColumnTransformer", "- feature_names: List[str]", "- is_fitted: bool = False"]
    prep_methods = ["+ fit(df: DataFrame): void", "+ transform(df: DataFrame): ndarray", "+ fit_transform(df: DataFrame): ndarray", "+ get_feature_names(): List[str]", "+ save(filepath: str): void", "+ load(filepath: str): Preprocessor"]
    draw_uml_class(8.7, 7.8, 6.6, 5.2, "NetworkPreprocessor", "Component / Pipeline", prep_attrs, prep_methods)

    det_attrs = ["- model: IsolationForest", "- threshold: float = 0.55", "- is_trained: bool = False", "- contamination: float = 0.01"]
    det_methods = ["+ fit(X_train: ndarray): void", "+ get_anomaly_score(X): ndarray", "+ predict(X): Tuple[ndarray, ndarray]", "+ save(filepath: str): void", "+ load(filepath: str): Detector"]
    draw_uml_class(16.2, 7.8, 6.6, 5.2, "AnomalyDetector", "ML Model / Engine", det_attrs, det_methods)

    # Row 2: Drift Detector, XAI Engine, Dashboard Controller
    drift_attrs = ["- window_size: int = 250", "- alpha: float = 0.01", "- features_to_monitor: List[str]", "- reference_data: Dict[str, ndarray]", "- window_buffer: Dict[str, List]", "- last_p_values: Dict[str, float]"]
    drift_methods = ["+ update(record: dict): Tuple[bool, dict]", "- _check_bonferroni(p_vals): bool", "+ reset_reference(new_df): void"]
    draw_uml_class(1.2, 1.2, 6.6, 5.6, "ConceptDriftDetector", "Statistical Monitor", drift_attrs, drift_methods)

    xai_attrs = ["- detector: AnomalyDetector", "- preprocessor: NetworkPreprocessor", "- explainer: shap.TreeExplainer", "- feature_names: List[str]"]
    xai_methods = ["+ explain_instance(raw, X): dict", "- _group_categorical_contributions(): dict", "- _get_feature_interpretation(f, v): str"]
    draw_uml_class(8.7, 1.2, 6.6, 5.6, "NetworkXAI", "Explainable AI Engine", xai_attrs, xai_methods)

    dash_attrs = ["- simulator: NetworkTrafficSimulator", "- preprocessor: NetworkPreprocessor", "- detector: AnomalyDetector", "- drift_detector: ConceptDriftDetector", "- xai: NetworkXAI", "- stream_active: bool = False"]
    dash_methods = ["+ initialize_models_if_needed(): void", "+ retrain_model_on_drift(): void", "+ render_live_telemetry_tab(): void", "+ render_unsw_validation_tab(): void"]
    draw_uml_class(16.2, 1.2, 6.6, 5.6, "StreamlitDashboardController", "UI / Controller", dash_attrs, dash_methods)

    # Association Arrows (Crimson Red)
    def draw_assoc(x1, y1, x2, y2, label=""):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", color=COLOR_RED, lw=2.0, mutation_scale=15))
        if label:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2 + 0.16
            ax.text(mx, my, label, fontsize=9.8, color=COLOR_RED, fontweight='bold',
                    ha='center', va='bottom', bbox=dict(boxstyle='round,pad=0.2', facecolor=COLOR_WHITE, edgecolor=COLOR_RED, lw=0.6))

    draw_assoc(7.8, 10.4, 8.7, 10.4, "raw flow dict")
    draw_assoc(15.3, 10.4, 16.2, 10.4, "scaled vector X")
    draw_assoc(16.2, 8.8, 15.3, 6.5, "explains model")
    draw_assoc(12.0, 7.8, 12.0, 6.8, "extracts feature names")
    draw_assoc(19.5, 6.8, 19.5, 7.8, "orchestrates engine")
    draw_assoc(16.2, 4.0, 15.3, 4.0, "queries local SHAP")
    draw_assoc(8.7, 4.0, 7.8, 4.0, "updates sliding buffer")

    filepath = os.path.join(OUTPUT_DIR, "class_diagram.png")
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {filepath}")

# ==============================================================================
# 8. STATE MACHINE DIAGRAM
# ==============================================================================
def generate_state_machine_diagram():
    fig, ax = plt.subplots(figsize=(24, 15), dpi=300)
    ax.set_xlim(0, 24)
    ax.set_ylim(-0.5, 14.5)
    ax.axis('off')
    fig.patch.set_facecolor(COLOR_BG)

    draw_boundary(ax, 24, 15, "Autonomous Real-Time Network Anomaly Detection System - State Machine Diagram")

    def draw_state(x, y, w, h, name, activities=[]):
        box = FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.25",
                             facecolor=COLOR_YELLOW, edgecolor=COLOR_RED, lw=2.2)
        ax.add_patch(box)
        header_y = y + h / 2 - 0.42
        ax.text(x, header_y, name, ha='center', va='center', fontsize=12.5, fontweight='bold', color=COLOR_RED)
        if activities:
            ax.plot([x - w / 2, x + w / 2], [header_y - 0.30, header_y - 0.30], color=COLOR_RED, lw=1.4)
            curr_y = header_y - 0.62
            for act in activities:
                ax.text(x - w / 2 + 0.30, curr_y, act, ha='left', va='center',
                        fontsize=10.0, color=COLOR_TEXT, fontfamily="monospace")
                curr_y -= 0.36

    # Start State (Filled Red Circle)
    start_c = Circle((2.0, 10.8), 0.28, facecolor=COLOR_RED, edgecolor=COLOR_RED)
    ax.add_patch(start_c)
    ax.annotate("", xy=(3.8, 10.8), xytext=(2.35, 10.8),
                arrowprops=dict(arrowstyle="-|>", lw=2.0, color=COLOR_RED, mutation_scale=15))
    ax.text(3.05, 11.2, "launch", fontsize=11.0, fontweight='bold', color=COLOR_RED, ha='center')

    # States
    draw_state(6.8, 10.8, 5.8, 2.5, "INITIALIZING", [
        "entry / check_dependencies()",
        "do / fit_baseline_models()",
        "exit / load_preprocessor_&_IF()"
    ])

    draw_state(17.2, 10.8, 6.8, 2.8, "NORMAL_MONITORING", [
        "entry / stream_active = True",
        "do / predict(flow) [log latency < 2ms]",
        "do / update_sliding_buffer()",
        "exit / log_telemetry_hud()"
    ])

    draw_state(17.2, 5.2, 6.8, 2.8, "ANOMALY_EXPLAINING", [
        "entry / flag_alert(score)",
        "do / compute_tree_shap(flow)",
        "do / synthesize_nlp_explanation()",
        "exit / push_alert_console()"
    ])

    draw_state(6.8, 5.2, 6.4, 2.8, "DRIFT_ANALYSIS", [
        "entry / window_buffer_full (N=250)",
        "do / run_2sample_ks_test()",
        "do / apply_bonferroni(alpha=0.002)",
        "exit / log_drift_pvalues()"
    ])

    draw_state(6.8, 1.2, 6.8, 2.5, "ADAPTIVE_RETRAINING", [
        "entry / filter_clean_normal_flows()",
        "do / refit_isolation_forest()",
        "do / reset_dynamic_threshold()",
        "exit / reset_ks_reference()"
    ])

    # Transitions (Crimson Red)
    # 1. Init -> Normal Monitoring
    ax.annotate("", xy=(13.8, 10.8), xytext=(9.7, 10.8),
                arrowprops=dict(arrowstyle="-|>", lw=2.0, color=COLOR_RED, mutation_scale=15))
    ax.text(11.75, 11.15, "models_ready", fontsize=11.0, color=COLOR_RED, fontweight='bold', ha='center')

    # 2. Normal -> Anomaly
    ax.annotate("", xy=(17.2, 6.6), xytext=(17.2, 9.4),
                arrowprops=dict(arrowstyle="-|>", lw=2.0, color=COLOR_RED, mutation_scale=15))
    ax.text(17.35, 8.0, "score > threshold\n[threat identified]", fontsize=10.5, color=COLOR_RED,
            fontweight='bold', ha='left', va='center')

    # 3. Anomaly -> Normal return loop
    ax.annotate("", xy=(20.6, 9.4), xytext=(20.6, 6.6),
                arrowprops=dict(arrowstyle="-|>", lw=2.0, color=COLOR_RED, connectionstyle="arc3,rad=-0.25", mutation_scale=15))
    ax.text(21.4, 8.0, "explanation_logged\n[resume stream]", fontsize=10.5, color=COLOR_RED,
            fontweight='bold', ha='left', va='center')

    # 4. Normal -> Drift Analysis
    ax.plot([13.8, 11.0, 11.0, 10.0], [9.8, 9.8, 5.2, 5.2], color=COLOR_RED, lw=1.8)
    ax.annotate("", xy=(10.0, 5.2), xytext=(10.3, 5.2),
                arrowprops=dict(arrowstyle="-|>", lw=2.0, color=COLOR_RED, mutation_scale=15))
    ax.text(11.15, 7.5, "buffer_full\n[eval_tick]", fontsize=10.5, color=COLOR_RED,
            fontweight='bold', ha='left', va='center')

    # 5. Drift -> Retraining
    ax.annotate("", xy=(6.8, 2.45), xytext=(6.8, 3.8),
                arrowprops=dict(arrowstyle="-|>", lw=2.0, color=COLOR_RED, mutation_scale=15))
    ax.text(6.95, 3.12, "drift_detected\n[p < 0.002]", fontsize=10.5, color=COLOR_RED,
            fontweight='bold', ha='left', va='center')

    # 6. Retraining -> Normal Monitoring
    ax.plot([10.2, 11.8, 11.8, 13.8], [1.2, 1.2, 10.0, 10.0], color=COLOR_RED, lw=1.8)
    ax.annotate("", xy=(13.8, 10.0), xytext=(13.5, 10.0),
                arrowprops=dict(arrowstyle="-|>", lw=2.0, color=COLOR_RED, mutation_scale=15))
    ax.text(11.8, 2.8, "model_adapted\n[baseline realigned]", fontsize=11.0, color=COLOR_RED,
            fontweight='bold', ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.2', facecolor=COLOR_WHITE, edgecolor=COLOR_RED, lw=0.6))

    filepath = os.path.join(OUTPUT_DIR, "state_machine_diagram.png")
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {filepath}")

def main():
    print("Generating all 8 College-Style UML & Architecture diagrams...")
    generate_architecture_diagram()
    generate_collaboration_diagram()
    generate_sequence_diagram()
    generate_component_diagram()
    generate_deployment_diagram()
    generate_activity_diagram()
    generate_class_diagram()
    generate_state_machine_diagram()
    print("All college-style diagrams generated successfully!")

if __name__ == "__main__":
    main()
