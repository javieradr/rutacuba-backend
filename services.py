from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime, timezone, timedelta
from typing import Optional, Tuple, List
from models import (
    Reservation, ReservationStatus, CheckIn, CheckInStatus,
    Trip, TripStatus, User, PaymentStatus, TripSummary
)

class ReservationService:
    """Service for managing reservations with cash-only payment"""
    
    @staticmethod
    def create_reservation(
        db: Session,
        user: User,
        trip_id: int,
        seat_number: Optional[int],
        passenger_name: str,
        passenger_phone: Optional[str],
        passenger_email: Optional[str],
        is_full_rental: bool = False,
        notes: Optional[str] = None
    ) -> Tuple[Optional[Reservation], Optional[str]]:
        """
        Creates a reservation with all validations.
        Returns (reservation, error_message).
        """
        try:
            # Verify trip exists
            trip = db.query(Trip).filter(Trip.id == trip_id).first()
            if not trip:
                return None, "Viaje no encontrado"
            
            # Verify trip is available
            if trip.status != TripStatus.SCHEDULED:
                return None, "Este viaje no está disponible para reservas"
            
            # Verify trip hasn't departed
            if trip.departure_time <= datetime.now(timezone.utc):
                return None, "El viaje ya ha salido"
            
            # Verify user is not the driver
            if trip.driver_id and trip.driver_id == user.id:
                return None, "No puedes reservar en tu propio viaje como conductor"
            
            if is_full_rental:
                # Full rental validation
                if not trip.is_full_rental_allowed:
                    return None, "Este viaje no permite alquiler completo"
                
                # Check no existing reservations
                existing = db.query(Reservation).filter(
                    Reservation.trip_id == trip_id,
                    Reservation.status.in_([
                        ReservationStatus.CONFIRMED,
                        ReservationStatus.PENDING_PAYMENT
                    ])
                ).first()
                
                if existing:
                    return None, "Ya existen reservas en este viaje"
                
                total_price = trip.full_rental_price or (trip.price_per_seat * trip.van.capacity)
                seat_number = None
            else:
                # Individual seat validation
                if not seat_number:
                    return None, "Debe seleccionar un asiento"
                
                if seat_number < 1 or seat_number > trip.van.capacity:
                    return None, f"Asiento inválido. Debe ser entre 1 y {trip.van.capacity}"
                
                # Check seat availability with lock
                existing = db.query(Reservation).filter(
                    and_(
                        Reservation.trip_id == trip_id,
                        Reservation.seat_number == seat_number,
                        Reservation.status.in_([
                            ReservationStatus.CONFIRMED,
                            ReservationStatus.PENDING_PAYMENT
                        ])
                    )
                ).with_for_update().first()
                
                if existing:
                    return None, f"El asiento {seat_number} ya está ocupado"
                
                total_price = trip.price_per_seat
            
            # Create reservation
            reservation = Reservation(
                user_id=user.id,
                trip_id=trip_id,
                seat_number=seat_number,
                passenger_name=passenger_name,
                passenger_phone=passenger_phone,
                passenger_email=passenger_email or user.email,
                total_price=total_price,
                notes=notes,
                is_full_rental=is_full_rental,
                status=ReservationStatus.PENDING_PAYMENT,
                payment_status=PaymentStatus.UNPAID
            )
            
            db.add(reservation)
            db.commit()
            db.refresh(reservation)
            
            # Create associated check-in record
            check_in = CheckIn(
                reservation_id=reservation.id,
                check_in_status=CheckInStatus.PENDING,
                payment_status=PaymentStatus.UNPAID
            )
            db.add(check_in)
            db.commit()
            db.refresh(check_in)
            
            # NUEVO: Enviar notificación por WhatsApp al administrador
            try:
                from whatsapp_service import WhatsAppService
                WhatsAppService.notify_new_reservation(
                    passenger_name=passenger_name,
                    reservation_id=reservation.id,
                    origin=trip.origin,
                    destination=trip.destination,
                    departure_time=trip.departure_time.strftime("%d/%m/%Y %H:%M"),
                    total_price=total_price
                )
            except Exception as e:
                print(f"Advertencia: No se pudo enviar WhatsApp: {e}")
            
            return reservation, None
            
        except Exception as e:
            db.rollback()
            return None, f"Error al crear la reserva: {str(e)}"
    
    @staticmethod
    def cancel_reservation(
        db: Session,
        reservation_id: int,
        cancelled_by: str = "user"
    ) -> Tuple[bool, Optional[str]]:
        """Cancel a reservation"""
        try:
            reservation = db.query(Reservation).filter(
                Reservation.id == reservation_id
            ).first()
            
            if not reservation:
                return False, "Reserva no encontrada"
            
            if reservation.status in [ReservationStatus.CANCELLED, ReservationStatus.COMPLETED]:
                return False, "La reserva ya está cancelada o completada"
            
            reservation.status = ReservationStatus.CANCELLED
            reservation.cancelled_at = datetime.now(timezone.utc)
            
            db.commit()
            
            return True, None
            
        except Exception as e:
            db.rollback()
            return False, f"Error al cancelar reserva: {str(e)}"

class CheckInService:
    """Service for managing passenger check-ins"""
    
    @staticmethod
    def check_in_passenger(
        db: Session,
        reservation_id: int
    ) -> Tuple[Optional[CheckIn], Optional[str]]:
        """Check in a passenger (mark as boarded)"""
        try:
            reservation = db.query(Reservation).filter(
                Reservation.id == reservation_id
            ).first()
            
            if not reservation:
                return None, "Reserva no encontrada"
            
            check_in = db.query(CheckIn).filter(
                CheckIn.reservation_id == reservation_id
            ).first()
            
            if not check_in:
                return None, "Check-in no encontrado"
            
            if check_in.check_in_status == CheckInStatus.CHECKED_IN:
                return None, "Este pasajero ya hizo check-in"
            
            check_in.check_in_status = CheckInStatus.CHECKED_IN
            check_in.checked_in_at = datetime.now(timezone.utc)
            
            db.commit()
            db.refresh(check_in)
            
            return check_in, None
            
        except Exception as e:
            db.rollback()
            return None, f"Error al hacer check-in: {str(e)}"
    
    @staticmethod
    def mark_no_show(
        db: Session,
        reservation_id: int,
        notes: Optional[str] = None
    ) -> Tuple[Optional[CheckIn], Optional[str]]:
        """Mark a passenger as no-show"""
        try:
            check_in = db.query(CheckIn).filter(
                CheckIn.reservation_id == reservation_id
            ).first()
            
            if not check_in:
                return None, "Check-in no encontrado"
            
            check_in.check_in_status = CheckInStatus.NO_SHOW
            check_in.notes = notes or "No se presentó"
            
            reservation = check_in.reservation
            reservation.status = ReservationStatus.NO_SHOW
            
            db.commit()
            db.refresh(check_in)
            
            return check_in, None
            
        except Exception as e:
            db.rollback()
            return None, f"Error al marcar como no show: {str(e)}"
    
    @staticmethod
    def register_cash_payment(
        db: Session,
        reservation_id: int,
        paid_by_driver: bool = True
    ) -> Tuple[Optional[CheckIn], Optional[str]]:
        """Register cash payment received"""
        try:
            check_in = db.query(CheckIn).filter(
                CheckIn.reservation_id == reservation_id
            ).first()
            
            if not check_in:
                return None, "Check-in no encontrado"
            
            check_in.payment_status = PaymentStatus.PAID
            check_in.paid_at = datetime.now(timezone.utc)
            check_in.paid_by_driver = paid_by_driver
            
            reservation = check_in.reservation
            reservation.payment_status = PaymentStatus.PAID
            
            db.commit()
            db.refresh(check_in)
            
            return check_in, None
            
        except Exception as e:
            db.rollback()
            return None, f"Error al registrar pago: {str(e)}"

class TripService:
    """Service for managing trips"""
    
    @staticmethod
    def start_trip(
        db: Session,
        trip_id: int
    ) -> Tuple[Optional[Trip], Optional[str]]:
        """Start a trip (change status to IN_PROGRESS)"""
        try:
            trip = db.query(Trip).filter(Trip.id == trip_id).first()
            
            if not trip:
                return None, "Viaje no encontrado"
            
            if trip.status != TripStatus.SCHEDULED:
                return None, f"El viaje no está en estado programado (actual: {trip.status.value})"
            
            # Check if there's at least one confirmed passenger
            confirmed_count = db.query(Reservation).filter(
                Reservation.trip_id == trip_id,
                Reservation.status == ReservationStatus.CONFIRMED
            ).count()
            
            if confirmed_count == 0:
                return None, "No hay pasajeros confirmados para este viaje"
            
            trip.status = TripStatus.IN_PROGRESS
            trip.real_departure_time = datetime.now(timezone.utc)
            
            # Mark all pending check-ins as no-show
            pending_check_ins = db.query(CheckIn).join(Reservation).filter(
                Reservation.trip_id == trip_id,
                CheckIn.check_in_status == CheckInStatus.PENDING
            ).all()
            
            for check_in in pending_check_ins:
                check_in.check_in_status = CheckInStatus.NO_SHOW
                check_in.reservation.status = ReservationStatus.NO_SHOW
            
            db.commit()
            db.refresh(trip)
            
            return trip, None
            
        except Exception as e:
            db.rollback()
            return None, f"Error al iniciar viaje: {str(e)}"
    
    @staticmethod
    def complete_trip(
        db: Session,
        trip_id: int
    ) -> Tuple[Optional['TripReport'], Optional[str]]:
        """Complete a trip and generate detailed financial report"""
        try:
            from models import TripReport
            from whatsapp_service import WhatsAppService
            from config import get_settings
            
            settings = get_settings()
            
            trip = db.query(Trip).filter(Trip.id == trip_id).first()
            
            if not trip:
                return None, "Viaje no encontrado"
            
            if trip.status != TripStatus.IN_PROGRESS:
                return None, f"El viaje no está en progreso (actual: {trip.status.value})"
            
            trip.status = TripStatus.COMPLETED
            trip.real_arrival_time = datetime.now(timezone.utc)
            
            # Get reservations and calculate money
            reservations = db.query(Reservation).filter(
                Reservation.trip_id == trip_id
            ).all()
            
            total_boarded = sum(1 for r in reservations if r.check_in and r.check_in.check_in_status == CheckInStatus.CHECKED_IN)
            total_no_shows = sum(1 for r in reservations if r.status == ReservationStatus.NO_SHOW)
            money_collected = sum(r.total_price for r in reservations if r.check_in and r.check_in.payment_status == PaymentStatus.PAID)
            
            # Use trip fuel data or defaults from settings
            distance_km = trip.distance_km or 0
            fuel_consumption_per_km = trip.fuel_consumption_per_km or settings.DEFAULT_FUEL_CONSUMPTION_KM
            fuel_price_per_liter = trip.fuel_price_per_liter or settings.DEFAULT_FUEL_PRICE
            
            # Calculate fuel costs
            total_fuel_consumed = distance_km * fuel_consumption_per_km
            total_fuel_cost = total_fuel_consumed * fuel_price_per_liter
            
            # Calculate driver salary (15% of money AFTER fuel cost)
            money_after_fuel = money_collected - total_fuel_cost
            driver_salary = money_after_fuel * (settings.DRIVER_COMMISSION_PERCENTAGE / 100)
            
            # Calculate net profit
            net_profit = money_collected - total_fuel_cost - driver_salary
            
            # Create detailed trip report
            trip_report = TripReport(
                trip_id=trip_id,
                origin=trip.origin,
                destination=trip.destination,
                distance_km=distance_km,
                total_passengers_boarded=total_boarded,
                total_passengers_no_show=total_no_shows,
                money_collected=money_collected,
                fuel_consumption_per_km=fuel_consumption_per_km,
                fuel_price_per_liter=fuel_price_per_liter,
                total_fuel_consumed=total_fuel_consumed,
                total_fuel_cost=total_fuel_cost,
                money_after_fuel=money_after_fuel,
                driver_salary=driver_salary,
                net_profit=net_profit
            )
            
            # Mark all completed check-ins
            for reservation in reservations:
                if reservation.check_in and reservation.check_in.check_in_status == CheckInStatus.CHECKED_IN:
                    reservation.status = ReservationStatus.COMPLETED
            
            db.add(trip_report)
            db.commit()
            db.refresh(trip_report)
            
            # Send WhatsApp notification to admin
            if trip.driver:
                WhatsAppService.notify_trip_completed(
                    trip_id=trip_id,
                    origin=trip.origin,
                    destination=trip.destination,
                    money_collected=money_collected,
                    net_profit=net_profit,
                    driver_name=trip.driver.full_name,
                    driver_salary=driver_salary
                )
            
            return trip_report, None
            
        except Exception as e:
            db.rollback()
            return None, f"Error al completar viaje: {str(e)}"
    
    @staticmethod
    def get_trip_summary_for_driver(
        db: Session,
        trip_id: int
    ) -> dict:
        """Get financial summary of trip for driver"""
        trip = db.query(Trip).filter(Trip.id == trip_id).first()
        if not trip:
            return {}
        
        reservations = db.query(Reservation).filter(
            Reservation.trip_id == trip_id
        ).all()
        
        total_confirmed = sum(1 for r in reservations if r.status == ReservationStatus.CONFIRMED)
        total_paid = sum(1 for r in reservations if r.check_in and r.check_in.payment_status == PaymentStatus.PAID)
        total_unpaid = sum(1 for r in reservations if r.check_in and r.check_in.payment_status == PaymentStatus.UNPAID)
        total_collected = sum(r.total_price for r in reservations if r.check_in and r.check_in.payment_status == PaymentStatus.PAID)
        
        return {
            "total_confirmed": total_confirmed,
            "total_paid": total_paid,
            "total_unpaid": total_unpaid,
            "total_collected": total_collected,
            "total_expected": sum(r.total_price for r in reservations if r.status == ReservationStatus.CONFIRMED)
        }
