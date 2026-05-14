import requests
import random

BASE_URL = "http://localhost:8000"
phone = f"535{random.randint(1000000,9999999)}"

print("🚀 PRUEBA FINAL RUTACUBA - TELÉFONO NUEVO\n")
print(f"Teléfono usado: {phone}\n")

# 1. Registro
print("1. 📝 Registro...")
r = requests.post(f"{BASE_URL}/auth/register", json={
    "phone": phone,
    "full_name": "Usuario Final",
    "email": "final@test.com",
    "password": "123456"
})
print(f"   Registro → {r.status_code}")

if r.status_code != 200:
    print("   ❌ Registro falló:", r.text)

# 2. Login
print("\n2. 🔑 Login...")
r = requests.post(f"{BASE_URL}/auth/login", json={
    "phone": phone,
    "password": "123456"
})
print(f"   Login → {r.status_code}")

if r.status_code == 200:
    token = r.json().get("access_token")
    print("   ✅ Login exitoso")

    headers = {"Authorization": f"Bearer {token}"}

    # 3. Crear Minivan
    print("\n3. 🚐 Crear Minivan...")
    r = requests.post(f"{BASE_URL}/admin/vans", json={
        "brand": "Hyundai",
        "model": "H1",
        "license_plate": f"HAB{random.randint(100000,999999)}",
        "capacity": 12,
        "has_ac": True
    }, headers=headers)
    print(f"   Crear Van → {r.status_code}")
    if r.status_code >= 400:
        print("   Detalle:", r.text[:200])
else:
    print("   ❌ Login falló")
