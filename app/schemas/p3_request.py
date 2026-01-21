from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime

class EnergyRequest(BaseModel):
    BuildingType: str = Field(json_schema_extra={"example": "NonResidential"})
    PrimaryPropertyType: str = Field(json_schema_extra={"example": "Mixed Use Property"})
    ZipCode: int = Field(json_schema_extra={"example": 98119})
    CouncilDistrictCode: int = Field(json_schema_extra={"example": 7})
    Neighborhood: str = Field(json_schema_extra={"example": "MAGNOLIA / QUEEN ANNE"})
    Latitude: float = Field(json_schema_extra={"example": 47.65532})
    Longitude: float = Field(json_schema_extra={"example": -122.37133})
    YearBuilt: int = Field(json_schema_extra={"example": 1961})
    NumberofBuildings: int = Field(json_schema_extra={"example": 1})
    NumberofFloors: int = Field(json_schema_extra={"example": 2})
    PropertyGFATotal: float = Field(json_schema_extra={"example": 37600.0})
    PropertyGFAParking: float = Field(json_schema_extra={"example": 0.0})
    PropertyGFABuildings: float = Field(json_schema_extra={"example": 37600.0})
    ListOfAllPropertyUseTypes: str = Field(json_schema_extra={"example": "Non-Refrigerated Warehouse, Office, Other"})
    LargestPropertyUseType: str = Field(json_schema_extra={"example": "Non-Refrigerated Warehouse"})
    LargestPropertyUseTypeGFA: float = Field(json_schema_extra={"example": 18400.0})
    SecondLargestPropertyUseType: Optional[str] = Field(default=None, json_schema_extra={"example": "Other"})
    SecondLargestPropertyUseTypeGFA: Optional[float] = Field(default=None, json_schema_extra={"example": 16200.0})
    ThirdLargestPropertyUseType: Optional[str] = Field(default=None, json_schema_extra={"example": "Office"})
    ThirdLargestPropertyUseTypeGFA: Optional[float] = Field(default=None, json_schema_extra={"example": 3000.0})
    YearsENERGYSTARCertified: Optional[int] = Field(default=None, json_schema_extra={"example": 5})
    Outlier: str = Field(json_schema_extra={"example": "No"})
    BuildingAge: float = Field(json_schema_extra={"example": 55.0})
    SurfacePerFloor: float = Field(json_schema_extra={"example": 18800.0})
    IsMultiUse: bool = Field(json_schema_extra={"example": True})
    LatZone: int = Field(json_schema_extra={"example": 3})
    LonZone: int = Field(json_schema_extra={"example": 1})


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
