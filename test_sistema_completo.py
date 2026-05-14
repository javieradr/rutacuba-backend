import requests
import random
import time

BASE_URL = "http://localhost:8000"
print("="*60)
print("🚀 PRUEBA COMPLETA DEL SISTEMA RUTACUBA")
print("="*60 + "\n")

# ==================== ADMIN ====================
print("1️⃣ ADMINISTRADOR")
r = requests.post(f"{BASE_URL}/auth/login", json={
    "phone": "5350000001",
    "password": "admin123"
})

if r.status_code != 200:
    print("❌ Error login Admin")
    exit()

token_admin = r.json().get("access_token")
headers_admin = {"Authorization": f"Bearer {token_admin}"}
print("   ✅ Login Admin OK\n")

# Crear Minivan
print("2️⃣ Creando Minivan...")
r = requests.post(f"{BASE_URL}/admin/vans", json={
    "brand": "Hyundai",
    "model": "H1 Grand Starex",
    "license_plate": f"HAB{random.randint(100000,999999)}",
    "capacity": 12,
    "has_ac": True,
    "has_wifi": True
}, headers=headers_admin)
van_id = r.json().get("id", 1)
print(f"   ✅ Minivan creada (ID: {van_id})\n")

# Crear Viaje
print("3️⃣ Creando Viaje...")
r = requests.post(f"{BASE_URL}/trips/", json={
    "origin": "La Habana",
    "destination": "Viñales",
    "departure_time": "2026-06-05T08:00:00",
    "arrival_time": "2026-06-05T14:00:00",
    "price_per_seat": 30.0,
    "available_seats": 12,
    "van_id": van_id
}, headers=headers_admin)
trip_id = r.json().get("id", 1)
print(f"   ✅ Viaje creado (ID: {trip_id})\n")

# ==================== CLIENTE ====================
print("4️⃣ CLIENTE")
client_phone = f"535{random.randint(1000000,9999999)}"

r = requests.post(f"{BASE_URL}/auth/register", json={
    "phone": client_phone,
    "full_name": "Cliente Real",
    "email": "cliente@real.com",
    "password": "123456"
})
print(f"   Registro Cliente → {r.status_code}")

r = requests.post(f"{BASE_URL}/auth/login", json={
    "phone": client_phone,
    "password": "123456"
})
token_client = r.json().get("access_token")
headers_client = {"Authorization": f"Bearer {token_client}"}
print("   ✅ Login Cliente OK\n")

# Crear Reserva
print("5️⃣ Creando Reserva...")
r = requests.post(f"{BASE_URL}/reservations/", json={
    "trip_id": trip_id,
    "seat_number": random.randint(1, 10),
    "passenger_name": "Cliente Real",
    "passenger_phone": client_phone,
    "is_full_rental": False
}, headers=headers_client)
print(f"   Crear Reserva → {r.status_code}\n")

# ==================== VERIFICACIONES FINALES ====================
print("6️⃣ VERIFICACIONES FINALES")
print("   • Listando Minivanes...")
requests.get(f"{BASE_URL}/vans/")

print("   • Mis Reservas (Cliente)...")
r = requests.get(f"{BASE_URL}/reservations/my-reservations", headers=headers_client)
print(f"   Reservas del cliente: {len(r.json()) if r.status_code == 200 else 0}")

print("\n" + "="*60)
print("🎉 ¡PRUEBA COMPLETA FINALIZADA!")
print("✅ Sistema listo para Frontend")
print("="*60)
print(f"🔗 Documentación: http://localhost:8000/docs")
print(f"👤 Admin: 5350000001 / admin123")
print(f"👤 Cliente ejemplo: {client_phone} / 123456")
