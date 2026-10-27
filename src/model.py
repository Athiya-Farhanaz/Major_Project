import pandas as pd
import numpy as np
import pickle
import os
import argparse
from typing import Tuple
from sklearn.ensemble import IsolationForest
from src.config import MODEL_PATH, BASELINE_TRAIN_SIZE
from src.preprocessor import NetworkPreprocessor
from src.data_generator import NetworkTrafficSimulator

class AnomalyDetector:
    def __init__(self, contamination: float = 0.01, random_state: int = 42):
        self.model = IsolationForest(
            n_estimators=100,
            contamination=contamination,
            random_state=random_state,
            n_jobs=-1
        )
        self.threshold = 0.55  # Fallback threshold
        self.is_trained = False

    def fit(self, X_train: np.ndarray):
        """Fits the Isolation Forest on preprocessed features and sets the adaptive threshold."""
        self.model.fit(X_train)
        
        # Calculate raw anomaly scores on the training set
        # score_samples returns negative anomaly scores (more negative = more anomalous)
        # We define score = -score_samples, so higher = more anomalous
        train_scores = -self.model.score_samples(X_train)
        
        # Set threshold at the 99th percentile of normal training traffic
        self.threshold = float(np.percentile(train_scores, 99))
        self.is_trained = True
        print(f"Model trained successfully. Dynamic anomaly threshold set at: {self.threshold:.4f}")

    def get_anomaly_score(self, X: np.ndarray) -> np.ndarray:
        """Returns anomaly score (higher = more anomalous)."""
        if not self.is_trained:
            raise ValueError("Model has not been trained yet!")
        return -self.model.score_samples(X)

    def predict(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Predicts if samples are anomalies.
        Returns:
            is_anomaly: Binary array (1 for anomaly, 0 for normal)
            scores: Continuous anomaly scores
        """
        scores = self.get_anomaly_score(X)
        is_anomaly = (scores > self.threshold).astype(int)
        return is_anomaly, scores

    def save(self, filepath: str = MODEL_PATH):
        """Saves the model to disk."""
        with open(filepath, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load(filepath: str = MODEL_PATH) -> 'AnomalyDetector':
        """Loads a model from disk."""
        with open(filepath, 'rb') as f:
            return pickle.load(f)


def run_verification():
    """Verifies that the preprocessor, simulator, and model work together."""
    print("Starting verification for Anomaly Detection Model...")
    
    # 1. Initialize Simulator
    sim = NetworkTrafficSimulator(random_state=42)
    print("Simulator initialized.")
    
    # 2. Generate Baseline normal traffic
    print(f"Generating {BASELINE_TRAIN_SIZE} baseline normal traffic records...")
    df_baseline = sim.generate_baseline(BASELINE_TRAIN_SIZE)
    
    # 3. Fit Preprocessor
    preprocessor = NetworkPreprocessor()
    print("Fitting preprocessor...")
    X_train = preprocessor.fit_transform(df_baseline)
    print(f"Processed training shape: {X_train.shape}")
    
    # 4. Train Model
    detector = AnomalyDetector()
    print("Training Isolation Forest...")
    detector.fit(X_train)
    
    # 5. Generate Test Traffic (with anomalies)
    print("Generating mixed test traffic...")
    df_test = sim.generate_batch(100)
    X_test = preprocessor.transform(df_test)
    
    # 6. Predict
    is_anomaly, scores = detector.predict(X_test)
    df_test['pred_anomaly'] = is_anomaly
    df_test['anomaly_score'] = scores
    
    # Save objects to verify saving works
    preprocessor.save()
    detector.save()
    print("Verification models saved to data/ directory.")
    
    # 7. Print summary statistics
    anomaly_rate = df_test['pred_anomaly'].mean()
    print(f"\nVerification Results:")
    print(f"  Detected anomaly rate: {anomaly_rate * 100:.1f}%")
    print(f"  Ground truth anomaly rate: {df_test['is_anomaly'].mean() * 100:.1f}%")
    
    # Check confusion matrix
    tp = ((df_test['is_anomaly'] == 1) & (df_test['pred_anomaly'] == 1)).sum()
    fp = ((df_test['is_anomaly'] == 0) & (df_test['pred_anomaly'] == 1)).sum()
    fn = ((df_test['is_anomaly'] == 1) & (df_test['pred_anomaly'] == 0)).sum()
    tn = ((df_test['is_anomaly'] == 0) & (df_test['pred_anomaly'] == 0)).sum()
    
    print(f"  True Positives (Attacks detected): {tp}")
    print(f"  False Positives (Normal flagged): {fp}")
    print(f"  False Negatives (Attacks missed): {fn}")
    print(f"  True Negatives (Normal allowed): {tn}")
    print("Verification completed successfully!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Anomaly Detection Model Training and Verification")
    parser.add_argument("--verify", action="store_true", help="Run model verification script")
    args = parser.parse_args()

    if args.verify:
        run_verification()
