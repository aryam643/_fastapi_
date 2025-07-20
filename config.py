import os
from typing import Optional

class Settings:
    """Application settings and configuration"""
    
    # MongoDB Configuration
    MONGODB_URL: str = os.getenv(
        "MONGODB_URL",
        "mongodb+srv://username:password@cluster.mongodb.net/hrone_ecommerce?retryWrites=true&w=majority"
    )
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "hrone_ecommerce")
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "HROne E-commerce Backend"
    
    # Server Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"

settings = Settings()
