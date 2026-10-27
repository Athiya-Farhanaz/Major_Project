import os

# Base paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
os.makedirs(DATA_DIR, exist_ok=True)

# Model paths
MODEL_PATH = os.path.join(DATA_DIR, "isolation_forest.pkl")
PREPROCESSOR_PATH = os.path.join(DATA_DIR, "preprocessor.pkl")

# Traffic Simulator Configuration
SIMULATION_TICK_RATE = 0.5  # Seconds between streamed records in dashboard
BASELINE_TRAIN_SIZE = 1200   # Number of normal samples to train initial model

# Network Traffic Features
NUMERIC_FEATURES = [
    "duration",
    "src_bytes",
    "dst_bytes",
    "wrong_fragment",
    "hot",
    "num_failed_logins",
    "count",
    "srv_count",
    "serror_rate",
    "rerror_rate",
    "same_srv_rate",
    "diff_srv_rate"
]

CATEGORICAL_FEATURES = [
    "protocol_type",
    "service",
    "flag"
]

ALL_FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES

# XAI Configuration
SHAP_BACKGROUND_SIZE = 150  # Size of background data used to initialize SHAP Explainer
MAX_SHAP_FEATURES = 5       # Max features to show in text explanations

# Concept Drift Detector Configuration
DRIFT_WINDOW_SIZE = 250     # Size of rolling windows to check for distribution drift
DRIFT_ALPHA = 0.01          # Significance level for KS statistical test (p-value threshold)
DRIFT_MIN_INTERVAL = 300    # Minimum records between retraining triggers to prevent thrashing
