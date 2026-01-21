import joblib
from pathlib import Path
import pandas as pd
import urllib.request
import os
import threading

MODEL_PATH = Path("models/model_p3.joblib")
MODEL_URL = "https://github.com/DagueG/Model_Machine_Learning/releases/download/v1.0.0-model/model_p3.joblib"

class EnergyModel:
    _model = None
    _lock = threading.Lock()

    @classmethod
    def load(cls):
        if cls._model is None:
            with cls._lock:
                # Double-check pattern: verify again inside lock
                if cls._model is None:
                    # Try local path first
                    if MODEL_PATH.exists():
                        cls._model = joblib.load(MODEL_PATH)
                    else:
                        # Download from GitHub if not found locally
                        try:
                            print("Downloading model from GitHub...")
                            os.makedirs("models", exist_ok=True)
                            urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
                            cls._model = joblib.load(MODEL_PATH)
                        except Exception as e:
                            raise RuntimeError(f"Failed to load model: {e}")
        return cls._model

    @classmethod
    def predict(cls, df: pd.DataFrame) -> float:
        model = cls.load()
        prediction = model.predict(df)
        return float(prediction[0])
