from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from models import UserRole, TripStatus, ReservationStatus, CheckInStatus, PaymentStatus

# ============ USER SCHEMAS ============

class UserBase(BaseModel):
    phone: str
    full_name: str
    email: Optional[str] = None

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
    token_type: str = "bearer"
    user: UserResponse

# ============ VAN SCHEMAS ============

class VanBase(BaseModel):
    brand: str
    model: Optional[str] = None
    license_plate: str
    capacity: int
    has_ac: bool = True
    has_wifi: bool = False

class VanCreate(VanBase):
    insurance_expiry: Optional[datetime] = None
    license_expiry: Optional[datetime] = None
    notes: Optional[str] = None
    photo_url: Optional[str] = None

class VanUpdate(BaseModel):
    brand: Optional[str] = None
    model: Optional[str] = None
    capacity: Optional[int] = None
    has_ac: Optional[bool] = None
    has_wifi: Optional[bool] = None
    insurance_expiry: Optional[datetime] = None
    license_expiry: Optional[datetime] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None

class VanResponse(VanBase):
    id: int
    is_active: bool
    insurance_expiry: Optional[datetime]
    license_expiry: Optional[datetime]
    photo_url: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

# ============ TRIP SCHEMAS ============

class TripBase(BaseModel):
    origin: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    price_per_seat: float
    available_seats: int
    van_id: int
    driver_id: Optional[int] = None
    pickup_points: Optional[str] = None
    notes: Optional[str] = None
    # NUEVO: Datos de distancia y combustible
    distance_km: Optional[float] = None
    fuel_consumption_per_km: Optional[float] = None
    fuel_price_per_liter: Optional[float] = None

class TripCreate(TripBase):
    is_full_rental_allowed: bool = False
    full_rental_price: Optional[float] = None

class TripUpdate(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None
    real_departure_time: Optional[datetime] = None
    real_arrival_time: Optional[datetime] = None

class TripResponse(TripBase):
    id: int
    status: str
    is_full_rental_allowed: bool
    full_rental_price: Optional[float]
    created_at: datetime
    
    class Config:
        from_attributes = True

class TripDetailResponse(TripResponse):
    van: VanResponse
    driver: Optional[UserResponse]

# ============ SEAT SCHEMAS ============

class SeatInfo(BaseModel):
    number: int
    available: bool
    status: str  # "free", "occupied", "reserved_pending"

class TripSeatsResponse(BaseModel):
    trip_id: int
    total_seats: int
    available_seats: int
    seats: List[SeatInfo]

# ============ RESERVATION SCHEMAS ============

class ReservationCreate(BaseModel):
    trip_id: int
    seat_number: Optional[int] = None
    passenger_name: str
    passenger_phone: Optional[str] = None
    passenger_email: Optional[str] = None
    is_full_rental: bool = False
    notes: Optional[str] = None

class ReservationResponse(BaseModel):
    id: int
    trip_id: int
    user_id: int
    seat_number: Optional[int]
    passenger_name: str
    passenger_phone: Optional[str]
    passenger_email: Optional[str]
    status: str
    payment_status: str
    total_price: float
    notes: Optional[str]
    is_full_rental: bool
    created_at: datetime
    confirmed_at: Optional[datetime]
    cancelled_at: Optional[datetime]
    
    class Config:
        from_attributes = True

# ============ CHECK-IN SCHEMAS ============

class CheckInCreate(BaseModel):
    reservation_id: int

class CheckInUpdate(BaseModel):
    check_in_status: Optional[str] = None
    payment_status: Optional[str] = None
    notes: Optional[str] = None

class CheckInResponse(BaseModel):
    id: int
    reservation_id: int
    check_in_status: str
    payment_status: str
    checked_in_at: Optional[datetime]
    paid_at: Optional[datetime]
    notes: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

# ============ DRIVER PANEL SCHEMAS ============

class PassengerForDriver(BaseModel):
    """Info about a passenger for the driver's view"""
    reservation_id: int
    passenger_name: str
    passenger_phone: Optional[str]
    seat_number: Optional[int]
    payment_status: str
    check_in_status: str
    total_price: float
    notes: Optional[str]

class DriverTripResponse(BaseModel):
    """Trip info for driver"""
    id: int
    origin: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    status: str
    van: VanResponse
    passengers: List[PassengerForDriver] = []
    total_confirmed_passengers: int = 0
    total_paid_passengers: int = 0
    total_unpaid_passengers: int = 0
    total_collected: float = 0.0

class TripSummaryResponse(BaseModel):
    """Summary of a completed trip"""
    trip_id: int
    origin: str
    destination: str
    departure_time: datetime
    arrival_time: Optional[datetime]
    real_departure_time: Optional[datetime]
    real_arrival_time: Optional[datetime]
    total_passengers_confirmed: int
    total_passengers_boarded: int
    total_no_shows: int
    total_amount_collected: float
    total_expected_amount: float
    
    class Config:
        from_attributes = True

# ============ ADMIN SCHEMAS ============

class AdminReservationResponse(ReservationResponse):
    user: UserResponse
    trip: TripResponse
    check_in: Optional[CheckInResponse]

class DashboardStats(BaseModel):
    trips_today: int
    pending_verification: int
    daily_income: float
    occupancy_rate: float
    total_confirmed_today: int
    upcoming_trips: List[dict]

class ExpiringDocumentInfo(BaseModel):
    type: str
    expiry_date: str
    days_left: int

class VanWithExpiringDocs(BaseModel):
    id: int
    brand: str
    model: Optional[str]
    license_plate: str
    expiring_documents: List[ExpiringDocumentInfo]

# ============ TRIP REPORT SCHEMAS ============

class TripReportResponse(BaseModel):
    """Reporte detallado del viaje con cálculos financieros"""
    id: int
    trip_id: int
    origin: str
    destination: str
    distance_km: float
    
    # Pasajeros
    total_passengers_boarded: int
    total_passengers_no_show: int
    money_collected: float
    
    # Combustible
    fuel_consumption_per_km: float
    fuel_price_per_liter: float
    total_fuel_consumed: float
    total_fuel_cost: float
    
    # Conductor y ganancia
    money_after_fuel: float
    driver_salary: float
    net_profit: float
    
    created_at: datetime
    
    class Config:
        from_attributes = True
