from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# Esquemas para Camionetas (Vans) - LO QUE FALTABA
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

# Esquemas de Usuario / Auth
class UserBase(BaseModel):
    phone: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_admin: bool = False
    class Config:
        from_attributes = True

# Añade aquí otros esquemas que uses (TripCreate, ReservationCreate, etc.)
