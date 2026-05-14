from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# Auth & User
class UserBase(BaseModel):
    phone: str
class UserCreate(UserBase):
    password: str
class UserResponse(UserBase):
    id: int
    is_admin: bool = False
    class Config:
        from_attributes = True

# Camionetas (Vans)
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

# Viajes (Trips)
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

# Reservas (Reservations)
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
