from twilio.rest import Client
from config import get_settings
from typing import Optional
import logging

settings = get_settings()
logger = logging.getLogger(__name__)

class WhatsAppService:
    """Service for sending WhatsApp notifications via Twilio"""
    
    _client = None
    
    @classmethod
    def get_client(cls):
        """Get or create Twilio client"""
        if cls._client is None:
            try:
                cls._client = Client(
                    settings.TWILIO_ACCOUNT_SID,
                    settings.TWILIO_AUTH_TOKEN
                )
            except Exception as e:
                logger.error(f"Error initializing Twilio client: {e}")
                return None
        return cls._client
    
    @staticmethod
    def send_message(
        to_number: str,
        message: str
    ) -> bool:
        """
        Send a WhatsApp message
        
        Args:
            to_number: Recipient number (format: whatsapp:+5399999999)
            message: Message text
            
        Returns:
            True if sent successfully, False otherwise
        """
        try:
            client = WhatsAppService.get_client()
            
            if not client:
                logger.warning("Twilio client not initialized")
                return False
            
            message_obj = client.messages.create(
                from_=settings.TWILIO_WHATSAPP_FROM,
                body=message,
                to=to_number
            )
            
            logger.info(f"WhatsApp message sent: {message_obj.sid}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending WhatsApp message: {e}")
            return False
    
    @staticmethod
    def send_new_reservation_notification(
        passenger_name: str,
        trip_origin: str,
        trip_destination: str,
        departure_time: str,
        total_price: float,
        reservation_id: int
    ) -> bool:
        """Send notification to admin about new reservation"""
        
        message = f"""
🚐 NUEVA RESERVA - RutaCuba

Reserva #{reservation_id}
Pasajero: {passenger_name}
Ruta: {trip_origin} → {trip_destination}
Salida: {departure_time}
Precio: ${total_price:.2f}

Estado: Pendiente de pago

Revisa la aplicación para más detalles.
"""
        
        return WhatsAppService.send_message(
            settings.ADMIN_WHATSAPP_NUMBER,
            message.strip()
        )
    
    @staticmethod
    def send_trip_completed_notification(
        trip_origin: str,
        trip_destination: str,
        driver_name: str,
        total_collected: float,
        fuel_cost: float,
        driver_commission: float,
        net_profit: float,
        distance_km: float
    ) -> bool:
        """Send notification to admin about trip completion and earnings"""
        
        message = f"""
✅ VIAJE COMPLETADO - RutaCuba

Ruta: {trip_origin} → {trip_destination}
Conductor: {driver_name}
Distancia: {distance_km:.2f} km

📊 REPORTE FINANCIERO
━━━━━━━━━━━━━━━━━━━━━━
Dinero Recaudado: ${total_collected:.2f}
Gasto Combustible: -${fuel_cost:.2f}

Salario Conductor (15%): -${driver_commission:.2f}

💰 GANANCIA NETA: ${net_profit:.2f}
━━━━━━━━━━━━━━━━━━━━━━

Revisa el reporte completo en la app.
"""
        
        return WhatsAppService.send_message(
            settings.ADMIN_WHATSAPP_NUMBER,
            message.strip()
        )
    
    @staticmethod
    def send_error_notification(error_message: str) -> bool:
        """Send error notification to admin"""
        
        message = f"""
⚠️ ERROR - RutaCuba

{error_message}

Por favor revisa la aplicación.
"""
        
        return WhatsAppService.send_message(
            settings.ADMIN_WHATSAPP_NUMBER,
            message.strip()
        )
