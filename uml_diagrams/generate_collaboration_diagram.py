import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, ArrowStyle
import numpy as np

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "collaboration_diagram.png")

FONT_FAMILY = "DejaVu Sans"
COLOR_PRIMARY = "#1A365D"     # Deep corporate navy
COLOR_SECONDARY = "#2B6CB0"   # Classic slate blue
COLOR_ACCENT = "#C53030"      # Crimson alert
COLOR_GREEN = "#276749"       # Deep emerald
COLOR_BG = "#FFFFFF"          # Pure white
COLOR_BOX_FILL = "#F7FAFC"    # Crisp light slate
COLOR_LINE = "#2D3748"        # Charcoal line

def generate_collaboration_diagram():
    fig, ax = plt.subplots(figsize=(19, 13), dpi=300)
    ax.set_xlim(0, 19)
    ax.set_ylim(0, 13)
    ax.axis('off')
    fig.patch.set_facecolor(COLOR_BG)

    # Header
    ax.text(9.5, 12.5, "UML COLLABORATION / COMMUNICATION DIAGRAM", ha='center', va='center',
            fontsize=24, fontweight='bold', color=COLOR_PRIMARY, fontname=FONT_FAMILY)
    ax.text(9.5, 12.1, "Autonomous Real-Time Network Anomaly Detection System (Object Collaboration & Message Flow)",
            ha='center', va='center', fontsize=13, fontstyle='italic', color=COLOR_SECONDARY, fontname=FONT_FAMILY)
    ax.plot([1.0, 18.0], [11.8, 11.8], color=COLOR_PRIMARY, lw=2.2)

    def draw_object(x, y, w, h, name, class_name, fill="#FFFFFF", border=COLOR_PRIMARY):
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.2",
                             facecolor=fill, edgecolor=border, linewidth=2.2)
        ax.add_patch(box)
        ax.text(x + w / 2, y + h / 2 + 0.18, name, ha='center', va='center',
                fontsize=11.5, fontweight='bold', color=border, fontname=FONT_FAMILY)
        ax.text(x + w / 2, y + h / 2 - 0.22, f": {class_name}", ha='center', va='center',
                fontsize=10.5, fontstyle='italic', color="#4A5568", fontname=FONT_FAMILY)

    # Objects / Roles
    # 1. Actor
    head = Circle((1.8, 6.75), 0.38, facecolor="#E2E8F0", edgecolor=COLOR_PRIMARY, lw=2.2)
    ax.add_patch(head)
    ax.plot([1.8, 1.8], [6.37, 5.55], color=COLOR_PRIMARY, lw=2.6)
    ax.plot([1.25, 2.35], [6.05, 6.05], color=COLOR_PRIMARY, lw=2.6)
    ax.plot([1.8, 1.35], [5.55, 4.75], color=COLOR_PRIMARY, lw=2.6)
    ax.plot([1.8, 2.25], [5.55, 4.75], color=COLOR_PRIMARY, lw=2.6)
    ax.text(1.8, 4.4, "SOC Analyst\n/ Operator", ha='center', va='top',
            fontsize=11, fontweight='bold', color=COLOR_PRIMARY)

    # 2. Simulator
    draw_object(4.2, 5.0, 2.8, 1.8, "trafficSim", "NetworkTrafficSimulator", "#EBF8FF", COLOR_SECONDARY)

    # 3. Preprocessor
    draw_object(8.2, 8.8, 2.8, 1.8, "preprocessor", "NetworkPreprocessor", "#EDF2F7", COLOR_PRIMARY)

    # 4. AnomalyDetector
    draw_object(8.2, 5.0, 2.8, 1.8, "detector", "AnomalyDetector (IsolationForest)", "#FEFCBF", "#B7791F")

    # 5. XAI Engine
    draw_object(13.2, 8.8, 3.0, 1.8, "xaiEngine", "NetworkXAI (TreeSHAP)", "#FFF5F5", COLOR_ACCENT)

    # 6. DriftDetector
    draw_object(13.2, 5.0, 3.0, 1.8, "driftMonitor", "ConceptDriftDetector (KS-Test)", "#F0FFF4", COLOR_GREEN)

    # 7. Dashboard / Controller
    draw_object(8.2, 1.2, 3.2, 1.8, "dashboardUI", "StreamlitOperationsConsole", "#FAF5FF", "#6B46C1")

    # Links and Numbered Collaboration Messages
    def draw_link_with_msg(x1, y1, x2, y2, messages, label_pos=(0, 0), side='top'):
        ax.plot([x1, x2], [y1, y2], color=COLOR_LINE, lw=1.8, zorder=1)
        mx, my = (x1 + x2) / 2 + label_pos[0], (y1 + y2) / 2 + label_pos[1]
        
        # Draw messages box
        msg_text = "\n".join(messages)
        ax.text(mx, my, msg_text, ha='center', va='center',
                fontsize=9.0, fontweight='bold', color=COLOR_PRIMARY,
                bbox=dict(boxstyle='round,pad=0.25', facecolor='#FFFFFF', edgecolor='#CBD5E0', lw=1.2, alpha=0.95))

    # Link: Analyst -> Dashboard
    draw_link_with_msg(2.4, 5.2, 8.2, 2.1,
                       ["1: startStream()", "2: injectAttackWave(type)", "3: adjustSensitivity(mult)"],
                       label_pos=(-1.0, -0.6))

    # Link: Dashboard -> Simulator
    draw_link_with_msg(8.2, 2.6, 6.0, 5.0,
                       ["1.1: generateFlow()", "2.1: setAttackBurst()"],
                       label_pos=(-0.8, -0.5))

    # Link: Simulator -> Preprocessor
    draw_link_with_msg(5.6, 6.8, 8.2, 9.4,
                       ["1.2: transform(rawFlow)"],
                       label_pos=(-0.5, 0.4))

    # Link: Preprocessor -> Detector
    draw_link_with_msg(9.6, 8.8, 9.6, 6.8,
                       ["1.3: predict(X_single)", "returns: [is_anom, score]"],
                       label_pos=(1.8, 0.0))

    # Link: Detector -> XAI Engine (Conditional on Anomaly)
    draw_link_with_msg(11.0, 6.5, 13.2, 9.2,
                       ["1.4 [if is_anom==1]:", "explainInstance(raw, X)", "returns: waterfall & NLP"],
                       label_pos=(0.4, 0.6))

    # Link: Detector -> DriftDetector
    draw_link_with_msg(11.0, 5.9, 13.2, 5.9,
                       ["1.5: update(rawFlow)", "evaluates: KS p-values"],
                       label_pos=(0.0, 0.45))

    # Link: DriftDetector -> Detector (Retraining Feedback Loop)
    draw_link_with_msg(14.7, 5.0, 11.0, 5.2,
                       ["1.6 [if drift_detected]:", "filterBuffer(pred==0)", "retrainModel()"],
                       label_pos=(-0.2, -0.9))

    # Link: DriftDetector & XAI -> Dashboard
    draw_link_with_msg(14.7, 8.8, 11.4, 2.5,
                       ["1.7: updateTimeline()", "1.8: renderWaterfall()", "1.9: logDriftPValues()"],
                       label_pos=(1.2, -0.2))

    # Legend / Note at bottom
    note_box = FancyBboxPatch((1.2, 0.5), 6.0, 1.8, boxstyle="round,pad=0.2",
                              facecolor="#FFFFF0", edgecolor="#ECC94B", lw=1.5)
    ax.add_patch(note_box)
    ax.text(1.4, 2.0, "UML Collaboration Notation Key:", fontsize=10, fontweight='bold', color="#744210")
    ax.text(1.4, 1.5, "• Links show bidirectional communication paths between objects.", fontsize=9, color="#4A5568")
    ax.text(1.4, 1.1, "• Numbered labels (1.x) show sequential message execution order.", fontsize=9, color="#4A5568")
    ax.text(1.4, 0.7, "• Guard conditions [if ...] represent conditional streaming actions.", fontsize=9, color="#4A5568")

    plt.tight_layout()
    plt.savefig(OUTPUT_FILE, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Collaboration diagram successfully generated at: {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_collaboration_diagram()
