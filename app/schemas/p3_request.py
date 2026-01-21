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


class DatasetResponse(BaseModel):
    """Response model for dataset records."""
    id: int
    building_type: str
    primary_property_type: str
    zip_code: int
    council_district_code: int
    neighborhood: Optional[str] = None
    latitude: float
    longitude: float
    year_built: int
    number_of_buildings: int
    number_of_floors: int
    property_gfa_total: float
    property_gfa_parking: float
    property_gfa_buildings: float
    list_of_all_property_use_types: Optional[str] = None
    largest_property_use_type: str
    largest_property_use_type_gfa: float
    second_largest_property_use_type: Optional[str] = None
    second_largest_property_use_type_gfa: Optional[float] = None
    third_largest_property_use_type: Optional[str] = None
    third_largest_property_use_type_gfa: Optional[float] = None
    years_energystar_certified: Optional[int] = None
    outlier: str
    building_age: float
    surface_per_floor: float
    is_multi_use: bool
    lat_zone: int
    lon_zone: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class PredictionResponse(BaseModel):
    """Response model for a single prediction."""
    id: int
    dataset_id: int
    prediction: float
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class PredictionWithDatasetResponse(BaseModel):
    """Response model for prediction with dataset details."""
    id: int
    prediction: float
    created_at: datetime
    dataset: DatasetResponse
    
    model_config = ConfigDict(from_attributes=True)


class PredictionHistoryResponse(BaseModel):
    """Response model for prediction history."""
    total: int
    predictions: list[PredictionResponse]
