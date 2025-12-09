# app/core/config.py
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Customer API"
    API_V1_STR: str = "/api/v1" 
    POSTGRES_SERVER: str = "dbpostgres16" # Si on passe par un réseau externe il faut mettre le nom du container postgres et nom le nom du service
    POSTGRES_PORT: str = "5432"
    POSTGRES_USER: str = "admin"
    POSTGRES_PASSWORD: str = "admin"
    POSTGRES_DB: str = "myshop_db"

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    class Config:
        env_file = ".env"

settings = Settings()
