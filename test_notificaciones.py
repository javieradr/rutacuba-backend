import requests

BASE_URL = "http://localhost:8000"
print("🧪 PRUEBA DE NOTIFICACIONES\n")

# Login Admin
r = requests.post(f"{BASE_URL}/auth/login", json={
    "phone": "5350000001",
    "password": "admin123"
})
token = r.json().get("access_token")
headers = {"Authorization": f"Bearer {token}"}

print("1. Creando Reserva (debería enviar notificaciones)...")
r = requests.post(f"{BASE_URL}/reservations/", json={
    "trip_id": 4,
    "seat_number": 8,
    "passenger_name": "Juan Carlos",
    "passenger_phone": "5351112222"
}, headers=headers)

print(f"   Status: {r.status_code}")

if r.status_code == 200:
    print("   ✅ Reserva creada")
    print("   📧 Debería haber enviado email")
    print("   📱 Debería haber enviado WhatsApp al Admin")
else:
    print("   ❌ Error:", r.text)
