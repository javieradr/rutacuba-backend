# ⚡ GUÍA RÁPIDA - RutaCuba Backend

## 🚀 En 5 minutos

### 1. Copiar archivos
Crea una carpeta llamada `rutacuba_backend` y copia todos los archivos `.py`:

```
rutacuba_backend/
├── main.py
├── config.py
├── database.py
├── models.py
├── schemas.py
├── security.py
├── services.py
├── dependencies.py
├── routers_auth.py
├── routers_trips.py
├── routers_reservations.py
├── routers_vans.py
├── routers_driver.py
├── routers_admin.py
├── requirements.txt
└── .env
```

### 2. Instalar Python (si no lo tienes)
```bash
# Windows/Mac/Linux
# Descarga desde: https://www.python.org/downloads/
# Elige Python 3.9 o superior
```

### 3. Abrir terminal en la carpeta
```bash
cd rutacuba_backend
```

### 4. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 5. Ejecutar servidor
```bash
uvicorn main:app --reload
```

### 6. ¡Listo!
Abre navegador en: **http://localhost:8000/docs**

---

## 📋 Lo que ves en /docs

### Secciones principales:
- **Autenticación (auth)** - Login, registro, perfil
- **Viajes (trips)** - Crear, buscar viajes
- **Reservas (reservations)** - Hacer reservas
- **Conductor (driver)** - Panel del conductor
- **Administración (admin)** - Gestión de sistema
- **Minivans (vans)** - Listar vehículos

---

## 🧪 Prueba rápida

### 1. Abre http://localhost:8000/docs

### 2. Encuentra "POST /auth/register"

### 3. Click en "Try it out"

### 4. Completa con:
```json
{
  "phone": "5355555555",
  "password": "prueba123",
  "full_name": "Mi Nombre",
  "email": "mi@email.com"
}
```

### 5. Click en "Execute"

Verás la respuesta con tu token de acceso.

---

## 🔑 Primeros pasos como admin

1. **Registra tu cuenta como cliente**
   - Usa /auth/register

2. **Cambia tu rol a admin**
   - Necesitas acceso directo a la base de datos
   - O pídele a alguien que lo haga
   - SQL: `UPDATE users SET role='admin' WHERE id=1;`

3. **Agrega una minivan**
   - POST /admin/vans

4. **Crea un viaje**
   - POST /trips/

5. **Los clientes pueden reservar**
   - GET /trips/search
   - POST /reservations/

---

## 📱 Para el conductor

1. **Registrate como cliente**
   - POST /auth/register

2. **Admin te cambia a conductor**
   - POST /admin/users/{id}/set-role

3. **Ves tus viajes**
   - GET /driver/my-trips-today

4. **Haces check-in de pasajeros**
   - POST /driver/passenger/{id}/check-in

5. **Registras pagos**
   - POST /driver/passenger/{id}/mark-paid

6. **Completas el viaje**
   - POST /driver/trip/{id}/complete

---

## 🆘 Si algo falla

### "ModuleNotFoundError: No module named 'fastapi'"
```bash
pip install -r requirements.txt
```

### "Address already in use"
El puerto 8000 ya está en uso. Cambia de puerto:
```bash
uvicorn main:app --reload --port 8001
```

### "Database is locked"
Cierra otras conexiones a SQLite o reinicia el servidor

### "Invalid token"
Tu token expiró (24 horas). Haz login nuevamente.

---

## 📚 Documentación completa

- **README.md** - Guía detallada
- **EJEMPLOS_USO.md** - Ejemplos de uso con curl
- **http://localhost:8000/docs** - Documentación interactiva

---

## 🎯 Estructura de carpetas creada

Después de ejecutar, verás:
```
rutacuba_backend/
├── rutacuba.db          ← Base de datos SQLite
├── uploads/
│   ├── payments/        ← Comprobantes de pago
│   └── proofs/          ← Evidencias
├── *.py files
└── .env
```

---

## ✅ Checklist

- [ ] Descargué Python 3.9+
- [ ] Copié todos los archivos .py
- [ ] Ejecuté `pip install -r requirements.txt`
- [ ] Ejecuté `uvicorn main:app --reload`
- [ ] Abrí http://localhost:8000/docs
- [ ] Hice registro de prueba
- [ ] Ví los endpoints en Swagger

---

¡Ya está lista! 🎉

**Próximo paso:** Lee EJEMPLOS_USO.md para ver casos reales
