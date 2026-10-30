import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, ArrowStyle
import numpy as np

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "architecture_diagram.png")

FONT_FAMILY = "DejaVu Sans"
COLOR_PRIMARY = "#1A365D"     # Deep corporate navy
COLOR_SECONDARY = "#2B6CB0"   # Classic slate blue
COLOR_ACCENT = "#C53030"      # Crimson alert
COLOR_GREEN = "#276749"       # Emerald green
COLOR_BG = "#F8FAFC"          # Light canvas
COLOR_BOX_FILL = "#FFFFFF"    # Clean white
COLOR_LINE = "#2D3748"        # Dark slate
COLOR_BORDER = "#CBD5E0"      # Subtle border

def generate_architecture_diagram():
    fig, ax = plt.subplots(figsize=(20, 14), dpi=300)
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 14)
    ax.axis('off')
    fig.patch.set_facecolor(COLOR_BG)

    # 1. Header Banner
    ax.text(10.0, 13.5, "SYSTEM ARCHITECTURE DIAGRAM", ha='center', va='center',
            fontsize=26, fontweight='bold', color=COLOR_PRIMARY, fontname=FONT_FAMILY)
    ax.text(10.0, 13.1, "Autonomous Real-Time Network Anomaly Detection System with Explainable AI & Adaptive Retraining",
            ha='center', va='center', fontsize=14, fontstyle='italic', color=COLOR_SECONDARY, fontname=FONT_FAMILY)
    ax.plot([1.0, 19.0], [12.8, 12.8], color=COLOR_PRIMARY, lw=2.5)

    def draw_box(x, y, w, h, title, items, fill_color, border_color, title_color=COLOR_PRIMARY, title_size=12, text_size=10.5):
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.2",
                             facecolor=fill_color, edgecolor=border_color, linewidth=2.0)
        ax.add_patch(box)
        # Title
        ax.text(x + w / 2, y + h - 0.35, title, ha='center', va='top',
                fontsize=title_size, fontweight='bold', color=title_color, fontname=FONT_FAMILY)
        # Divider under title
        ax.plot([x + 0.2, x + w - 0.2], [y + h - 0.55, y + h - 0.55], color=border_color, lw=1.2)
        # Content bullet points
        line_y = y + h - 0.8
        for item in items:
            ax.text(x + 0.3, line_y, f"• {item}", ha='left', va='top',
                    fontsize=text_size, color="#2D3748", fontname=FONT_FAMILY)
            line_y -= 0.38

    def draw_connector(x1, y1, x2, y2, label=None, color=COLOR_LINE, style="-|>", lw=2.0, dashed=False):
        ls = '--' if dashed else '-'
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle=style, color=color, lw=lw, ls=ls, mutation_scale=18))
        if label:
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            ax.text(mid_x, mid_y + 0.15, label, ha='center', va='bottom',
                    fontsize=9.5, fontweight='bold', color=color,
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='none', alpha=0.9))

    # ==========================================
    # LAYER 1: DATA INGESTION & SIMULATION (LEFT)
    # ==========================================
    layer1_bg = FancyBboxPatch((0.8, 4.0), 3.8, 8.2, boxstyle="round,pad=0.3",
                               facecolor="#EDF2F7", edgecolor=COLOR_PRIMARY, lw=1.8, linestyle=":")
    ax.add_patch(layer1_bg)
    ax.text(2.7, 11.9, "1. INGESTION TIER", ha='center', va='center',
            fontsize=13, fontweight='bold', color=COLOR_PRIMARY)

    draw_box(1.1, 8.8, 3.2, 2.7, "Network Flow Source",
             ["Streaming NetFlow Ingestion", "15 Dimension Capture", "12 Continuous Metrics", "3 Categorical Metrics"],
             "#FFFFFF", COLOR_SECONDARY)

    draw_box(1.1, 4.4, 3.2, 4.0, "Threat Vector Simulation",
             ["Normal Baseline Profile", "TCP SYN Flood Wave", "SSH Brute Force Wave", "Data Exfiltration Wave", "Port Recon Sweep", "WFH / VPN Concept Drift"],
             "#FFF5F5", COLOR_ACCENT, title_color=COLOR_ACCENT)

    # ==========================================
    # LAYER 2: FEATURE PREPROCESSING (CENTER-LEFT)
    # ==========================================
    layer2_bg = FancyBboxPatch((5.2, 4.0), 3.8, 8.2, boxstyle="round,pad=0.3",
                               facecolor="#F7FAFC", edgecolor=COLOR_SECONDARY, lw=1.8, linestyle=":")
    ax.add_patch(layer2_bg)
    ax.text(7.1, 11.9, "2. PREPROCESSING TIER", ha='center', va='center',
            fontsize=13, fontweight='bold', color=COLOR_SECONDARY)

    draw_box(5.5, 8.8, 3.2, 2.7, "Feature Preprocessor",
             ["ColumnTransformer Pipeline", "StandardScaler (μ=0, σ=1)", "OneHotEncoder (Categoricals)", "handle_unknown='ignore'"],
             "#FFFFFF", COLOR_SECONDARY)

    draw_box(5.5, 4.4, 3.2, 4.0, "Feature Alignment",
             ["Duration, Packets, Rates", "Source & Destination Bytes", "TCP Flags (SF, S0, REJ)", "Service Protocol Encodings", "Output: (N × 25) Vector", "Zero-crash Novel Port Shield"],
             "#EBF8FF", COLOR_SECONDARY)

    # Connector 1 -> 2
    draw_connector(4.3, 10.0, 5.5, 10.0, "Raw Packets")
    draw_connector(4.3, 6.4, 5.5, 6.4, "Threat Waves")

    # ==========================================
    # LAYER 3: DETECTION & DECISION CORE (CENTER)
    # ==========================================
    layer3_bg = FancyBboxPatch((9.6, 4.0), 4.2, 8.2, boxstyle="round,pad=0.3",
                               facecolor="#FEFCBF", edgecolor="#B7791F", lw=1.8, linestyle=":")
    ax.add_patch(layer3_bg)
    ax.text(11.7, 11.9, "3. DETECTION CORE", ha='center', va='center',
            fontsize=13, fontweight='bold', color="#744210")

    draw_box(9.9, 7.8, 3.6, 3.7, "Isolation Forest Ensemble",
             ["100 Isolation Trees (iTrees)", "Unsupervised Learning Mode", "Score = -score_samples(X)", "Dynamic 99th % Threshold", "Sub-millisecond Latency (<1ms)", "Zero-Day Anomaly Detection"],
             "#FFFFFF", "#B7791F", title_color="#744210")

    draw_box(9.9, 4.4, 3.6, 3.0, "Dynamic Boundary Arbiter",
             ["If Score > Threshold: ANOMALY", "If Score ≤ Threshold: NORMAL", "Adjustable Sensitivity Slider", "Severity: Critical, High, Elev."],
             "#FFFFF0", "#D69E2E", title_color="#744210")

    # Connector 2 -> 3
    draw_connector(8.7, 9.5, 9.9, 9.5, "Normalized (N×25)")

    # ==========================================
    # LAYER 4 & 5: DUAL OUTPUT PATHS (RIGHT)
    # ==========================================
    
    # Path A: TOP-RIGHT (Explainable AI)
    layer4_bg = FancyBboxPatch((14.5, 7.5), 4.8, 4.7, boxstyle="round,pad=0.3",
                               facecolor="#FFF5F5", edgecolor=COLOR_ACCENT, lw=1.8, linestyle=":")
    ax.add_patch(layer4_bg)
    ax.text(16.9, 11.9, "4. EXPLAINABLE AI (XAI) TIER", ha='center', va='center',
            fontsize=13, fontweight='bold', color=COLOR_ACCENT)

    draw_box(14.8, 8.0, 4.2, 3.6, "TreeSHAP Attribution Engine",
             ["shap.TreeExplainer (Game Theory)", "Exact Tree Path Decompositions", "Semantic Sign Inversion (-shap_val)", "One-Hot Categorical Grouping", "Interactive Waterfall Plot Generation", "Plain-English Security Diagnostics"],
             "#FFFFFF", COLOR_ACCENT, title_color=COLOR_ACCENT)

    # Connector 3 -> 4 (Anomalies)
    draw_connector(13.5, 9.5, 14.8, 9.5, "Threat Flagged", color=COLOR_ACCENT, lw=2.4)

    # Path B: BOTTOM-RIGHT (Concept Drift & Adaptation)
    layer5_bg = FancyBboxPatch((14.5, 1.8), 4.8, 5.2, boxstyle="round,pad=0.3",
                               facecolor="#F0FFF4", edgecolor=COLOR_GREEN, lw=1.8, linestyle=":")
    ax.add_patch(layer5_bg)
    ax.text(16.9, 6.7, "5. ADAPTIVE SELF-HEALING TIER", ha='center', va='center',
            fontsize=13, fontweight='bold', color=COLOR_GREEN)

    draw_box(14.8, 2.2, 4.2, 4.2, "Statistical Drift & Adaptation",
             ["Rolling FIFO Window (N=250)", "2-Sample Kolmogorov-Smirnov Test", "Bonferroni Correction (α = 0.002)", "Anti-Thrashing Cooldown (N=300)", "Anti-Poison Filter: pred_anomaly==0", "Autonomous Model Realignment"],
             "#FFFFFF", COLOR_GREEN, title_color=COLOR_GREEN)

    # Connector 3 -> 5 (Normal Traffic & Drift)
    draw_connector(13.5, 5.5, 14.8, 4.5, "Verified Normal Stream", color=COLOR_GREEN, lw=2.4)

    # Feedback Loop: 5 -> 3 (Retraining realignment)
    draw_connector(14.8, 3.2, 11.7, 3.2, "Retrained Weights", color=COLOR_GREEN, lw=2.2, dashed=True)
    draw_connector(11.7, 3.2, 11.7, 4.4, color=COLOR_GREEN, lw=2.2, dashed=True)

    # ==========================================
    # LAYER 6: PRESENTATION & BENCHMARK FOOTER
    # ==========================================
    footer_box = FancyBboxPatch((0.8, 0.4), 18.5, 1.5, boxstyle="round,pad=0.2",
                                facecolor="#FFFFFF", edgecolor=COLOR_PRIMARY, lw=2.0)
    ax.add_patch(footer_box)

    ax.text(2.5, 1.3, "PRESENTATION TIER", fontsize=11, fontweight='bold', color=COLOR_PRIMARY)
    ax.text(2.5, 0.7, "• Streamlit Real-Time Dashboard\n• Plotly SOC Telemetry Gauges\n• Unified Threat Timeline\n• CSV Forensic Report Exporter",
            fontsize=9.5, color="#4A5568")

    ax.plot([7.2, 7.2], [0.5, 1.7], color=COLOR_BORDER, lw=1.5)

    ax.text(9.5, 1.3, "OFFLINE BENCHMARK TIER", fontsize=11, fontweight='bold', color=COLOR_SECONDARY)
    ax.text(9.5, 0.7, "• UNSW-NB15 Benchmark (ACCS)\n• 29,600 Normal / 14,800 Mixed\n• Isolation Forest vs One-Class SVM\n• IF ROC-AUC: 0.7121 (O(N log N))",
            fontsize=9.5, color="#4A5568")

    ax.plot([14.2, 14.2], [0.5, 1.7], color=COLOR_BORDER, lw=1.5)

    ax.text(16.5, 1.3, "TESTING & INTEGRITY TIER", fontsize=11, fontweight='bold', color=COLOR_GREEN)
    ax.text(16.5, 0.7, "• PyTest 6-Test Automated Suite\n• Preprocessor & Shape Integrity\n• Scoring & Drift Verification\n• 100% Passing in 5.60 Seconds",
            fontsize=9.5, color="#4A5568")

    plt.tight_layout()
    plt.savefig(OUTPUT_FILE, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Architecture diagram successfully generated at: {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_architecture_diagram()
