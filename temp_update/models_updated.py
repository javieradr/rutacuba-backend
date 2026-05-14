from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base
import enum
from datetime import datetime, timezone

# ============ ENUMS ============

class UserRole(str, enum.Enum):
    CLIENT = "client"
    ADMIN = "admin"
    DRIVER = "driver"

class TripStatus(str, enum.Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class ReservationStatus(str, enum.Enum):
    PENDING_PAYMENT = "pending_payment"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    NO_SHOW = "no_show"

class CheckInStatus(str, enum.Enum):
    PENDING = "pending"
    CHECKED_IN = "checked_in"
    NO_SHOW = "no_show"

class PaymentStatus(str, enum.Enum):
    UNPAID = "unpaid"
    PAID = "paid"

# ============ MODELS ============

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String(20), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=True)
    full_name = Column(String(200), nullable=False)
    hashed_password = Column(String(200), nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.CLIENT)
    is_active = Column(Boolean, default=True)
    created_at = Column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc)
    )
    
    # Relationships
    reservations = relationship(
        "Reservation", 
        back_populates="user",
        foreign_keys="Reservation.user_id"
    )
    trips_as_driver = relationship(
        "Trip",
        back_populates="driver",
        foreign_keys="Trip.driver_id"
    )

class Van(Base):
    __tablename__ = "vans"
    
    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String(50), nullable=False)  # Hyundai, Mercedes, etc
    model = Column(String(50), nullable=True)
    license_plate = Column(String(10), unique=True, nullable=False)
    capacity = Column(Integer, nullable=False)  # Number of seats
    has_ac = Column(Boolean, default=True)
    has_wifi = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    insurance_expiry = Column(DateTime, nullable=True)
    license_expiry = Column(DateTime, nullable=True)
    notes = Column(String(500), nullable=True)
    photo_url = Column(String(500), nullable=True)
    created_at = Column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )
    
    # Relationships
    trips = relationship("Trip", back_populates="van")

class Trip(Base):
    __tablename__ = "trips"
    
    id = Column(Integer, primary_key=True, index=True)
    origin = Column(String(100), nullable=False)
    destination = Column(String(100), nullable=False)
    departure_time = Column(DateTime, nullable=False)
    arrival_time = Column(DateTime, nullable=False)
    price_per_seat = Column(Float, nullable=False)
    available_seats = Column(Integer, nullable=False)
    status = Column(SQLEnum(TripStatus), default=TripStatus.SCHEDULED)
    is_full_rental_allowed = Column(Boolean, default=False)
    full_rental_price = Column(Float, nullable=True)
    pickup_points = Column(Text, nullable=True)  # JSON string with multiple pickup points
    notes = Column(String(500), nullable=True)
    real_departure_time = Column(DateTime, nullable=True)  # Actual departure time
    real_arrival_time = Column(DateTime, nullable=True)  # Actual arrival time
    distance_km = Column(Float, nullable=True)  # Distance traveled in KM
    created_at = Column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )
    
    # Foreign Keys
    van_id = Column(Integer, ForeignKey("vans.id"), nullable=False)
    driver_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    van = relationship("Van", back_populates="trips")
    driver = relationship("User", back_populates="trips_as_driver", foreign_keys=[driver_id])
    reservations = relationship(
        "Reservation", 
        back_populates="trip",
        cascade="all, delete-orphan"
    )
    trip_report = relationship(
        "TripReport",
        back_populates="trip",
        uselist=False,
        cascade="all, delete-orphan"
    )

class Reservation(Base):
    __tablename__ = "reservations"
    
    id = Column(Integer, primary_key=True, index=True)
    seat_number = Column(Integer, nullable=True)  # NULL if full rental
    passenger_name = Column(String(200), nullable=False)
    passenger_phone = Column(String(20), nullable=True)
    passenger_email = Column(String(100), nullable=True)
    status = Column(
        SQLEnum(ReservationStatus), 
        default=ReservationStatus.PENDING_PAYMENT
    )
    payment_status = Column(
        SQLEnum(PaymentStatus),
        default=PaymentStatus.UNPAID
    )
    total_price = Column(Float, nullable=False)
    notes = Column(String(500), nullable=True)
    is_full_rental = Column(Boolean, default=False)
    created_at = Column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc)
    )
    confirmed_at = Column(DateTime, nullable=True)
    cancelled_at = Column(DateTime, nullable=True)
    
    # Foreign Keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    
    # Relationships
    user = relationship(
        "User", 
        back_populates="reservations",
        foreign_keys=[user_id]
    )
    trip = relationship(
        "Trip", 
        back_populates="reservations",
        foreign_keys=[trip_id]
    )
    check_in = relationship(
        "CheckIn",
        back_populates="reservation",
        uselist=False,
        cascade="all, delete-orphan"
    )

class CheckIn(Base):
    __tablename__ = "check_ins"
    
    id = Column(Integer, primary_key=True, index=True)
    check_in_status = Column(SQLEnum(CheckInStatus), default=CheckInStatus.PENDING)
    payment_status = Column(
        SQLEnum(PaymentStatus),
        default=PaymentStatus.UNPAID
    )
    checked_in_at = Column(DateTime, nullable=True)  # When passenger boarded
    paid_at = Column(DateTime, nullable=True)  # When payment was received
    paid_by_driver = Column(Boolean, default=False)  # Was payment registered by driver
    notes = Column(String(500), nullable=True)  # Driver notes about this passenger
    created_at = Column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )
    
    # Foreign Key
    reservation_id = Column(Integer, ForeignKey("reservations.id"), nullable=False)
    
    # Relationship
    reservation = relationship("Reservation", back_populates="check_in")

class TripReport(Base):
    """Financial report for completed trips"""
    __tablename__ = "trip_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Trip Info
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    
    # Distance and Fuel
    distance_km = Column(Float, nullable=False)  # Kilometers traveled
    fuel_consumption_rate = Column(Float, nullable=False)  # Kilometers per liter
    fuel_price_per_liter = Column(Float, nullable=False)  # Price per liter
    total_fuel_liters = Column(Float, nullable=False)  # Total liters consumed
    fuel_cost = Column(Float, nullable=False)  # Total fuel cost
    
    # Passengers and Revenue
    total_passengers_confirmed = Column(Integer, default=0)
    total_passengers_boarded = Column(Integer, default=0)
    total_no_shows = Column(Integer, default=0)
    total_revenue_collected = Column(Float, default=0.0)  # Money from passengers
    
    # Expenses
    driver_commission = Column(Float, default=0.0)  # 15% of revenue after fuel
    driver_commission_percentage = Column(Float, default=15.0)
    
    # Net Profit
    net_profit = Column(Float, default=0.0)  # Final profit after all expenses
    
    # Timestamps
    created_at = Column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc)
    )
    
    # Relationship
    trip = relationship("Trip", back_populates="trip_report")
    
    def calculate_fuel_cost(self):
        """Calculate fuel cost based on distance"""
        liters_needed = self.distance_km / self.fuel_consumption_rate
        cost = liters_needed * self.fuel_price_per_liter
        return round(cost, 2)
    
    def calculate_driver_commission(self):
        """Calculate driver commission (15% after fuel cost)"""
        available_after_fuel = self.total_revenue_collected - self.fuel_cost
        commission = available_after_fuel * (self.driver_commission_percentage / 100)
        return round(commission, 2)
    
    def calculate_net_profit(self):
        """Calculate net profit"""
        profit = self.total_revenue_collected - self.fuel_cost - self.driver_commission
        return round(profit, 2)
