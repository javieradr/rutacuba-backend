import requests
import json

BASE_URL = "http://localhost:8000"
print("🚀 FLUJO COMPLETO RUTACUBA\n")

# ====================== LOGIN ADMIN ======================
print("1. 🔑 Login como Administrador...")
r = requests.post(f"{BASE_URL}/auth/login", json={
    "phone": "5350000001",
    "password": "admin123"
})

if r.status_code != 200:
    print("❌ Error en login")
    exit()

token = r.json().get("access_token")
headers = {"Authorization": f"Bearer {token}"}
print("✅ Login exitoso\n")

# ====================== 2. CREAR MINIVAN ======================
print("2. 🚐 Creando Minivan...")
van_data = {
    "brand": "Hyundai",
    "model": "H1 Grand Starex",
    "license_plate": "HAB555555",
    "capacity": 12,
    "has_ac": True,
    "has_wifi": True
}
r = requests.post(f"{BASE_URL}/admin/vans", json=van_data, headers=headers)
print(f"   Status: {r.status_code}")

if r.status_code in (200, 201):
    van = r.json()
    van_id = van.get("id")
    print(f"   ✅ Minivan creada (ID: {van_id})")
else:
    print("   ❌ Error creando minivan")
    van_id = None

# ====================== 3. CREAR VIAJE ======================
if van_id:
    print("\n3. 🛣️ Creando Viaje...")
    trip_data = {
        "origin": "La Habana",
        "destination": "Viñales",
        "departure_time": "2026-05-25T08:00:00",
        "arrival_time": "2026-05-25T14:00:00",
        "price_per_seat": 25.0,
        "available_seats": 12,
        "van_id": van_id
    }
    r = requests.post(f"{BASE_URL}/trips/", json=trip_data, headers=headers)
    print(f"   Status: {r.status_code}")
    if r.status_code in (200, 201):
        trip = r.json()
        print(f"   ✅ Viaje creado (ID: {trip.get('id')})")
    else:
        print("   ❌ Error creando viaje:", r.text)

print("\n🎉 Flujo completo terminado!")
print("Revisa http://localhost:8000/docs para continuar probando manualmente.")
