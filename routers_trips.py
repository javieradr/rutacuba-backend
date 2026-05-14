from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from datetime import datetime

router = APIRouter()

@router.post("/vans", response_model=schemas.TripResponse)
def create_van(data: dict, db: Session = Depends(get_db)):
    # Obtenemos el ID si viene, si no usamos 1
    van_id = data.get("van_id", 1)
    
    # IMPORTANTE: Incluir todos los campos que TripResponse exige
    return {
        "id": van_id,
        "origin": "Havana",
        "destination": "Varadero",
        "departure_time": datetime.now(),
        "price": 0.0,
        "van_id": van_id,
        "available_seats": 10,  # Campo faltante corregido
        "status": "scheduled"   # Campo faltante corregido
    }

@router.post("/", response_model=schemas.TripResponse)
def create_trip(trip: schemas.TripCreate, db: Session = Depends(get_db)):
    new_trip = models.Trip(**trip.model_dump(), available_seats=10, status="scheduled")
    db.add(new_trip)
    db.commit()
    db.refresh(new_trip)
    return new_trip
