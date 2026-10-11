import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models.db_models import Base

# Locate the backend project directory
BACKEND_DIR = Path(__file__).resolve().parent.parent

# Store the database inside the backend/data folder
DATA_DIR = BACKEND_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_SQLITE_PATH = DATA_DIR / "scheduler.db"

# Allow PostgreSQL or another configured database through DATABASE_URL
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{DEFAULT_SQLITE_PATH.as_posix()}"
)

# SQLite connection settings
connect_args = (
    {"check_same_thread": False}
    if DATABASE_URL.startswith("sqlite")
    else {}
)

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def init_db():
    """Create database tables if they don't already exist."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Provide a database session to FastAPI endpoints."""
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()