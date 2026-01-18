"""Database initialization script to create tables and seed initial data."""

import sys
from sqlalchemy import text
from app.core.database import engine, Base
from app.models import EnergyPrediction


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
            # For SQLite
            elif "sqlite" in str(engine.url):
                conn.execute(text("DELETE FROM sqlite_sequence WHERE name='energy_predictions'"))
            conn.commit()
    except Exception as e:
        print(f"⚠️  Warning when resetting sequence: {e}")
    
    print("✅ Database tables created successfully!")


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
