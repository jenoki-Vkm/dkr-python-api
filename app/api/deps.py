# Dependance FastAPI pour obtenir une session de base de données
from typing import Generator

# Manage exceptions during DB session creation
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from app.db.session import SessionLocal
import logging


logger = logging.getLogger(__name__)


def get_db() -> Generator:
    
    try: # ensure the database session is closed after use
        db = SessionLocal()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Could not connect to the database"
        ) from e
                                
    try:
        yield db    
    except OperationalError as oe:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database operational error"
        ) from oe
    finally:
        db.close()