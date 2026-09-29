# AI-Based Phishing URL Detection

A machine learning project that classifies URLs as **Phishing** or **Legitimate** based purely on lexical/structural characteristics of the URL string — no DNS lookups, WHOIS queries, or page content required.

**Status:** Complete (baseline pipeline) — see [Future Improvements](#future-improvements) for planned extensions.

## Problem Statement

Phishing remains one of the most common initial attack vectors in cybersecurity incidents. Many phishing detection systems rely on blacklists, which fail against newly registered or slightly modified URLs. This project explores whether a URL's _structure alone_ — without visiting the site — carries enough signal to flag it as suspicious.

## Motivation

As a Penetration Testing-focused student, I wanted a portfolio project that demonstrates the ability to apply machine learning to a genuine cybersecurity problem, end-to-end: from raw, messy data to a working prediction pipeline — not just running `.fit()` on a clean textbook dataset.

## Objective

Build and evaluate a binary classifier (Phishing vs. Legitimate) using only features extractable from the URL string itself, with an emphasis on understanding _why_ each feature works (or doesn't) rather than chasing the highest possible accuracy score.

## Dataset

- **Source:** [Phishing Site URLs](https://www.kaggle.com/datasets/taruntiwarihp/phishing-site-urls) (Kaggle)
- **Original size:** 549,346 rows (`URL`, `Label`)
- **Label distribution (raw):** 71.5% legitimate (`good`), 28.5% phishing (`bad`)

### Data Cleaning

The raw dataset required explicit cleaning before use:

| Issue                                                     | Rows Affected  | Action Taken                                                                                     |
| --------------------------------------------------------- | -------------- | ------------------------------------------------------------------------------------------------ |
| Full-row duplicates                                       | 42,150         | Dropped                                                                                          |
| Conflicting labels (same URL, different label)            | 1 URL (2 rows) | Dropped — label could not be trusted                                                             |
| Corrupted/invalid URL strings (e.g. `?`, garbled unicode) | 114            | Dropped via validation rule (min length 7, must contain `.`, must contain ≥3 alphanumeric chars) |

**Final clean dataset:** 507,080 rows — 392,831 legitimate (77.5%), 114,249 phishing (22.5%)

## Methodology

1. Data cleaning & validation
2. Exploratory Data Analysis (EDA) to identify candidate features from evidence, not assumption
3. Feature extraction from raw URL strings
4. Baseline modeling (Logistic Regression) → iterative improvement (Decision Tree → Random Forest)
5. Evaluation with a strong emphasis on recall for the phishing class, not just accuracy
6. Export of the final model into a standalone prediction pipeline

## Feature Engineering

Eight features were extracted from each URL, each validated against the data before inclusion (not assumed from theory alone):

| Feature              | Description                                                       | Validated Signal                                                                                                                                           |
| -------------------- | ----------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `url_length`         | Total character length                                            | Right-skewed for phishing; strong in the tail, weak in the mid-range                                                                                       |
| `dot_count`          | Number of `.` characters                                          | Median identical between classes; distinguishing power mostly in outliers                                                                                  |
| `digit_count`        | Number of digits                                                  | **Strongest individual signal** — clear gap even outside outliers                                                                                          |
| `hyphen_count`       | Number of `-` characters                                          | Counter-intuitive: _higher_ in legitimate URLs due to SEO-friendly article slugs (e.g. news sites), not phishing brand-spoofing as originally hypothesized |
| `special_char_count` | Non-alphanumeric characters (excluding `.` and `/`)               | Weak individually; useful in combination                                                                                                                   |
| `has_at_symbol`      | Presence of `@`                                                   | Rare overall, but ~24x more common in phishing when present                                                                                                |
| `subdomain_count`    | Estimated subdomain depth (hostname-based, not just dot-counting) | Correlates with `dot_count` (r≈0.73); kept as it measures a more precise concept                                                                           |
| `has_ip_address`     | Whether the hostname is a raw IPv4 address                        | Strong signal: 3.19% of phishing URLs vs. 0.006% of legitimate URLs                                                                                        |

**Deliberately excluded:**

- **HTTPS usage** — 99.98% of URLs in this dataset lack scheme information (`http://`/`https://`) entirely, making this feature unusable here.
- **URL shortener detection** — tested and found to have an inverted, misleading signal (6.35% of legitimate URLs vs. 4.95% of phishing URLs used shorteners), likely because legitimate marketing/social content commonly uses shorteners while phishing in this dataset does not.

## Model

Three models were trained and compared, in increasing complexity:

1. **Logistic Regression** (with `class_weight='balanced'`) — linear baseline
2. **Decision Tree** (`max_depth=10`) — captures non-linear feature interactions, still interpretable
3. **Random Forest** (`n_estimators=200`, `max_depth=15`) — ensemble of decision trees

All models used a stratified 80/20 train/test split to preserve class balance across sets.

## Evaluation

Accuracy alone is misleading on this imbalanced dataset (a model that always predicts "legitimate" would already score ~77.5%). Evaluation therefore prioritized **recall on the phishing class**, since a missed phishing URL (false negative) is more dangerous than a false alarm.

| Model                          | Accuracy  | Precision (phishing) | Recall (phishing) | F1 (phishing) | ROC-AUC   |
| ------------------------------ | --------- | -------------------- | ----------------- | ------------- | --------- |
| Logistic Regression (balanced) | 0.717     | 0.415                | 0.627             | 0.500         | 0.755     |
| Decision Tree                  | 0.803     | 0.547                | 0.726             | 0.624         | 0.865     |
| **Random Forest**              | **0.824** | **0.586**            | **0.747**         | **0.657**     | **0.892** |

**Random Forest was selected as the final model** — it outperformed the other two on every metric simultaneously (no trade-off had to be accepted).

### Feature Importance (Random Forest)

```
digit_count           0.258
url_length            0.218
dot_count             0.204
special_char_count    0.130
hyphen_count          0.098
subdomain_count       0.069
has_ip_address        0.017
has_at_symbol         0.007
```

## Results

The final Random Forest model achieves **ROC-AUC 0.892**, correctly identifying **~75% of phishing URLs** in the test set, with a precision of ~59% on flagged phishing predictions.

## Limitations

- **Lexical-only approach.** The model has no access to DNS records, WHOIS registration data, page content, JavaScript behavior, or threat intelligence feeds — all of which are commonly used in production-grade phishing detection systems. This model captures _one signal among many_.
- **Recall ceiling (~75%).** Roughly 1 in 4 phishing URLs in the test set are missed. This is a meaningful gap for a real-world security tool and should not be understated.
- **No HTTPS signal.** The dataset does not reliably include URL scheme information, so a genuinely useful feature (HTTPS vs. HTTP) could not be tested.
- **Dataset recency.** The source dataset reflects phishing patterns as collected at the time of scraping; it may not capture more recent obfuscation techniques.
- **Probability output is not a real-world probability.** The model's `predict_proba()` output reflects internal model confidence based on training data patterns — not a calibrated, real-world likelihood.

## Future Improvements

- Incorporate WHOIS/domain-age features (newly registered domains are a strong phishing indicator)
- Test threshold tuning instead of `class_weight='balanced'` to explore the precision/recall trade-off more granularly
- Cross-validate feature importance across multiple random seeds for stability
- Explore gradient boosting models (XGBoost/LightGBM) as a further comparison point
- Build a lightweight web demo (e.g. Streamlit) for interactive testing

## How to Run

```bash
# 1. Clone the repository
git clone https://github.com/ilham0A/ai-phishing-url-detection
cd ai-phishing-url-detection

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download the dataset (see Dataset section above) into data/raw/

# 4. Run notebooks in order:
#    notebooks/01_data_exploration.ipynb
#    notebooks/02_feature_engineering.ipynb
#    notebooks/03_model_training.ipynb

# 5. Run predictions on new URLs
python src/predict.py
```

## Project Structure

```
ai-phishing-url-detection/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_feature_engineering.ipynb
│   └── 03_model_training.ipynb
├── src/
│   ├── feature_extraction.py
│   └── predict.py
├── models/
│   └── random_forest_phishing.joblib
├── reports/
│   └── model_comparison.csv
├── requirements.txt
└── README.md
```
