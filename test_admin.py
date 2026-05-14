import requests

BASE_URL = "http://localhost:8000"
phone = "5350000001"
password = "admin123"

print("🚀 FLUJO COMPLETO CON ADMINISTRADOR\n")

# Login como Admin
r = requests.post(f"{BASE_URL}/auth/login", json={"phone": phone, "password": password})
if r.status_code == 200:
    token = r.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    print("✅ Login como Admin exitoso\n")

    # Crear Minivan
    print("🚐 Creando Minivan...")
    r = requests.post(f"{BASE_URL}/admin/vans", json={
        "brand": "Mercedes",
        "model": "Sprinter",
        "license_plate": "HAB777777",
        "capacity": 15,
        "has_ac": True,
        "has_wifi": True
    }, headers=headers)
    print(f"   Status: {r.status_code} - {r.text[:100]}")

    # Crear Viaje (si tienes el endpoint)
    print("\n🛣️  Creando Viaje...")
    r = requests.post(f"{BASE_URL}/trips/", json={
        "origin": "La Habana",
        "destination": "Viñales",
        "departure_time": "2026-05-20T08:00:00",
        "arrival_time": "2026-05-20T12:00:00",
        "price_per_seat": 25.0,
        "available_seats": 15,
        "van_id": 1
    }, headers=headers)
    print(f"   Status: {r.status_code}")

else:
    print("❌ Login falló")
