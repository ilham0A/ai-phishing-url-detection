# AI Phishing URL Detection

Deteksi URL phishing menggunakan Machine Learning.

## Struktur Project

```
ai-phishing-url-detection/
├── data/
│   ├── raw/          # Dataset mentah
│   └── processed/    # Dataset setelah diproses
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_model_training.ipynb
│   └── 04_model_evaluation.ipynb
├── src/
│   ├── preprocessing.py
│   ├── feature_extraction.py
│   ├── train.py
│   ├── evaluate.py
│   └── predict.py
├── models/
├── reports/
│   ├── figures/
│   └── evaluation.md
├── requirements.txt
└── .gitignore
```

## Setup

```bash
pip install -r requirements.txt
```

## Workflow

1. **Data Exploration** - `notebooks/01_data_exploration.ipynb`
2. **Feature Engineering** - `notebooks/02_feature_engineering.ipynb`
3. **Model Training** - `notebooks/03_model_training.ipynb`
4. **Model Evaluation** - `notebooks/04_model_evaluation.ipynb`
