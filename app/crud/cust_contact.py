from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.cust_contact import CustContact as CustContactModel
from app.schemas.cust_contact import CustContactCreate, CustContactUpdate

def get_custContact(db: Session, customer_id: int, address_type: str) -> Optional[CustContactModel]:
    return db.query(CustContactModel).filter(CustContactModel.id == customer_id and CustContactModel.address_type == address_type).first()

def get_custContactss(db: Session, skip: int = 0, limit: int = 100) -> List[CustContactModel]:
    return db.query(CustContactModel).offset(skip).limit(limit).all()

def create_customer(db: Session, custContact: CustContactCreate) -> CustContactModel:
    db_custContact = CustContactModel (
        client_id=custContact.client_id,
        address_type=custContact.address_type,
        phone_number=custContact.phone_number,
        address_line1=custContact.address_line1,
        address_line2=custContact.address_line2,
        city=custContact.city,
        zip_code=custContact.zip_code,
        country=custContact.country
        """ hashed_password=customer.password  # In a real app, hash the password! """
    )
    db.add(db_custContact)
    db.commit()
    db.refresh(db_custContact)
    return db_custContact

def update_customer(db: Session, db_custContact: CustContactModel, custContact_update: CustContactUpdate) -> CustContactModel:
    for var, value in vars(custContact_update).items():
        if value is not None:
            setattr(db_custContact, var, value)
    db.commit()
    db.refresh(db_custContact)
    return db_custContact

def delete_customer(db: Session, db_custContact: CustContactModel) -> None:
    db.delete(db_custContact)
    db.commit() 
    
def get_customer_by_email(db: Session, email: str) -> Optional[CustContactModel]:
    return db.query(CustContactModel).filter(CustContactModel.email == email).first() 

def get_customer_by_phone(db: Session, phone_number: str) -> Optional[CustContactModel]:
    return db.query(CustContactModel).filter(CustContactModel.phone_number == phone_number).first()