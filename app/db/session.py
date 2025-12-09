# app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

DATABASE_URL = settings.SQLALCHEMY_DATABASE_URI

try:
    # Test the database connection
    engine = create_engine(
        DATABASE_URL,
        future=True,
        pool_pre_ping=True  # test the connection before each request
    )
    logger.info("Database connection successful.")
except OperationalError as exc:
    logger.error(f"Database connection failed, cannot create SQLAlchemy engine: {exc}")
    raise RuntimeError("Could not connect to the database") from exc
    


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True
)
