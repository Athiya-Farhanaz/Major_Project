import json
import uuid
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_MDJ = os.path.join(OUTPUT_DIR, "major_project_diagrams.mdj")

def get_id():
    return str(uuid.uuid4()).replace("-", "")[:24]

def build_full_staruml_project():
    project_id = get_id()
    model_id = get_id()

    # Model Elements
    # Actors
    actor1_id = get_id()
    actor2_id = get_id()

    # Use Cases
    uc1_id = get_id()
    uc2_id = get_id()
    uc3_id = get_id()
    uc4_id = get_id()
    uc5_id = get_id()
    uc6_id = get_id()

    # Use Case Diagram ID
    uc_diag_id = get_id()

    # Views for Use Case Diagram
    v_actor1_id = get_id()
    v_actor2_id = get_id()
    v_uc1_id = get_id()
    v_uc2_id = get_id()
    v_uc3_id = get_id()
    v_uc4_id = get_id()
    v_uc5_id = get_id()
    v_uc6_id = get_id()

    # Create Views
    def make_actor_view(view_id, model_ref_id, name, left, top):
        nc_id = get_id()
        return {
            "_type": "UMLActorView",
            "_id": view_id,
            "_parent": {"$ref": uc_diag_id},
            "model": {"$ref": model_ref_id},
            "font": "Arial;13;0",
            "left": left,
            "top": top,
            "width": 60,
            "height": 85,
            "nameCompartment": {
                "_type": "UMLNameCompartmentView",
                "_id": nc_id,
                "_parent": {"$ref": view_id},
                "model": {"$ref": model_ref_id},
                "font": "Arial;13;0",
                "left": left - 25,
                "top": top + 90,
                "width": 110,
                "height": 26,
                "text": name
            }
        }

    def make_usecase_view(view_id, model_ref_id, name, left, top, w=260, h=65):
        nc_id = get_id()
        return {
            "_type": "UMLUseCaseView",
            "_id": view_id,
            "_parent": {"$ref": uc_diag_id},
            "model": {"$ref": model_ref_id},
            "font": "Arial;13;0",
            "left": left,
            "top": top,
            "width": w,
            "height": h,
            "nameCompartment": {
                "_type": "UMLNameCompartmentView",
                "_id": nc_id,
                "_parent": {"$ref": view_id},
                "model": {"$ref": model_ref_id},
                "font": "Arial;13;0",
                "left": left + 10,
                "top": top + 15,
                "width": w - 20,
                "height": 26,
                "text": name
            }
        }

    # Construct the views
    uc_views = [
        # Actor 1: Security Analyst
        make_actor_view(v_actor1_id, actor1_id, "Security Analyst\n(Operator)", 80, 240),
        # Actor 2: Network Stream
        make_actor_view(v_actor2_id, actor2_id, "Network Gateway\n(Traffic Stream)", 760, 240),
        # Use cases
        make_usecase_view(v_uc1_id, uc1_id, "UC1: Ingest Streaming NetFlow Packets", 320, 60),
        make_usecase_view(v_uc2_id, uc2_id, "UC2: Preprocess Features (Scale & Encode)", 320, 150),
        make_usecase_view(v_uc3_id, uc3_id, "UC3: Detect Anomalies (Isolation Forest)", 320, 240),
        make_usecase_view(v_uc4_id, uc4_id, "UC4: Generate TreeSHAP Attribution", 320, 330),
        make_usecase_view(v_uc5_id, uc5_id, "UC5: Monitor Concept Drift (KS-Test)", 320, 420),
        make_usecase_view(v_uc6_id, uc6_id, "UC6: Retrain Model (Anti-Poison Filter)", 320, 510),
    ]

    # Links / Associations in views
    # Helper to connect actor to usecase
    def make_assoc_view(diag_id, parent_view1_id, parent_view2_id, p1, p2):
        return {
            "_type": "UMLAssociationView",
            "_id": get_id(),
            "_parent": {"$ref": diag_id},
            "font": "Arial;13;0",
            "head": {"$ref": parent_view2_id},
            "tail": {"$ref": parent_view1_id},
            "lineStyle": 1,
            "points": f"{p1[0]};{p1[1]}:{p2[0]};{p2[1]}"
        }

    # Add association lines
    assoc_views = [
        make_assoc_view(uc_diag_id, v_actor1_id, v_uc1_id, (140, 280), (320, 90)),
        make_assoc_view(uc_diag_id, v_actor1_id, v_uc3_id, (140, 280), (320, 270)),
        make_assoc_view(uc_diag_id, v_actor1_id, v_uc4_id, (140, 280), (320, 360)),
        make_assoc_view(uc_diag_id, v_actor1_id, v_uc6_id, (140, 280), (320, 540)),
        make_assoc_view(uc_diag_id, v_actor2_id, v_uc1_id, (760, 280), (580, 90)),
        make_assoc_view(uc_diag_id, v_actor2_id, v_uc5_id, (760, 280), (580, 450)),
    ]

    # Combine views
    all_uc_views = uc_views + assoc_views

    # Build Class / Architecture Diagram Views
    arch_diag_id = get_id()
    class1_id = get_id()
    class2_id = get_id()
    class3_id = get_id()
    class4_id = get_id()
    class5_id = get_id()

    def make_class_view(view_id, model_ref_id, name, left, top, w=220, h=110):
        nc_id = get_id()
        return {
            "_type": "UMLClassView",
            "_id": view_id,
            "_parent": {"$ref": arch_diag_id},
            "model": {"$ref": model_ref_id},
            "font": "Arial;13;0",
            "left": left,
            "top": top,
            "width": w,
            "height": h,
            "nameCompartment": {
                "_type": "UMLNameCompartmentView",
                "_id": nc_id,
                "_parent": {"$ref": view_id},
                "model": {"$ref": model_ref_id},
                "font": "Arial;13;1",
                "left": left + 5,
                "top": top + 5,
                "width": w - 10,
                "height": 23,
                "text": name
            }
        }

    v_c1 = get_id()
    v_c2 = get_id()
    v_c3 = get_id()
    v_c4 = get_id()
    v_c5 = get_id()

    arch_views = [
        make_class_view(v_c1, class1_id, "NetworkTrafficSimulator", 50, 80, 240, 120),
        make_class_view(v_c2, class2_id, "NetworkPreprocessor", 340, 80, 240, 120),
        make_class_view(v_c3, class3_id, "AnomalyDetector (IsolationForest)", 630, 80, 270, 140),
        make_class_view(v_c4, class4_id, "NetworkXAI (TreeSHAP)", 340, 280, 240, 120),
        make_class_view(v_c5, class5_id, "ConceptDriftDetector (KS-Test)", 630, 280, 270, 140),
        make_assoc_view(arch_diag_id, v_c1, v_c2, (290, 140), (340, 140)),
        make_assoc_view(arch_diag_id, v_c2, v_c3, (580, 140), (630, 140)),
        make_assoc_view(arch_diag_id, v_c3, v_c4, (630, 180), (580, 320)),
        make_assoc_view(arch_diag_id, v_c3, v_c5, (765, 220), (765, 280)),
    ]

    # Build Component Diagram Views
    comp_diag_id = get_id()
    comp1_id = get_id()
    comp2_id = get_id()
    comp3_id = get_id()
    comp4_id = get_id()

    def make_component_view(view_id, model_ref_id, name, left, top, w=220, h=90):
        nc_id = get_id()
        return {
            "_type": "UMLComponentView",
            "_id": view_id,
            "_parent": {"$ref": comp_diag_id},
            "model": {"$ref": model_ref_id},
            "font": "Arial;13;0",
            "left": left,
            "top": top,
            "width": w,
            "height": h,
            "nameCompartment": {
                "_type": "UMLNameCompartmentView",
                "_id": nc_id,
                "_parent": {"$ref": view_id},
                "model": {"$ref": model_ref_id},
                "font": "Arial;13;1",
                "left": left + 25,
                "top": top + 15,
                "width": w - 35,
                "height": 23,
                "text": name
            }
        }

    v_comp1 = get_id()
    v_comp2 = get_id()
    v_comp3 = get_id()
    v_comp4 = get_id()

    comp_views = [
        make_component_view(v_comp1, comp1_id, "DataIngestionEngine", 60, 100),
        make_component_view(v_comp2, comp2_id, "AnomalyDetectionCore", 350, 100),
        make_component_view(v_comp3, comp3_id, "TreeSHAPExplanationModule", 640, 100),
        make_component_view(v_comp4, comp4_id, "DriftAdaptationController", 350, 260),
        make_assoc_view(comp_diag_id, v_comp1, v_comp2, (280, 145), (350, 145)),
        make_assoc_view(comp_diag_id, v_comp2, v_comp3, (570, 145), (640, 145)),
        make_assoc_view(comp_diag_id, v_comp2, v_comp4, (460, 190), (460, 260)),
    ]

    # Build Activity Diagram Views
    act_diag_id = get_id()
    act1_id = get_id()
    act2_id = get_id()
    act3_id = get_id()
    act4_id = get_id()

    def make_action_view(view_id, model_ref_id, name, left, top, w=230, h=55):
        nc_id = get_id()
        return {
            "_type": "UMLActionView",
            "_id": view_id,
            "_parent": {"$ref": act_diag_id},
            "model": {"$ref": model_ref_id},
            "font": "Arial;13;0",
            "left": left,
            "top": top,
            "width": w,
            "height": h,
            "nameCompartment": {
                "_type": "UMLNameCompartmentView",
                "_id": nc_id,
                "_parent": {"$ref": view_id},
                "model": {"$ref": model_ref_id},
                "font": "Arial;13;0",
                "left": left + 10,
                "top": top + 15,
                "width": w - 20,
                "height": 23,
                "text": name
            }
        }

    v_act1 = get_id()
    v_act2 = get_id()
    v_act3 = get_id()
    v_act4 = get_id()

    act_views = [
        make_action_view(v_act1, act1_id, "Ingest & Normalize Packet", 320, 50),
        make_action_view(v_act2, act2_id, "Score with Isolation Forest", 320, 150),
        make_action_view(v_act3, act3_id, "Generate SHAP Waterfall Plot", 520, 260),
        make_action_view(v_act4, act4_id, "Update FIFO Drift Buffer (KS-Test)", 120, 260),
        make_assoc_view(act_diag_id, v_act1, v_act2, (435, 105), (435, 150)),
        make_assoc_view(act_diag_id, v_act2, v_act3, (470, 205), (550, 260)),
        make_assoc_view(act_diag_id, v_act2, v_act4, (400, 205), (280, 260)),
    ]

    # Assemble Entire StarUML Document
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
                        "ownedViews": all_uc_views
                    },
                    # 2. System Architecture / Class Diagram
                    {
                        "_type": "UMLClassDiagram",
                        "_id": arch_diag_id,
                        "_parent": {"$ref": model_id},
                        "name": "System Architecture Diagram",
                        "ownedViews": arch_views
                    },
                    # 3. Component Diagram
                    {
                        "_type": "UMLComponentDiagram",
                        "_id": comp_diag_id,
                        "_parent": {"$ref": model_id},
                        "name": "Component Diagram",
                        "ownedViews": comp_views
                    },
                    # 4. Activity Diagram
                    {
                        "_type": "UMLActivityDiagram",
                        "_id": act_diag_id,
                        "_parent": {"$ref": model_id},
                        "name": "Activity Diagram",
                        "ownedViews": act_views
                    },
                    # Underlying Models
                    {"_type": "UMLActor", "_id": actor1_id, "name": "Security Analyst"},
                    {"_type": "UMLActor", "_id": actor2_id, "name": "Network Gateway"},
                    {"_type": "UMLUseCase", "_id": uc1_id, "name": "UC1: Ingest Streaming NetFlow Packets"},
                    {"_type": "UMLUseCase", "_id": uc2_id, "name": "UC2: Preprocess Features (Scale & Encode)"},
                    {"_type": "UMLUseCase", "_id": uc3_id, "name": "UC3: Detect Anomalies (Isolation Forest)"},
                    {"_type": "UMLUseCase", "_id": uc4_id, "name": "UC4: Generate TreeSHAP Attribution"},
                    {"_type": "UMLUseCase", "_id": uc5_id, "name": "UC5: Monitor Concept Drift (KS-Test)"},
                    {"_type": "UMLUseCase", "_id": uc6_id, "name": "UC6: Retrain Model (Anti-Poison Filter)"},
                    {"_type": "UMLClass", "_id": class1_id, "name": "NetworkTrafficSimulator"},
                    {"_type": "UMLClass", "_id": class2_id, "name": "NetworkPreprocessor"},
                    {"_type": "UMLClass", "_id": class3_id, "name": "AnomalyDetector"},
                    {"_type": "UMLClass", "_id": class4_id, "name": "NetworkXAI"},
                    {"_type": "UMLClass", "_id": class5_id, "name": "ConceptDriftDetector"},
                    {"_type": "UMLComponent", "_id": comp1_id, "name": "DataIngestionEngine"},
                    {"_type": "UMLComponent", "_id": comp2_id, "name": "AnomalyDetectionCore"},
                    {"_type": "UMLComponent", "_id": comp3_id, "name": "TreeSHAPExplanationModule"},
                    {"_type": "UMLComponent", "_id": comp4_id, "name": "DriftAdaptationController"},
                    {"_type": "UMLAction", "_id": act1_id, "name": "Ingest & Normalize Packet"},
                    {"_type": "UMLAction", "_id": act2_id, "name": "Score with Isolation Forest"},
                    {"_type": "UMLAction", "_id": act3_id, "name": "Generate SHAP Waterfall Plot"},
                    {"_type": "UMLAction", "_id": act4_id, "name": "Update FIFO Drift Buffer (KS-Test)"}
                ]
            }
        ]
    }

    with open(OUTPUT_MDJ, "w", encoding="utf-8") as f:
        json.dump(project, f, indent=2)

    print(f"Updated StarUML file with visual ownedViews generated: {OUTPUT_MDJ}")

if __name__ == "__main__":
    build_full_staruml_project()
