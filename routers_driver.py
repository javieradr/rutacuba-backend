from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timezone, timedelta
from database import get_db
from models import Trip, TripStatus, Reservation, ReservationStatus, CheckIn, CheckInStatus, User, PaymentStatus
from schemas import DriverTripResponse, PassengerForDriver, CheckInResponse, TripSummaryResponse
from dependencies import get_current_user, get_driver_user
from services import CheckInService, TripService

router = APIRouter(prefix="/driver", tags=["Conductor"])

@router.get("/my-trips-today")
def get_today_trips(
    db: Session = Depends(get_db),
    driver: User = Depends(get_driver_user)
):
    """Get trips for today"""
    
    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow = today + timedelta(days=1)
    
    trips = db.query(Trip).filter(
        Trip.driver_id == driver.id,
        Trip.departure_time >= today,
        Trip.departure_time < tomorrow,
        Trip.status != TripStatus.CANCELLED
    ).order_by(Trip.departure_time).all()
    
    result = []
    for trip in trips:
        reservations = db.query(Reservation).filter(
            Reservation.trip_id == trip.id,
            Reservation.status != ReservationStatus.CANCELLED
        ).all()
        
        confirmed = sum(1 for r in reservations if r.status == ReservationStatus.CONFIRMED)
        paid = sum(1 for r in reservations if r.check_in and r.check_in.payment_status == PaymentStatus.PAID)
        collected = sum(r.total_price for r in reservations if r.check_in and r.check_in.payment_status == PaymentStatus.PAID)
        
        result.append({
            "id": trip.id,
            "origin": trip.origin,
            "destination": trip.destination,
            "departure_time": trip.departure_time,
            "arrival_time": trip.arrival_time,
            "status": trip.status.value,
            "van": {
                "brand": trip.van.brand,
                "model": trip.van.model,
                "license_plate": trip.van.license_plate,
                "capacity": trip.van.capacity
            },
            "total_confirmed": confirmed,
            "total_paid": paid,
            "total_collected": collected
        })
    
    return result

@router.get("/my-upcoming-trips")
def get_upcoming_trips(
    days: int = Query(7, ge=1, le=30),
    db: Session = Depends(get_db),
    driver: User = Depends(get_driver_user)
):
    """Get upcoming trips for the next N days"""
    
    now = datetime.now(timezone.utc)
    future = now + timedelta(days=days)
    
    trips = db.query(Trip).filter(
        Trip.driver_id == driver.id,
        Trip.departure_time >= now,
        Trip.departure_time <= future,
        Trip.status != TripStatus.CANCELLED
    ).order_by(Trip.departure_time).all()
    
    result = []
    for trip in trips:
        reservations = db.query(Reservation).filter(
            Reservation.trip_id == trip.id,
            Reservation.status != ReservationStatus.CANCELLED
        ).all()
        
        confirmed = sum(1 for r in reservations if r.status == ReservationStatus.CONFIRMED)
        
        result.append({
            "id": trip.id,
            "origin": trip.origin,
            "destination": trip.destination,
            "departure_time": trip.departure_time,
            "status": trip.status.value,
            "total_confirmed": confirmed
        })
    
    return result

@router.get("/trip/{trip_id}/detail")
def get_trip_detail_for_driver(
    trip_id: int,
    db: Session = Depends(get_db),
    driver: User = Depends(get_driver_user)
):
    """Get detailed info about a trip"""
    
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    
    if not trip:
        raise HTTPException(status_code=404, detail="Viaje no encontrado")
    
    if trip.driver_id != driver.id:
        raise HTTPException(status_code=403, detail="No eres el conductor de este viaje")
    
    reservations = db.query(Reservation).filter(
        Reservation.trip_id == trip_id,
        Reservation.status != ReservationStatus.CANCELLED
    ).all()
    
    passengers = []
    for reservation in reservations:
        check_in = reservation.check_in
        passengers.append(PassengerForDriver(
            reservation_id=reservation.id,
            passenger_name=reservation.passenger_name,
            passenger_phone=reservation.passenger_phone,
            seat_number=reservation.seat_number,
            payment_status=reservation.payment_status.value,
            check_in_status=check_in.check_in_status.value if check_in else CheckInStatus.PENDING.value,
            total_price=reservation.total_price,
            notes=reservation.notes
        ))
    
    total_confirmed = sum(1 for r in reservations if r.status == ReservationStatus.CONFIRMED)
    total_paid = sum(1 for r in reservations if r.check_in and r.check_in.payment_status == PaymentStatus.PAID)
    total_unpaid = total_confirmed - total_paid
    total_collected = sum(r.total_price for r in reservations if r.check_in and r.check_in.payment_status == PaymentStatus.PAID)
    
    return {
        "trip": {
            "id": trip.id,
            "origin": trip.origin,
            "destination": trip.destination,
            "departure_time": trip.departure_time,
            "arrival_time": trip.arrival_time,
            "status": trip.status.value,
            "pickup_points": trip.pickup_points,
            "notes": trip.notes
        },
        "van": {
            "brand": trip.van.brand,
            "model": trip.van.model,
            "license_plate": trip.van.license_plate,
            "capacity": trip.van.capacity,
            "has_ac": trip.van.has_ac,
            "has_wifi": trip.van.has_wifi
        },
        "passengers": passengers,
        "summary": {
            "total_confirmed": total_confirmed,
            "total_paid": total_paid,
            "total_unpaid": total_unpaid,
            "total_collected": total_collected
        }
    }

@router.post("/trip/{trip_id}/start")
def start_trip(
    trip_id: int,
    db: Session = Depends(get_db),
    driver: User = Depends(get_driver_user)
):
    """Start a trip (mark as in progress)"""
    
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    
    if not trip:
        raise HTTPException(status_code=404, detail="Viaje no encontrado")
    
    if trip.driver_id != driver.id:
        raise HTTPException(status_code=403, detail="No eres el conductor de este viaje")
    
    success, error = TripService.start_trip(db, trip_id)
    
    if not success:
        raise HTTPException(status_code=400, detail=error)
    
    return {
        "message": "Viaje iniciado exitosamente",
        "trip_id": trip_id,
        "status": "in_progress"
    }

@router.post("/trip/{trip_id}/complete")
def complete_trip(
    trip_id: int,
    db: Session = Depends(get_db),
    driver: User = Depends(get_driver_user)
):
    """Complete a trip"""
    
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    
    if not trip:
        raise HTTPException(status_code=404, detail="Viaje no encontrado")
    
    if trip.driver_id != driver.id:
        raise HTTPException(status_code=403, detail="No eres el conductor de este viaje")
    
    summary, error = TripService.complete_trip(db, trip_id)
    
    if not summary:
        raise HTTPException(status_code=400, detail=error)
    
    return TripSummaryResponse.model_validate(summary)

@router.post("/passenger/{reservation_id}/check-in")
def check_in_passenger(
    reservation_id: int,
    db: Session = Depends(get_db),
    driver: User = Depends(get_driver_user)
):
    """Check in a passenger (mark as boarded)"""
    
    reservation = db.query(Reservation).filter(
        Reservation.id == reservation_id
    ).first()
    
    if not reservation:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    
    if reservation.trip.driver_id != driver.id:
        raise HTTPException(status_code=403, detail="Este pasajero no es de tu viaje")
    
    check_in, error = CheckInService.check_in_passenger(db, reservation_id)
    
    if not check_in:
        raise HTTPException(status_code=400, detail=error)
    
    return CheckInResponse.model_validate(check_in)

@router.post("/passenger/{reservation_id}/mark-paid")
def mark_passenger_paid(
    reservation_id: int,
    db: Session = Depends(get_db),
    driver: User = Depends(get_driver_user)
):
    """Mark a passenger as paid (received cash)"""
    
    reservation = db.query(Reservation).filter(
        Reservation.id == reservation_id
    ).first()
    
    if not reservation:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    
    if reservation.trip.driver_id != driver.id:
        raise HTTPException(status_code=403, detail="Este pasajero no es de tu viaje")
    
    check_in, error = CheckInService.register_cash_payment(db, reservation_id, paid_by_driver=True)
    
    if not check_in:
        raise HTTPException(status_code=400, detail=error)
    
    return {
        "message": "Pago registrado exitosamente",
        "reservation_id": reservation_id,
        "amount": reservation.total_price,
        "payment_status": "paid"
    }

@router.post("/passenger/{reservation_id}/no-show")
def mark_no_show(
    reservation_id: int,
    notes: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    driver: User = Depends(get_driver_user)
):
    """Mark a passenger as no-show"""
    
    reservation = db.query(Reservation).filter(
        Reservation.id == reservation_id
    ).first()
    
    if not reservation:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    
    if reservation.trip.driver_id != driver.id:
        raise HTTPException(status_code=403, detail="Este pasajero no es de tu viaje")
    
    check_in, error = CheckInService.mark_no_show(db, reservation_id, notes)
    
    if not check_in:
        raise HTTPException(status_code=400, detail=error)
    
    return {
        "message": "Pasajero marcado como no show",
        "reservation_id": reservation_id
    }

@router.get("/my-completed-trips")
def get_completed_trips(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    driver: User = Depends(get_driver_user)
):
    """Get completed trips"""
    
    trips = db.query(Trip).filter(
        Trip.driver_id == driver.id,
        Trip.status == TripStatus.COMPLETED
    ).order_by(Trip.real_departure_time.desc()).offset(skip).limit(limit).all()
    
    result = []
    for trip in trips:
        reservations = db.query(Reservation).filter(
            Reservation.trip_id == trip.id
        ).all()
        
        boarded = sum(1 for r in reservations if r.check_in and r.check_in.check_in_status == CheckInStatus.CHECKED_IN)
        no_shows = sum(1 for r in reservations if r.status == ReservationStatus.NO_SHOW)
        collected = sum(r.total_price for r in reservations if r.check_in and r.check_in.payment_status == PaymentStatus.PAID)
        
        result.append({
            "id": trip.id,
            "origin": trip.origin,
            "destination": trip.destination,
            "real_departure_time": trip.real_departure_time,
            "real_arrival_time": trip.real_arrival_time,
            "passengers_boarded": boarded,
            "no_shows": no_shows,
            "amount_collected": collected
        })
    
    return result

@router.get("/statistics")
def get_driver_statistics(
    db: Session = Depends(get_db),
    driver: User = Depends(get_driver_user)
):
    """Get driver statistics"""
    
    now = datetime.now(timezone.utc)
    this_month_start = now.replace(day=1, hour=0, minute=0, second=0)
    
    # Completed trips this month
    completed_trips = db.query(Trip).filter(
        Trip.driver_id == driver.id,
        Trip.status == TripStatus.COMPLETED,
        Trip.real_departure_time >= this_month_start
    ).all()
    
    total_trips = len(completed_trips)
    
    # Calculate totals
    total_passengers = 0
    total_collected = 0
    
    for trip in completed_trips:
        reservations = db.query(Reservation).filter(
            Reservation.trip_id == trip.id
        ).all()
        
        boarded = sum(1 for r in reservations if r.check_in and r.check_in.check_in_status == CheckInStatus.CHECKED_IN)
        collected = sum(r.total_price for r in reservations if r.check_in and r.check_in.payment_status == PaymentStatus.PAID)
        
        total_passengers += boarded
        total_collected += collected
    
    return {
        "trips_completed_this_month": total_trips,
        "total_passengers_transported": total_passengers,
        "total_amount_collected": total_collected,
        "average_per_trip": total_collected / total_trips if total_trips > 0 else 0
    }
