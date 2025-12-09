# app/models/customer.py
from sqlalchemy import Column, Integer, String, Boolean
from app.db.base import Base

class Customer(Base):
    __tablename__ = "client"

    # Define table columns with appropriate name, data types and constraints
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_pwd = Column(String(255), nullable=False)
    firstname = Column(String(255), nullable=False)
    lastname = Column(String(255), nullable=False)    
    gender = Column(String(1), unique=True, index=True, nullable=False)
    age = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False)
    
