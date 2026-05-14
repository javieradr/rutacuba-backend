from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import models, routers_auth, routers_trips, routers_reservations
import os

# INSTRUCCIÓN CLAVE: Crea las tablas en Neon al arrancar
try:
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas sincronizadas con la base de datos.")
except Exception as e:
    print(f"❌ Error sincronizando tablas: {e}")

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
    return {"status": "online", "database": "connected"}
