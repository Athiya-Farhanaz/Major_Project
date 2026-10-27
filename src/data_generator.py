import numpy as np
import pandas as pd
import time
from typing import Dict, Any, Tuple

class NetworkTrafficSimulator:
    def __init__(self, random_state: int = 42):
        self.rng = np.random.RandomState(random_state)
        self.drift_active = False
        self.current_phase = "Normal Baseline"
        self.step_counter = 0

    def set_drift(self, active: bool):
        """Enable or disable concept drift simulation."""
        self.drift_active = active
        self.current_phase = "Concept Drift (WFH/VPN Shift)" if active else "Normal Baseline"

    def generate_single_flow(self, force_anomaly_type: str = None) -> Dict[str, Any]:
        """
        Generates a single network flow record.
        If force_anomaly_type is provided, it guarantees generating that specific attack.
        Otherwise, it generates traffic based on the active phase (normal or drifted normal).
        """
        self.step_counter += 1
        
        # Decide if we generate an anomaly (if not forced)
        # In standard simulation, anomaly rate is about 3-5%
        is_anomaly = False
        anomaly_type = "normal"
        
        if force_anomaly_type:
            is_anomaly = True
            anomaly_type = force_anomaly_type
        else:
            # Random chance of spontaneous anomaly (4%)
            if self.rng.rand() < 0.04:
                is_anomaly = True
                anomaly_type = self.rng.choice(["syn_flood", "data_exfiltration", "brute_force", "port_scan"])

        if is_anomaly:
            return self._generate_anomaly(anomaly_type)
        else:
            return self._generate_normal()

    def _generate_normal(self) -> Dict[str, Any]:
        """Generates standard normal background traffic."""
        # Baseline normal distributions
        if not self.drift_active:
            # Standard network profiles
            protocol = self.rng.choice(["tcp", "udp", "icmp"], p=[0.80, 0.15, 0.05])
            
            if protocol == "tcp":
                service = self.rng.choice(["http", "smtp", "ssh", "ftp", "other"], p=[0.70, 0.15, 0.05, 0.05, 0.05])
                flag = self.rng.choice(["SF", "S0", "REJ"], p=[0.92, 0.04, 0.04])
            elif protocol == "udp":
                service = self.rng.choice(["dns", "other"], p=[0.85, 0.15])
                flag = "SF"
            else: # icmp
                service = "ecr_i"
                flag = "SF"

            duration = float(self.rng.exponential(scale=1.5))
            src_bytes = int(self.rng.lognormal(mean=6.0, sigma=1.0))
            dst_bytes = int(self.rng.lognormal(mean=7.5, sigma=1.2))
            
            # Normal counts (rolling window summaries)
            count = int(self.rng.randint(1, 15))
            srv_count = int(self.rng.randint(1, 10))
            serror_rate = float(self.rng.uniform(0.0, 0.05))
            rerror_rate = float(self.rng.uniform(0.0, 0.05))
            same_srv_rate = float(self.rng.uniform(0.85, 1.0))
            diff_srv_rate = float(self.rng.uniform(0.0, 0.15))
            
            wrong_fragment = 0
            hot = 0
            num_failed_logins = 0
            logged_in = 1 if (protocol == "tcp" and service in ["http", "ssh", "smtp"]) else 0

        else:
            # Concept Drift Phase (Work from Home / VPN shift)
            # - Massive increase in UDP traffic (video conferencing/streaming)
            # - Higher duration and dst_bytes
            # - More SSH/VPN activity
            protocol = self.rng.choice(["tcp", "udp", "icmp"], p=[0.40, 0.55, 0.05])
            
            if protocol == "tcp":
                service = self.rng.choice(["http", "ssh", "other"], p=[0.40, 0.40, 0.20])
                flag = self.rng.choice(["SF", "S0", "REJ"], p=[0.95, 0.02, 0.03])
            elif protocol == "udp":
                # Video packets have high ports, treated as "other"
                service = self.rng.choice(["dns", "other"], p=[0.30, 0.70])
                flag = "SF"
            else:
                service = "ecr_i"
                flag = "SF"

            # Long duration, higher volume (video streaming / SSH sessions)
            duration = float(self.rng.exponential(scale=12.0))
            src_bytes = int(self.rng.lognormal(mean=7.5, sigma=0.8))
            dst_bytes = int(self.rng.lognormal(mean=9.5, sigma=1.0)) # Video downloads
            
            count = int(self.rng.randint(5, 40))
            srv_count = int(self.rng.randint(5, 30))
            serror_rate = float(self.rng.uniform(0.0, 0.02))
            rerror_rate = float(self.rng.uniform(0.0, 0.02))
            same_srv_rate = float(self.rng.uniform(0.90, 1.0))
            diff_srv_rate = float(self.rng.uniform(0.0, 0.10))
            
            wrong_fragment = 0
            hot = 0
            num_failed_logins = 0
            logged_in = 1 if (protocol == "tcp" and service in ["http", "ssh"]) else 0

        return {
            "duration": round(duration, 4),
            "protocol_type": protocol,
            "service": service,
            "flag": flag,
            "src_bytes": src_bytes,
            "dst_bytes": dst_bytes,
            "wrong_fragment": wrong_fragment,
            "hot": hot,
            "num_failed_logins": num_failed_logins,
            "logged_in": logged_in,
            "count": count,
            "srv_count": srv_count,
            "serror_rate": round(serror_rate, 4),
            "rerror_rate": round(rerror_rate, 4),
            "same_srv_rate": round(same_srv_rate, 4),
            "diff_srv_rate": round(diff_srv_rate, 4),
            "label": "normal",
            "is_anomaly": 0
        }

    def _generate_anomaly(self, attack_type: str) -> Dict[str, Any]:
        """Generates specific anomalous attack patterns."""
        if attack_type == "syn_flood":
            # SYN Flood: Many connections from same host to same service with no response (S0)
            return {
                "duration": 0.0,
                "protocol_type": "tcp",
                "service": "http",
                "flag": "S0",
                "src_bytes": 0,
                "dst_bytes": 0,
                "wrong_fragment": 0,
                "hot": 0,
                "num_failed_logins": 0,
                "logged_in": 0,
                "count": int(self.rng.randint(250, 450)),
                "srv_count": int(self.rng.randint(250, 450)),
                "serror_rate": round(float(self.rng.uniform(0.95, 1.0)), 4),
                "rerror_rate": 0.0,
                "same_srv_rate": round(float(self.rng.uniform(0.90, 1.0)), 4),
                "diff_srv_rate": round(float(self.rng.uniform(0.0, 0.05)), 4),
                "label": "SYN Flood",
                "is_anomaly": 1
            }
            
        elif attack_type == "data_exfiltration":
            # Data Exfiltration: Large src_bytes (upload), long duration, SF flag, using SSH/FTP
            duration = float(self.rng.uniform(300.0, 900.0))
            src_bytes = int(self.rng.lognormal(mean=16.0, sigma=0.5))  # ~5MB to ~20MB
            dst_bytes = int(self.rng.lognormal(mean=8.0, sigma=1.0))
            return {
                "duration": round(duration, 4),
                "protocol_type": "tcp",
                "service": self.rng.choice(["ftp", "ssh"]),
                "flag": "SF",
                "src_bytes": src_bytes,
                "dst_bytes": dst_bytes,
                "wrong_fragment": 0,
                "hot": int(self.rng.randint(2, 6)),  # File operations, command executions
                "num_failed_logins": 0,
                "logged_in": 1,
                "count": int(self.rng.randint(1, 5)),
                "srv_count": int(self.rng.randint(1, 3)),
                "serror_rate": 0.0,
                "rerror_rate": 0.0,
                "same_srv_rate": 1.0,
                "diff_srv_rate": 0.0,
                "label": "Data Exfiltration",
                "is_anomaly": 1
            }
            
        elif attack_type == "brute_force":
            # Brute Force: many failed logins, short duration, SSH service
            return {
                "duration": round(float(self.rng.uniform(1.0, 10.0)), 4),
                "protocol_type": "tcp",
                "service": "ssh",
                "flag": "SF",
                "src_bytes": int(self.rng.randint(100, 500)),
                "dst_bytes": int(self.rng.randint(100, 500)),
                "wrong_fragment": 0,
                "hot": 0,
                "num_failed_logins": int(self.rng.randint(3, 8)),
                "logged_in": 0,
                "count": int(self.rng.randint(30, 80)),
                "srv_count": int(self.rng.randint(30, 80)),
                "serror_rate": 0.0,
                "rerror_rate": 0.0,
                "same_srv_rate": 1.0,
                "diff_srv_rate": 0.0,
                "label": "Brute Force",
                "is_anomaly": 1
            }
            
        elif attack_type == "port_scan":
            # Port Scan: Connects to many different services (high diff_srv_rate), flags are REJ or RSTR
            return {
                "duration": 0.0,
                "protocol_type": "tcp",
                "service": self.rng.choice(["other", "ftp", "ssh", "http"]),
                "flag": "REJ",
                "src_bytes": 0,
                "dst_bytes": 0,
                "wrong_fragment": 0,
                "hot": 0,
                "num_failed_logins": 0,
                "logged_in": 0,
                "count": int(self.rng.randint(100, 200)),
                "srv_count": int(self.rng.randint(1, 5)),
                "serror_rate": 0.0,
                "rerror_rate": 1.0,
                "same_srv_rate": round(float(self.rng.uniform(0.0, 0.15)), 4),
                "diff_srv_rate": round(float(self.rng.uniform(0.85, 1.0)), 4),
                "label": "Port Scan",
                "is_anomaly": 1
            }
            
        else:
            return self._generate_normal()

    def generate_batch(self, batch_size: int) -> pd.DataFrame:
        """Generates a batch of traffic records in a pandas DataFrame."""
        records = [self.generate_single_flow() for _ in range(batch_size)]
        return pd.DataFrame(records)

    def generate_baseline(self, num_samples: int) -> pd.DataFrame:
        """Generates baseline traffic (guaranteed normal) for initial model training."""
        records = [self._generate_normal() for _ in range(num_samples)]
        return pd.DataFrame(records)


if __name__ == "__main__":
    # Quick sanity check
    sim = NetworkTrafficSimulator()
    df_normal = sim.generate_baseline(100)
    print("Normal Baseline columns:", df_normal.columns.tolist())
    print("Normal Sample:", df_normal.head(1).to_dict('records')[0])
    
    df_batch = sim.generate_batch(10)
    print("\nBatch anomaly value counts:\n", df_batch['label'].value_counts())
    
    df_syn = sim._generate_anomaly("syn_flood")
    print("\nSYN Flood Sample:", df_syn)
