from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# --- USUARIOS ---
class UserBase(BaseModel):
    phone: str
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    phone: str
    password: str

class UserResponse(UserBase):
    id: int
    role: str
    is_active: bool
    created_at: datetime
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

# --- VIAJES (TRIPS) ---
class TripBase(BaseModel):
    origin: str
    destination: str
    departure_time: datetime
    price: float
    van_id: int

class TripCreate(TripBase):
    pass

class TripResponse(TripBase):
    id: int
    available_seats: int
    status: str
    class Config:
        from_attributes = True

# Esta es la que faltaba:
class TripDetailResponse(TripResponse):
    pass

# --- ASIENTOS Y RESERVAS ---
class SeatInfo(BaseModel):
    seat_number: int
    is_occupied: bool

class TripSeatsResponse(BaseModel):
    trip_id: int
    seats: List[SeatInfo]

class ReservationCreate(BaseModel):
    trip_id: int
    seat_numbers: List[int]

class ReservationResponse(BaseModel):
    id: int
    user_id: int
    trip_id: int
    seat_numbers: List[int]
    total_price: float
    status: str
    created_at: datetime
    class Config:
        from_attributes = True
