import os
from twilio.rest import Client
from config import settings

def enviar_whatsapp_manual():
    print("📱 Probando conexión directa con Twilio...")
    
    # Extraemos credenciales del config o del entorno
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    from_whatsapp = settings.TWILIO_PHONE_NUMBER # Debe ser 'whatsapp:+14155238886' o similar
    
    # Tu número de prueba (asegúrate de incluir el código de país, ej: whatsapp:+53...)
    to_whatsapp = "whatsapp:+5350000000" 

    try:
        client = Client(account_sid, auth_token)
        
        message = client.messages.create(
            from_=from_whatsapp,
            body="🚀 Javi, si lees esto, el backend de RutaCuba ya envía notificaciones.",
            to=to_whatsapp
        )
        
        print(f"✅ Mensaje enviado con éxito!")
        print(f"ID del Mensaje: {message.sid}")
        print(f"Estado: {message.status}")
        
    except Exception as e:
        print(f"❌ Error al enviar el mensaje:")
        print(str(e))

if __name__ == "__main__":
    enviar_whatsapp_manual()
