import numpy as np
import pandas as pd
import shap
from typing import Dict, List, Any, Tuple
from src.config import MAX_SHAP_FEATURES
from src.preprocessor import NetworkPreprocessor
from src.model import AnomalyDetector

class NetworkXAI:
    def __init__(self, detector: AnomalyDetector, preprocessor: NetworkPreprocessor, background_X: np.ndarray):
        """
        Initializes the XAI engine.
        
        Args:
            detector: Trained AnomalyDetector instance.
            preprocessor: Trained NetworkPreprocessor instance.
            background_X: Preprocessed baseline normal data to serve as SHAP background reference.
        """
        self.detector = detector
        self.preprocessor = preprocessor
        self.feature_names = preprocessor.get_feature_names()
        
        # Initialize the TreeExplainer for the Isolation Forest model
        # Using a background dataset allows path-dependent / conditional calculations
        self.explainer = shap.TreeExplainer(self.detector.model, data=background_X)

    def explain_instance(self, raw_record: Dict[str, Any], preprocessed_X: np.ndarray) -> Dict[str, Any]:
        """
        Generates feature attribution explanations for a single network flow instance.
        
        Args:
            raw_record: Dict containing the original raw features (before preprocessing).
            preprocessed_X: 1D array or 2D array of shape (1, n_features) preprocessed features.
            
        Returns:
            A dictionary containing:
                - shap_values: Dict mapping feature names to their contribution score
                - top_contributors: List of tuples (feature_name, shap_value, raw_value, interpretation)
                - explanation_text: Human-readable paragraph explanation
        """
        # Ensure 2D array shape
        if preprocessed_X.ndim == 1:
            preprocessed_X = preprocessed_X.reshape(1, -1)

        # Compute SHAP values. TreeExplainer output shape is (1, n_features)
        shap_vals = self.explainer.shap_values(preprocessed_X)
        if isinstance(shap_vals, list):
            # For some configurations SHAP returns a list of arrays
            shap_vals = shap_vals[0]
        shap_vals = shap_vals[0]  # Take the first (and only) sample

        # In scikit-learn's Isolation Forest, trees return the path length.
        # Anomalies have SHORTER path lengths.
        # Therefore, if a feature makes the path length shorter (negative SHAP value),
        # it contributed to making the instance ANOMALOUS.
        # To make explanations intuitive (where positive value = contributes to anomaly),
        # we negate the SHAP values.
        anomaly_contributions = -shap_vals

        # Map contributions to features
        contributions_dict = {}
        for feat_name, val in zip(self.feature_names, anomaly_contributions):
            contributions_dict[feat_name] = float(val)

        # Group one-hot encoded categorical features back to their original columns
        # for clean user-facing presentation.
        grouped_contributions = self._group_categorical_contributions(contributions_dict)

        # Sort features by absolute contribution to anomaly
        sorted_features = sorted(
            grouped_contributions.items(),
            key=lambda item: abs(item[1]),
            reverse=True
        )

        top_contributors = []
        explanation_bullets = []

        # Generate natural language interpretations for the top features
        for feat, val in sorted_features[:MAX_SHAP_FEATURES]:
            raw_val = raw_record.get(feat, "N/A")
            
            # Formulate description of contribution direction
            if val > 0.01:
                direction = "elevated the anomaly score"
                # Formulate domain-specific description
                detail = self._get_feature_interpretation(feat, raw_val, is_high=True)
            elif val < -0.01:
                direction = "reduced the anomaly score (acted normal)"
                detail = self._get_feature_interpretation(feat, raw_val, is_high=False)
            else:
                continue

            top_contributors.append({
                "feature": feat,
                "contribution": val,
                "value": raw_val,
                "detail": detail
            })
            
            explanation_bullets.append(f"- **{feat}** ({raw_val}): {detail} (Contribution: {val:+.3f})")

        # Generate summary text
        if explanation_bullets:
            explanation_text = "This flow was flagged as anomalous primarily due to the following factors:\n" + "\n".join(explanation_bullets)
        else:
            explanation_text = "The flow was flagged as anomalous, but feature contributions are evenly distributed."

        # Store expected value if available
        base_val = 0.50
        try:
            if hasattr(self.explainer, 'expected_value') and self.explainer.expected_value is not None:
                base_val = float(np.ravel(self.explainer.expected_value)[0])
        except Exception:
            pass

        return {
            "shap_values": contributions_dict,
            "grouped_shap_values": grouped_contributions,
            "top_contributors": top_contributors,
            "explanation_text": explanation_text,
            "base_value": base_val
        }

    def _group_categorical_contributions(self, contributions: Dict[str, float]) -> Dict[str, float]:
        """Groups one-hot encoded categories back to their original raw categorical columns."""
        grouped = {}
        # Copy numeric contributions directly
        for feat in self.preprocessor.preprocessor.transformers_[0][2]:  # Numeric features
            grouped[feat] = contributions.get(feat, 0.0)

        # Group categories
        cat_features = self.preprocessor.preprocessor.transformers_[1][2]  # Categorical features
        for cat_feat in cat_features:
            grouped[cat_feat] = 0.0
            # Accumulate contributions of all one-hot dummy features of this root categorical
            for encoded_feat, val in contributions.items():
                if encoded_feat.startswith(f"{cat_feat}_"):
                    grouped[cat_feat] += val
        return grouped

    def _get_feature_interpretation(self, feature: str, value: Any, is_high: bool) -> str:
        """Translates raw feature values into security-oriented interpretations."""
        if feature == "duration":
            return "Connection was open longer than normal" if is_high else "Connection terminated instantly"
        elif feature == "src_bytes":
            return f"High volume of transmitted data ({value} bytes)" if is_high else "Low volume of transmitted data"
        elif feature == "dst_bytes":
            return f"High volume of received data ({value} bytes)" if is_high else "Low volume of received data"
        elif feature == "count":
            return f"High volume of connections ({value}) to the same host in the last 2 seconds (indicates rapid traffic spike)"
        elif feature == "srv_count":
            return f"High volume of connections ({value}) to the same port/service in the last 2 seconds"
        elif feature == "serror_rate":
            return f"High rate of SYN transmission errors ({value * 100:.1f}%), suggesting half-open connection attempts (DDoS/SYN flood)"
        elif feature == "rerror_rate":
            return f"High rate of connection rejection errors ({value * 100:.1f}%), indicating closed-port probes"
        elif feature == "num_failed_logins":
            return f"Multiple failed login attempts ({value}), suggesting a dictionary or brute force attack"
        elif feature == "same_srv_rate":
            return f"All connections directed to the same service ({value * 100:.1f}%)" if is_high else "Connections scattered across different services"
        elif feature == "diff_srv_rate":
            return f"High rate of connections to different services ({value * 100:.1f}%), suggesting a port scanning sweep"
        elif feature == "service":
            return f"Connection is requesting service '{value}', which deviates from baseline distributions"
        elif feature == "protocol_type":
            return f"Unusual usage of protocol '{value}'"
        elif feature == "flag":
            return f"Connection ended with status flag '{value}' (e.g. S0 indicates no response, REJ indicates connection rejected)"
        else:
            state = "higher than average" if is_high else "lower than average"
            return f"Value is {state} (value: {value})"
