import requests

BASE_URL = "http://localhost:8000"

# Login Admin
r = requests.post(f"{BASE_URL}/auth/login", json={
    "phone": "5350000001", 
    "password": "admin123"
})
token = r.json().get("access_token")
headers = {"Authorization": f"Bearer {token}"}

print("🔄 Probando notificaciones...\n")

r = requests.post(f"{BASE_URL}/reservations/", json={
    "trip_id": 4,
    "seat_number": 9,
    "passenger_name": "Prueba Notificación",
    "passenger_phone": "5351112222"
}, headers=headers)

print(f"Reserva creada: {r.status_code}")
print("\nRevisa los logs del servidor para ver si se enviaron las notificaciones.")
