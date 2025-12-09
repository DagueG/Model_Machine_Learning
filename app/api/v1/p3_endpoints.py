from fastapi import APIRouter
import pandas as pd
from app.schemas.p3_request import EnergyRequest
from app.services.p3_model import EnergyModel

router = APIRouter()

@router.post("/predict")
def predict_energy(payload: EnergyRequest):
    data = payload.model_dump()

    # Renommage pour correspondre au modèle sklearn
    data["PropertyGFABuilding(s)"] = data.pop("PropertyGFABuildings")

    df = pd.DataFrame([data])
    y = EnergyModel.predict(df)
    return {"prediction": y}
