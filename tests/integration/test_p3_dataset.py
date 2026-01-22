"""Integration tests using original P3 test dataset."""

import pytest
import pandas as pd
from pathlib import Path
from app.models import EnergyPrediction, EnergyDataset
from app.services.p3_model import EnergyModel
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import numpy as np


@pytest.fixture
def test_data():
    """Load P3 test dataset."""
    data_dir = Path("data")
    
    # Check if test data exists
    if not (data_dir / "X_test.csv").exists():
        pytest.skip("Test data not found at data/X_test.csv")
    
    X_test = pd.read_csv(data_dir / "X_test.csv")
    y_test = pd.read_csv(data_dir / "y_test.csv").squeeze()
    
    return X_test, y_test


def test_model_with_p3_dataset(test_data):
    """Test model predictions with original P3 test dataset."""
    X_test, y_test = test_data
    
    # Run predictions for each row (model predicts one row at a time)
    predictions = []
    for idx in range(len(X_test)):
        pred = EnergyModel.predict(X_test.iloc[[idx]])
        predictions.append(pred)
    
    predictions = np.array(predictions)
    
    # Verify predictions are valid
    assert len(predictions) == len(y_test), "Predictions length mismatch"
    assert all(isinstance(p, (int, float, np.number)) for p in predictions), "Invalid prediction types"
    assert all(p > 0 for p in predictions), "Predictions should be positive"
    
    # Calculate metrics
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    
    # Basic sanity checks
    assert rmse < 20_000_000, f"RMSE too high: {rmse}"  # Reasonable threshold for energy consumption
    assert r2 > -1, "R² should be > -1"
    
    print(f"\n📊 Model Performance on P3 Test Data:")
    print(f"   RMSE: {rmse:,.2f}")
    print(f"   MAE:  {mae:,.2f}")
    print(f"   R²:   {r2:.4f}")


def test_dataset_predictions_saved_to_db(test_data, test_db):
    """Test that dataset predictions are correctly saved to database."""
    X_test, y_test = test_data
    
    # Limit to first 10 samples for quick test
    X_sample = X_test.iloc[:10]
    y_sample = y_test.iloc[:10]
    
    # Run predictions
    predictions = []
    for idx in range(len(X_sample)):
        pred = EnergyModel.predict(X_sample.iloc[[idx]])
        predictions.append(pred)
    
    predictions = np.array(predictions)
    
    # Save to test database
    db = test_db()
    
    for idx, pred in enumerate(predictions):
        # First, create dataset record
        dataset_record = EnergyDataset(
            building_type=X_sample.iloc[idx].get("BuildingType", "Unknown"),
            primary_property_type=X_sample.iloc[idx].get("PrimaryPropertyType", "Unknown"),
            zip_code=int(X_sample.iloc[idx].get("ZipCode", 0)),
            council_district_code=int(X_sample.iloc[idx].get("CouncilDistrictCode", 0)),
            neighborhood=X_sample.iloc[idx].get("Neighborhood", ""),
            latitude=float(X_sample.iloc[idx].get("Latitude", 0)),
            longitude=float(X_sample.iloc[idx].get("Longitude", 0)),
            year_built=int(X_sample.iloc[idx].get("YearBuilt", 0)),
            number_of_buildings=int(X_sample.iloc[idx].get("NumberofBuildings", 1)),
            number_of_floors=int(X_sample.iloc[idx].get("NumberofFloors", 1)),
            property_gfa_total=float(X_sample.iloc[idx].get("PropertyGFATotal", 0)),
            property_gfa_parking=float(X_sample.iloc[idx].get("PropertyGFAParking", 0)),
            property_gfa_buildings=float(X_sample.iloc[idx].get("PropertyGFABuilding(s)", 0)),
            list_of_all_property_use_types=X_sample.iloc[idx].get("ListOfAllPropertyUseTypes", ""),
            largest_property_use_type=X_sample.iloc[idx].get("LargestPropertyUseType", ""),
            largest_property_use_type_gfa=float(X_sample.iloc[idx].get("LargestPropertyUseTypeGFA", 0)),
            second_largest_property_use_type=X_sample.iloc[idx].get("SecondLargestPropertyUseType"),
            second_largest_property_use_type_gfa=X_sample.iloc[idx].get("SecondLargestPropertyUseTypeGFA"),
            third_largest_property_use_type=X_sample.iloc[idx].get("ThirdLargestPropertyUseType"),
            third_largest_property_use_type_gfa=X_sample.iloc[idx].get("ThirdLargestPropertyUseTypeGFA"),
            years_energystar_certified=int(X_sample.iloc[idx].get("YearsENERGYSTARCertified", 0)) if pd.notna(X_sample.iloc[idx].get("YearsENERGYSTARCertified")) else 0,
            outlier=str(X_sample.iloc[idx].get("Outlier", "No")) if pd.notna(X_sample.iloc[idx].get("Outlier")) else "No",
            building_age=float(X_sample.iloc[idx].get("BuildingAge", 0)),
            surface_per_floor=float(X_sample.iloc[idx].get("SurfacePerFloor", 0)),
            is_multi_use=1 if X_sample.iloc[idx].get("IsMultiUse") == True else 0,
            lat_zone=int(X_sample.iloc[idx].get("LatZone", 0)),
            lon_zone=int(X_sample.iloc[idx].get("LonZone", 0)),
        )
        db.add(dataset_record)
        db.flush()  # Get the ID
        
        # Then create prediction record with dataset_id
        prediction_record = EnergyPrediction(
            dataset_id=dataset_record.id,
            prediction=float(pred)
        )
        db.add(prediction_record)
    
    db.commit()
    
    # Verify all records were saved
    saved_predictions = db.query(EnergyPrediction).all()
    assert len(saved_predictions) >= 10, "Not all prediction records were saved"
    
    # Verify data integrity
    for record in saved_predictions[-10:]:
        assert record.prediction > 0, "Prediction should be positive"
        assert record.dataset_id > 0, "Dataset ID should be valid"
    
    db.close()
