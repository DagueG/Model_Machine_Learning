from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime

class EnergyRequest(BaseModel):
    BuildingType: str = Field(example="NonResidential")
    PrimaryPropertyType: str = Field(example="Mixed Use Property")
    ZipCode: int = Field(example=98119)
    CouncilDistrictCode: int = Field(example=7)
    Neighborhood: str = Field(example="MAGNOLIA / QUEEN ANNE")
    Latitude: float = Field(example=47.65532)
    Longitude: float = Field(example=-122.37133)
    YearBuilt: int = Field(example=1961)
    NumberofBuildings: int = Field(example=1)
    NumberofFloors: int = Field(example=2)
    PropertyGFATotal: float = Field(example=37600.0)
    PropertyGFAParking: float = Field(example=0.0)
    PropertyGFABuildings: float = Field(example=37600.0)
    ListOfAllPropertyUseTypes: str = Field(example="Non-Refrigerated Warehouse, Office, Other")
    LargestPropertyUseType: str = Field(example="Non-Refrigerated Warehouse")
    LargestPropertyUseTypeGFA: float = Field(example=18400.0)
    SecondLargestPropertyUseType: Optional[str] = Field(default=None, example="Other")
    SecondLargestPropertyUseTypeGFA: Optional[float] = Field(default=None, example=16200.0)
    ThirdLargestPropertyUseType: Optional[str] = Field(default=None, example="Office")
    ThirdLargestPropertyUseTypeGFA: Optional[float] = Field(default=None, example=3000.0)
    YearsENERGYSTARCertified: Optional[int] = Field(default=None, example=5)
    Outlier: str = Field(example="No")
    BuildingAge: float = Field(example=55.0)
    SurfacePerFloor: float = Field(example=18800.0)
    IsMultiUse: bool = Field(example=True)
    LatZone: int = Field(example=3)
    LonZone: int = Field(example=1)


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
