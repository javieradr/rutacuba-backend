from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./rutacuba.db"
    
    # JWT Authentication
    SECRET_KEY: str = "cambia-esta-clave-por-una-muy-segura-y-larga-2024"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    
    # Frontend URL
    FRONTEND_URL: str = "http://localhost:3000"
    
    # Twilio WhatsApp Configuration
    TWILIO_ACCOUNT_SID: str = "tu_account_sid_aqui"
    TWILIO_AUTH_TOKEN: str = "tu_auth_token_aqui"
    TWILIO_WHATSAPP_FROM: str = "whatsapp:+1234567890"
    ADMIN_WHATSAPP_NUMBER: str = "whatsapp:+53119975"
    
    # Trip Configuration
    DEFAULT_FUEL_CONSUMPTION_KM: float = 0.08  # Litros por km
    DEFAULT_FUEL_PRICE: float = 1.50  # Precio por litro
    DRIVER_COMMISSION_PERCENTAGE: float = 15.0  # 15% after fuel cost
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
