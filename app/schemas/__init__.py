# Expose Pydantic schemas
from .customer import (Customer, CustomerCreate, CustomerUpdate, CustomerInDB)

__all__ = ["Customer", "CustomerCreate", "CustomerUpdate", "CustomerInDB"]
