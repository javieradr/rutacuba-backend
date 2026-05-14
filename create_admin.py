from database import SessionLocal
from models import User
from security import get_password_hash

db = SessionLocal()

phone = "5350000001"
password = "admin123"

existing = db.query(User).filter(User.phone == phone).first()

if existing:
    print("✅ Admin ya existe")
else:
    admin = User(
        phone=phone,
        full_name="Administrador Principal",
        email="admin@rutacuba.com",
        hashed_password=get_password_hash(password),
        role="admin",
        is_active=True
    )
    db.add(admin)
    db.commit()
    print("✅ Administrador creado exitosamente")

print(f"Teléfono: {phone}")
print(f"Contraseña: {password}")
db.close()
