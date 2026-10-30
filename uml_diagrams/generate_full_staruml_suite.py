import json
import uuid
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_MDJ = os.path.join(OUTPUT_DIR, "major_project_diagrams.mdj")

def get_id():
    return str(uuid.uuid4()).replace("-", "")[:24]

# Exact College Style Palette (Photo 2)
COLOR_RED = "#B81D24"       # Deep crisp crimson/red
COLOR_YELLOW = "#FFFFE0"    # Soft light cream-yellow
COLOR_BLACK = "#000000"
COLOR_WHITE = "#FFFFFF"

def build_full_staruml_suite():
    project_id = get_id()
    model_id = get_id()

    # Diagram IDs
    uc_diag_id = get_id()
    arch_diag_id = get_id()
    comm_diag_id = get_id()
    seq_diag_id = get_id()
    comp_diag_id = get_id()
    dep_diag_id = get_id()
    act_diag_id = get_id()
    class_diag_id = get_id()
    sm_diag_id = get_id()

    # Containers
    interact_id = get_id()
    comm_interact_id = get_id()
    act_container_id = get_id()
    sm_container_id = get_id()

    # Master list of model elements under Major Project UML Model
    model_elements = []

    # Helper to add standard System Boundary Subject View
    def make_boundary_view(diag_id, title, left=50, top=30, width=1200, height=720):
        v_sub_id = get_id()
        nc_sub_id = get_id()
        return {
            "_type": "UMLUseCaseSubjectView",
            "_id": v_sub_id,
            "_parent": {"$ref": diag_id},
            "font": "Arial;13;1",
            "left": left,
            "top": top,
            "width": width,
            "height": height,
            "name": title,
            "lineColor": COLOR_RED,
            "fillColor": COLOR_WHITE,
            "nameCompartment": {
                "_type": "UMLNameCompartmentView",
                "_id": nc_sub_id,
                "_parent": {"$ref": v_sub_id},
                "font": "Arial;14;1",
                "left": left + width // 4,
                "top": top + 10,
                "width": width // 2,
                "height": 22,
                "text": title,
                "fontColor": COLOR_BLACK
            }
        }

    # =========================================================================
    # 1. USE CASE DIAGRAM
    # =========================================================================
    uc_views = []
    uc_views.append(make_boundary_view(uc_diag_id, "Autonomous Real-Time Network Anomaly Detection System - Use Cases", 180, 30, 860, 720))

    # Actors
    act_analyst_id = get_id()
    act_admin_id = get_id()
    act_gateway_id = get_id()
    model_elements.extend([
        {"_type": "UMLActor", "_id": act_analyst_id, "name": "Security Analyst"},
        {"_type": "UMLActor", "_id": act_admin_id, "name": "Security Admin"},
        {"_type": "UMLActor", "_id": act_gateway_id, "name": "Network Gateway"}
    ])

    def add_actor_view(diag_id, m_id, name, left, top):
        v_id = get_id()
        nc_id = get_id()
        return {
            "_type": "UMLActorView",
            "_id": v_id,
            "_parent": {"$ref": diag_id},
            "model": {"$ref": m_id},
            "font": "Arial;13;0",
            "left": left,
            "top": top,
            "width": 60,
            "height": 85,
            "lineColor": COLOR_RED,
            "fillColor": COLOR_YELLOW,
            "nameCompartment": {
                "_type": "UMLNameCompartmentView",
                "_id": nc_id,
                "_parent": {"$ref": v_id},
                "model": {"$ref": m_id},
                "font": "Arial;12;1",
                "left": left - 30,
                "top": top + 90,
                "width": 120,
                "height": 24,
                "text": name,
                "lineColor": COLOR_RED,
                "fillColor": COLOR_YELLOW,
                "fontColor": COLOR_BLACK
            }
        }

    v_uc_analyst = add_actor_view(uc_diag_id, act_analyst_id, "Security Analyst", 60, 340)
    v_uc_admin = add_actor_view(uc_diag_id, act_admin_id, "Security Admin", 1080, 120)
    v_uc_gateway = add_actor_view(uc_diag_id, act_gateway_id, "Network Gateway", 1080, 480)
    uc_views.extend([v_uc_analyst, v_uc_admin, v_uc_gateway])

    # Use Cases Definitions
    uc_defs = [
        ("uc_start", "Start Live Traffic Stream", 210, 80, 200, 55),
        ("uc_inject", "Inject Threat Vectors", 210, 180, 200, 55),
        ("uc_detect", "Inspect Anomaly Decisions", 210, 290, 200, 55),
        ("uc_xai", "Inspect XAI Insights", 210, 400, 200, 55),
        ("uc_drift", "Monitor Concept Drift", 210, 510, 200, 55),
        ("uc_retrain", "Autonomous Retraining", 210, 600, 200, 55),
        ("uc_export", "Export Forensic Report", 210, 680, 200, 55),

        ("uc_auth", "Authenticate User Session", 500, 80, 200, 55),
        ("uc_preproc", "Normalize 15 NetFlow Features", 500, 180, 200, 55),
        ("uc_scoring", "Evaluate Isolation Forest Score", 500, 290, 200, 55),
        ("uc_shap", "Compute TreeSHAP Attribution", 500, 400, 200, 55),
        ("uc_ks", "Execute Rolling KS-Test (α=0.002)", 500, 510, 200, 55),
        ("uc_filter", "Filter Buffer (pred_anomaly==0)", 500, 600, 200, 55),
        ("uc_bench", "View UNSW-NB15 Benchmark", 500, 680, 200, 55),

        ("uc_adm_users", "Manage User Accounts", 790, 70, 190, 50),
        ("uc_adm_sens", "Configure Sensitivity Slider", 790, 130, 190, 50),
        ("uc_adm_health", "Audit System Health (psutil)", 790, 190, 190, 50),
        ("uc_syn", "Simulate SYN Flood Wave", 790, 260, 190, 50),
        ("uc_brute", "Simulate SSH Brute Force", 790, 320, 190, 50),
        ("uc_exfil", "Simulate Data Exfiltration", 790, 380, 190, 50),
        ("uc_waterfall", "View SHAP Waterfall Chart", 790, 450, 190, 50),
        ("uc_nlp", "View Plain-English Diagnosis", 790, 510, 190, 50),
        ("uc_json", "Inspect Raw Flow JSON", 790, 570, 190, 50),
        ("uc_pvals", "Track Log-Scale p-Values", 790, 640, 190, 50)
    ]

    uc_map = {}
    for key, name, left, top, w, h in uc_defs:
        m_id = get_id()
        v_id = get_id()
        nc_id = get_id()
        model_elements.append({"_type": "UMLUseCase", "_id": m_id, "name": name})
        uc_views.append({
            "_type": "UMLUseCaseView",
            "_id": v_id,
            "_parent": {"$ref": uc_diag_id},
            "model": {"$ref": m_id},
            "font": "Arial;12;0",
            "left": left,
            "top": top,
            "width": w,
            "height": h,
            "lineColor": COLOR_RED,
            "fillColor": COLOR_YELLOW,
            "nameCompartment": {
                "_type": "UMLNameCompartmentView",
                "_id": nc_id,
                "_parent": {"$ref": v_id},
                "model": {"$ref": m_id},
                "font": "Arial;11;0",
                "left": left + 10,
                "top": top + 15,
                "width": w - 20,
                "height": 24,
                "text": name,
                "fontColor": COLOR_BLACK
            }
        })
        uc_map[key] = (v_id, m_id, (left, top, w, h))

    # Helper for Solid Association Line (Actor -> Use Case)
    def add_uc_assoc(v1_id, v2_id, p1, p2):
        uc_views.append({
            "_type": "UMLAssociationView",
            "_id": get_id(),
            "_parent": {"$ref": uc_diag_id},
            "font": "Arial;13;0",
            "head": {"$ref": v2_id},
            "tail": {"$ref": v1_id},
            "lineStyle": 1,
            "lineColor": COLOR_RED,
            "points": f"{p1[0]};{p1[1]}:{p2[0]};{p2[1]}"
        })

    # Helper for Dashed Relationship Arrow with <<include>> or <<extend>>
    def add_uc_dep(v1_id, v2_id, p1, p2, stereotype="<<include>>"):
        uc_views.append({
            "_type": "UMLDependencyView",
            "_id": get_id(),
            "_parent": {"$ref": uc_diag_id},
            "font": "Arial;11;2",
            "head": {"$ref": v2_id},
            "tail": {"$ref": v1_id},
            "lineStyle": 1,
            "lineColor": COLOR_RED,
            "points": f"{p1[0]};{p1[1]}:{p2[0]};{p2[1]}",
            "name": stereotype
        })

    # Connect Analyst
    for key, pt in [("uc_start", (210, 105)), ("uc_inject", (210, 205)), ("uc_detect", (210, 315)),
                    ("uc_xai", (210, 425)), ("uc_drift", (210, 535)), ("uc_retrain", (210, 625)), ("uc_export", (210, 705))]:
        add_uc_assoc(v_uc_analyst["_id"], uc_map[key][0], (120, 380), pt)

    # Connect Admin
    for key, pt in [("uc_auth", (700, 105)), ("uc_adm_users", (980, 95)), ("uc_adm_sens", (980, 155)), ("uc_adm_health", (980, 215))]:
        add_uc_assoc(v_uc_admin["_id"], uc_map[key][0], (1080, 160), pt)

    # Connect Gateway
    for key, pt in [("uc_preproc", (700, 205)), ("uc_ks", (700, 535)), ("uc_filter", (700, 625))]:
        add_uc_assoc(v_uc_gateway["_id"], uc_map[key][0], (1080, 520), pt)

    # Includes
    add_uc_dep(uc_map["uc_start"][0], uc_map["uc_auth"][0], (410, 105), (500, 105), "<<include>>")
    add_uc_dep(uc_map["uc_inject"][0], uc_map["uc_preproc"][0], (410, 205), (500, 205), "<<include>>")
    add_uc_dep(uc_map["uc_detect"][0], uc_map["uc_scoring"][0], (410, 315), (500, 315), "<<include>>")
    add_uc_dep(uc_map["uc_xai"][0], uc_map["uc_shap"][0], (410, 425), (500, 425), "<<include>>")
    add_uc_dep(uc_map["uc_drift"][0], uc_map["uc_ks"][0], (410, 535), (500, 535), "<<include>>")
    add_uc_dep(uc_map["uc_retrain"][0], uc_map["uc_filter"][0], (410, 625), (500, 625), "<<include>>")
    add_uc_dep(uc_map["uc_export"][0], uc_map["uc_bench"][0], (410, 705), (500, 705), "<<include>>")

    # Extends
    add_uc_dep(uc_map["uc_inject"][0], uc_map["uc_syn"][0], (410, 215), (790, 280), "<<extend>>")
    add_uc_dep(uc_map["uc_inject"][0], uc_map["uc_brute"][0], (410, 215), (790, 345), "<<extend>>")
    add_uc_dep(uc_map["uc_inject"][0], uc_map["uc_exfil"][0], (410, 215), (790, 405), "<<extend>>")
    add_uc_dep(uc_map["uc_shap"][0], uc_map["uc_waterfall"][0], (700, 425), (790, 470), "<<extend>>")
    add_uc_dep(uc_map["uc_shap"][0], uc_map["uc_nlp"][0], (700, 425), (790, 535), "<<extend>>")
    add_uc_dep(uc_map["uc_shap"][0], uc_map["uc_json"][0], (700, 425), (790, 595), "<<extend>>")
    add_uc_dep(uc_map["uc_ks"][0], uc_map["uc_pvals"][0], (700, 545), (790, 660), "<<extend>>")

    # =========================================================================
    # 2. SYSTEM ARCHITECTURE DIAGRAM (UMLClassDiagram)
    # =========================================================================
    arch_views = []
    arch_views.append(make_boundary_view(arch_diag_id, "Autonomous Real-Time Network Anomaly Detection System - Architecture", 40, 30, 1260, 680))

    def make_tier_class_view(diag_id, name, left, top, w=220, h=130, attributes=[], methods=[]):
        m_id = get_id()
        v_id = get_id()
        nc_id = get_id()
        model_elements.append({"_type": "UMLClass", "_id": m_id, "name": name})
        
        attr_views = []
        for attr in attributes:
            attr_views.append({
                "_type": "UMLAttributeView",
                "_id": get_id(),
                "_parent": {"$ref": v_id},
                "font": "Arial;11;0",
                "text": attr,
                "fontColor": COLOR_BLACK
            })
            
        oper_views = []
        for m in methods:
            oper_views.append({
                "_type": "UMLOperationView",
                "_id": get_id(),
                "_parent": {"$ref": v_id},
                "font": "Arial;11;0",
                "text": m,
                "fontColor": COLOR_BLACK
            })

        view = {
            "_type": "UMLClassView",
            "_id": v_id,
            "_parent": {"$ref": diag_id},
            "model": {"$ref": m_id},
            "font": "Arial;12;0",
            "left": left,
            "top": top,
            "width": w,
            "height": h,
            "lineColor": COLOR_RED,
            "fillColor": COLOR_YELLOW,
            "nameCompartment": {
                "_type": "UMLNameCompartmentView",
                "_id": nc_id,
                "_parent": {"$ref": v_id},
                "model": {"$ref": m_id},
                "font": "Arial;12;1",
                "left": left + 5,
                "top": top + 5,
                "width": w - 10,
                "height": 24,
                "text": name,
                "lineColor": COLOR_RED,
                "fillColor": COLOR_YELLOW,
                "fontColor": COLOR_BLACK
            }
        }
        return view, (v_id, m_id, (left, top, w, h))

    # 5 Tiers
    v_arch_ingest, t_ingest = make_tier_class_view(arch_diag_id, "1. Ingestion Tier\nNetworkTrafficSimulator", 70, 100, 210, 150,
                                                  ["+ raw_flow: dict", "+ is_drift: bool"], ["+ generate_flow()", "+ simulate_attacks()"])
    v_arch_threat, t_threat = make_tier_class_view(arch_diag_id, "Threat Synthesizer\n(SYN/Brute/Exfil)", 70, 320, 210, 140,
                                                  ["+ syn_flood: Wave", "+ exfil: Wave"], ["+ inject_attack()"])

    v_arch_prep, t_prep = make_tier_class_view(arch_diag_id, "2. Preprocessing Tier\nNetworkPreprocessor", 310, 100, 210, 150,
                                              ["- scaler: StandardScaler", "- encoder: OneHot"], ["+ fit_transform()", "+ transform()"])
    v_arch_buf, t_buf = make_tier_class_view(arch_diag_id, "Sliding Buffer Cache\n(Window N=250)", 310, 320, 210, 140,
                                            ["+ buffer: List[Flow]", "+ size: int = 250"], ["+ push(record)", "+ get_clean()"])

    v_arch_if, t_if = make_tier_class_view(arch_diag_id, "3. ML Detection Tier\nIsolationForestCore", 550, 100, 220, 150,
                                          ["- n_estimators: 100", "- threshold: 99th %tile"], ["+ predict()", "+ get_score()"])
    v_arch_gate, t_gate = make_tier_class_view(arch_diag_id, "Decision Logic Gate\n(Real-Time Filter)", 550, 320, 220, 140,
                                              ["+ contamination: 0.01", "+ latency: < 2ms"], ["+ flag_threat()", "+ log_alert()"])

    v_arch_xai, t_xai = make_tier_class_view(arch_diag_id, "4. XAI Tier\nTreeSHAPEngine", 800, 100, 220, 150,
                                            ["- explainer: TreeExplainer", "+ overhead: ~95ms"], ["+ explain_instance()", "+ get_nlp_text()"])
    v_arch_ks, t_ks = make_tier_class_view(arch_diag_id, "Concept Drift Monitor\n(2-Sample KS-Test)", 800, 320, 220, 140,
                                          ["+ alpha: 0.002", "+ bonferroni: True"], ["+ run_ks_test()", "+ trigger_retrain()"])

    v_arch_ui, t_ui = make_tier_class_view(arch_diag_id, "5. Presentation Tier\nStreamlitDashboard", 1050, 100, 220, 150,
                                          ["+ port: 8501", "+ session_state"], ["+ render_kpis()", "+ stream_plotly()"])
    v_arch_soc, t_soc = make_tier_class_view(arch_diag_id, "SOC Analyst Control\n(Interactive HUD)", 1050, 320, 220, 140,
                                            ["+ one_click_inject", "+ alert_console"], ["+ export_csv()", "+ toggle_drift()"])

    arch_views.extend([v_arch_ingest, v_arch_threat, v_arch_prep, v_arch_buf, v_arch_if, v_arch_gate, v_arch_xai, v_arch_ks, v_arch_ui, v_arch_soc])

    def add_arch_dep(diag_id, v1, v2, p1, p2, label=""):
        arch_views.append({
            "_type": "UMLDependencyView",
            "_id": get_id(),
            "_parent": {"$ref": diag_id},
            "font": "Arial;10;1",
            "head": {"$ref": v2[0]},
            "tail": {"$ref": v1[0]},
            "lineStyle": 1,
            "lineColor": COLOR_RED,
            "points": f"{p1[0]};{p1[1]}:{p2[0]};{p2[1]}",
            "name": label
        })

    add_arch_dep(arch_diag_id, t_ingest, t_prep, (280, 160), (310, 160), "raw netflow")
    add_arch_dep(arch_diag_id, t_prep, t_if, (520, 160), (550, 160), "vector X")
    add_arch_dep(arch_diag_id, t_if, t_xai, (770, 160), (800, 160), "if anomaly")
    add_arch_dep(arch_diag_id, t_xai, t_ui, (1020, 160), (1050, 160), "SHAP & NLP")
    add_arch_dep(arch_diag_id, t_prep, t_buf, (415, 250), (415, 320), "buffer stream")
    add_arch_dep(arch_diag_id, t_buf, t_ks, (520, 380), (800, 380), "eval buffer")
    add_arch_dep(arch_diag_id, t_ks, t_if, (800, 320), (770, 220), "retrain refit")
    add_arch_dep(arch_diag_id, t_gate, t_ui, (770, 340), (1050, 220), "threat alert")

    # =========================================================================
    # 3. COLLABORATION / COMMUNICATION DIAGRAM
    # =========================================================================
    comm_views = []
    comm_views.append(make_boundary_view(comm_diag_id, "Autonomous Real-Time Network Anomaly Detection System - Collaboration Diagram", 50, 30, 1160, 660))

    comm_nodes = [
        ("c_analyst", "Security Analyst\n(Operator)", 80, 300, 160, 80),
        ("c_dash", ":DashboardController\n(Streamlit UI)", 300, 300, 180, 80),
        ("c_sim", ":TrafficSimulator\n(NetFlow Source)", 540, 100, 180, 80),
        ("c_prep", ":NetworkPreprocessor\n(Scaler/Encoder)", 540, 300, 180, 80),
        ("c_det", ":AnomalyDetector\n(Isolation Forest)", 780, 300, 180, 80),
        ("c_xai", ":NetworkXAI\n(TreeSHAP Engine)", 780, 100, 180, 80),
        ("c_drift", ":DriftDetector\n(KS-Test Monitor)", 780, 500, 180, 80),
        ("c_retrain", ":RetrainEngine\n(Anti-Poison Filter)", 540, 500, 180, 80),
        ("c_store", ":ModelStore\n(Pickle/JSON)", 1000, 300, 160, 80)
    ]

    comm_map = {}
    for key, name, left, top, w, h in comm_nodes:
        m_id = get_id()
        v_id = get_id()
        nc_id = get_id()
        comm_views.append({
            "_type": "UMLClassView",
            "_id": v_id,
            "_parent": {"$ref": comm_diag_id},
            "font": "Arial;12;0",
            "left": left,
            "top": top,
            "width": w,
            "height": h,
            "lineColor": COLOR_RED,
            "fillColor": COLOR_YELLOW,
            "nameCompartment": {
                "_type": "UMLNameCompartmentView",
                "_id": nc_id,
                "_parent": {"$ref": v_id},
                "font": "Arial;11;1",
                "left": left + 5,
                "top": top + 20,
                "width": w - 10,
                "height": 26,
                "text": name,
                "fontColor": COLOR_BLACK
            }
        })
        comm_map[key] = (v_id, m_id, (left, top, w, h))

    def add_comm_link(diag_id, n1, n2, p1, p2, label=""):
        comm_views.append({
            "_type": "UMLAssociationView",
            "_id": get_id(),
            "_parent": {"$ref": diag_id},
            "font": "Arial;10;1",
            "head": {"$ref": n2[0]},
            "tail": {"$ref": n1[0]},
            "lineStyle": 1,
            "lineColor": COLOR_RED,
            "points": f"{p1[0]};{p1[1]}:{p2[0]};{p2[1]}",
            "name": label
        })

    add_comm_link(comm_diag_id, comm_map["c_analyst"], comm_map["c_dash"], (240, 340), (300, 340), "1: click 'Start Stream' ➔\n8: inspect HUD ➔")
    add_comm_link(comm_diag_id, comm_map["c_dash"], comm_map["c_sim"], (390, 300), (540, 140), "2: generate_flow() ➔\n2.1: raw_flow record ➔")
    add_comm_link(comm_diag_id, comm_map["c_dash"], comm_map["c_prep"], (480, 340), (540, 340), "3: transform(raw) ➔\n3.1: scaled vector X ➔")
    add_comm_link(comm_diag_id, comm_map["c_prep"], comm_map["c_det"], (720, 340), (780, 340), "4: predict(X) ➔\n4.1: score & flag ➔")
    add_comm_link(comm_diag_id, comm_map["c_det"], comm_map["c_xai"], (870, 300), (870, 180), "5: [if threat] explain() ➔\n5.1: SHAP values & NLP ➔")
    add_comm_link(comm_diag_id, comm_map["c_det"], comm_map["c_drift"], (870, 380), (870, 500), "6: update(raw) ➔\n6.1: drift p-values ➔")
    add_comm_link(comm_diag_id, comm_map["c_drift"], comm_map["c_retrain"], (780, 540), (720, 540), "7: [if drift] retrain() ➔\n7.1: clean buffer filtered ➔")
    add_comm_link(comm_diag_id, comm_map["c_retrain"], comm_map["c_det"], (630, 500), (780, 370), "7.2: refit_model() ➔")
    add_comm_link(comm_diag_id, comm_map["c_det"], comm_map["c_store"], (960, 340), (1000, 340), "4.2: load weights ➔\n7.3: persist model ➔")

    # =========================================================================
    # 4. SEQUENCE DIAGRAM (UMLSequenceDiagram)
    # =========================================================================
    seq_views = []
    seq_views.append(make_boundary_view(seq_diag_id, "Autonomous Real-Time Network Anomaly Detection System - Sequence Diagram", 40, 30, 1260, 680))

    seq_lifelines = [
        ("Security Analyst\n(SOC)", 70),
        ("Dashboard Controller\n(UI)", 240),
        ("Traffic Simulator\n(NetFlow)", 410),
        ("Preprocessor\n(Pipeline)", 580),
        ("Anomaly Detector\n(Isolation Forest)", 750),
        ("TreeSHAP Engine\n(XAI)", 920),
        ("Drift Monitor\n(KS-Test)", 1090)
    ]

    seq_map = {}
    for name, left in seq_lifelines:
        m_id = get_id()
        v_id = get_id()
        nc_id = get_id()
        seq_views.append({
            "_type": "UMLSeqLifelineView",
            "_id": v_id,
            "_parent": {"$ref": seq_diag_id},
            "font": "Arial;12;0",
            "left": left,
            "top": 80,
            "width": 140,
            "height": 580,
            "lineColor": COLOR_RED,
            "fillColor": COLOR_YELLOW,
            "nameCompartment": {
                "_type": "UMLNameCompartmentView",
                "_id": nc_id,
                "_parent": {"$ref": v_id},
                "font": "Arial;11;1",
                "left": left + 5,
                "top": 85,
                "width": 130,
                "height": 26,
                "text": name,
                "lineColor": COLOR_RED,
                "fillColor": COLOR_YELLOW,
                "fontColor": COLOR_BLACK
            }
        })
        seq_map[name] = (v_id, left + 70)

    seq_messages = [
        (seq_lifelines[0][0], seq_lifelines[1][0], 140, "1: Click 'Start Live Stream'", "synchCall"),
        (seq_lifelines[1][0], seq_lifelines[2][0], 175, "2: generate_single_flow()", "synchCall"),
        (seq_lifelines[2][0], seq_lifelines[1][0], 210, "3: return raw_flow record", "reply"),
        (seq_lifelines[1][0], seq_lifelines[3][0], 245, "4: transform(raw_flow)", "synchCall"),
        (seq_lifelines[3][0], seq_lifelines[1][0], 280, "5: return scaled vector X", "reply"),
        (seq_lifelines[1][0], seq_lifelines[4][0], 315, "6: predict(X) [Latency < 2ms]", "synchCall"),
        (seq_lifelines[4][0], seq_lifelines[1][0], 350, "7: return (anomaly_flag, score)", "reply"),
        (seq_lifelines[1][0], seq_lifelines[5][0], 385, "8: [if threat] explain(raw, X)", "synchCall"),
        (seq_lifelines[5][0], seq_lifelines[1][0], 420, "9: return SHAP values & NLP summary", "reply"),
        (seq_lifelines[1][0], seq_lifelines[6][0], 455, "10: update(raw_flow) [buffer N=250]", "synchCall"),
        (seq_lifelines[6][0], seq_lifelines[1][0], 490, "11: return (drift_flag, p_values)", "reply"),
        (seq_lifelines[1][0], seq_lifelines[4][0], 525, "12: [if drift: p < 0.002] retrain_model()", "synchCall"),
        (seq_lifelines[4][0], seq_lifelines[1][0], 560, "13: model refit & threshold updated", "reply"),
        (seq_lifelines[1][0], seq_lifelines[0][0], 595, "14: render Live HUD, KPIs & Gauges", "reply")
    ]

    for from_name, to_name, y, text, m_sort in seq_messages:
        x1 = seq_map[from_name][1]
        x2 = seq_map[to_name][1]
        seq_views.append({
            "_type": "UMLSeqMessageView",
            "_id": get_id(),
            "_parent": {"$ref": seq_diag_id},
            "font": "Arial;10;1",
            "head": {"$ref": seq_map[to_name][0]},
            "tail": {"$ref": seq_map[from_name][0]},
            "lineStyle": 1,
            "lineColor": COLOR_RED,
            "points": f"{x1};{y}:{x2};{y}",
            "name": text,
            "messageSort": m_sort
        })

    # =========================================================================
    # 5. COMPONENT DIAGRAM (UMLComponentDiagram)
    # =========================================================================
    comp_views = []
    comp_views.append(make_boundary_view(comp_diag_id, "Autonomous Real-Time Network Anomaly Detection System - Component Diagram", 50, 30, 1160, 680))

    components_def = [
        ("cp_dash", "Web Dashboard Subsystem\n(src/dashboard.py)", "Streamlit HUD, Plotly Gauges,\nSession State, Latency Cards", 80, 100, 320, 110),
        ("cp_sim", "Network Simulation Subsystem\n(src/data_generator.py)", "Baseline Profiler, Attack Waves\n& VPN Drift Engine", 460, 100, 320, 110),
        ("cp_prep", "Preprocessing Pipeline\n(src/preprocessor.py)", "ColumnTransformer (StandardScaler\n& OneHotEncoder)", 80, 280, 320, 110),
        ("cp_det", "Isolation Forest Core\n(src/model.py)", "Unsupervised Tree Scoring\n& Dynamic 99th %tile Cutoff", 460, 280, 320, 110),
        ("cp_xai", "Explainable AI Engine\n(src/xai_engine.py)", "TreeSHAP Local Attributions\n& NLP Synthesizer", 820, 280, 320, 110),
        ("cp_drift", "Statistical Drift Monitor\n(src/drift_detector.py)", "Sliding Window (N=250), 2-Sample\nKS-Test (Bonferroni α=0.002)", 80, 470, 320, 110),
        ("cp_retrain", "Anti-Poison Retraining Engine\n(src/model.py)", "Clean Buffer Extraction &\nAutonomous Model Refitting", 460, 470, 320, 110),
        ("cp_store", "Persistence & Model Store\n(data/*.pkl, data/*.json)", "Serialized Isolation Forest Pickles\n& UNSW-NB15 Metrics", 820, 470, 320, 110)
    ]

    comp_map = {}
    for key, name, sub, left, top, w, h in components_def:
        m_id = get_id()
        v_id = get_id()
        nc_id = get_id()
        model_elements.append({"_type": "UMLComponent", "_id": m_id, "name": name})
        comp_views.append({
            "_type": "UMLComponentView",
            "_id": v_id,
            "_parent": {"$ref": comp_diag_id},
            "model": {"$ref": m_id},
            "font": "Arial;12;0",
            "left": left,
            "top": top,
            "width": w,
            "height": h,
            "lineColor": COLOR_RED,
            "fillColor": COLOR_YELLOW,
            "nameCompartment": {
                "_type": "UMLNameCompartmentView",
                "_id": nc_id,
                "_parent": {"$ref": v_id},
                "model": {"$ref": m_id},
                "font": "Arial;11;1",
                "left": left + 25,
                "top": top + 20,
                "width": w - 35,
                "height": 24,
                "text": name,
                "fontColor": COLOR_BLACK
            }
        })
        comp_map[key] = (v_id, m_id, (left, top, w, h))

    def add_comp_dep(diag_id, c1, c2, p1, p2, label=""):
        comp_views.append({
            "_type": "UMLDependencyView",
            "_id": get_id(),
            "_parent": {"$ref": diag_id},
            "font": "Arial;10;1",
            "head": {"$ref": c2[0]},
            "tail": {"$ref": c1[0]},
            "lineStyle": 1,
            "lineColor": COLOR_RED,
            "points": f"{p1[0]};{p1[1]}:{p2[0]};{p2[1]}",
            "name": label
        })

    add_comp_dep(comp_diag_id, comp_map["cp_dash"], comp_map["cp_sim"], (400, 155), (460, 155), "polls telemetry flows")
    add_comp_dep(comp_diag_id, comp_map["cp_dash"], comp_map["cp_prep"], (240, 210), (240, 280), "raw netflow dict")
    add_comp_dep(comp_diag_id, comp_map["cp_prep"], comp_map["cp_det"], (400, 335), (460, 335), "scaled vector X")
    add_comp_dep(comp_diag_id, comp_map["cp_det"], comp_map["cp_xai"], (780, 335), (820, 335), "explains anomaly")
    add_comp_dep(comp_diag_id, comp_map["cp_prep"], comp_map["cp_drift"], (240, 390), (240, 470), "sliding buffer stream")
    add_comp_dep(comp_diag_id, comp_map["cp_drift"], comp_map["cp_retrain"], (400, 525), (460, 525), "triggers retrain upon drift")
    add_comp_dep(comp_diag_id, comp_map["cp_retrain"], comp_map["cp_det"], (620, 470), (620, 390), "hot-swaps retrained model")
    add_comp_dep(comp_diag_id, comp_map["cp_retrain"], comp_map["cp_store"], (780, 525), (820, 525), "persists/loads model state")

    # =========================================================================
    # 6. DEPLOYMENT DIAGRAM (UMLDeploymentDiagram)
    # =========================================================================
    dep_views = []
    dep_views.append(make_boundary_view(dep_diag_id, "Autonomous Real-Time Network Anomaly Detection System - Deployment Diagram", 50, 30, 1160, 680))

    def make_node_view(diag_id, name, left, top, w, h):
        m_id = get_id()
        v_id = get_id()
        nc_id = get_id()
        model_elements.append({"_type": "UMLNode", "_id": m_id, "name": name})
        dep_views.append({
            "_type": "UMLNodeView",
            "_id": v_id,
            "_parent": {"$ref": diag_id},
            "model": {"$ref": m_id},
            "font": "Arial;12;0",
            "left": left,
            "top": top,
            "width": w,
            "height": h,
            "lineColor": COLOR_RED,
            "fillColor": COLOR_YELLOW,
            "nameCompartment": {
                "_type": "UMLNameCompartmentView",
                "_id": nc_id,
                "_parent": {"$ref": v_id},
                "model": {"$ref": m_id},
                "font": "Arial;12;1",
                "left": left + 10,
                "top": top + 15,
                "width": w - 20,
                "height": 26,
                "text": name,
                "fontColor": COLOR_BLACK
            }
        })
        return (v_id, m_id, (left, top, w, h))

    def make_artifact_view(diag_id, name, left, top, w=260, h=45):
        m_id = get_id()
        v_id = get_id()
        nc_id = get_id()
        model_elements.append({"_type": "UMLArtifact", "_id": m_id, "name": name})
        dep_views.append({
            "_type": "UMLArtifactView",
            "_id": v_id,
            "_parent": {"$ref": diag_id},
            "model": {"$ref": m_id},
            "font": "Arial;11;0",
            "left": left,
            "top": top,
            "width": w,
            "height": h,
            "lineColor": COLOR_RED,
            "fillColor": COLOR_WHITE,
            "nameCompartment": {
                "_type": "UMLNameCompartmentView",
                "_id": nc_id,
                "_parent": {"$ref": v_id},
                "model": {"$ref": m_id},
                "font": "Arial;10;1",
                "left": left + 10,
                "top": top + 10,
                "width": w - 20,
                "height": 22,
                "text": name,
                "fontColor": COLOR_BLACK
            }
        })
        return (v_id, m_id)

    # 3 Physical Hardware Nodes
    n_client = make_node_view(dep_diag_id, "Client SOC Workstation\n«device»", 80, 100, 320, 320)
    make_artifact_view(dep_diag_id, "«artifact» Web Browser Engine\n(Google Chrome / MS Edge)", 110, 180)
    make_artifact_view(dep_diag_id, "«artifact» Plotly Visualization Engine\n(WebGL / HTML5 Interactive Canvas)", 110, 240)
    make_artifact_view(dep_diag_id, "«artifact» REST / WebSocket Client\n(Port :8501 Stream Receiver)", 110, 300)

    n_server = make_node_view(dep_diag_id, "Application & ML Compute Node\n«execution environment»", 580, 80, 420, 560)
    make_artifact_view(dep_diag_id, "«artifact» Python 3.9+ Runtime & Async Engine", 640, 150, 310, 45)
    make_artifact_view(dep_diag_id, "«artifact» Streamlit Web Server (dashboard.py)", 640, 210, 310, 45)
    make_artifact_view(dep_diag_id, "«artifact» Isolation Forest Core (Inference < 2ms)", 640, 270, 310, 45)
    make_artifact_view(dep_diag_id, "«artifact» TreeSHAP Attribution Engine (~95ms)", 640, 330, 310, 45)
    make_artifact_view(dep_diag_id, "«artifact» KS-Test Concept Drift Monitor (α=0.002)", 640, 390, 310, 45)
    make_artifact_view(dep_diag_id, "«artifact» Anti-Poison Retraining Engine", 640, 450, 310, 45)

    n_storage = make_node_view(dep_diag_id, "Persistent Storage Node\n«file system»", 80, 460, 320, 180)
    make_artifact_view(dep_diag_id, "«artifact» Serialized Model Binaries\n(isolation_forest.pkl, preprocessor.pkl)", 110, 520)
    make_artifact_view(dep_diag_id, "«artifact» Validation Benchmarks & Logs\n(UNSW-NB15 metrics.json)", 110, 580)

    # Connections
    dep_views.append({
        "_type": "UMLAssociationView",
        "_id": get_id(),
        "_parent": {"$ref": dep_diag_id},
        "font": "Arial;11;1",
        "head": {"$ref": n_server[0]},
        "tail": {"$ref": n_client[0]},
        "lineStyle": 1,
        "lineColor": COLOR_RED,
        "points": "400;260:580;260",
        "name": "HTTPS / WebSockets (Port :8501)"
    })

    dep_views.append({
        "_type": "UMLAssociationView",
        "_id": get_id(),
        "_parent": {"$ref": dep_diag_id},
        "font": "Arial;11;1",
        "head": {"$ref": n_storage[0]},
        "tail": {"$ref": n_server[0]},
        "lineStyle": 1,
        "lineColor": COLOR_RED,
        "points": "580;550:400;550",
        "name": "Local File I/O (Pickle & JSON)"
    })

    # =========================================================================
    # 7. ACTIVITY DIAGRAM (UMLActivityDiagram)
    # =========================================================================
    act_views = []
    act_views.append(make_boundary_view(act_diag_id, "Autonomous Real-Time Network Anomaly Detection System - Activity Diagram", 50, 30, 1160, 700))

    def make_action_node(diag_id, name, left, top, w=320, h=50):
        m_id = get_id()
        v_id = get_id()
        nc_id = get_id()
        act_views.append({
            "_type": "UMLActionView",
            "_id": v_id,
            "_parent": {"$ref": diag_id},
            "font": "Arial;11;0",
            "left": left,
            "top": top,
            "width": w,
            "height": h,
            "lineColor": COLOR_RED,
            "fillColor": COLOR_YELLOW,
            "nameCompartment": {
                "_type": "UMLNameCompartmentView",
                "_id": nc_id,
                "_parent": {"$ref": v_id},
                "font": "Arial;11;1",
                "left": left + 10,
                "top": top + 12,
                "width": w - 20,
                "height": 24,
                "text": name,
                "fontColor": COLOR_BLACK
            }
        })
        return (v_id, m_id, (left, top, w, h))

    def make_decision_node(diag_id, name, left, top, w=200, h=60):
        v_id = get_id()
        nc_id = get_id()
        act_views.append({
            "_type": "UMLControlNodeView",
            "_id": v_id,
            "_parent": {"$ref": diag_id},
            "font": "Arial;10;1",
            "left": left,
            "top": top,
            "width": w,
            "height": h,
            "lineColor": COLOR_RED,
            "fillColor": COLOR_YELLOW,
            "nameCompartment": {
                "_type": "UMLNameCompartmentView",
                "_id": nc_id,
                "_parent": {"$ref": v_id},
                "font": "Arial;10;1",
                "left": left + 10,
                "top": top + 18,
                "width": w - 20,
                "height": 22,
                "text": name,
                "fontColor": COLOR_BLACK
            }
        })
        return (v_id, (left, top, w, h))

    # Initial Node
    v_init_id = get_id()
    act_views.append({
        "_type": "UMLControlNodeView",
        "_id": v_init_id,
        "_parent": {"$ref": act_diag_id},
        "font": "Arial;12;0",
        "left": 470,
        "top": 70,
        "width": 30,
        "height": 30,
        "lineColor": COLOR_RED,
        "fillColor": COLOR_RED
    })

    # Steps
    a_ingest = make_action_node(act_diag_id, "Ingest / Synthesize NetFlow Record (15 Features)", 325, 125)
    a_prep = make_action_node(act_diag_id, "Preprocess: Z-Score Scaling & One-Hot Encoding", 325, 200)
    a_score = make_action_node(act_diag_id, "Isolation Forest Path Evaluation (Latency < 2ms)", 325, 275)

    d_threat = make_decision_node(act_diag_id, "Anomaly Score > Threshold?", 385, 350)
    a_shap = make_action_node(act_diag_id, "Compute TreeSHAP Attributions & NLP", 700, 355, 300, 50)
    a_alert = make_action_node(act_diag_id, "Dispatch High-Priority Threat Alert", 700, 430, 300, 50)

    a_buffer = make_action_node(act_diag_id, "Update Sliding Feature Buffers (Window N=250)", 325, 430)
    d_buf = make_decision_node(act_diag_id, "Buffer Full (N=250)?", 385, 505)

    a_ks = make_action_node(act_diag_id, "Execute 2-Sample KS-Test (Bonferroni α=0.002)", 325, 580)
    d_drift = make_decision_node(act_diag_id, "Drift Detected (p < 0.002)?", 385, 645)

    a_retrain = make_action_node(act_diag_id, "Filter Clean Buffer & Retrain Isolation Forest", 700, 650, 300, 50)
    a_hud = make_action_node(act_diag_id, "Render Real-Time Dashboard & Update KPI HUD", 100, 500, 240, 70)

    def add_flow(diag_id, n1_id, n2_id, p1, p2, label=""):
        act_views.append({
            "_type": "UMLControlFlowView",
            "_id": get_id(),
            "_parent": {"$ref": diag_id},
            "font": "Arial;10;1",
            "head": {"$ref": n2_id},
            "tail": {"$ref": n1_id},
            "lineStyle": 1,
            "lineColor": COLOR_RED,
            "points": f"{p1[0]};{p1[1]}:{p2[0]};{p2[1]}",
            "name": label
        })

    add_flow(act_diag_id, v_init_id, a_ingest[0], (485, 100), (485, 125))
    add_flow(act_diag_id, a_ingest[0], a_prep[0], (485, 175), (485, 200))
    add_flow(act_diag_id, a_prep[0], a_score[0], (485, 250), (485, 275))
    add_flow(act_diag_id, a_score[0], d_threat[0], (485, 325), (485, 350))

    add_flow(act_diag_id, d_threat[0], a_shap[0], (585, 380), (700, 380), "Yes [Anomaly]")
    add_flow(act_diag_id, a_shap[0], a_alert[0], (850, 405), (850, 430))
    add_flow(act_diag_id, a_alert[0], a_buffer[0], (700, 455), (645, 455))

    add_flow(act_diag_id, d_threat[0], a_buffer[0], (485, 410), (485, 430), "No [Normal]")
    add_flow(act_diag_id, a_buffer[0], d_buf[0], (485, 480), (485, 505))

    add_flow(act_diag_id, d_buf[0], a_ks[0], (485, 565), (485, 580), "Yes")
    add_flow(act_diag_id, a_ks[0], d_drift[0], (485, 630), (485, 645))

    add_flow(act_diag_id, d_drift[0], a_retrain[0], (585, 675), (700, 675), "Yes [Drift]")
    add_flow(act_diag_id, a_retrain[0], a_hud[0], (700, 675), (220, 570))
    add_flow(act_diag_id, d_drift[0], a_hud[0], (385, 675), (220, 570), "No")
    add_flow(act_diag_id, d_buf[0], a_hud[0], (385, 535), (340, 535), "No")
    add_flow(act_diag_id, a_hud[0], a_ingest[0], (220, 500), (325, 150), "Next Stream Tick")

    # =========================================================================
    # 8. CLASS DIAGRAM (UMLClassDiagram)
    # =========================================================================
    class_views = []
    class_views.append(make_boundary_view(class_diag_id, "Autonomous Real-Time Network Anomaly Detection System - Class Diagram", 40, 30, 1260, 680))

    classes_def = [
        ("NetworkTrafficSimulator", "«entity»", 60, 80, 350, 260,
         ["- rng: RandomState", "- drift_active: bool = False", "- current_phase: str", "- step_counter: int = 0"],
         ["+ set_drift(active: bool): void", "+ generate_single_flow(force: str): dict", "- _generate_normal(): dict", "- _generate_anomaly(type: str): dict", "+ generate_baseline(n: int): DataFrame"]),
        
        ("NetworkPreprocessor", "«component»", 470, 80, 350, 260,
         ["- preprocessor: ColumnTransformer", "- feature_names: List[str]", "- is_fitted: bool = False"],
         ["+ fit(df: DataFrame): void", "+ transform(df: DataFrame): ndarray", "+ fit_transform(df: DataFrame): ndarray", "+ get_feature_names(): List[str]", "+ save(filepath: str): void", "+ load(filepath: str): Preprocessor"]),
        
        ("AnomalyDetector", "«ML model»", 880, 80, 350, 260,
         ["- model: IsolationForest", "- threshold: float = 0.55", "- is_trained: bool = False", "- contamination: float = 0.01"],
         ["+ fit(X_train: ndarray): void", "+ get_anomaly_score(X): ndarray", "+ predict(X): Tuple[ndarray, ndarray]", "+ save(filepath: str): void", "+ load(filepath: str): Detector"]),
        
        ("ConceptDriftDetector", "«monitor»", 60, 380, 350, 270,
         ["- window_size: int = 250", "- alpha: float = 0.01", "- features_to_monitor: List[str]", "- reference_data: Dict[str, ndarray]", "- window_buffer: Dict[str, List]"],
         ["+ update(record: dict): Tuple[bool, dict]", "- _check_bonferroni(p_vals): bool", "+ reset_reference(new_df): void"]),
        
        ("NetworkXAI", "«XAI engine»", 470, 380, 350, 270,
         ["- detector: AnomalyDetector", "- preprocessor: NetworkPreprocessor", "- explainer: TreeExplainer", "- feature_names: List[str]"],
         ["+ explain_instance(raw, X): dict", "- _group_categorical_contributions(): dict", "- _get_feature_interpretation(f, v): str"]),
        
        ("StreamlitDashboardController", "«controller»", 880, 380, 350, 270,
         ["- simulator: NetworkTrafficSimulator", "- preprocessor: NetworkPreprocessor", "- detector: AnomalyDetector", "- drift_detector: ConceptDriftDetector", "- xai: NetworkXAI"],
         ["+ initialize_models_if_needed(): void", "+ retrain_model_on_drift(): void", "+ render_live_telemetry_tab(): void", "+ render_unsw_validation_tab(): void"])
    ]

    class_map = {}
    for cname, stype, left, top, w, h, attrs, meths in classes_def:
        view, meta = make_tier_class_view(class_diag_id, f"{stype}\n{cname}", left, top, w, h, attrs, meths)
        class_views.append(view)
        class_map[cname] = meta

    def add_class_assoc(diag_id, c1, c2, p1, p2, label=""):
        class_views.append({
            "_type": "UMLAssociationView",
            "_id": get_id(),
            "_parent": {"$ref": diag_id},
            "font": "Arial;10;1",
            "head": {"$ref": c2[0]},
            "tail": {"$ref": c1[0]},
            "lineStyle": 1,
            "lineColor": COLOR_RED,
            "points": f"{p1[0]};{p1[1]}:{p2[0]};{p2[1]}",
            "name": label
        })

    add_class_assoc(class_diag_id, class_map["NetworkTrafficSimulator"], class_map["NetworkPreprocessor"], (410, 210), (470, 210), "raw netflow dict")
    add_class_assoc(class_diag_id, class_map["NetworkPreprocessor"], class_map["AnomalyDetector"], (820, 210), (880, 210), "scaled vector X")
    add_class_assoc(class_diag_id, class_map["AnomalyDetector"], class_map["NetworkXAI"], (950, 340), (820, 420), "explains model")
    add_class_assoc(class_diag_id, class_map["NetworkPreprocessor"], class_map["NetworkXAI"], (645, 340), (645, 380), "feature names")
    add_class_assoc(class_diag_id, class_map["NetworkPreprocessor"], class_map["ConceptDriftDetector"], (470, 310), (410, 420), "updates buffer")
    add_class_assoc(class_diag_id, class_map["StreamlitDashboardController"], class_map["AnomalyDetector"], (1055, 380), (1055, 340), "orchestrates")

    # =========================================================================
    # 9. STATE MACHINE DIAGRAM (UMLStatechartDiagram)
    # =========================================================================
    sm_views = []
    sm_views.append(make_boundary_view(sm_diag_id, "Autonomous Real-Time Network Anomaly Detection System - State Machine Diagram", 50, 30, 1160, 680))

    def make_state_view(diag_id, name, left, top, w=260, h=130):
        v_id = get_id()
        nc_id = get_id()
        sm_views.append({
            "_type": "UMLStateView",
            "_id": v_id,
            "_parent": {"$ref": diag_id},
            "font": "Arial;12;0",
            "left": left,
            "top": top,
            "width": w,
            "height": h,
            "lineColor": COLOR_RED,
            "fillColor": COLOR_YELLOW,
            "nameCompartment": {
                "_type": "UMLNameCompartmentView",
                "_id": nc_id,
                "_parent": {"$ref": v_id},
                "font": "Arial;11;1",
                "left": left + 10,
                "top": top + 15,
                "width": w - 20,
                "height": 24,
                "text": name,
                "fontColor": COLOR_BLACK
            }
        })
        return (v_id, (left, top, w, h))

    # Initial State
    v_sm_init = get_id()
    sm_views.append({
        "_type": "UMLPseudostateView",
        "_id": v_sm_init,
        "_parent": {"$ref": sm_diag_id},
        "font": "Arial;12;0",
        "left": 90,
        "top": 150,
        "width": 30,
        "height": 30,
        "lineColor": COLOR_RED,
        "fillColor": COLOR_RED
    })

    s_init = make_state_view(sm_diag_id, "INITIALIZING\n\nentry / load_models()\ndo / fit_baseline_pipeline()\nexit / stream_ready", 180, 100)
    s_normal = make_state_view(sm_diag_id, "NORMAL_MONITORING\n\nentry / stream_active = True\ndo / predict(flow) [lat < 2ms]\ndo / update_sliding_buffer()\nexit / log_telemetry()", 680, 100, 280, 150)
    s_threat = make_state_view(sm_diag_id, "ANOMALY_EXPLAINING\n\nentry / flag_alert(score)\ndo / compute_tree_shap()\ndo / synthesize_nlp()\nexit / push_alert()", 680, 360, 280, 150)
    s_drift = make_state_view(sm_diag_id, "DRIFT_ANALYSIS\n\nentry / window_buffer_full\ndo / run_2sample_ks_test()\ndo / apply_bonferroni(α=0.002)\nexit / log_pvalues()", 180, 360, 260, 150)
    s_retrain = make_state_view(sm_diag_id, "ADAPTIVE_RETRAINING\n\nentry / filter_clean_buffer\ndo / refit_isolation_forest()\ndo / recalibrate_threshold()\nexit / reset_ks_reference()", 180, 550, 260, 130)

    def add_sm_trans(diag_id, s1_id, s2_id, p1, p2, label=""):
        sm_views.append({
            "_type": "UMLTransitionView",
            "_id": get_id(),
            "_parent": {"$ref": diag_id},
            "font": "Arial;10;1",
            "head": {"$ref": s2_id},
            "tail": {"$ref": s1_id},
            "lineStyle": 1,
            "lineColor": COLOR_RED,
            "points": f"{p1[0]};{p1[1]}:{p2[0]};{p2[1]}",
            "name": label
        })

    add_sm_trans(sm_diag_id, v_sm_init, s_init[0], (120, 165), (180, 165), "launch")
    add_sm_trans(sm_diag_id, s_init[0], s_normal[0], (440, 165), (680, 165), "models_ready")
    add_sm_trans(sm_diag_id, s_normal[0], s_threat[0], (780, 250), (780, 360), "score > threshold [threat]")
    add_sm_trans(sm_diag_id, s_threat[0], s_normal[0], (880, 360), (880, 250), "explanation_logged [resume]")
    add_sm_trans(sm_diag_id, s_normal[0], s_drift[0], (680, 200), (440, 400), "buffer_full [tick]")
    add_sm_trans(sm_diag_id, s_drift[0], s_retrain[0], (310, 510), (310, 550), "drift_detected [p < 0.002]")
    add_sm_trans(sm_diag_id, s_retrain[0], s_normal[0], (440, 615), (780, 250), "model_adapted [realigned]")

    # =========================================================================
    # MASTER STARUML PROJECT JSON STRUCTURE
    # =========================================================================
    project = {
        "_type": "Project",
        "_id": project_id,
        "name": "Autonomous Real-Time Network Anomaly Detection System",
        "ownedElements": [
            {
                "_type": "UMLModel",
                "_id": model_id,
                "_parent": {"$ref": project_id},
                "name": "Major Project UML Model",
                "ownedElements": [
                    # 1. Use Case Diagram
                    {
                        "_type": "UMLUseCaseDiagram",
                        "_id": uc_diag_id,
                        "_parent": {"$ref": model_id},
                        "name": "Use Case Diagram",
                        "ownedViews": uc_views
                    },
                    # 2. System Architecture Diagram
                    {
                        "_type": "UMLClassDiagram",
                        "_id": arch_diag_id,
                        "_parent": {"$ref": model_id},
                        "name": "System Architecture Diagram",
                        "ownedViews": arch_views
                    },
                    # 3. Collaboration / Communication Diagram
                    {
                        "_type": "UMLClassDiagram",
                        "_id": comm_diag_id,
                        "_parent": {"$ref": model_id},
                        "name": "Collaboration Diagram",
                        "ownedViews": comm_views
                    },
                    # 4. Sequence Diagram (under UMLInteraction)
                    {
                        "_type": "UMLInteraction",
                        "_id": interact_id,
                        "_parent": {"$ref": model_id},
                        "name": "Real-Time Telemetry & Retraining Flow",
                        "ownedElements": [
                            {
                                "_type": "UMLSequenceDiagram",
                                "_id": seq_diag_id,
                                "_parent": {"$ref": interact_id},
                                "name": "Sequence Diagram",
                                "ownedViews": seq_views
                            }
                        ]
                    },
                    # 5. Component Diagram
                    {
                        "_type": "UMLComponentDiagram",
                        "_id": comp_diag_id,
                        "_parent": {"$ref": model_id},
                        "name": "Component Diagram",
                        "ownedViews": comp_views
                    },
                    # 6. Deployment Diagram
                    {
                        "_type": "UMLDeploymentDiagram",
                        "_id": dep_diag_id,
                        "_parent": {"$ref": model_id},
                        "name": "Deployment Diagram",
                        "ownedViews": dep_views
                    },
                    # 7. Activity Diagram (under UMLActivity)
                    {
                        "_type": "UMLActivity",
                        "_id": act_container_id,
                        "_parent": {"$ref": model_id},
                        "name": "Detection Pipeline Lifecycle",
                        "ownedElements": [
                            {
                                "_type": "UMLActivityDiagram",
                                "_id": act_diag_id,
                                "_parent": {"$ref": act_container_id},
                                "name": "Activity Diagram",
                                "ownedViews": act_views
                            }
                        ]
                    },
                    # 8. Class Diagram
                    {
                        "_type": "UMLClassDiagram",
                        "_id": class_diag_id,
                        "_parent": {"$ref": model_id},
                        "name": "Class Diagram",
                        "ownedViews": class_views
                    },
                    # 9. State Machine Diagram (under UMLStateMachine)
                    {
                        "_type": "UMLStateMachine",
                        "_id": sm_container_id,
                        "_parent": {"$ref": model_id},
                        "name": "Self-Adaptive Lifecycle",
                        "ownedElements": [
                            {
                                "_type": "UMLStatechartDiagram",
                                "_id": sm_diag_id,
                                "_parent": {"$ref": sm_container_id},
                                "name": "State Machine Diagram",
                                "ownedViews": sm_views
                            }
                        ]
                    }
                ] + model_elements
            }
        ]
    }

    with open(OUTPUT_MDJ, "w", encoding="utf-8") as f:
        json.dump(project, f, indent=2)

    print(f"StarUML Complete 9-Diagram Project successfully written to: {OUTPUT_MDJ}")

if __name__ == "__main__":
    build_full_staruml_suite()
