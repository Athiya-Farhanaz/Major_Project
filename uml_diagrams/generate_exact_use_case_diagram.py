import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Ellipse, Rectangle, Circle
import numpy as np

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "use_case_diagram.png")

FONT_FAMILY = "DejaVu Sans"
COLOR_RED = "#B81D24"       # Deep crisp crimson/red (like Photo 2)
COLOR_YELLOW = "#FFFFE0"    # Soft light cream-yellow (like Photo 2)
COLOR_TEXT = "#000000"      # Sharp black text
COLOR_BG = "#FFFFFF"        # Pure white background

def generate_exact_use_case_diagram():
    fig, ax = plt.subplots(figsize=(24, 15), dpi=300)
    ax.set_xlim(0, 24)
    ax.set_ylim(0, 15)
    ax.axis('off')
    fig.patch.set_facecolor(COLOR_BG)

    # 1. Outer Red System Boundary Box (Like Photo 2)
    boundary_rect = Rectangle((2.5, 0.4), 18.5, 14.2, linewidth=2.6,
                              edgecolor=COLOR_RED, facecolor='none')
    ax.add_patch(boundary_rect)

    # Title at top center of boundary
    ax.text(11.75, 14.2, "Autonomous Real-Time Network Anomaly Detection System",
            ha='center', va='center', fontsize=18, fontweight='bold', color=COLOR_TEXT,
            fontname=FONT_FAMILY, bbox=dict(boxstyle='square,pad=0.4', facecolor='white', edgecolor='none'))

    # Helper function to draw Actor (Like Photo 2: red lines, circle head, yellow label box)
    def draw_actor(x, y, label, label_w=2.2):
        # Head
        head = Circle((x, y + 0.55), 0.32, facecolor='none', edgecolor=COLOR_RED, lw=2.4)
        ax.add_patch(head)
        # Body
        ax.plot([x, x], [y + 0.23, y - 0.45], color=COLOR_RED, lw=2.6)
        # Arms
        ax.plot([x - 0.45, x + 0.45], [y - 0.05, y - 0.05], color=COLOR_RED, lw=2.6)
        # Legs
        ax.plot([x, x - 0.42], [y - 0.45, y - 1.15], color=COLOR_RED, lw=2.6)
        ax.plot([x, x + 0.42], [y - 0.45, y - 1.15], color=COLOR_RED, lw=2.6)
        # Name box below actor (cream-yellow with red border)
        lbl_box = Rectangle((x - label_w/2, y - 1.7), label_w, 0.48, facecolor=COLOR_YELLOW,
                            edgecolor=COLOR_RED, lw=1.8)
        ax.add_patch(lbl_box)
        ax.text(x, y - 1.46, label, ha='center', va='center', fontsize=11, fontweight='bold',
                color=COLOR_TEXT, fontname=FONT_FAMILY)

    # Actors:
    # Left: Security Analyst
    draw_actor(1.2, 7.5, "Security Analyst", label_w=2.0)
    # Right-Top: Security Administrator
    draw_actor(22.4, 12.0, "Security Admin", label_w=2.0)
    # Right-Bottom: Automated Network Gateway
    draw_actor(22.4, 4.0, "Network Gateway\n(Traffic Engine)", label_w=2.2)

    # Helper function to draw Use Case Oval (Like Photo 2: red border, cream-yellow fill)
    def draw_use_case(cx, cy, w, h, text, fontsize=10.5, fontweight='bold'):
        oval = Ellipse((cx, cy), w, h, facecolor=COLOR_YELLOW, edgecolor=COLOR_RED, lw=2.0)
        ax.add_patch(oval)
        ax.text(cx, cy, text, ha='center', va='center', fontsize=fontsize,
                fontweight=fontweight, color=COLOR_TEXT, fontname=FONT_FAMILY, multialignment='center')
        return (cx, cy, w, h)

    # Draw lines: Solid red line from actor to use case
    def draw_assoc(ax_x, ax_y, uc_cx, uc_cy, uc_w, uc_h):
        dx = uc_cx - ax_x
        dy = uc_cy - ax_y
        dist = np.hypot(dx, dy)
        # Point on ellipse boundary
        scale = 1.0 - (0.5 * uc_w / dist) if dist > 0 else 0.8
        target_x = ax_x + dx * scale
        target_y = ax_y + dy * scale
        ax.plot([ax_x, target_x], [ax_y, target_y], color=COLOR_RED, lw=1.8, zorder=1)

    # Draw dashed red arrow with <<include>> or <<extend>> label (Like Photo 2)
    def draw_relation(uc1, uc2, rel_type="<<include>>", label_pos=0.5, label_dy=0.25):
        x1, y1 = uc1[0], uc1[1]
        x2, y2 = uc2[0], uc2[1]
        dx = x2 - x1
        dy = y2 - y1
        dist = np.hypot(dx, dy)
        
        # Start and end points on ellipse boundaries
        start_scale = (0.5 * uc1[2]) / dist
        end_scale = 1.0 - (0.5 * uc2[2]) / dist
        
        sx = x1 + dx * start_scale
        sy = y1 + dy * start_scale
        ex = x1 + dx * end_scale
        ey = y1 + dy * end_scale

        ax.annotate('', xy=(ex, ey), xytext=(sx, sy),
                    arrowprops=dict(arrowstyle="-|>", color=COLOR_RED, lw=1.8, ls='--',
                                    mutation_scale=16))
        
        # Midpoint label
        mx = sx + (ex - sx) * label_pos
        my = sy + (ey - sy) * label_pos + label_dy
        ax.text(mx, my, rel_type, ha='center', va='center', fontsize=9.0,
                fontstyle='italic', color=COLOR_RED, fontname=FONT_FAMILY,
                bbox=dict(boxstyle='square,pad=0.15', facecolor='white', edgecolor='none', alpha=0.9))

    # ==========================================
    # DEFINE USE CASES BY COLUMN
    # ==========================================
    
    # --- ROW 1: Authentication & Stream Start ---
    uc_auth = draw_use_case(12.0, 13.0, 3.2, 1.1, "Authenticate &\nAuthorize Session")
    uc_start = draw_use_case(6.0, 13.0, 3.2, 1.1, "Start / Pause Live\nTraffic Stream")
    draw_relation(uc_start, uc_auth, "<<include>>")
    draw_assoc(1.2, 7.5, 6.0, 13.0, 3.2, 1.1)
    draw_assoc(22.4, 12.0, 12.0, 13.0, 3.2, 1.1)

    # Admin Management Cases (Top Right - Like Photo 2)
    uc_admin1 = draw_use_case(18.0, 13.4, 3.2, 0.9, "Manage User Access &\nPermissions", fontsize=9.5)
    uc_admin2 = draw_use_case(18.0, 12.3, 3.2, 0.9, "Configure Sensitivity\nMultiplier Slider", fontsize=9.5)
    uc_admin3 = draw_use_case(18.0, 11.2, 3.2, 0.9, "Audit System Health &\nHardware Telemetry", fontsize=9.5)
    draw_assoc(22.4, 12.0, 18.0, 13.4, 3.2, 0.9)
    draw_assoc(22.4, 12.0, 18.0, 12.3, 3.2, 0.9)
    draw_assoc(22.4, 12.0, 18.0, 11.2, 3.2, 0.9)

    # --- ROW 2: Threat Injection ---
    uc_inject = draw_use_case(5.5, 11.2, 3.2, 1.1, "Simulate Cyber Threat\nWave Bursts")
    uc_preproc = draw_use_case(11.2, 11.2, 3.2, 1.1, "Normalize 15 Features\n(Scale & One-Hot)")
    draw_relation(uc_inject, uc_preproc, "<<include>>")
    draw_assoc(1.2, 7.5, 5.5, 11.2, 3.2, 1.1)
    
    # Extensions of Threat Injection (Top-Mid-Right)
    uc_syn = draw_use_case(16.5, 10.1, 2.6, 0.8, "SYN Flood Wave", fontsize=9.0)
    uc_brute = draw_use_case(16.5, 9.2, 2.6, 0.8, "SSH Brute Force", fontsize=9.0)
    uc_exfil = draw_use_case(16.5, 8.3, 2.6, 0.8, "Data Exfiltration", fontsize=9.0)
    uc_port = draw_use_case(16.5, 7.4, 2.6, 0.8, "Port Scan Sweep", fontsize=9.0)
    draw_relation(uc_inject, uc_syn, "<<extend>>", label_pos=0.45, label_dy=0.2)
    draw_relation(uc_inject, uc_brute, "<<extend>>", label_pos=0.5, label_dy=0.15)
    draw_relation(uc_inject, uc_exfil, "<<extend>>", label_pos=0.55, label_dy=-0.15)
    draw_relation(uc_inject, uc_port, "<<extend>>", label_pos=0.6, label_dy=-0.2)

    # --- ROW 3: Anomaly Detection ---
    uc_detect = draw_use_case(5.5, 9.0, 3.2, 1.1, "Detect Anomalies\n(Isolation Forest)")
    uc_scoring = draw_use_case(11.2, 9.0, 3.2, 1.1, "Evaluate Path Length\nScore vs 99th % Thresh")
    draw_relation(uc_detect, uc_scoring, "<<include>>")
    draw_assoc(1.2, 7.5, 5.5, 9.0, 3.2, 1.1)

    # --- ROW 4: Explainable AI (XAI) ---
    uc_xai = draw_use_case(5.5, 6.8, 3.2, 1.1, "Inspect Explainable AI\n(XAI) Insights")
    uc_shap = draw_use_case(11.2, 6.8, 3.2, 1.1, "Compute TreeSHAP\nShapley Attribution")
    draw_relation(uc_xai, uc_shap, "<<include>>")
    draw_assoc(1.2, 7.5, 5.5, 6.8, 3.2, 1.1)

    # Extensions of XAI (Mid-Right)
    uc_waterfall = draw_use_case(16.5, 6.4, 2.8, 0.85, "View Interactive\nWaterfall Plot", fontsize=9.0)
    uc_nlp = draw_use_case(16.5, 5.4, 2.8, 0.85, "View Plain-English\nSecurity Diagnosis", fontsize=9.0)
    uc_json = draw_use_case(16.5, 4.4, 2.8, 0.85, "Inspect Raw Flow\nJSON Packet Data", fontsize=9.0)
    draw_relation(uc_shap, uc_waterfall, "<<extend>>", label_pos=0.5, label_dy=0.2)
    draw_relation(uc_shap, uc_nlp, "<<extend>>", label_pos=0.5, label_dy=0.15)
    draw_relation(uc_shap, uc_json, "<<extend>>", label_pos=0.5, label_dy=-0.15)

    # --- ROW 5: Concept Drift Monitoring ---
    uc_drift = draw_use_case(5.5, 4.6, 3.2, 1.1, "Monitor Concept Drift\n(WFH / VPN Shift)")
    uc_ks = draw_use_case(11.2, 4.6, 3.2, 1.1, "Execute 2-Sample KS-Test\nwith Bonferroni (α=0.002)")
    draw_relation(uc_drift, uc_ks, "<<include>>")
    draw_assoc(1.2, 7.5, 5.5, 4.6, 3.2, 1.1)
    draw_assoc(22.4, 4.0, 11.2, 4.6, 3.2, 1.1)

    # Extensions of Drift
    uc_pvals = draw_use_case(16.5, 3.4, 2.8, 0.85, "Track Log-Scale\np-Value Curves", fontsize=9.0)
    uc_audit = draw_use_case(16.5, 2.4, 2.8, 0.85, "Audit Retraining\nMaintenance Logs", fontsize=9.0)
    draw_relation(uc_ks, uc_pvals, "<<extend>>", label_pos=0.5, label_dy=0.15)
    draw_relation(uc_ks, uc_audit, "<<extend>>", label_pos=0.5, label_dy=-0.15)

    # --- ROW 6: Adaptive Retraining with Anti-Poisoning ---
    uc_retrain = draw_use_case(5.5, 2.4, 3.2, 1.1, "Autonomous Adaptive\nModel Retraining")
    uc_filter = draw_use_case(11.2, 2.4, 3.2, 1.1, "Filter Retraining Buffer\n(pred_anomaly == 0)")
    draw_relation(uc_retrain, uc_filter, "<<include>>")
    draw_assoc(1.2, 7.5, 5.5, 2.4, 3.2, 1.1)
    draw_assoc(22.4, 4.0, 5.5, 2.4, 3.2, 1.1)

    # --- ROW 7: Forensic Report Export & Offline Validation ---
    uc_export = draw_use_case(5.5, 0.9, 3.2, 0.8, "Export Incident Forensics\nReport (CSV)", fontsize=9.5)
    uc_bench = draw_use_case(11.2, 0.9, 3.2, 0.8, "View UNSW-NB15 Offline\nBenchmark & Metrics", fontsize=9.5)
    draw_assoc(1.2, 7.5, 5.5, 0.9, 3.2, 0.8)
    draw_assoc(1.2, 7.5, 11.2, 0.9, 3.2, 0.8)
    draw_assoc(22.4, 4.0, 11.2, 0.9, 3.2, 0.8)

    plt.tight_layout()
    plt.savefig(OUTPUT_FILE, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Exact Use Case diagram generated successfully at: {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_exact_use_case_diagram()
