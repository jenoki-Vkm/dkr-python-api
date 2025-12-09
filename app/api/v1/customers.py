from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.customer import Customer, CustomerCreate, CustomerUpdate, CustomerChangePwd
from app.api.deps import get_db
from app import crud
from app.core.security import hash_password

router = APIRouter()

# Get customers list endpoint
@router.get("/", response_model=List[Customer])
def read_customers(skip: int = 0, 
                   limit: int = 100, 
                   db: Session = Depends(get_db)) -> List[Customer]:
    try: 
        
        print("...Try to get customers list...")
        customers = crud.customer.get_customers(db, skip=skip, limit=limit)
        
        ''' Mocked data for illustration; replace with actual DB call
        customer = Customer(
        id=1,
        first_name="John",
        last_name="Doe",
        email="john.doe@gmail.com",
        phone_number="1234567890",
        gender="M",
        age=30
        )    
        customers = [customer]    
        '''
    except Exception as e:
        print("❌ Failed to get customers list:", e)
        customers = []
        raise HTTPException(status_code=500, detail="Internal Server Error")    
    finally:
        print("✅ Customers list retrieval attempt finished.")  
       
    return customers

# Create customer endpoint
@router.post("/create", response_model=Customer, status_code=status.HTTP_201_CREATED)
def create_customer(customer_in: CustomerCreate, db: Session = Depends(get_db)) -> Customer:
    try:
        db_customer = crud.customer.get_customer_by_email(db, email=customer_in.email)        
        if db_customer:
            raise HTTPException(status_code=400, detail="Email already registered")
        # Hash the password before storing it
        print(f"✅ pwd entered: {customer_in.pwd}") 
        hashed_pwd = hash_password(customer_in.pwd)
        # hashed_pwd = 'hashme123'  # Temporary hardcoded for testing
        print(f"✅ hashed pwd produced: {hashed_pwd}") 
        
        customer_data = customer_in.model_dump() # Convert pydantic object (python model) to dict (python dictionnary)
        customer_data.pop("pwd")                # 
        customer_data['hashed_pwd'] = hashed_pwd # Store hashed password
        print("...Try to create new customer...")
        db_customer = crud.customer.create_customer(db, customer_data=customer_data)
        return db_customer
    except HTTPException:
        raise   
    except Exception as e:
        print("❌ Failed to create customer:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")    
    finally:
        print("✅ Customer creation attempt finished.") 
        
# Get customer by ID endpoint
@router.get("/{customer_id}", response_model=Customer)
def read_customer(customer_id: int, db: Session = Depends(get_db)) -> Customer:
    try:
        print(f"...Try to get customer with ID {customer_id}...")
        db_customer = crud.customer.get_customer(db, customer_id=customer_id)
        if not db_customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        return db_customer
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Failed to get customer with ID {customer_id}:", e)   
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        print(f"✅ Customer retrieval attempt for ID {customer_id} finished.")
        
# Update customer endpoint
@router.put("/{customer_id}", response_model=Customer)
def update_customer(customer_id: int, customer_in: CustomerUpdate, db: Session = Depends(get_db)) -> Customer:
    try:
        db_customer = crud.customer.get_customer(db, customer_id=customer_id)
        if not db_customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        db_customer = crud.customer.update_customer(db, db_customer=db_customer, customer_update=customer_in)
        return db_customer  
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Failed to update customer with ID {customer_id}:", e)   
        raise HTTPException(status_code=500, detail="Internal Server Error")    
    finally:
        print(f"✅ Customer update attempt for ID {customer_id} finished.")
        
# Change password endpoint
@router.post("/{customer_id}/change-password", status_code=status.HTTP_204_NO_CONTENT)
def change_customer_password(
    customer_id: int,
    password_data: CustomerChangePwd,
    db: Session = Depends(get_db),
):
    """
    Change le mot de passe si l'ancien mot de passe est correct.
    """
    crud.customer.change_password(db=db, customer_id=customer_id, password_data=password_data)
    return  # 204 No Content        

# Delete customer endpoint
@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: int, db: Session = Depends(get_db)) -> None:   
    try:
        print(f"...Try to delete customer with ID {customer_id}...")    
        db_customer = crud.customer.get_customer(db, customer_id=customer_id)
        if not db_customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        crud.customer.delete_customer(db, db_customer=db_customer)   
        return None
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Failed to delete customer with ID {customer_id}:", e)   
        raise HTTPException(status_code=500, detail="Internal Server Error")    
    finally:
        print(f"✅ Customer deletion attempt for ID {customer_id} finished.")
        

