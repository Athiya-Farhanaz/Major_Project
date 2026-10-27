import os
import sys
import subprocess
import argparse

def check_dependencies():
    """Checks if the required packages are installed, and installs them if missing."""
    print("Checking dependencies...")
    try:
        import streamlit
        import pandas
        import numpy
        import sklearn
        import shap
        import plotly
        import matplotlib
        import scipy
        print("All dependencies are already installed.")
    except ImportError as e:
        missing_pkg = str(e).split("'")[-2] if "'" in str(e) else str(e)
        print(f"Missing dependency detected: {missing_pkg}")
        requirements_file = os.path.join(os.path.dirname(__file__), "requirements.txt")
        if os.path.exists(requirements_file):
            print(f"Installing dependencies from {requirements_file}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
                print("Dependencies installed successfully!")
            except subprocess.CalledProcessError as err:
                print(f"Error occurred while installing dependencies: {err}")
                sys.exit(1)
        else:
            print("Error: requirements.txt not found. Cannot auto-install dependencies.")
            sys.exit(1)

def check_offline_metrics():
    """Checks if the offline metrics file exists, and runs the script if it doesn't."""
    metrics_path = os.path.join(os.path.dirname(__file__), "data", "offline_metrics.json")
    if not os.path.exists(metrics_path):
        print("Offline metrics from UNSW-NB15 dataset not found. Running offline validation...")
        try:
            subprocess.check_call([sys.executable, "-m", "src.offline_validation"], cwd=os.path.dirname(__file__))
            print("Offline validation metrics computed successfully.")
        except subprocess.CalledProcessError as err:
            print(f"Warning: Failed to compute offline validation metrics: {err}")

def run_streamlit():
    """Launches the Streamlit dashboard."""
    dashboard_path = os.path.join(os.path.dirname(__file__), "src", "dashboard.py")
    if not os.path.exists(dashboard_path):
        print(f"Error: Dashboard file not found at {dashboard_path}")
        sys.exit(1)
        
    print(f"Starting Streamlit dashboard at {dashboard_path}...")
    try:
        subprocess.run(["streamlit", "run", dashboard_path], shell=True)
    except KeyboardInterrupt:
        print("\nStopping Streamlit dashboard...")
    except Exception as e:
        print(f"Error starting Streamlit: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Real-Time Explainable Network Anomaly Detection System")
    parser.add_argument("--skip-install", action="store_true", help="Skip checking and installing dependencies")
    args = parser.parse_args()

    if not args.skip_install:
        check_dependencies()
        
    check_offline_metrics()
    run_streamlit()
