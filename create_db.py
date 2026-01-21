"""Database initialization script to create tables and seed initial data."""

import sys
import pandas as pd
from pathlib import Path
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.core.database import engine, Base
from app.models import EnergyDataset, EnergyPrediction


def load_test_dataset():
    """Load X_test.csv into the database."""
    print("📊 Loading X_test.csv into database...")
    
    test_file = Path("data/X_test.csv")
    if not test_file.exists():
        print(f"⚠️  {test_file} not found, skipping dataset load")
        return
    
    df = pd.read_csv(test_file)
    
    with Session(engine) as session:
        # Check if already loaded
        existing = session.query(EnergyDataset).count()
        if existing > 0:
            print(f"✅ Dataset already loaded ({existing} records)")
            return
        
        # Insert all rows
        for _, row in df.iterrows():
            dataset_record = EnergyDataset(
                building_type=row.get("BuildingType", ""),
                primary_property_type=row.get("PrimaryPropertyType", ""),
                zip_code=int(row.get("ZipCode", 0)),
                council_district_code=int(row.get("CouncilDistrictCode", 0)),
                neighborhood=row.get("Neighborhood", ""),
                latitude=float(row.get("Latitude", 0)),
                longitude=float(row.get("Longitude", 0)),
                year_built=int(row.get("YearBuilt", 0)),
                number_of_buildings=int(row.get("NumberofBuildings", 1)),
                number_of_floors=int(row.get("NumberofFloors", 0)),
                property_gfa_total=float(row.get("PropertyGFATotal", 0)),
                property_gfa_parking=float(row.get("PropertyGFAParking", 0)),
                property_gfa_buildings=float(row.get("PropertyGFABuildings", 0)),
                list_of_all_property_use_types=row.get("ListOfAllPropertyUseTypes", ""),
                largest_property_use_type=row.get("LargestPropertyUseType", ""),
                largest_property_use_type_gfa=float(row.get("LargestPropertyUseTypeGFA", 0)),
                second_largest_property_use_type=row.get("SecondLargestPropertyUseType"),
                second_largest_property_use_type_gfa=row.get("SecondLargestPropertyUseTypeGFA"),
                third_largest_property_use_type=row.get("ThirdLargestPropertyUseType"),
                third_largest_property_use_type_gfa=row.get("ThirdLargestPropertyUseTypeGFA"),
                years_energystar_certified=int(row.get("YearsENERGYSTARCertified", 0)),
                outlier=row.get("Outlier", ""),
                building_age=float(row.get("BuildingAge", 0)),
                surface_per_floor=float(row.get("SurfacePerFloor", 0)),
                is_multi_use=int(row.get("IsMultiUse", 0)),
                lat_zone=int(row.get("LatZone", 0)),
                lon_zone=int(row.get("LonZone", 0)),
            )
            session.add(dataset_record)
        
        session.commit()
        print(f"✅ Loaded {len(df)} records into energy_dataset")


def create_database():
    """Create all database tables."""
    print("🔄 Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    # Reset sequence to start from 1 (for PostgreSQL and SQLite)
    try:
        with engine.connect() as conn:
            # For PostgreSQL
            if "postgresql" in str(engine.url):
                conn.execute(text("ALTER SEQUENCE energy_predictions_id_seq RESTART WITH 1"))
                conn.execute(text("ALTER SEQUENCE energy_dataset_id_seq RESTART WITH 1"))
            # For SQLite
            elif "sqlite" in str(engine.url):
                conn.execute(text("DELETE FROM sqlite_sequence WHERE name='energy_predictions'"))
                conn.execute(text("DELETE FROM sqlite_sequence WHERE name='energy_dataset'"))
            conn.commit()
    except Exception as e:
        print(f"⚠️  Warning when resetting sequence: {e}")
    
    print("✅ Database tables created successfully!")
    
    # Load test dataset
    load_test_dataset()


def drop_database():
    """Drop all database tables (use with caution)."""
    print("⚠️  Dropping all database tables...")
    Base.metadata.drop_all(bind=engine)
    print("✅ Database tables dropped successfully!")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "drop":
        drop_database()
    else:
        create_database()
