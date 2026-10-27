import os
import urllib.request
import pandas as pd
import numpy as np
import json
import time
import argparse
from sklearn.model_selection import train_test_split
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix

DATASET_URL = "https://raw.githubusercontent.com/Nir-J/ML-Projects/master/UNSW-Network_Packet_Classification/UNSW_NB15_testing-set.csv"
LOCAL_CSV_PATH = os.path.join("data", "UNSW_NB15_testing-set.csv")
METRICS_JSON_PATH = os.path.join("data", "offline_metrics.json")

def download_dataset():
    """Downloads the UNSW-NB15 testing partition if not already downloaded."""
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(LOCAL_CSV_PATH):
        print(f"Downloading UNSW-NB15 testing set from GitHub (~7.3 MB)...")
        try:
            urllib.request.urlretrieve(DATASET_URL, LOCAL_CSV_PATH)
            print("Download completed successfully.")
        except Exception as e:
            print(f"Error downloading dataset: {e}")
            raise e
    else:
        print("UNSW-NB15 testing dataset already exists locally.")

def run_offline_validation():
    """Trains Isolation Forest and One-Class SVM on normal traffic and evaluates on mixed traffic."""
    download_dataset()
    
    print("Loading UNSW-NB15 dataset...")
    df = pd.read_csv(LOCAL_CSV_PATH)
    print(f"Dataset loaded. Shape: {df.shape}")
    
    # Define columns to use
    numeric_cols = [
        "dur", "spkts", "dpkts", "sbytes", "dbytes", "rate", 
        "sload", "dload", "sloss", "dloss", "smean", "dmean"
    ]
    categorical_cols = ["proto", "service", "state"]
    
    numeric_cols = [c for c in numeric_cols if c in df.columns]
    categorical_cols = [c for c in categorical_cols if c in df.columns]
    
    # Clean data
    df["service"] = df["service"].replace("-", "other").fillna("other")
    df["state"] = df["state"].fillna("other")
    df["proto"] = df["proto"].fillna("other")
    
    df_normal = df[df["label"] == 0]
    df_attack = df[df["label"] == 1]
    
    print(f"Normal flows: {len(df_normal)} | Attack flows: {len(df_attack)}")
    
    # Split normal data: 80% train, 20% test
    normal_train, normal_test = train_test_split(df_normal, test_size=0.2, random_state=42)
    
    # Balance test set with matched sizes of normal and attacks
    n_test_normal = len(normal_test)
    attack_test = df_attack.sample(n=min(n_test_normal, len(df_attack)), random_state=42)
    test_set = pd.concat([normal_test, attack_test]).sample(frac=1.0, random_state=42)
    
    X_train_raw = normal_train[numeric_cols + categorical_cols]
    X_test_raw = test_set[numeric_cols + categorical_cols]
    y_test = test_set["label"].values  # 1 for attack, 0 for normal
    
    # Preprocessing
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_cols)
        ]
    )
    
    print("Fitting preprocessor...")
    X_train = preprocessor.fit_transform(X_train_raw)
    X_test = preprocessor.transform(X_test_raw)
    
    # ----------------- Model 1: Isolation Forest -----------------
    print("\nTraining Isolation Forest...")
    t0 = time.time()
    if_model = IsolationForest(n_estimators=100, contamination=0.005, random_state=42, n_jobs=-1)
    if_model.fit(X_train)
    if_train_time = time.time() - t0
    
    # Evaluate Isolation Forest
    if_raw_scores = -if_model.score_samples(X_test)
    if_train_scores = -if_model.score_samples(X_train)
    if_threshold = float(np.percentile(if_train_scores, 98))
    if_pred = (if_raw_scores > if_threshold).astype(int)
    
    if_acc = accuracy_score(y_test, if_pred)
    if_prec = precision_score(y_test, if_pred, zero_division=0)
    if_rec = recall_score(y_test, if_pred, zero_division=0)
    if_f1 = f1_score(y_test, if_pred, zero_division=0)
    if_roc_auc = roc_auc_score(y_test, if_raw_scores)
    if_cm = confusion_matrix(y_test, if_pred)
    
    print(f"Isolation Forest trained in {if_train_time:.2f}s. ROC-AUC: {if_roc_auc:.4f}")

    # ----------------- Model 2: One-Class SVM -----------------
    # OCSVM can be extremely slow on large datasets (O(N^3)). 
    # We sample a subset (5,000 samples) of normal training data to keep validation fast and stable.
    print("\nTraining One-Class SVM (on sampled 5,000 normal flows)...")
    ocsvm_train_sample = X_train[np.random.default_rng(42).choice(len(X_train), size=min(5000, len(X_train)), replace=False)]
    
    t0 = time.time()
    ocsvm_model = OneClassSVM(kernel='rbf', gamma='scale', nu=0.05)
    ocsvm_model.fit(ocsvm_train_sample)
    ocsvm_train_time = time.time() - t0
    
    # Evaluate OCSVM
    # score_samples returns raw values related to distance to boundary (lower means anomaly)
    # So we negate it for score representation
    ocsvm_raw_scores = -ocsvm_model.score_samples(X_test)
    ocsvm_train_scores = -ocsvm_model.score_samples(ocsvm_train_sample)
    ocsvm_threshold = float(np.percentile(ocsvm_train_scores, 98))
    ocsvm_pred = (ocsvm_raw_scores > ocsvm_threshold).astype(int)
    
    ocsvm_acc = accuracy_score(y_test, ocsvm_pred)
    ocsvm_prec = precision_score(y_test, ocsvm_pred, zero_division=0)
    ocsvm_rec = recall_score(y_test, ocsvm_pred, zero_division=0)
    ocsvm_f1 = f1_score(y_test, ocsvm_pred, zero_division=0)
    ocsvm_roc_auc = roc_auc_score(y_test, ocsvm_raw_scores)
    
    print(f"One-Class SVM trained in {ocsvm_train_time:.2f}s. ROC-AUC: {ocsvm_roc_auc:.4f}")
    
    # Save metrics to JSON
    metrics = {
        "isolation_forest": {
            "accuracy": float(if_acc),
            "precision": float(if_prec),
            "recall": float(if_rec),
            "f1_score": float(if_f1),
            "roc_auc": float(if_roc_auc),
            "train_time": float(if_train_time),
            "threshold": float(if_threshold),
            "confusion_matrix": {
                "tn": int(if_cm[0][0]),
                "fp": int(if_cm[0][1]),
                "fn": int(if_cm[1][0]),
                "tp": int(if_cm[1][1])
            }
        },
        "one_class_svm": {
            "accuracy": float(ocsvm_acc),
            "precision": float(ocsvm_prec),
            "recall": float(ocsvm_rec),
            "f1_score": float(ocsvm_f1),
            "roc_auc": float(ocsvm_roc_auc),
            "train_time": float(ocsvm_train_time),
            "threshold": float(ocsvm_threshold)
        },
        "attack_categories": test_set["attack_cat"].fillna("normal").value_counts().to_dict(),
        "evaluated_at": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    with open(METRICS_JSON_PATH, "w") as f:
        json.dump(metrics, f, indent=4)
    print(f"Offline comparison metrics successfully saved to {METRICS_JSON_PATH}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run offline validation on UNSW-NB15 and benchmark baseline models.")
    args = parser.parse_args()
    run_offline_validation()
