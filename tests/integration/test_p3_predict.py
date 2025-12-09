import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_p3_predict_success():
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
