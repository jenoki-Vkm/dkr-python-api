#  from ctypes import Union
# app/main.py
from fastapi import FastAPI
from app.core.config import settings
from app.api.v1 import customers
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from app.db.session import engine

'''
import debugpy
debugpy.listen(("0.0.0.0", 5678))
debugpy.wait_for_client()

app = FastAPI()
# r = redis.Redis(host="redis", port=6379)

@app.get("/")
def read_root():
    return {"Bonjour":"Comment allez vous ??"}

@app.get("/hits")
def getHits():
    r.incr("hits")
    return {"Nb of hits": r.get("hits")}
    

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
'''


app = FastAPI(title=settings.PROJECT_NAME)

@app.on_event("startup")
def test_db_connection():
    try:
        print("...Try to connect to the database...")
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("🔌 DB connexion OK")
    except OperationalError:
        print("❌ Impossible de se connecter à la base au démarrage")
        # Optionnel : raise pour stopper le service
        # raise

app.include_router(
    customers.router,
    prefix=f"{settings.API_V1_STR}/customers",
    tags=["customers"],
)

# Fournir une route racine simple
@app.get("/")
def root():
    return {
        "message": "API client en ligne",   # Simple message to indicate the API is running
        "docs": "/docs",                    # Swagger UI
        "redoc": "/redoc",                  # ReDoc
        "customers": f"{settings.API_V1_STR}/customers",    # Customers endpoint
    }

# Si tu veux un petit health check :
@app.get("/health")
def health_check():
    return {"status": "ok"}
    