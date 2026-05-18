from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Any
from datetime import datetime

# --- CONFIGURACIÓN BASE PARA ESQUEMAS FLEXIBLES ---
class FlexibleModel(BaseModel):
    model_config = ConfigDict(extra="allow", from_attributes=True)

# --- RUTAS DE CHOFERES (FALTANTES REQUERIDOS) ---
class DriverTripResponse(FlexibleModel):
    id: int

class PassengerForDriver(FlexibleModel):
    id: int

class CheckInResponse(FlexibleModel):
    status: str

class TripSummaryResponse(FlexibleModel):
    trip_id: int

# --- AUTENTICACIÓN Y USUARIOS ---
class UserLogin(BaseModel):
    phone: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserBase(BaseModel):
    phone: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_admin: bool = False
    class Config:
        from_attributes = True

# --- CAMIONETAS (VANS) ---
class VanBase(BaseModel):
    model: str
    plate: str
    capacity: int

class VanCreate(VanBase):
    pass

class VanResponse(VanBase):
    id: int
    class Config:
        from_attributes = True

# --- VIAJES (TRIPS) ---
class TripBase(BaseModel):
    destination: str
    price: float
    date: datetime

class TripCreate(TripBase):
    van_id: int

class TripResponse(TripBase):
    id: int
    van_id: int
    class Config:
        from_attributes = True

# --- RESERVAS (RESERVATIONS) ---
class ReservationBase(BaseModel):
    trip_id: int
    seats: int

class ReservationCreate(ReservationBase):
    pass

class ReservationResponse(ReservationBase):
    id: int
    user_id: int
    class Config:
        from_attributes = True
