# Exposer les principales sous-packages de l'application: "api", "core", "crud", "db", "models", "schemas"
# --- IGNORE ---
'''
from app.api import api_v1
from app.db import base  # Importer les modèles de base pour la création des tables 
'''
# --- IGNORE END ---
from . import api
from . import core
from . import crud
from . import db
from . import models
from . import schemas

__all__ = ["api", "core", "crud", "db", "models", "schemas"]


