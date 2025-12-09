import joblib
from pathlib import Path
import pandas as pd

MODEL_PATH = Path("models/model_p3.joblib")

class EnergyModel:
    _model = None

    @classmethod
    def load(cls):
        if cls._model is None:
            if not MODEL_PATH.exists():
                raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
            cls._model = joblib.load(MODEL_PATH)
        return cls._model

    @classmethod
    def predict(cls, df: pd.DataFrame) -> float:
        model = cls.load()
        prediction = model.predict(df)
        return float(prediction[0])
