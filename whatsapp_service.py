from twilio.rest import Client
from config import get_settings

settings = get_settings()

class WhatsAppService:
    def __init__(self):
        self.client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        self.from_whatsapp = f"whatsapp:{settings.TWILIO_PHONE_NUMBER}"

    def send_message(self, to_number: str, message: str):
        try:
            # Asegurar formato del número
            if not to_number.startswith('+'):
                to_number = f"+{to_number}"
            
            message = self.client.messages.create(
                body=message,
                from_=self.from_whatsapp,
                to=f"whatsapp:{to_number}"
            )
            return message.sid
        except Exception as e:
            print(f"❌ Error enviando WhatsApp: {e}")
            return None

whatsapp_service = WhatsAppService()
