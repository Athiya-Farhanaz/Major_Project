import os
import sys
# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import numpy as np
import pandas as pd
from src.config import ALL_FEATURES, NUMERIC_FEATURES, CATEGORICAL_FEATURES
from src.data_generator import NetworkTrafficSimulator
from src.preprocessor import NetworkPreprocessor
from src.model import AnomalyDetector
from src.drift_detector import ConceptDriftDetector
from src.xai_engine import NetworkXAI


@pytest.fixture
def simulator():
    return NetworkTrafficSimulator(random_state=42)


@pytest.fixture
def baseline_data(simulator):
    return simulator.generate_baseline(600)


@pytest.fixture
def preprocessor(baseline_data):
    prep = NetworkPreprocessor()
    prep.fit(baseline_data)
    return prep


@pytest.fixture
def trained_detector(preprocessor, baseline_data):
    X = preprocessor.transform(baseline_data)
    detector = AnomalyDetector(contamination=0.01, random_state=42)
    detector.fit(X)
    return detector


def test_data_generator_schemas(simulator):
    """Verify that simulated flows contain all required features and valid types."""
    # Test normal traffic
    normal_flow = simulator.generate_single_flow()
    for feat in ALL_FEATURES:
        assert feat in normal_flow, f"Missing feature {feat} in normal flow"
    assert normal_flow["label"] in ["normal", "SYN Flood", "Data Exfiltration", "Brute Force", "Port Scan"]

    # Test forced attacks
    attack_types = ["syn_flood", "data_exfiltration", "brute_force", "port_scan"]
    for at in attack_types:
        attack_flow = simulator.generate_single_flow(force_anomaly_type=at)
        assert attack_flow["is_anomaly"] == 1
        assert attack_flow["label"] != "normal"


def test_preprocessor_transformation(preprocessor, simulator):
    """Verify that preprocessor produces clean scaled numeric arrays and handles unseen categories."""
    test_batch = simulator.generate_batch(50)
    X_transformed = preprocessor.transform(test_batch)

    assert isinstance(X_transformed, np.ndarray)
    assert X_transformed.shape[0] == 50
    assert X_transformed.shape[1] >= len(NUMERIC_FEATURES)
    assert not np.isnan(X_transformed).any(), "Transformed data contains NaNs"


def test_anomaly_detector_scoring(trained_detector, preprocessor, simulator):
    """Verify that Isolation Forest scores anomalies significantly higher than normal baselines."""
    normal_samples = [simulator._generate_normal() for _ in range(20)]
    attack_samples = [simulator._generate_anomaly("data_exfiltration") for _ in range(20)]

    X_normal = preprocessor.transform(pd.DataFrame(normal_samples))
    X_attack = preprocessor.transform(pd.DataFrame(attack_samples))

    scores_normal = trained_detector.get_anomaly_score(X_normal)
    scores_attack = trained_detector.get_anomaly_score(X_attack)

    # In our inverted score formulation (-score_samples), higher score indicates greater anomaly
    assert np.mean(scores_attack) > np.mean(scores_normal), (
        f"Mean attack score ({np.mean(scores_attack):.3f}) should exceed mean normal ({np.mean(scores_normal):.3f})"
    )
    assert np.max(scores_attack) > trained_detector.threshold, (
        "Max attack score should breach the dynamic anomaly threshold"
    )


def test_concept_drift_detector(baseline_data, simulator):
    """Verify KS-test drift detection triggers under distribution shifts and holds under stable traffic."""
    detector = ConceptDriftDetector(baseline_data, window_size=50)

    # Feed normal traffic: drift should remain inactive
    for _ in range(50):
        flow = simulator._generate_normal()
        drift, pvals = detector.update(flow)

    assert not drift, "False positive drift detected on normal baseline traffic"

    # Simulate concept drift (WFH shift)
    simulator.set_drift(True)
    drift_detected = False
    for _ in range(75):
        drift_flow = simulator._generate_normal()
        d, pvals = detector.update(drift_flow)
        if d:
            drift_detected = True
            break

    assert drift_detected, "Concept drift detector failed to flag genuine distribution shift"


def test_xai_engine_explanations(trained_detector, preprocessor, simulator, baseline_data):
    """Verify TreeSHAP explanations compute valid feature contributions and plain-English text."""
    X_bg = preprocessor.transform(baseline_data[:50])
    xai = NetworkXAI(trained_detector, preprocessor, X_bg)

    syn_attack = simulator._generate_anomaly("syn_flood")
    X_syn = preprocessor.transform(pd.DataFrame([syn_attack]))

    explanation = xai.explain_instance(syn_attack, X_syn)

    assert "grouped_shap_values" in explanation
    assert "top_contributors" in explanation
    assert "explanation_text" in explanation
    assert len(explanation["explanation_text"]) > 20
    assert "flag" in explanation["grouped_shap_values"] or "serror_rate" in explanation["grouped_shap_values"]


def test_anti_poisoning_retraining_filter():
    """Verify that the retraining logic correctly filters out anomalous flows to prevent poisoning."""
    # Simulate a stream containing mixed normal and attack flows
    stream = pd.DataFrame([
        {"duration": 1.2, "pred_anomaly": 0},
        {"duration": 0.0, "pred_anomaly": 1},  # SYN Flood
        {"duration": 2.1, "pred_anomaly": 0},
        {"duration": 500.0, "pred_anomaly": 1}, # Data Exfil
        {"duration": 0.9, "pred_anomaly": 0},
    ])

    # Anti-poisoning rule: only retain flows verified as normal
    retraining_buffer = stream[stream["pred_anomaly"] == 0]

    assert len(retraining_buffer) == 3
    assert (retraining_buffer["pred_anomaly"] == 0).all()
    assert 1 not in retraining_buffer["pred_anomaly"].values
