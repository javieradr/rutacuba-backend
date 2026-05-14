import requests

BASE_URL = "http://127.0.0.1:8000"

def run_final_test():
    print("\n🚀 EJECUTANDO PRUEBA DE FLUJO FINAL...")
    print("="*50)

    # Datos exactos según tus modelos
    user_payload = {
        "phone": "5350000000",
        "full_name": "Javi Admin",
        "email": "javi@rutacuba.com",
        "password": "admin123password"
    }

    # 1. Registro (Para asegurar que existe)
    requests.post(f"{BASE_URL}/auth/register", json=user_payload)

    # 2. Login con el campo 'phone' corregido
    print("[1] Intentando Login en /auth/login...")
    # Enviamos como JSON ya que tu error 422 mostró que espera un body con 'phone'
    r_login = requests.post(f"{BASE_URL}/auth/login", json={
        "phone": user_payload["phone"],
        "password": user_payload["password"]
    })

    if r_login.status_code == 200:
        token = r_login.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        print("    ✅ Login Exitoso. Token obtenido.")

        # 3. Prueba de acceso a un área protegida (Vans)
        print("\n[2] Verificando acceso a Vanes...")
        # Probamos con /vans/ o /vans dependiendo de tu router
        r_vans = requests.get(f"{BASE_URL}/vans/", headers=headers)
        if r_vans.status_code == 404:
            r_vans = requests.get(f"{BASE_URL}/vans", headers=headers)
        
        print(f"    Respuesta: {r_vans.status_code}")
        if r_vans.status_code == 200:
            print(f"    📦 Datos: {r_vans.json()}")
            print("\n✨ ¡SISTEMA 100% OPERATIVO!")
        else:
            print(f"    ❌ Error de acceso: {r_vans.text}")
    else:
        print(f"    ❌ Error en Login (422): {r_login.text}")

if __name__ == "__main__":
    run_final_test()
