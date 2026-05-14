import jwt
from config import settings

# Simula el proceso de login
token_data = {"sub": "5350000000"}
test_token = jwt.encode(token_data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

print(f"Clave usada: {settings.SECRET_KEY}")
print(f"Token generado localmente: {test_token[:20]}...")

try:
    decoded = jwt.decode(test_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    print("✅ Decodificación local: EXITOSA")
except Exception as e:
    print(f"❌ Error decodificando con settings: {e}")
