import requests

BASE_URL = "http://localhost:8000"
phone = "5350000001"
password = "admin123"

r = requests.post(f"{BASE_URL}/auth/login", json={"phone": phone, "password": password})
token = r.json().get("access_token")
headers = {"Authorization": f"Bearer {token}"}

print("🔍 Probando crear viaje con más información...")

data = {
    "origin": "La Habana",
    "destination": "Viñales",
    "departure_time": "2026-05-25T08:00:00",
    "arrival_time": "2026-05-25T14:00:00",
    "price_per_seat": 25.0,
    "available_seats": 12,
    "van_id": 1
}

r = requests.post(f"{BASE_URL}/trips/", json=data, headers=headers)
print(f"Status: {r.status_code}")
print("Respuesta:", r.text)
