# app/core/security.py
# utilitaire de hash pour mot de passe
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    print(f"🔐 Hashing password: {password}")
    print("DEBUG hash_password:", type(password), repr(password), "len =", len(password))
    return pwd_context.hash(password)
