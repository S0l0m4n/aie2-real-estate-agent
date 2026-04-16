import os

import joblib
import pandas as pd
from dotenv import load_dotenv

MODEL_DIR = "data"

load_dotenv()

ML_MODEL = MODEL_DIR + "/" + os.getenv("ML_MODEL", "")

_model = None


def load_model():
    global _model
    if not os.path.exists(ML_MODEL):
        raise FileNotFoundError(
            f"Model file not found at '{ML_MODEL}'. "
            "Drop the joblib file there and restart the server."
        )
    _model = joblib.load(ML_MODEL)


def predict(features: dict) -> float:
    if _model is None:
        raise RuntimeError("Model is not loaded.")
    df = pd.DataFrame([features])
    result = _model.predict(df)
    return float(result[0])
