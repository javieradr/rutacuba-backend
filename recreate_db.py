from database import engine, Base
import models  # Esto importa todos los modelos
import schemas

print("Creando todas las tablas...")

Base.metadata.create_all(bind=engine)

print("✅ Todas las tablas han sido creadas correctamente")
print("Tablas creadas:")
for table in Base.metadata.tables.keys():
    print("   -", table)
