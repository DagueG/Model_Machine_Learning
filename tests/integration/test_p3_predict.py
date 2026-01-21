import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import get_db
from app.models import EnergyPrediction, EnergyDataset


@pytest.fixture
def client(test_db):
    """Override the get_db dependency with test database for each test."""
    def override_get_db():
        try:
            db = test_db()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_p3_predict_success(client):
    payload = {
        "BuildingType": "NonResidential",
        "PrimaryPropertyType": "Office",
        "ZipCode": 98101,
        "CouncilDistrictCode": 3,
        "Neighborhood": "Downtown",
        "Latitude": 47.61,
        "Longitude": -122.33,
        "YearBuilt": 1999,
        "NumberofBuildings": 1,
        "NumberofFloors": 12,
        "PropertyGFATotal": 100000,
        "PropertyGFAParking": 20000,
        "PropertyGFABuildings": 80000,
        "ListOfAllPropertyUseTypes": "Office",
        "LargestPropertyUseType": "Office",
        "LargestPropertyUseTypeGFA": 80000,
        "SecondLargestPropertyUseType": None,
        "SecondLargestPropertyUseTypeGFA": None,
        "ThirdLargestPropertyUseType": None,
        "ThirdLargestPropertyUseTypeGFA": None,
        "YearsENERGYSTARCertified": 0,
        "Outlier": "No",
        "BuildingAge": 17,
        "SurfacePerFloor": 80000,
        "IsMultiUse": False,
        "LatZone": 2,
        "LonZone": 3
    }

    response = client.post("/api/p3/predict", json=payload)

    # Le code doit être 200
    assert response.status_code == 200

    data = response.json()

    # La réponse doit contenir une prédiction
    assert "prediction" in data
    assert isinstance(data["prediction"], float)


def test_prediction_logged_to_database(client, test_db):
    """Test that predictions are logged to the database."""
    # Note: Each test gets a fresh database from the fixture, so no need to clear
    
    payload = {
        "BuildingType": "Residential",
        "PrimaryPropertyType": "Apartment",
        "ZipCode": 98102,
        "CouncilDistrictCode": 5,
        "Neighborhood": "Capitol Hill",
        "Latitude": 47.62,
        "Longitude": -122.32,
        "YearBuilt": 2005,
        "NumberofBuildings": 2,
        "NumberofFloors": 5,
        "PropertyGFATotal": 50000,
        "PropertyGFAParking": 10000,
        "PropertyGFABuildings": 40000,
        "ListOfAllPropertyUseTypes": "Residential",
        "LargestPropertyUseType": "Residential",
        "LargestPropertyUseTypeGFA": 40000,
        "SecondLargestPropertyUseType": None,
        "SecondLargestPropertyUseTypeGFA": None,
        "ThirdLargestPropertyUseType": None,
        "ThirdLargestPropertyUseTypeGFA": None,
        "YearsENERGYSTARCertified": 3,
        "Outlier": "No",
        "BuildingAge": 19,
        "SurfacePerFloor": 8000,
        "IsMultiUse": False,
        "LatZone": 47,
        "LonZone": 122
    }

    # Make prediction
    response = client.post("/api/p3/predict", json=payload)
    assert response.status_code == 200

    # Verify it was saved in database
    db = test_db()
    predictions = db.query(EnergyPrediction).all()
    assert len(predictions) > 0
    prediction = predictions[-1]  # Get the last one
    assert prediction.id > 0  # Verify id exists
    assert prediction.prediction > 0
    db.close()


def test_get_prediction_history(client):
    """Test retrieving prediction history."""
    response = client.get("/api/p3/history")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "predictions" in data
    assert isinstance(data["predictions"], list)

