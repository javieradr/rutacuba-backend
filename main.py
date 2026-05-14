from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import models
# Importamos todos los archivos que encontramos en tu carpeta
import routers_auth, routers_trips, routers_reservations, routers_admin, routers_driver, routers_vans

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

# Registramos cada router para que aparezca en Swagger (/docs)
app.include_router(routers_auth.router, prefix="/auth", tags=["Autenticación"])
app.include_router(routers_trips.router, prefix="/trips", tags=["Viajes"])
app.include_router(routers_reservations.router, prefix="/reservations", tags=["Reservas"])
app.include_router(routers_admin.router, prefix="/admin", tags=["Administración"])
app.include_router(routers_driver.router, prefix="/driver", tags=["Choferes"])
app.include_router(routers_vans.router, prefix="/vans", tags=["Camionetas"])

@app.get("/")
def root():
    return {"status": "online", "database": "connected"}
