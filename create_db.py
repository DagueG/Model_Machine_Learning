"""Database initialization script to create tables and seed initial data."""

import sys
from app.core.database import engine, Base
from app.models import EnergyPrediction


def create_database():
    """Create all database tables."""
    print("🔄 Creating database tables...")
    Base.metadata.create_all(bind=engine)
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
