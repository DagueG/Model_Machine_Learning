"""SQLAlchemy models for database tables."""

from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime, JSON
from app.core.database import Base


class EnergyPrediction(Base):
    """Model for storing energy consumption predictions."""
    
    __tablename__ = "energy_predictions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Input features (stored as JSON for flexibility)
    building_type = Column(String, nullable=False)
    primary_property_type = Column(String, nullable=False)
    zip_code = Column(Integer, nullable=False)
    council_district_code = Column(Integer, nullable=False)
    neighborhood = Column(String, nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    year_built = Column(Integer, nullable=False)
    number_of_buildings = Column(Integer, nullable=False)
    number_of_floors = Column(Integer, nullable=False)
    property_gfa_total = Column(Float, nullable=False)
    property_gfa_parking = Column(Float, nullable=False)
    property_gfa_buildings = Column(Float, nullable=False)
    list_of_all_property_use_types = Column(String, nullable=True)
    largest_property_use_type = Column(String, nullable=False)
    largest_property_use_type_gfa = Column(Float, nullable=False)
    second_largest_property_use_type = Column(String, nullable=True)
    second_largest_property_use_type_gfa = Column(Float, nullable=True)
    third_largest_property_use_type = Column(String, nullable=True)
    third_largest_property_use_type_gfa = Column(Float, nullable=True)
    years_energystar_certified = Column(Integer, nullable=False)
    outlier = Column(String, nullable=False)
    building_age = Column(Float, nullable=False)
    surface_per_floor = Column(Float, nullable=False)
    is_multi_use = Column(Integer, nullable=False)  # Boolean stored as int
    lat_zone = Column(Integer, nullable=False)
    lon_zone = Column(Integer, nullable=False)
    
    # Prediction output
    prediction = Column(Float, nullable=False)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<EnergyPrediction(id={self.id}, prediction={self.prediction}, created_at={self.created_at})>"
