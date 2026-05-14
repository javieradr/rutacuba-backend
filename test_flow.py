import requests

BASE_URL = "http://127.0.0.1:8000"

def test():
    print("\n🔍 INICIANDO VERIFICACIÓN DINÁMICA...")
    
    user_payload = {
        "phone": "5350000000",
        "full_name": "Javi Admin",
        "email": "javi@rutacuba.com",
        "password": "admin123password"
    }

    # 1. Intentar Registro
    print("[1] Registro:")
    # Usamos la ruta que confirmaste que funciona
    r = requests.post(f"{BASE_URL}/auth/auth/register", json=user_payload)
    
    if r.status_code == 201 or r.status_code == 200:
        print("    ✅ Usuario creado con éxito.")
    elif r.status_code == 400:
        print("    ℹ️ El usuario ya existe, procediendo al Login...")
    else:
        print(f"    ⚠️ Respuesta inesperada en registro: {r.status_code}")

    # 2. Login
    # Usamos la ruta duplicada /auth/auth/login o /auth/auth/token según tu Swagger
    print("[2] Login:")
    login_data = {
        "username": user_payload["phone"],
        "password": user_payload["password"]
    }
    
    # Probamos la ruta que te salió en el log anteriormente
    l = requests.post(f"{BASE_URL}/auth/auth/login", data=login_data)
    
    if l.status_code == 200:
        token = l.json().get("access_token")
        print(f"    ✅ Login exitoso. Token: {token[:10]}...")
        
        # 3. Verificación de Vanes (Usando el prefijo que te dio 200 antes)
        headers = {"Authorization": f"Bearer {token}"}
        print("[3] Verificando acceso a Vanes...")
        v = requests.get(f"{BASE_URL}/vans/vans/", headers=headers)
        print(f"    Status: {v.status_code} - Datos: {v.json()}")
    else:
        print(f"    ❌ Error en Login: {l.status_code} - {l.text}")
        print("    💡 Sugerencia: Revisa en Swagger si la ruta de login es /auth/auth/login o /auth/auth/token")

if __name__ == '__main__':
    test()
