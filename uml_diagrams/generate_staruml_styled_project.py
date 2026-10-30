import json
import uuid
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_MDJ = os.path.join(OUTPUT_DIR, "major_project_diagrams.mdj")

def get_id():
    return str(uuid.uuid4()).replace("-", "")[:24]

COLOR_RED = "#B81D24"       # Crimson line/border
COLOR_YELLOW = "#FFFFE0"    # Cream-yellow fill
COLOR_BLACK = "#000000"

def build_staruml_exact_styled_project():
    project_id = get_id()
    model_id = get_id()
    uc_diag_id = get_id()

    # Model Elements (Logical layer)
    # Actors
    act_analyst_id = get_id()
    act_admin_id = get_id()
    act_gateway_id = get_id()

    # Boundary Subject
    subject_id = get_id()

    # Use cases
    # Col 1 (Primary)
    uc_start_id = get_id()
    uc_inject_id = get_id()
    uc_detect_id = get_id()
    uc_xai_id = get_id()
    uc_drift_id = get_id()
    uc_retrain_id = get_id()
    uc_export_id = get_id()

    # Col 2 (Include/Core)
    uc_auth_id = get_id()
    uc_preproc_id = get_id()
    uc_scoring_id = get_id()
    uc_shap_id = get_id()
    uc_ks_id = get_id()
    uc_filter_id = get_id()
    uc_bench_id = get_id()

    # Col 3 (Extend/Admin)
    uc_adm_users_id = get_id()
    uc_adm_sens_id = get_id()
    uc_adm_health_id = get_id()
    uc_syn_id = get_id()
    uc_brute_id = get_id()
    uc_exfil_id = get_id()
    uc_waterfall_id = get_id()
    uc_nlp_id = get_id()
    uc_json_id = get_id()
    uc_pvals_id = get_id()

    # View Builders (Visual layer with exact colors)
    views = []

    # 1. System Boundary Subject View
    v_subject_id = get_id()
    nc_sub_id = get_id()
    views.append({
        "_type": "UMLUseCaseSubjectView",
        "_id": v_subject_id,
        "_parent": {"$ref": uc_diag_id},
        "font": "Arial;13;1",
        "left": 180,
        "top": 30,
        "width": 840,
        "height": 720,
        "name": "Autonomous Real-Time Network Anomaly Detection System",
        "lineColor": COLOR_RED,
        "fillColor": "#FFFFFF",
        "nameCompartment": {
            "_type": "UMLNameCompartmentView",
            "_id": nc_sub_id,
            "_parent": {"$ref": v_subject_id},
            "font": "Arial;14;1",
            "left": 360,
            "top": 40,
            "width": 480,
            "height": 20,
            "text": "Autonomous Real-Time Network Anomaly Detection System",
            "fontColor": COLOR_BLACK
        }
    })

    # 2. Helper for Actors (with red lines & yellow boxes)
    def add_actor(model_id, name, left, top):
        v_id = get_id()
        nc_id = get_id()
        views.append({
            "_type": "UMLActorView",
            "_id": v_id,
            "_parent": {"$ref": uc_diag_id},
            "model": {"$ref": model_id},
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
                "model": {"$ref": model_id},
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
        })
        return v_id

    # Add 3 Actors (matching Photo 2 layout)
    v_act_analyst = add_actor(act_analyst_id, "Security Analyst", 60, 340)
    v_act_admin = add_actor(act_admin_id, "Security Admin", 1060, 120)
    v_act_gateway = add_actor(act_gateway_id, "Network Gateway", 1060, 480)

    # 3. Helper for Use Cases (Red border, cream-yellow fill)
    def add_use_case(model_id, name, left, top, w=200, h=55):
        v_id = get_id()
        nc_id = get_id()
        views.append({
            "_type": "UMLUseCaseView",
            "_id": v_id,
            "_parent": {"$ref": uc_diag_id},
            "model": {"$ref": model_id},
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
                "model": {"$ref": model_id},
                "font": "Arial;11;0",
                "left": left + 10,
                "top": top + 15,
                "width": w - 20,
                "height": 24,
                "text": name,
                "fontColor": COLOR_BLACK
            }
        })
        return v_id

    # Column 1: Primary User Cases (Left Column inside boundary)
    v_uc_start = add_use_case(uc_start_id, "Start Live Traffic Stream", 210, 80)
    v_uc_inject = add_use_case(uc_inject_id, "Inject Threat Vectors", 210, 180)
    v_uc_detect = add_use_case(uc_detect_id, "Inspect Anomaly Decisions", 210, 290)
    v_uc_xai = add_use_case(uc_xai_id, "Inspect XAI Insights", 210, 400)
    v_uc_drift = add_use_case(uc_drift_id, "Monitor Concept Drift", 210, 510)
    v_uc_retrain = add_use_case(uc_retrain_id, "Autonomous Retraining", 210, 600)
    v_uc_export = add_use_case(uc_export_id, "Export Forensic Report", 210, 680)

    # Column 2: Included / Core Processing Cases (Center Column)
    v_uc_auth = add_use_case(uc_auth_id, "Authenticate User Session", 490, 80)
    v_uc_preproc = add_use_case(uc_preproc_id, "Normalize 15 NetFlow Features", 490, 180)
    v_uc_scoring = add_use_case(uc_scoring_id, "Evaluate Isolation Forest Score", 490, 290)
    v_uc_shap = add_use_case(uc_shap_id, "Compute TreeSHAP Attribution", 490, 400)
    v_uc_ks = add_use_case(uc_ks_id, "Execute Rolling KS-Test (α=0.002)", 490, 510)
    v_uc_filter = add_use_case(uc_filter_id, "Filter Buffer (pred_anomaly==0)", 490, 600)
    v_uc_bench = add_use_case(uc_bench_id, "View UNSW-NB15 Benchmark", 490, 680)

    # Column 3: Extended / Specialized Cases (Right Column inside boundary)
    v_uc_adm_users = add_use_case(uc_adm_users_id, "Manage User Accounts", 770, 70, 190, 50)
    v_uc_adm_sens = add_use_case(uc_adm_sens_id, "Configure Sensitivity Slider", 770, 130, 190, 50)
    v_uc_adm_health = add_use_case(uc_adm_health_id, "Audit System Health (psutil)", 770, 190, 190, 50)
    
    v_uc_syn = add_use_case(uc_syn_id, "Simulate SYN Flood Wave", 770, 260, 190, 50)
    v_uc_brute = add_use_case(uc_brute_id, "Simulate SSH Brute Force", 770, 320, 190, 50)
    v_uc_exfil = add_use_case(uc_exfil_id, "Simulate Data Exfiltration", 770, 380, 190, 50)
    
    v_uc_waterfall = add_use_case(uc_waterfall_id, "View SHAP Waterfall Chart", 770, 450, 190, 50)
    v_uc_nlp = add_use_case(uc_nlp_id, "View Plain-English Diagnosis", 770, 510, 190, 50)
    v_uc_json = add_use_case(uc_json_id, "Inspect Raw Flow JSON", 770, 570, 190, 50)
    
    v_uc_pvals = add_use_case(uc_pvals_id, "Track Log-Scale p-Values", 770, 640, 190, 50)

    # Helper for Solid Association Line (Actor -> Use Case)
    def add_solid_line(v1_id, v2_id, p1, p2):
        views.append({
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
    def add_dashed_arrow(v1_id, v2_id, p1, p2, stereotype="<<include>>"):
        views.append({
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

    # Add Actor Associations (Left: Security Analyst)
    add_solid_line(v_act_analyst, v_uc_start, (120, 380), (210, 110))
    add_solid_line(v_act_analyst, v_uc_inject, (120, 380), (210, 210))
    add_solid_line(v_act_analyst, v_uc_detect, (120, 380), (210, 320))
    add_solid_line(v_act_analyst, v_uc_xai, (120, 380), (210, 430))
    add_solid_line(v_act_analyst, v_uc_drift, (120, 380), (210, 540))
    add_solid_line(v_act_analyst, v_uc_retrain, (120, 380), (210, 630))
    add_solid_line(v_act_analyst, v_uc_export, (120, 380), (210, 700))

    # Add Admin Associations (Right-Top)
    add_solid_line(v_act_admin, v_uc_auth, (1060, 160), (690, 105))
    add_solid_line(v_act_admin, v_uc_adm_users, (1060, 160), (960, 95))
    add_solid_line(v_act_admin, v_uc_adm_sens, (1060, 160), (960, 155))
    add_solid_line(v_act_admin, v_uc_adm_health, (1060, 160), (960, 215))

    # Add Gateway Associations (Right-Bottom)
    add_solid_line(v_act_gateway, v_uc_preproc, (1060, 520), (690, 210))
    add_solid_line(v_act_gateway, v_uc_ks, (1060, 520), (690, 535))
    add_solid_line(v_act_gateway, v_uc_filter, (1060, 520), (690, 625))

    # Add <<include>> Dashed Arrows (Col 1 -> Col 2)
    add_dashed_arrow(v_uc_start, v_uc_auth, (410, 105), (490, 105), "<<include>>")
    add_dashed_arrow(v_uc_inject, v_uc_preproc, (410, 205), (490, 205), "<<include>>")
    add_dashed_arrow(v_uc_detect, v_uc_scoring, (410, 315), (490, 315), "<<include>>")
    add_dashed_arrow(v_uc_xai, v_uc_shap, (410, 425), (490, 425), "<<include>>")
    add_dashed_arrow(v_uc_drift, v_uc_ks, (410, 535), (490, 535), "<<include>>")
    add_dashed_arrow(v_uc_retrain, v_uc_filter, (410, 625), (490, 625), "<<include>>")
    add_dashed_arrow(v_uc_export, v_uc_bench, (410, 705), (490, 705), "<<include>>")

    # Add <<extend>> Dashed Arrows (Col 2 -> Col 3 or Col 1 -> Col 3)
    add_dashed_arrow(v_uc_inject, v_uc_syn, (410, 215), (770, 280), "<<extend>>")
    add_dashed_arrow(v_uc_inject, v_uc_brute, (410, 215), (770, 345), "<<extend>>")
    add_dashed_arrow(v_uc_inject, v_uc_exfil, (410, 215), (770, 405), "<<extend>>")

    add_dashed_arrow(v_uc_shap, v_uc_waterfall, (690, 425), (770, 470), "<<extend>>")
    add_dashed_arrow(v_uc_shap, v_uc_nlp, (690, 425), (770, 535), "<<extend>>")
    add_dashed_arrow(v_uc_shap, v_uc_json, (690, 425), (770, 595), "<<extend>>")

    add_dashed_arrow(v_uc_ks, v_uc_pvals, (690, 545), (770, 660), "<<extend>>")

    # Create StarUML Model Structure
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
                    {
                        "_type": "UMLUseCaseDiagram",
                        "_id": uc_diag_id,
                        "_parent": {"$ref": model_id},
                        "name": "Use Case Diagram",
                        "ownedViews": views
                    },
                    # Model Elements
                    {"_type": "UMLActor", "_id": act_analyst_id, "name": "Security Analyst"},
                    {"_type": "UMLActor", "_id": act_admin_id, "name": "Security Admin"},
                    {"_type": "UMLActor", "_id": act_gateway_id, "name": "Network Gateway"},
                    {"_type": "UMLUseCase", "_id": uc_start_id, "name": "Start Live Traffic Stream"},
                    {"_type": "UMLUseCase", "_id": uc_inject_id, "name": "Inject Threat Vectors"},
                    {"_type": "UMLUseCase", "_id": uc_detect_id, "name": "Inspect Anomaly Decisions"},
                    {"_type": "UMLUseCase", "_id": uc_xai_id, "name": "Inspect XAI Insights"},
                    {"_type": "UMLUseCase", "_id": uc_drift_id, "name": "Monitor Concept Drift"},
                    {"_type": "UMLUseCase", "_id": uc_retrain_id, "name": "Autonomous Retraining"},
                    {"_type": "UMLUseCase", "_id": uc_export_id, "name": "Export Forensic Report"},
                    {"_type": "UMLUseCase", "_id": uc_auth_id, "name": "Authenticate User Session"},
                    {"_type": "UMLUseCase", "_id": uc_preproc_id, "name": "Normalize 15 NetFlow Features"},
                    {"_type": "UMLUseCase", "_id": uc_scoring_id, "name": "Evaluate Isolation Forest Score"},
                    {"_type": "UMLUseCase", "_id": uc_shap_id, "name": "Compute TreeSHAP Attribution"},
                    {"_type": "UMLUseCase", "_id": uc_ks_id, "name": "Execute Rolling KS-Test (α=0.002)"},
                    {"_type": "UMLUseCase", "_id": uc_filter_id, "name": "Filter Buffer (pred_anomaly==0)"},
                    {"_type": "UMLUseCase", "_id": uc_bench_id, "name": "View UNSW-NB15 Benchmark"},
                    {"_type": "UMLUseCase", "_id": uc_adm_users_id, "name": "Manage User Accounts"},
                    {"_type": "UMLUseCase", "_id": uc_adm_sens_id, "name": "Configure Sensitivity Slider"},
                    {"_type": "UMLUseCase", "_id": uc_adm_health_id, "name": "Audit System Health (psutil)"},
                    {"_type": "UMLUseCase", "_id": uc_syn_id, "name": "Simulate SYN Flood Wave"},
                    {"_type": "UMLUseCase", "_id": uc_brute_id, "name": "Simulate SSH Brute Force"},
                    {"_type": "UMLUseCase", "_id": uc_exfil_id, "name": "Simulate Data Exfiltration"},
                    {"_type": "UMLUseCase", "_id": uc_waterfall_id, "name": "View SHAP Waterfall Chart"},
                    {"_type": "UMLUseCase", "_id": uc_nlp_id, "name": "View Plain-English Diagnosis"},
                    {"_type": "UMLUseCase", "_id": uc_json_id, "name": "Inspect Raw Flow JSON"},
                    {"_type": "UMLUseCase", "_id": uc_pvals_id, "name": "Track Log-Scale p-Values"}
                ]
            }
        ]
    }

    with open(OUTPUT_MDJ, "w", encoding="utf-8") as f:
        json.dump(project, f, indent=2)

    print(f"StarUML exact styled project saved at: {OUTPUT_MDJ}")

if __name__ == "__main__":
    build_staruml_exact_styled_project()
