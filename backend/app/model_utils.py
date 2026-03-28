import joblib
import os
import numpy as np
from .config import MODEL_PATH

_model = None


def load_model():
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Model file not found at {MODEL_PATH}. Run train_model.py first."
            )
        _model = joblib.load(MODEL_PATH)
    return _model


def predict_failure_probability(features: list[float]) -> float:
    model = load_model()
    arr = np.array([features], dtype=float)
    proba = model.predict_proba(arr)[0][1]
    return float(proba)
