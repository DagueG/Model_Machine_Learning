from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
from app.schemas.p3_request import EnergyRequest, PredictionResponse, PredictionHistoryResponse, DatasetResponse
from app.services.p3_model import EnergyModel
from app.core.database import get_db
from app.models import EnergyDataset, EnergyPrediction

app = FastAPI(title="Futurisys ML API", version="0.1.0")


@app.get("/")
def root():
    return {
        "message": "Futurisys ML API",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
def health_check():
    try:
        # Validate model can be loaded
        EnergyModel.load()
        return {"status": "ok", "message": "API en ligne 🚀", "model_loaded": True}
    except Exception as e:
        return {"status": "error", "message": f"Impossible de charger le modèle: {str(e)}", "model_loaded": False}


@app.post("/api/p3/predict")
def predict_energy(payload: EnergyRequest, db: Session = Depends(get_db)):
    data = payload.model_dump()

    # Renommage pour correspondre au modèle sklearn
    data["PropertyGFABuilding(s)"] = data.pop("PropertyGFABuildings")

    df = pd.DataFrame([data])
    y = EnergyModel.predict(df)
    
    # 1. First, add the data to EnergyDataset
    dataset_record = EnergyDataset(
        building_type=payload.BuildingType,
        primary_property_type=payload.PrimaryPropertyType,
        zip_code=payload.ZipCode,
        council_district_code=payload.CouncilDistrictCode,
        neighborhood=payload.Neighborhood,
        latitude=payload.Latitude,
        longitude=payload.Longitude,
        year_built=payload.YearBuilt,
        number_of_buildings=payload.NumberofBuildings,
        number_of_floors=payload.NumberofFloors,
        property_gfa_total=payload.PropertyGFATotal,
        property_gfa_parking=payload.PropertyGFAParking,
        property_gfa_buildings=payload.PropertyGFABuildings,
        list_of_all_property_use_types=payload.ListOfAllPropertyUseTypes,
        largest_property_use_type=payload.LargestPropertyUseType,
        largest_property_use_type_gfa=payload.LargestPropertyUseTypeGFA,
        second_largest_property_use_type=payload.SecondLargestPropertyUseType,
        second_largest_property_use_type_gfa=payload.SecondLargestPropertyUseTypeGFA,
        third_largest_property_use_type=payload.ThirdLargestPropertyUseType,
        third_largest_property_use_type_gfa=payload.ThirdLargestPropertyUseTypeGFA,
        years_energystar_certified=payload.YearsENERGYSTARCertified,
        outlier=payload.Outlier,
        building_age=payload.BuildingAge,
        surface_per_floor=payload.SurfacePerFloor,
        is_multi_use=int(payload.IsMultiUse),
        lat_zone=payload.LatZone,
        lon_zone=payload.LonZone,
    )
    db.add(dataset_record)
    db.flush()  # Get the ID without committing
    dataset_id = dataset_record.id
    
    # 2. Then, add the prediction with the dataset_id
    prediction_record = EnergyPrediction(
        dataset_id=dataset_id,
        prediction=float(y)
    )
    db.add(prediction_record)
    db.commit()
    db.refresh(prediction_record)
    
    return {"prediction": y, "dataset_id": dataset_id}


@app.get("/api/p3/history", response_model=PredictionHistoryResponse)
def get_prediction_history(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """Get prediction history from database."""
    predictions = db.query(EnergyPrediction).offset(skip).limit(limit).all()
    total = db.query(EnergyPrediction).count()
    
    return {
        "total": total,
        "predictions": predictions
    }


@app.get("/api/p3/dataset/{dataset_id}", response_model=DatasetResponse)
def get_dataset(dataset_id: int, db: Session = Depends(get_db)):
    """Get a specific dataset record by ID."""
    dataset = db.query(EnergyDataset).filter(
        EnergyDataset.id == dataset_id
    ).first()
    
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset record not found")
    
    return dataset
