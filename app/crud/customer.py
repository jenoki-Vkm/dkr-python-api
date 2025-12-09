# app/crud/customer.py

from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.customer import Customer as CustomerModel
from app.schemas.customer import CustomerCreate, CustomerUpdate, CustomerChangePwd
from app.core.security import verify_password, hash_password

def get_customer(db: Session, customer_id: int) -> Optional[CustomerModel]:
    return db.query(CustomerModel).filter(CustomerModel.id == customer_id).first()

def get_customers(db: Session, skip: int = 0, limit: int = 100) -> List[CustomerModel]:
    return db.query(CustomerModel).offset(skip).limit(limit).all()

def create_customer(db: Session, customer_data: dict) -> CustomerModel:
    print("🔐 create_customer with data:", customer_data)
    db_customer = CustomerModel(**customer_data)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    print("✅ Customer created with ID:", db_customer.id)
    return db_customer  

def update_customer(db: Session, db_customer: CustomerModel, customer_update: CustomerUpdate) -> CustomerModel:
    for var, value in vars(customer_update).items():
        if value is not None:
            setattr(db_customer, var, value)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def change_password(
    db: Session,
    customer_id: int,
    password_data: CustomerChangePwd,
) -> None:
    # 1. Récupérer le client
    customer = db.query(CustomerModel).filter(CustomerModel.id == customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    # 2. Vérifier l'ancien mot de passe
    if not verify_password(password_data.old_pwd, customer.hashed_pwd):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ancien mot de passe incorrect.",
        )

    # 3. Mettre à jour avec le nouveau mot de passe (hashé)
    customer.hashed_pwd = hash_password(password_data.new_pwd)
    db.add(customer)
    db.commit()

def delete_customer(db: Session, db_customer: CustomerModel) -> None:
    db.delete(db_customer)
    db.commit() 
    
def get_customer_by_email(db: Session, email: str) -> Optional[CustomerModel]:
    print(f"🔍 Searching for customer with email: {email}")
    return db.query(CustomerModel).filter(CustomerModel.email == email).first() 

def get_customer_by_phone(db: Session, phone_number: str) -> Optional[CustomerModel]:
    return db.query(CustomerModel).filter(CustomerModel.phone_number == phone_number).first()

