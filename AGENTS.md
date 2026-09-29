# AGENTS.md

## Project Overview

Python ML project for phishing URL detection. All `src/*.py` files are currently **empty stubs** — implementation lives in the notebooks.

## Key Facts

- **Language**: Code is Python; docs and notebook comments are in Bahasa Indonesia.
- **Dataset**: `data/raw/phishing_site_urls.csv` — notebook loads via `../data/raw/phishing_site_urls.csv` (relative path from `notebooks/`).
- **No tests, no CI, no linting config, no build system.**
- **Dependencies**: Unpinned in `requirements.txt` (pandas, numpy, scikit-learn, matplotlib, seaborn, jupyter).
- **No `__init__.py`** in `src/` — not a package, scripts are run individually or from notebooks.

## Workflow

Run notebooks sequentially — each builds on the previous:

```
notebooks/01_data_exploration.ipynb     ← data loading, EDA, cleaning (drop duplicates, resolve label conflicts, filter invalid URLs)
notebooks/02_feature_engineering.ipynb  ← not yet created
notebooks/03_model_training.ipynb       ← not yet created
notebooks/04_model_evaluation.ipynb     ← not yet created
```

Do not skip ahead. Notebook 01 explicitly warns: complete data exploration findings before proceeding.

## Data Cleaning (in notebook 01)

Three cleaning steps applied in order:
1. `drop_duplicates()` — removes 42.150 duplicate rows
2. **Resolusi Konflik Label** — removes all rows where the same URL has conflicting labels (good & bad). Drops 1 URL (2 rows).
3. **Filter URL Tidak Valid** — `is_valid_url()` removes corrupt/non-ASCII URLs (min 7 chars, must contain `.`, must have 3+ alphanumeric chars in a row). Drops 114 rows.

Final shape after cleaning: **507.082 rows** (label distribution: 392.832 good / 114.250 bad).

## Gotchas

- The `.gitignore` excludes `data/raw/`, `data/processed/`, and `models/*.pkl|.h5|.joblib` — these are generated artifacts, not checked in. The CSV in `data/raw/` is also gitignored; it must be downloaded separately (Kaggle source).
- Label column in the CSV is `Label` (values: `good` / `bad`). URL column is `URL`.
- The notebook was originally written for Google Colab (user `MUHAMMAD ILHAM`). It uses a bare filename for the CSV, not a path relative to the project root.
- `reports/evaluation.md` and `reports/figures/` exist but are empty — generated after model evaluation runs.
- `src/` directory is empty — no modules exist yet. The README lists planned files (`preprocessing.py`, `feature_extraction.py`, etc.) but none have been created.

## Session Progress

### Selesai
- [x] Data loading & EDA (notebook 01)
- [x] Drop duplicates (42.150 baris)
- [x] Resolusi konflik label (1 URL, 2 baris)
- [x] Filter URL corrupt/non-ASCII (114 baris)
- [x] Fix DATA_PATH di notebook → `../data/raw/phishing_site_urls.csv`
- [x] Update AGENTS.md

### Berikutnya
- [ ] Notebook 02: Feature Engineering
- [ ] Notebook 03: Model Training
- [ ] Notebook 04: Model Evaluation
