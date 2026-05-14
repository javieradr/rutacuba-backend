import requests
import time

BASE_URL = "http://127.0.0.1:8000"

def test_original_style():
    print("\n🔙 VOLVIENDO AL FLUJO ORIGINAL...")
    
    # 1. Login
    admin_auth = {"phone": "5350000000", "password": "admin123password"}
    r_login = requests.post(f"{BASE_URL}/auth/login", json=admin_auth)
    token = r_login.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Van (Usando la ruta que no daba 405)
    print("[1] Registrando Van...")
    v_data = {"model": "Hyundai H1", "plate": "P" + str(int(time.time()))[-6:], "capacity": 12}
    r_van = requests.post(f"{BASE_URL}/admin/vans", json=v_data, headers=headers)
    van_id = r_van.json().get("id", 1)

    # 3. Viaje (Probando la ruta que daba 401 antes)
    print("[2] Creando Viaje...")
    t_data = {"origin": "Habana", "destination": "Varadero", "departure_time": "2026-06-15T08:00:00", "price": 25.0, "van_id": van_id}
    # Intentamos la ruta con barra final
    r_trip = requests.post(f"{BASE_URL}/trips/", json=t_data, headers=headers)
    
    if r_trip.status_code == 200 or r_trip.status_code == 201:
        print("✅ ¡LOGRADO! Viaje creado.")
    else:
        print(f"❌ Seguimos con error {r_trip.status_code}: {r_trip.text}")

if __name__ == "__main__":
    test_original_style()
