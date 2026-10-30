import json
import uuid
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_MDJ = os.path.join(OUTPUT_DIR, "major_project_diagrams.mdj")

def get_id():
    return str(uuid.uuid4()).replace("-", "")[:24]

def build_staruml_project():
    project_id = get_id()
    model_id = get_id()

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
                    # 1. Use Case Model
                    {
                        "_type": "UMLUseCaseDiagram",
                        "_id": get_id(),
                        "_parent": {"$ref": model_id},
                        "name": "Use Case Diagram",
                        "ownedViews": []
                    },
                    # 2. Activity Model
                    {
                        "_type": "UMLActivityDiagram",
                        "_id": get_id(),
                        "_parent": {"$ref": model_id},
                        "name": "Activity Diagram",
                        "ownedViews": []
                    },
                    # 3. Sequence Model
                    {
                        "_type": "UMLSequenceDiagram",
                        "_id": get_id(),
                        "_parent": {"$ref": model_id},
                        "name": "Sequence Diagram",
                        "ownedViews": []
                    },
                    # 4. Collaboration / Communication Model
                    {
                        "_type": "UMLCommunicationDiagram",
                        "_id": get_id(),
                        "_parent": {"$ref": model_id},
                        "name": "Collaboration Diagram",
                        "ownedViews": []
                    },
                    # 5. Component Model
                    {
                        "_type": "UMLComponentDiagram",
                        "_id": get_id(),
                        "_parent": {"$ref": model_id},
                        "name": "Component Diagram",
                        "ownedViews": []
                    },
                    # 6. Deployment Model
                    {
                        "_type": "UMLDeploymentDiagram",
                        "_id": get_id(),
                        "_parent": {"$ref": model_id},
                        "name": "Deployment Diagram",
                        "ownedViews": []
                    },
                    # 7. Architecture Model
                    {
                        "_type": "UMLClassDiagram",
                        "_id": get_id(),
                        "_parent": {"$ref": model_id},
                        "name": "System Architecture Diagram",
                        "ownedViews": []
                    },
                    # Underlying Classes / Components
                    {
                        "_type": "UMLClass",
                        "_id": get_id(),
                        "_parent": {"$ref": model_id},
                        "name": "NetworkTrafficSimulator",
                        "attributes": [
                            {"_type": "UMLAttribute", "_id": get_id(), "name": "rng"},
                            {"_type": "UMLAttribute", "_id": get_id(), "name": "drift_active"},
                            {"_type": "UMLAttribute", "_id": get_id(), "name": "current_phase"}
                        ],
                        "operations": [
                            {"_type": "UMLOperation", "_id": get_id(), "name": "generate_single_flow"},
                            {"_type": "UMLOperation", "_id": get_id(), "name": "set_drift"}
                        ]
                    },
                    {
                        "_type": "UMLClass",
                        "_id": get_id(),
                        "_parent": {"$ref": model_id},
                        "name": "NetworkPreprocessor",
                        "attributes": [
                            {"_type": "UMLAttribute", "_id": get_id(), "name": "preprocessor"},
                            {"_type": "UMLAttribute", "_id": get_id(), "name": "feature_names"}
                        ],
                        "operations": [
                            {"_type": "UMLOperation", "_id": get_id(), "name": "fit"},
                            {"_type": "UMLOperation", "_id": get_id(), "name": "transform"}
                        ]
                    },
                    {
                        "_type": "UMLClass",
                        "_id": get_id(),
                        "_parent": {"$ref": model_id},
                        "name": "AnomalyDetector",
                        "attributes": [
                            {"_type": "UMLAttribute", "_id": get_id(), "name": "model: IsolationForest"},
                            {"_type": "UMLAttribute", "_id": get_id(), "name": "threshold: float"}
                        ],
                        "operations": [
                            {"_type": "UMLOperation", "_id": get_id(), "name": "fit"},
                            {"_type": "UMLOperation", "_id": get_id(), "name": "predict"},
                            {"_type": "UMLOperation", "_id": get_id(), "name": "get_anomaly_score"}
                        ]
                    },
                    {
                        "_type": "UMLClass",
                        "_id": get_id(),
                        "_parent": {"$ref": model_id},
                        "name": "NetworkXAI",
                        "attributes": [
                            {"_type": "UMLAttribute", "_id": get_id(), "name": "explainer: TreeExplainer"}
                        ],
                        "operations": [
                            {"_type": "UMLOperation", "_id": get_id(), "name": "explain_instance"}
                        ]
                    },
                    {
                        "_type": "UMLClass",
                        "_id": get_id(),
                        "_parent": {"$ref": model_id},
                        "name": "ConceptDriftDetector",
                        "attributes": [
                            {"_type": "UMLAttribute", "_id": get_id(), "name": "window_size: int"},
                            {"_type": "UMLAttribute", "_id": get_id(), "name": "alpha: float"},
                            {"_type": "UMLAttribute", "_id": get_id(), "name": "last_drift_record: int"}
                        ],
                        "operations": [
                            {"_type": "UMLOperation", "_id": get_id(), "name": "update"},
                            {"_type": "UMLOperation", "_id": get_id(), "name": "reset_reference"}
                        ]
                    }
                ]
            }
        ]
    }

    with open(OUTPUT_MDJ, "w", encoding="utf-8") as f:
        json.dump(project, f, indent=2)

    print(f"StarUML native project file generated successfully: {OUTPUT_MDJ}")

if __name__ == "__main__":
    build_staruml_project()
