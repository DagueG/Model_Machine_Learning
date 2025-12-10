from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class EnergyRequest(BaseModel):
    BuildingType: str
    PrimaryPropertyType: str
    ZipCode: int
    CouncilDistrictCode: int
    Neighborhood: str
    Latitude: float
    Longitude: float
    YearBuilt: int
    NumberofBuildings: int
    NumberofFloors: int
    PropertyGFATotal: float
    PropertyGFAParking: float
    PropertyGFABuildings: float  # <-- colonne renommée
    ListOfAllPropertyUseTypes: str
    LargestPropertyUseType: str
    LargestPropertyUseTypeGFA: float
    SecondLargestPropertyUseType: Optional[str] = None
    SecondLargestPropertyUseTypeGFA: Optional[float] = None
    ThirdLargestPropertyUseType: Optional[str] = None
    ThirdLargestPropertyUseTypeGFA: Optional[float] = None
    YearsENERGYSTARCertified: Optional[int] = None
    Outlier: str
    BuildingAge: float
    SurfacePerFloor: float
    IsMultiUse: bool
    LatZone: int
    LonZone: int


class PredictionResponse(BaseModel):
    """Response model for a single prediction."""
    id: int
    prediction: float
    building_type: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class PredictionHistoryResponse(BaseModel):
    """Response model for prediction history."""
    total: int
    predictions: list[PredictionResponse]
