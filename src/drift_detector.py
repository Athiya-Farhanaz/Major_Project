import numpy as np
import pandas as pd
from scipy.stats import ks_2samp
from typing import Dict, List, Tuple, Any
from src.config import DRIFT_WINDOW_SIZE, DRIFT_ALPHA

class ConceptDriftDetector:
    def __init__(self, reference_df: pd.DataFrame, window_size: int = DRIFT_WINDOW_SIZE, alpha: float = DRIFT_ALPHA):
        """
        Initializes the drift detector.
        
        Args:
            reference_df: Baseline (normal) DataFrame to compare against.
            window_size: Size of the rolling window for current traffic.
            alpha: Significance level for the Kolmogorov-Smirnov test.
        """
        self.window_size = window_size
        self.alpha = alpha
        
        # We monitor key numeric features that represent volume and connection profile
        self.features_to_monitor = ["duration", "src_bytes", "dst_bytes", "count", "srv_count"]
        
        # Store reference baseline distributions
        self.reference_data = {feat: reference_df[feat].values for feat in self.features_to_monitor}
        
        # Initialize empty window buffers
        self.window_buffer = {feat: [] for feat in self.features_to_monitor}
        self.records_processed = 0
        self.last_p_values = {feat: 1.0 for feat in self.features_to_monitor}

    def update(self, record: Dict[str, Any]) -> Tuple[bool, Dict[str, float]]:
        """
        Updates the sliding window with a new record and performs the KS test.
        
        Args:
            record: Dict representing a single network flow record.
            
        Returns:
            drift_detected: True if distribution drift is detected in at least one feature.
            p_values: Dict mapping monitored features to their KS-test p-values.
        """
        self.records_processed += 1
        drift_detected = False
        p_values = {}

        # Add values to rolling buffers
        for feat in self.features_to_monitor:
            if feat in record:
                self.window_buffer[feat].append(record[feat])
                # Maintain sliding window size
                if len(self.window_buffer[feat]) > self.window_size:
                    self.window_buffer[feat].pop(0)

        # We start running the KS-test only when we have a full window
        # To avoid excessive computation, we test every 25 records once full
        if (len(self.window_buffer[self.features_to_monitor[0]]) == self.window_size and 
                self.records_processed % 25 == 0):
            
            # Bonferroni correction: divide alpha by the number of monitored features
            # to maintain family-wise error rate (FWER) control
            bonferroni_alpha = self.alpha / len(self.features_to_monitor)
            significant_shifts = 0
            
            for feat in self.features_to_monitor:
                ref_dist = self.reference_data[feat]
                curr_dist = np.array(self.window_buffer[feat])
                
                # Perform 2-sample Kolmogorov-Smirnov test
                stat, p_val = ks_2samp(ref_dist, curr_dist)
                p_values[feat] = float(p_val)
                self.last_p_values[feat] = float(p_val)
                
                # If p-value is below the Bonferroni-corrected alpha, reject the null hypothesis
                if p_val < bonferroni_alpha:
                    significant_shifts += 1
            
            # Declare drift if at least one feature shows significant statistical shift
            if significant_shifts >= 1:
                drift_detected = True
        else:
            # Return last computed p-values for continuity in UI
            p_values = self.last_p_values.copy()

        return drift_detected, p_values

    def reset_reference(self, new_reference_df: pd.DataFrame):
        """
        Resets the baseline reference distributions. 
        Useful after retraining the model on drifted data.
        """
        print("Resetting drift detector baseline reference distributions...")
        self.reference_data = {feat: new_reference_df[feat].values for feat in self.features_to_monitor}
        # Clear current window to start fresh
        self.window_buffer = {feat: [] for feat in self.features_to_monitor}
        self.last_p_values = {feat: 1.0 for feat in self.features_to_monitor}


if __name__ == "__main__":
    # Test drift detector sanity
    from src.data_generator import NetworkTrafficSimulator
    
    sim = NetworkTrafficSimulator(random_state=42)
    df_ref = sim.generate_baseline(500)
    
    detector = ConceptDriftDetector(df_ref)
    print("Drift detector initialized with baseline normal data.")
    
    # Feed 300 normal records (no drift should be detected)
    print("Feeding 300 normal records...")
    drift_hits = 0
    for i in range(300):
        rec = sim.generate_single_flow()
        drift, pvals = detector.update(rec)
        if drift:
            drift_hits += 1
            
    print(f"Normal phase - Drift detected: {drift_hits} times. P-values: {pvals}")
    
    # Activate concept drift
    print("\nActivating concept drift in simulator...")
    sim.set_drift(True)
    
    drift_hits = 0
    for i in range(300):
        rec = sim.generate_single_flow()
        drift, pvals = detector.update(rec)
        if drift:
            drift_hits += 1
            
    print(f"Drift phase - Drift detected: {drift_hits} times. P-values: {pvals}")
