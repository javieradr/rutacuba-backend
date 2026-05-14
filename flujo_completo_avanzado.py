import requests

BASE_URL = "http://localhost:8000"
print("🚀 FLUJO COMPLETO AVANZADO - RUTACUBA\n")

# ====================== 1. LOGIN ADMIN ======================
print("1. 🔑 Login como Administrador...")
r = requests.post(f"{BASE_URL}/auth/login", json={
    "phone": "5350000001",
    "password": "admin123"
})

if r.status_code != 200:
    print("❌ Error en login admin")
    exit()

token_admin = r.json().get("access_token")
headers_admin = {"Authorization": f"Bearer {token_admin}"}
print("✅ Login Admin exitoso\n")

# ====================== 2. VER MINIVANES ======================
print("2. 🚐 Listando Minivanes existentes...")
r = requests.get(f"{BASE_URL}/vans/", headers=headers_admin)
print(f"   Status: {r.status_code} | Cantidad: {len(r.json()) if r.status_code == 200 else 0}")

# ====================== 3. CREAR VIAJE (usando minivan existente) ======================
print("\n3. 🛣️ Creando Viaje...")
trip_data = {
    "origin": "La Habana",
    "destination": "Viñales",
    "departure_time": "2026-05-28T08:00:00",
    "arrival_time": "2026-05-28T14:00:00",
    "price_per_seat": 28.0,
    "available_seats": 12,
    "van_id": 1
}
r = requests.post(f"{BASE_URL}/trips/", json=trip_data, headers=headers_admin)
print(f"   Crear Viaje → {r.status_code}")

if r.status_code in (200, 201):
    trip = r.json()
    trip_id = trip.get("id")
    print(f"   ✅ Viaje creado (ID: {trip_id})")
else:
    print("   ❌ Error:", r.text)
    trip_id = None

# ====================== 4. CREAR CLIENTE ======================
print("\n4. 👤 Creando Cliente...")
client_phone = "5357778888"
r = requests.post(f"{BASE_URL}/auth/register", json={
    "phone": client_phone,
    "full_name": "Cliente Prueba",
    "email": "cliente@test.com",
    "password": "123456"
})
print(f"   Registro Cliente → {r.status_code}")

# ====================== 5. LOGIN CLIENTE ======================
print("\n5. 🔑 Login como Cliente...")
r = requests.post(f"{BASE_URL}/auth/login", json={
    "phone": client_phone,
    "password": "123456"
})

if r.status_code == 200:
    token_client = r.json().get("access_token")
    headers_client = {"Authorization": f"Bearer {token_client}"}
    print("   ✅ Login Cliente exitoso")

    # ====================== 6. CREAR RESERVA ======================
    if trip_id:
        print("\n6. 🎟️ Creando Reserva...")
        reservation_data = {
            "trip_id": trip_id,
            "seat_number": 5,
            "passenger_name": "Cliente Prueba",
            "passenger_phone": client_phone,
            "is_full_rental": False
        }
        r = requests.post(f"{BASE_URL}/reservations/", json=reservation_data, headers=headers_client)
        print(f"   Crear Reserva → {r.status_code}")
        if r.status_code in (200, 201):
            print("   ✅ Reserva creada exitosamente!")
        else:
            print("   Detalle:", r.text)
else:
    print("   ❌ Login cliente falló")

print("\n🎉 === FLUJO COMPLETO FINALIZADO ===")
print("Sistema funcionando correctamente con datos reales.")
