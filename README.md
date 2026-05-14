# 🚐 RutaCuba - API Backend
## Sistema de Gestión de Viajes en Minivan para Cuba

### 📋 REQUISITOS
- Python 3.8+
- pip (gestor de paquetes Python)

### 🚀 INSTALACIÓN Y EJECUCIÓN

#### Paso 1: Crear estructura de carpetas
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

#### Paso 2: Instalar dependencias
```bash
pip install -r requirements.txt
```

#### Paso 3: Configurar variables de entorno
Edita `.env` con tus valores:
```env
DATABASE_URL=sqlite:///./rutacuba.db
SECRET_KEY=tu-clave-secreta-muy-larga-y-aleatoria-2024
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
FRONTEND_URL=http://localhost:3000
```

#### Paso 4: Ejecutar servidor de desarrollo
```bash
# Opción 1: Usando uvicorn directamente
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Opción 2: Usando python
python main.py
```

#### Paso 5: Verificar que funciona
- API: http://localhost:8000
- Documentación interactiva: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health check: http://localhost:8000/health

---

## 📱 ENDPOINTS PRINCIPALES

### 🔐 AUTENTICACIÓN (/auth)
```
POST /auth/register          - Registrar nuevo usuario
POST /auth/login             - Iniciar sesión
GET  /auth/me                - Obtener perfil actual
```

### 🗺️ VIAJES (/trips)
```
POST /trips/                 - Crear viaje (admin)
GET  /trips/search           - Buscar viajes disponibles
GET  /trips/{id}             - Obtener detalles del viaje
GET  /trips/{id}/seats       - Ver mapa de asientos
GET  /trips/{id}/passengers  - Ver pasajeros (conductor/admin)
```

### 🎫 RESERVAS (/reservations)
```
POST /reservations/          - Crear nueva reserva
GET  /reservations/my-reservations - Mis reservas
GET  /reservations/{id}      - Ver detalle de reserva
POST /reservations/{id}/cancel    - Cancelar reserva
POST /reservations/{id}/confirm   - Confirmar reserva (admin)
```

### 👨‍✈️ CONDUCTOR (/driver)
```
GET  /driver/my-trips-today        - Viajes de hoy
GET  /driver/my-upcoming-trips     - Próximos viajes
GET  /driver/trip/{id}/detail      - Detalle del viaje
POST /driver/trip/{id}/start       - Iniciar viaje
POST /driver/trip/{id}/complete    - Completar viaje
POST /driver/passenger/{id}/check-in - Marcar pasajero como a bordo
POST /driver/passenger/{id}/mark-paid - Registrar pago en efectivo
POST /driver/passenger/{id}/no-show   - Marcar como no show
GET  /driver/my-completed-trips     - Viajes completados
GET  /driver/statistics             - Estadísticas personales
```

### 🚐 MINIVANS (/vans)
```
GET /vans/           - Listar minivans activas
GET /vans/{id}       - Obtener detalles de minivan
```

### 👨‍💼 ADMINISTRACIÓN (/admin)
```
POST /admin/vans                    - Agregar minivan
GET  /admin/vans                    - Listar todas las minivans
POST /admin/users/{id}/set-role    - Cambiar rol de usuario
POST /admin/users/{id}/deactivate  - Desactivar usuario
POST /admin/users/{id}/activate    - Activar usuario
POST /admin/reservations/{id}/confirm - Confirmar reserva
GET  /admin/dashboard-stats         - Estadísticas del día
GET  /admin/documents-expiring      - Documentos próximos a vencer
GET  /admin/all-reservations        - Todas las reservas
GET  /admin/all-trips               - Todos los viajes
```

---

## 🔑 ROLES DE USUARIO

### CLIENT (Cliente)
- Buscar viajes
- Hacer reservas
- Ver sus reservas
- Cancelar reservas
- Ver detalle de reservas

### DRIVER (Conductor)
- Ver mis viajes
- Ver lista de pasajeros
- Hacer check-in de pasajeros
- Registrar pagos en efectivo
- Marcar no-shows
- Iniciar/completar viajes
- Ver estadísticas personales

### ADMIN (Administrador)
- Crear viajes
- Gestionar minivans
- Cambiar roles de usuarios
- Confirmar reservas
- Ver estadísticas del sistema
- Ver documentos vencidos
- Gestionar toda la operación

---

## 💰 FLUJO DE PAGO (SOLO EFECTIVO)

1. **Cliente hace reserva** → Estado: PENDING_PAYMENT
2. **Pago en efectivo**
   - Opción A: En efectivo antes de salir (paga a administrador en oficina)
   - Opción B: En la minivan (paga al conductor al abordar)
3. **Registro de pago**
   - Admin: Usa `POST /admin/reservations/{id}/confirm`
   - Conductor: Usa `POST /driver/passenger/{id}/mark-paid`
4. **Reserva confirmada** → Estado: CONFIRMED
5. **Check-in** → Pasajero aborda
6. **Viaje completado** → Estado: COMPLETED

---

## 📊 SISTEMA DE CHECK-IN

### Estados posibles:
- **PENDING**: Pasajero no ha abordado aún
- **CHECKED_IN**: Pasajero a bordo
- **NO_SHOW**: Pasajero no se presentó

### Estados de pago:
- **UNPAID**: No ha pagado
- **PAID**: Ha pagado (en efectivo)

---

## 🧪 EJEMPLO DE FLUJO COMPLETO

### 1. Registro de cliente
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "5355555555",
    "password": "micontraseña123",
    "full_name": "Pedro Martínez",
    "email": "pedro@gmail.com"
  }'
```

### 2. Login
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "5355555555",
    "password": "micontraseña123"
  }'
```
Guarda el `access_token` que recibas.

### 3. Buscar viajes
```bash
curl -X GET "http://localhost:8000/trips/search?origin=Habana&destination=Viñales&date=2026-05-15" \
  -H "Authorization: Bearer {access_token}"
```

### 4. Ver asientos disponibles
```bash
curl -X GET "http://localhost:8000/trips/1/seats" \
  -H "Authorization: Bearer {access_token}"
```

### 5. Hacer reserva
```bash
curl -X POST "http://localhost:8000/reservations/" \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "trip_id": 1,
    "seat_number": 7,
    "passenger_name": "Pedro Martínez",
    "passenger_phone": "5355555555",
    "passenger_email": "pedro@gmail.com",
    "is_full_rental": false,
    "notes": "Llevar 2 paquetes"
  }'
```

### 6. Confirmar pago (como admin)
```bash
curl -X POST "http://localhost:8000/admin/reservations/1/confirm" \
  -H "Authorization: Bearer {admin_token}" \
  -H "Content-Type: application/json"
```

---

## 👨‍💻 PARA DESARROLLADORES

### Estructura del proyecto
- **models.py**: Modelos SQLAlchemy (base de datos)
- **schemas.py**: Esquemas Pydantic (validación)
- **services.py**: Lógica de negocio
- **routers_*.py**: Endpoints de la API
- **dependencies.py**: Funciones de autenticación
- **security.py**: Funciones de encriptación y JWT

### Agregar nuevo endpoint

1. Edita el router correspondiente en `routers_*.py`
2. Define el esquema en `schemas.py` si es necesario
3. Importa las dependencias necesarias
4. Escribe la función del endpoint
5. Reinicia el servidor

---

## 🛠️ TROUBLESHOOTING

### Error: "No module named 'main'"
```bash
# Asegúrate de estar en el directorio correcto
# y que tengas todos los archivos Python
ls -la *.py
```

### Error: "database is locked"
- SQLite solo permite una escritura a la vez
- En producción, usa PostgreSQL o MySQL

### Error: "Invalid credentials"
- Verifica el `SECRET_KEY` en .env
- Asegúrate que el token no haya expirado

### Error: "Permission denied"
- Verifica que tengas el rol correcto
- Admin endpoints requieren rol "admin"
- Driver endpoints requieren rol "driver"

---

## 📈 ESCALABILIDAD EN PRODUCCIÓN

### Cambios necesarios para producción:

1. **Database**
```python
# Cambiar de SQLite a PostgreSQL
DATABASE_URL=postgresql://user:password@localhost/rutacuba
```

2. **CORS**
```python
# Especificar dominios en lugar de "*"
allow_origins=["https://www.rutacuba.com", "https://app.rutacuba.com"]
```

3. **Environment variables**
```bash
# Usar variables de entorno seguras
export SECRET_KEY=$(openssl rand -hex 32)
export DATABASE_URL=postgresql://...
```

4. **HTTPS**
- Usar certificado SSL/TLS
- Configurar reverse proxy con Nginx
- Usar gunicorn en lugar de uvicorn

5. **Logging**
```python
import logging
logging.basicConfig(level=logging.INFO)
```

6. **Rate limiting**
```python
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)
```

---

## 📞 SOPORTE

Para reportar problemas o sugerencias, contacta al equipo de desarrollo.

## 📄 LICENCIA

Proyecto privado RutaCuba - Todos los derechos reservados

---

**¡Listo! Tu API está lista para funcionar. Accede a http://localhost:8000/docs para ver la documentación interactiva.**
