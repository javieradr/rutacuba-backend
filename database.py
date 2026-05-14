import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Buscamos la URL de Neon en las variables de entorno
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# 2. Si no hay variable (porque estás en local), usamos SQLite temporalmente
if not SQLALCHEMY_DATABASE_URL:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# 3. Ajuste para compatibilidad de SQLAlchemy con URLs antiguas de Postgres
if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 4. Configuración del motor (Engine)
# Si es SQLite, necesitamos el argumento especial, si es Postgres (Neon) no.
if "sqlite" in SQLALCHEMY_DATABASE_URL:
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
