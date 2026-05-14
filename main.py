from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base, SessionLocal
import models, routers_auth, routers_trips, routers_reservations
from security import get_password_hash
import os

# Crear tablas al iniciar
Base.metadata.create_all(bind=engine)

# Lógica de Auto-Admin (Solo si no existe)
db = SessionLocal()
try:
    admin_exists = db.query(models.User).filter(models.User.phone == "5350000000").first()
    if not admin_exists:
        admin_user = models.User(
            phone="5350000000",
            email="admin@rutacuba.com",
            full_name="Admin Sistema",
            hashed_password=get_password_hash("admin"),
            role="ADMIN"
        )
        db.add(admin_user)
        db.commit()
finally:
    db.close()

app = FastAPI(title="RutaCuba API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routers_auth.router, prefix="/auth")
app.include_router(routers_trips.router, prefix="/trips")
app.include_router(routers_reservations.router, prefix="/reservations")
app.include_router(routers_trips.router, prefix="/admin")

@app.get("/")
def root():
    return {"message": "RutaCuba API funcionando en Vercel", "docs": "/docs"}

# Importante para Vercel
export_app = app
