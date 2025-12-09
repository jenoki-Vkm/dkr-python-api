# app/models/cust_contact.py
# ORM (Object-Relational Mapping). Define the database table structure for customer contact information.
# Mapping a database table named "address" to a Python class using SQLAlchemy.

from sqlalchemy import Column, Integer, String, Boolean
from app.db.base import Base

class CustAddress(Base):
    __tablename__ = "client_contact"

    # Define table columns with appropriate name, data types and constraints
    client_id = Column(Integer, primary_key=True, index=True)
    address_type = Column(String(50), primary_key=True, index=True, nullable=False)    
    phone_number = Column(String(50), unique=True, index=True, nullable=True)    
    address_line1 = Column(String(255), nullable=False)
    address_line2 = Column(String(255), nullable=False)    
    city = Column(String(100), nullable=False)    
    zip_code = Column(String(20), nullable=False)
    country = Column(String(100), nullable=False)
    
    
    