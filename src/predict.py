"""
predict.py

Pipeline prediksi untuk mengklasifikasikan sebuah URL sebagai
Phishing atau Legitimate menggunakan model Random Forest yang sudah dilatih.
"""

import joblib
import pandas as pd
from feature_extraction import extract_features

from pathlib import Path

MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "random_forest_phishing.joblib"


def load_model(model_path: str = MODEL_PATH):
    """Load model Random Forest yang sudah dilatih dari file."""
    return joblib.load(model_path)


def predict_url(url: str, model) -> dict:
    df_single = pd.DataFrame({"URL": [url]})
    features = extract_features(df_single, url_col="URL")

    prediction = model.predict(features)[0]
    proba = model.predict_proba(features)[0]
    class_index = list(model.classes_).index(prediction)

    return {
        "url": url,
        "prediction": "Phishing" if prediction == "bad" else "Legitimate",
        "confidence": round(float(proba[class_index]), 4),
    }


if __name__ == "__main__":
    model = load_model()

    test_urls = [
        "https://example.com/login",
        "http://192.168.1.1/paypal-verify-account-12345.php",
    ]

    for url in test_urls:
        result = predict_url(url, model)
        print(result)