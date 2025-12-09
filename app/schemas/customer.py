# Pydantic schemas for Customer entity
# app/schemas/customer.py
# Use to define data validation and serialization for Customer-related operations.
# format send to client and receive from client
#prevent to expose ORM models directly such as encrypted password, etc ...
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

'''
✔️ CustomerInDBBase
Contient :
ce que contient l’objet SQLAlchemy
donc y compris le champ pwd (souvent sous forme hashée)
Il sert à mapper SQLAlchemy → Pydantic.

✔️ CustomerInDB: Est généralement utilisé en interne uniquement pour manipuler les objets venant de la base.
Il n’est pas exposé dans les réponses API.
✔️ Customer: Est ce que l’API renvoie → et ne doit PAS contenir de champs sensibles.

Pourquoi mettre pwd dans CustomerInDBBase et pas ailleurs ?
Parce que : pwd est nécessaire en interne (pour stocker, comparer, hasher)
mais interdit d’être exposé dans l’API
Donc on fait : 
-- Modele interne (pour la base)
class CustomerInDBBase(CustomerBase):
    pwd: str

-- Modèle public (pour les réponses API)
class Customer(CustomerInDBBase):
    pass

'''
# CustomerBase sert plutôt à décrire les champs métiers (sans id, sans champs techniques).
# CustomerBase = ce que l’API publique peut recevoir/envoyer, donc ne doit pas contenir de champs sensibles comme pwd
class CustomerBase(BaseModel):         
    email: EmailStr    
    firstname: str 
    lastname: str
    gender: str
    age: int
    is_active: bool    
    
class CustomerCreate(CustomerBase):  
    username: str  
    pwd: str # mot de passe en clair lors de la création
        
class CustomerUpdate(CustomerBase):    
    email: Optional[EmailStr] = None    
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    is_active: Optional[bool] = None        

class CustomerChangePwd(BaseModel):
    old_pwd: str # mot de passe en clair lors de la mise à jour
    new_pwd: str # mot de passe en clair lors de la mise à jour
        
# CustomerInDBBase (ce que la base contient y compris pwd hashé) hérite de CustomerBase et ajoute les champs techniques (id, etc ...)    
# contient l’objet SQLAlchemy donc y compris le champ "pwd", la bonne pratique est de hasher le mot de passe avant de le stocker dans la base
# Il sert à mapper SQLAlchemy → Pydantic.
class CustomerInDBBase(CustomerBase):
    id: int
    hashed_pwd: str    # mot de passe hashé dans la base
    model_config = ConfigDict(from_attributes=True) # permet à Pydantic de transformer un objet SQLAlchemy en modèle Pydantic :
                                                    # Sans ça → Pydantic ne sait traiter que des dicts.
                                                    # Avec ça → Pydantic peut lire :
                                                            # customer.id
                                                            # customer.email
                                                            # customer.firstname
    # class Config:
    #  orm_mode = True

# Customer est ce que la réponse de l'API renvoie (donc hérite de CustomerInDBBase SANS pwd)
class Customer(CustomerBase):
    id: int # renvoyé dans l'API
    hashed_pwd: str # renvoyé dans l'API
    pass

# CustomerInDB est généralement utilisé en interne uniquement pour manipuler les objets venant de la base
# Il n’est pas exposé dans les réponses API.
# Modèle interne (optionnel) qui inclut le hash
class CustomerInDB(CustomerInDBBase):
    hashed_pwd: str
    
