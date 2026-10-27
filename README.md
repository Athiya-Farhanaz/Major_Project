# Real-Time Adaptive & Explainable Network Anomaly Detection System

A self-contained network security telemetry prototype designed to tackle concept drift and model explainability.

---

## 💡 Core Technical Novelties & Methodology

Rather than a static machine learning workflow, this project is framed around two coupled streaming mechanisms:

### 1. Real-Time Streaming Anomaly Explanation (SHAP)
Incoming network flows are intercepted dynamically from the stream. The features are immediately processed and fed to a `shap.TreeExplainer` aligned with an unsupervised **Isolation Forest**. Shapley values are calculated in real-time, mapping features to their exact contributions to the anomaly score, and translated into plain English explanations before the flow is archived.

### 2. Statistical Concept Drift Detection (Bonferroni-Corrected KS-Test)
* **Methodology**: The system monitors a rolling window of streamed traffic features (e.g. `duration`, `src_bytes`, `dst_bytes`, `count`, `srv_count`). We perform two-sample **Kolmogorov-Smirnov (KS) tests** on each feature against the baseline normal dataset.
* **Why the KS-Test**: The Kolmogorov-Smirnov test is non-parametric and distribution-free (it does not assume a normal or any other specific shape of data distributions), making it highly robust for network traffic features which are often heavily skewed or multimodal.
* **Aggregation Rule (Bonferroni Correction)**: To control the family-wise error rate (FWER) and avoid false drift alarms due to multiple comparisons, we use a Bonferroni-corrected significance threshold. The system flags concept drift only if any single feature's p-value drops below:
  $$\text{Significance Threshold} = \frac{\alpha}{N_{\text{features}}} = \frac{0.01}{5} = 0.002$$
  *Why this rule?* Testing multiple features independently at a raw $\alpha=0.01$ would inflate the false alarm rate to $\approx 4.9\%$. The Bonferroni correction mathematically guarantees the overall false alarm probability is bounded by $\alpha = 0.01$.

### 3. Drift-Triggered Adaptive Retraining (Anti-Poisoning Security Filter)
When concept drift is confirmed, the model is retrained to align its normal baseline with the shifted environment.
* **Anti-Poisoning Filter**: To prevent adversarial attacks from poisoning the new baseline during retraining (e.g. a sustained DDoS attack being silently absorbed as "new normal" traffic), a security filter is implemented. The retraining logic filters the buffer to **only use flows classified as normal by the model (`pred_anomaly == 0`)**. This blocks malicious threat vectors from entering the training set.

### 4. Unsupervised Evaluation Framing
* **Training Time**: The Isolation Forest model trains in a completely **unsupervised/semi-supervised** manner, using only features representing normal baseline traffic. No labels or attack classes are seen by the model during training.
* **Evaluation Time**: The UNSW-NB15 ground-truth labels are strictly **eval-only**. They are used only to compute metrics (Accuracy, Precision, Recall, F1, ROC-AUC) and plot the confusion matrix.

---

## 📊 Real-World Offline Validation & Baseline Comparison

We validate the system offline using the **UNSW-NB15** dataset, a well-regarded modern benchmark reflecting contemporary attack behaviors.

### Baseline Model Comparison
We benchmark our chosen **Isolation Forest (IF)** model against another standard unsupervised baseline, **One-Class Support Vector Machine (OC-SVM)**, on the same UNSW-NB15 split:
* **Isolation Forest**: Achieves a **ROC-AUC of 0.7121** and trains in **~0.73s** on the full 29,600 normal samples (scaling at $O(N \log N)$).
* **One-Class SVM**: Achieves a **ROC-AUC of 0.6322** and trains in **~0.28s** (on a sampled subset of 5,000 samples due to its $O(N^3)$ computational scaling limitations).
* **Tradeoff Conclusion**: Isolation Forest significantly outperforms OC-SVM in classification accuracy while maintaining excellent scaling properties on larger baseline streams.

### Official Dataset Citation
When citing this benchmark, reference the original authors and Centre:
> *Moustafa, Nour, and Jill Slay. "UNSW-NB15: a comprehensive data set for network intrusion detection systems (UNSW-NB15 NIDS dataset)." Military Communications and Information Systems Conference (MilCIS), 2015.*
> *Cyber Security Research Group, Australian Centre for Cyber Security (ACCS), UNSW Canberra.*

---

## 📖 Literature Context & Related Work

Since approximately 2020, applying Explainable AI (XAI) to Network Intrusion Detection Systems (NIDS) has emerged as a key area of study to counter the "black-box" nature of deep learning and ensemble classifiers.
* **Prior Work**: Classic publications (e.g., *Moustafa et al., ACCS*) focused purely on static classification metrics. Early XAI adaptations (e.g., *Wang et al., 2020*; *Mahboob et al., 2021*) introduced post-hoc SHAP and LIME values to explain offline classifiers.
* **Our Work vs. Prior Art**: Existing literature predominantly applies explanations to *offline, static, supervised classifiers*. This system advances the state of the art by **coupling local SHAP attributions directly into a streaming loop** and linking it with **automated statistical drift realignment**. This keeps explanations calibrated even when data distributions shift.

---

## 🔬 Scientific Rigor & Analysis

### Explanation Stability Analysis
A common challenge in explainable tree ensembles is *explanation instability*: small variations in data or random forest paths can yield fluctuating Shapley values. In this project, we utilize `shap.TreeExplainer` which evaluates exact mathematical splits rather than sampling approximations (unlike KernelSHAP), ensuring high consistency. Furthermore, to prevent dummy feature fragmentation, **categorical one-hot encodings are grouped back to their parent columns** in `xai_engine.py` prior to visualization.

### Privacy & Ethical Considerations
Deploying network monitoring tools introduces privacy concerns (e.g., monitoring personal user payloads under GDPR). This system mitigates these risks by **exclusively tracking metadata** (flow duration, byte counts, packets, state flags) rather than running Deep Packet Inspection (DPI) on content payloads. In production environments, IP addresses should be anonymized (cryptographically salted and hashed) to satisfy PII protection standards.

---

## ⚠️ System Limitations

No system is silver-bullet, and acknowledging engineering tradeoffs is critical:
1. **Univariate Drift Limitations**: The KS-test drift detector evaluates features univariately. It does not monitor joint distribution shifts (e.g., covariance changes where individual metrics stay within normal bounds but correlation changes).
2. **Sub-Threshold Poisoning**: The anti-poisoning filter checks `pred_anomaly == 0`. While this stops blatant spikes from entering the training set, it remains vulnerable to *gradual adversarial poisoning*, where an attacker slowly drifts attack characteristics just below the decision threshold over time.
3. **Throughput Bounds**: Computing SHAP values takes approximately **~80-120ms per anomaly** (while standard inference takes **<2ms**). Under massive threat conditions (e.g. active DDoS), the SHAP explainer could throttle dashboard queue throughput, necessitating downsampling of explanations in high-speed enterprise settings.
4. **Simulator Simplicity**: The synthetic data generator uses mathematical distributions (log-normal, exponential) which model volume and rate trends well, but do not capture the fine-grained timing jitter or packet headers of real-world networks.

---

## File Structure

```
Majorproject/
├── data/                       # Contains serialized models and metrics
│   ├── isolation_forest.pkl    # Serialized Isolation Forest model
│   ├── preprocessor.pkl        # Serialized preprocessor pipeline
│   ├── UNSW_NB15_testing-set.csv # Downloaded UNSW-NB15 subset (7.3MB)
│   └── offline_metrics.json    # JSON storing offline metrics and confusion matrix
├── src/
│   ├── __init__.py
│   ├── config.py               # Hyperparameters and configurations
│   ├── data_generator.py       # Simulates network traffic & attacks
│   ├── preprocessor.py         # Handles scaling and category encoding
│   ├── model.py                # Isolation Forest training & predictions
│   ├── drift_detector.py       # Kolmogorov-Smirnov test drift tracking
│   ├── xai_engine.py           # SHAP explainer and NLP generator
│   ├── offline_validation.py   # UNSW-NB15 downloader and evaluator
│   └── dashboard.py            # Streamlit dashboard interface
├── requirements.txt            # Project dependencies
├── run.py                      # Startup script (dependency check + download + run)
└── README.md                   # System documentation
```

---

## Setup & Running Instructions

### 1. Prerequisites
Ensure you have **Python 3.9+** installed.

### 2. Run the System
Run the startup script:
```bash
python run.py
```

### 3. Open the Dashboard
Navigate to:
```
http://localhost:8501
```
* **⚡ Tab 1 (Live Stream)**: Tracks **Median Inference Latency** (typically < 2ms) and **Median SHAP Explanation Latency** (typically ~100ms) to log real-time speed.
* **📊 Tab 2 (Offline Validation)**: Inspect performance benchmarks and confusion matrices comparing Isolation Forest against One-Class SVM.
