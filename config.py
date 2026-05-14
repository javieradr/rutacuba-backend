from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Usa exactamente la clave que tu sistema esperaba antes
    SECRET_KEY: str = "cambiame_por_algo_seguro" 
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    DATABASE_URL: str = "sqlite:///./rutacuba.db"

    class Config:
        env_file = ".env"
        extra = "allow"

def get_settings():
    return Settings()

settings = get_settings()
