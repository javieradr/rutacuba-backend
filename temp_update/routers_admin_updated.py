from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone, timedelta
from database import get_db
from models import (
    Trip, TripStatus, Reservation, ReservationStatus, Van, User, CheckInStatus,
    UserRole, PaymentStatus, TripReport
)
from schemas import VanCreate, VanResponse, TripReportResponse
from dependencies import get_admin_user

router = APIRouter(prefix="/admin", tags=["Administración"])

@router.post("/vans", response_model=VanResponse)
def add_van(
    van_data: VanCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    """Add a new van"""
    
    # Verify license plate is unique
    existing_van = db.query(Van).filter(
        Van.license_plate == van_data.license_plate
    ).first()
    
    if existing_van:
        raise HTTPException(
            status_code=400,
            detail=f"Ya existe una minivan con placa {van_data.license_plate}"
        )
    
    van = Van(**van_data.model_dump())
    db.add(van)
    db.commit()
    db.refresh(van)
    
    return VanResponse.model_validate(van)

@router.get("/vans", response_model=List[VanResponse])
def list_all_vans(
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    """List all vans"""
    
    vans = db.query(Van).order_by(Van.created_at.desc()).all()
    return [VanResponse.model_validate(van) for van in vans]

@router.post("/users/{user_id}/set-role")
def set_user_role(
    user_id: int,
    role: str = Query(...),  # client, admin, driver
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    """Set user role"""
    
    valid_roles = ["client", "admin", "driver"]
    if role not in valid_roles:
        raise HTTPException(
            status_code=400,
            detail=f"Rol inválido. Valores válidos: {valid_roles}"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    user.role = UserRole(role)
    db.commit()
    
    return {"message": f"Rol de usuario actualizado a {role}", "user_id": user_id}

@router.post("/users/{user_id}/deactivate")
def deactivate_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    """Deactivate a user"""
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    user.is_active = False
    db.commit()
    
    return {"message": "Usuario desactivado", "user_id": user_id}

@router.post("/users/{user_id}/activate")
def activate_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    """Activate a user"""
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    user.is_active = True
    db.commit()
    
    return {"message": "Usuario activado", "user_id": user_id}

@router.post("/reservations/{reservation_id}/confirm")
def admin_confirm_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    """Confirm a pending reservation"""
    
    reservation = db.query(Reservation).filter(
        Reservation.id == reservation_id
    ).first()
    
    if not reservation:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    
    if reservation.status != ReservationStatus.PENDING_PAYMENT:
        raise HTTPException(
            status_code=400,
            detail=f"La reserva no está pendiente (estado: {reservation.status.value})"
        )
    
    reservation.status = ReservationStatus.CONFIRMED
    reservation.confirmed_at = datetime.now(timezone.utc)
    db.commit()
    
    return {"message": "Reserva confirmada", "reservation_id": reservation_id}

@router.get("/dashboard-stats")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    """Get dashboard statistics"""
    
    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow = today + timedelta(days=1)
    
    # Trips today
    trips_today = db.query(Trip).filter(
        Trip.departure_time >= today,
        Trip.departure_time < tomorrow,
        Trip.status != TripStatus.CANCELLED
    ).count()
    
    # Reservations pending confirmation
    pending_confirmation = db.query(Reservation).filter(
        Reservation.status == ReservationStatus.PENDING_PAYMENT
    ).count()
    
    # Today's income (completed and confirmed)
    confirmed_today = db.query(Reservation).filter(
        Reservation.confirmed_at >= today,
        Reservation.confirmed_at < tomorrow,
        Reservation.status == ReservationStatus.CONFIRMED
    ).all()
    
    total_income = sum(r.total_price for r in confirmed_today)
    
    # Occupancy rate
    trips_with_reservations = db.query(Trip).filter(
        Trip.departure_time >= today,
        Trip.departure_time < tomorrow,
        Trip.status == TripStatus.SCHEDULED
    ).all()
    
    total_seats = 0
    occupied_seats = 0
    
    for trip in trips_with_reservations:
        van_capacity = trip.van.capacity if trip.van else 0
        total_seats += van_capacity
        
        confirmed = db.query(Reservation).filter(
            Reservation.trip_id == trip.id,
            Reservation.status == ReservationStatus.CONFIRMED
        ).count()
        
        occupied_seats += confirmed
    
    occupancy_rate = (occupied_seats / total_seats * 100) if total_seats > 0 else 0
    
    # Upcoming departures
    upcoming_trips = db.query(Trip).filter(
        Trip.departure_time >= datetime.now(timezone.utc),
        Trip.status == TripStatus.SCHEDULED
    ).order_by(Trip.departure_time).limit(5).all()
    
    return {
        "trips_today": trips_today,
        "pending_confirmation": pending_confirmation,
        "daily_income": round(total_income, 2),
        "occupancy_rate": round(occupancy_rate, 1),
        "total_confirmed_today": len(confirmed_today),
        "upcoming_trips": [
            {
                "id": t.id,
                "route": f"{t.origin} → {t.destination}",
                "departure": t.departure_time.strftime("%H:%M"),
                "status": t.status.value
            }
            for t in upcoming_trips
        ]
    }

@router.get("/documents-expiring")
def get_expiring_documents(
    days: int = Query(15, ge=1, le=90),
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    """Get vans with documents expiring soon"""
    
    limit_date = datetime.now(timezone.utc) + timedelta(days=days)
    
    vans = db.query(Van).filter(
        Van.is_active == True
    ).all()
    
    result = []
    
    for van in vans:
        expiring_docs = []
        
        if van.insurance_expiry and van.insurance_expiry <= limit_date:
            days_left = (van.insurance_expiry - datetime.now(timezone.utc)).days
            expiring_docs.append({
                "type": "Seguro",
                "expiry_date": van.insurance_expiry.strftime("%d/%m/%Y"),
                "days_left": days_left
            })
        
        if van.license_expiry and van.license_expiry <= limit_date:
            days_left = (van.license_expiry - datetime.now(timezone.utc)).days
            expiring_docs.append({
                "type": "Licencia",
                "expiry_date": van.license_expiry.strftime("%d/%m/%Y"),
                "days_left": days_left
            })
        
        if expiring_docs:
            result.append({
                "id": van.id,
                "brand": van.brand,
                "model": van.model,
                "license_plate": van.license_plate,
                "expiring_documents": expiring_docs
            })
    
    return result

@router.get("/all-reservations")
def get_all_reservations(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status: str = Query(None),
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    """Get all reservations"""
    
    query = db.query(Reservation)
    
    if status:
        try:
            res_status = ReservationStatus(status)
            query = query.filter(Reservation.status == res_status)
        except ValueError:
            raise HTTPException(status_code=400, detail="Estado inválido")
    
    reservations = query.order_by(
        Reservation.created_at.desc()
    ).offset(skip).limit(limit).all()
    
    return [
        {
            "id": r.id,
            "passenger_name": r.passenger_name,
            "trip_origin": r.trip.origin,
            "trip_destination": r.trip.destination,
            "trip_departure": r.trip.departure_time,
            "user_phone": r.user.phone,
            "status": r.status.value,
            "payment_status": r.payment_status.value,
            "total_price": r.total_price,
            "created_at": r.created_at
        }
        for r in reservations
    ]

@router.get("/all-trips")
def get_all_trips(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status: str = Query(None),
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    """Get all trips"""
    
    query = db.query(Trip)
    
    if status:
        try:
            trip_status = TripStatus(status)
            query = query.filter(Trip.status == trip_status)
        except ValueError:
            raise HTTPException(status_code=400, detail="Estado inválido")
    
    trips = query.order_by(
        Trip.departure_time.desc()
    ).offset(skip).limit(limit).all()
    
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
            "arrival_time": trip.arrival_time,
            "status": trip.status.value,
            "van": f"{trip.van.brand} {trip.van.model} ({trip.van.license_plate})",
            "driver": trip.driver.full_name if trip.driver else "Sin asignar",
            "confirmed_passengers": confirmed,
            "capacity": trip.van.capacity,
            "price_per_seat": trip.price_per_seat,
            "distance_km": trip.distance_km
        })
    
    return result

# ============ NUEVO: ENDPOINT PARA VER REPORTE DE VIAJE ============

@router.get("/trip-report/{trip_id}", response_model=TripReportResponse)
def get_trip_report(
    trip_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    """
    NUEVO: Obtiene el reporte completo de un viaje completado
    
    Retorna:
    - Dinero recaudado
    - Distancia recorrida
    - Consumo de combustible
    - Costo de combustible
    - Salario del conductor (15%)
    - Ganancia neta del viaje
    """
    
    trip_report = db.query(TripReport).filter(
        TripReport.trip_id == trip_id
    ).first()
    
    if not trip_report:
        raise HTTPException(
            status_code=404,
            detail="Reporte no encontrado. El viaje debe estar completado."
        )
    
    return TripReportResponse.model_validate(trip_report)

@router.get("/trip-reports")
def get_all_trip_reports(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    """
    NUEVO: Lista todos los reportes de viajes completados
    Útil para ver historial financiero
    """
    
    reports = db.query(TripReport).order_by(
        TripReport.created_at.desc()
    ).offset(skip).limit(limit).all()
    
    return [
        {
            "id": r.id,
            "trip_id": r.trip_id,
            "origin": r.origin,
            "destination": r.destination,
            "distance_km": r.distance_km,
            "total_passengers_boarded": r.total_passengers_boarded,
            "money_collected": round(r.money_collected, 2),
            "total_fuel_cost": round(r.total_fuel_cost, 2),
            "driver_salary": round(r.driver_salary, 2),
            "net_profit": round(r.net_profit, 2),
            "created_at": r.created_at
        }
        for r in reports
    ]

@router.get("/trip-reports/summary")
def get_trip_reports_summary(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    """
    NUEVO: Resumen de reportes de los últimos N días
    Muestra totales de dinero, combustible, salarios y ganancias
    """
    
    start_date = datetime.now(timezone.utc) - timedelta(days=days)
    
    reports = db.query(TripReport).filter(
        TripReport.created_at >= start_date
    ).all()
    
    if not reports:
        return {
            "period_days": days,
            "total_trips": 0,
            "total_distance_km": 0.0,
            "total_money_collected": 0.0,
            "total_fuel_cost": 0.0,
            "total_driver_salaries": 0.0,
            "total_net_profit": 0.0,
            "average_profit_per_trip": 0.0
        }
    
    total_money = sum(r.money_collected for r in reports)
    total_fuel = sum(r.total_fuel_cost for r in reports)
    total_salaries = sum(r.driver_salary for r in reports)
    total_profit = sum(r.net_profit for r in reports)
    total_distance = sum(r.distance_km for r in reports)
    
    return {
        "period_days": days,
        "total_trips": len(reports),
        "total_distance_km": round(total_distance, 2),
        "total_money_collected": round(total_money, 2),
        "total_fuel_cost": round(total_fuel, 2),
        "total_driver_salaries": round(total_salaries, 2),
        "total_net_profit": round(total_profit, 2),
        "average_profit_per_trip": round(total_profit / len(reports), 2) if reports else 0
    }
