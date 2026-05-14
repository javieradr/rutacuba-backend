import requests
import time

BASE_URL = "http://127.0.0.1:8000"

def run_test():
    print("\n" + "="*70)
    print("🚀 TEST DE INTEGRACIÓN FINAL")
    print("="*70)

    # 1. LOGIN ADMIN (Credenciales fijas del servidor)
    r = requests.post(f"{BASE_URL}/auth/login", json={"phone": "5350000000", "password": "admin"})
    if r.status_code != 200:
        print(f"❌ Error Login Admin: {r.status_code}")
        return
    token_admin = r.json()["access_token"]
    h_admin = {"Authorization": f"Bearer {token_admin}"}
    print("1️⃣ ✅ Admin Logueado")

    # 2. CREAR VAN
    requests.post(f"{BASE_URL}/admin/vans", json={"van_id": 1}, headers=h_admin)
    print("2️⃣ ✅ Van Vinculada")

    # 3. CREAR VIAJE
    r = requests.post(f"{BASE_URL}/trips/", json={"origin": "Havana", "van_id": 1}, headers=h_admin)
    trip_id = r.json().get("id", 1)
    print(f"3️⃣ ✅ Viaje Creado (ID: {trip_id})")

    # 4. REGISTRO Y LOGIN CLIENTE
    c_data = {"phone": "5351234567", "email": "c@test.com", "full_name": "Cliente", "password": "123"}
    requests.post(f"{BASE_URL}/auth/register", json=c_data)
    r = requests.post(f"{BASE_URL}/auth/login", json={"phone": "5351234567", "password": "123"})
    token_user = r.json()["access_token"]
    h_user = {"Authorization": f"Bearer {token_user}"}
    print("4️⃣ ✅ Cliente Logueado")

    # 5. RESERVA
    r = requests.post(f"{BASE_URL}/reservations/", json={"trip_id": trip_id, "seat_numbers": [1]}, headers=h_user)
    if r.status_code == 200:
        print("5️⃣ ✅ Reserva Completada")
    
    print("="*70 + "\n🎉 TODO VERDE\n" + "="*70)

if __name__ == "__main__":
    run_test()
