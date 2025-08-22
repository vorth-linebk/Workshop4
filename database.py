import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

# Default to local SQLite for development; can be overridden by env
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# Create SQLAlchemy engine and session factory
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        future=True,
    )
else:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=3600,
        future=True,
    )

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
