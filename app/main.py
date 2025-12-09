from fastapi import FastAPI
import pandas as pd
from app.schemas.p3_request import EnergyRequest
from app.services.p3_model import EnergyModel

app = FastAPI(title="Futurisys ML API", version="0.1.0")


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API en ligne 🚀"}


@app.post("/api/p3/predict")
def predict_energy(payload: EnergyRequest):
    data = payload.model_dump()

    # Renommage pour correspondre au modèle sklearn
    data["PropertyGFABuilding(s)"] = data.pop("PropertyGFABuildings")

    df = pd.DataFrame([data])
    y = EnergyModel.predict(df)
    return {"prediction": y}
