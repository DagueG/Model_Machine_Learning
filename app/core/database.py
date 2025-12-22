"""Database configuration and session management."""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool

# Database URL from environment
# Auto-detect: use SQLite if no DATABASE_URL or on HF Spaces, else PostgreSQL
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    None
)

# If no DATABASE_URL set, use SQLite (for HF Spaces or offline dev)
if not DATABASE_URL:
    # Use SQLite with absolute path (works on HF Spaces)
    DATABASE_URL = "sqlite:////tmp/predictions.db"
    # For Windows local dev, use relative path
    if os.name == 'nt':
        DATABASE_URL = "sqlite:///./predictions.db"

# Create engine with appropriate settings for SQLite or PostgreSQL
if "sqlite" in DATABASE_URL:
    # SQLite-specific settings
    engine = create_engine(
        DATABASE_URL,
        echo=False,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    # PostgreSQL-specific settings
    engine = create_engine(
        DATABASE_URL,
        echo=False,
        pool_pre_ping=True,  # Verify connections before using
    )

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """Dependency for getting database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
