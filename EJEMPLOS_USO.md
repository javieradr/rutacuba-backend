# 📘 EJEMPLOS PRÁCTICOS DE USO - RutaCuba API

## 1️⃣ CREAR UN ADMINISTRADOR (Primera vez)

Cuando ejecutas la aplicación por primera vez, necesitas crear un admin manualmente.

```bash
# Opción: Usar la base de datos directamente
sqlite3 rutacuba.db

INSERT INTO users (phone, email, full_name, hashed_password, role, is_active, created_at)
VALUES (
    '5350000000',
    'admin@rutacuba.com',
    'Administrador RutaCuba',
    '$2b$12$...',  # Hash bcrypt - usar generate_hash.py
    'admin',
    1,
    datetime('now')
);
```

O crear un script `generate_hash.py`:
```python
from security import get_password_hash
print(get_password_hash("tu_contraseña_admin"))
```

Luego:
```bash
python generate_hash.py
# Copia el hash y pégalo en el SQL anterior
```

## 2️⃣ REGISTRO E INICIO DE SESIÓN

### 2.1 Registrar nuevo cliente
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

**Respuesta exitosa:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "phone": "5355555555",
    "full_name": "Pedro Martínez",
    "email": "pedro@gmail.com",
    "role": "client",
    "is_active": true,
    "created_at": "2026-05-10T14:30:00"
  }
}
```

**Guardar el token:**
```bash
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### 2.2 Login
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "5355555555",
    "password": "micontraseña123"
  }'
```

### 2.3 Ver mi perfil
```bash
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer $TOKEN"
```

---

## 3️⃣ ADMINISTRACIÓN - AGREGAR MINIVAN

Como administrador, primero necesitas registrar minivans.

```bash
ADMIN_TOKEN="tu_token_admin_aqui"

curl -X POST "http://localhost:8000/admin/vans" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "brand": "Hyundai",
    "model": "H350",
    "license_plate": "HAB123456",
    "capacity": 12,
    "has_ac": true,
    "has_wifi": false,
    "insurance_expiry": "2027-05-10T00:00:00",
    "license_expiry": "2027-12-31T00:00:00",
    "notes": "Minivan nueva con aire acondicionado"
  }'
```

**Respuesta:**
```json
{
  "id": 1,
  "brand": "Hyundai",
  "model": "H350",
  "license_plate": "HAB123456",
  "capacity": 12,
  "has_ac": true,
  "has_wifi": false,
  "is_active": true,
  "insurance_expiry": "2027-05-10T00:00:00",
  "license_expiry": "2027-12-31T00:00:00",
  "created_at": "2026-05-10T14:35:00"
}
```

---

## 4️⃣ ADMINISTRACIÓN - CREAR VIAJE

Ahora crea un viaje. Necesitas:
- ID de la minivan (1 del ejemplo anterior)
- ID del conductor (si lo tienes asignado)

### 4.1 Registrar un conductor
```bash
# Primero registra un usuario como cliente
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "5354444444",
    "password": "contraseña_conductor",
    "full_name": "Carlos Rodríguez",
    "email": "carlos@rutacuba.com"
  }'
```

Guarda el ID del conductor (ejemplo: id = 2)

### 4.2 Cambiar rol a conductor
```bash
curl -X POST "http://localhost:8000/admin/users/2/set-role" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"role": "driver"}'
```

### 4.3 Crear el viaje
```bash
curl -X POST "http://localhost:8000/trips/" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "La Habana",
    "destination": "Viñales",
    "departure_time": "2026-05-15T08:00:00",
    "arrival_time": "2026-05-15T10:30:00",
    "price_per_seat": 15.00,
    "available_seats": 12,
    "van_id": 1,
    "driver_id": 2,
    "is_full_rental_allowed": true,
    "full_rental_price": 150.00,
    "pickup_points": "Parque Central, Hotel Nacional, Plaza de la Revolución",
    "notes": "Viaje directo. Parada de 15 min en Las Terrazas"
  }'
```

**Respuesta:**
```json
{
  "id": 1,
  "origin": "La Habana",
  "destination": "Viñales",
  "departure_time": "2026-05-15T08:00:00",
  "arrival_time": "2026-05-15T10:30:00",
  "price_per_seat": 15.00,
  "available_seats": 12,
  "van_id": 1,
  "driver_id": 2,
  "status": "scheduled",
  "is_full_rental_allowed": true,
  "full_rental_price": 150.00,
  "created_at": "2026-05-10T14:40:00"
}
```

---

## 5️⃣ CLIENTE - BUSCAR Y RESERVAR

### 5.1 Buscar viajes disponibles
```bash
TOKEN_CLIENTE="token_del_cliente"

curl -X GET "http://localhost:8000/trips/search?origin=Habana&destination=Viñales&date=2026-05-15" \
  -H "Authorization: Bearer $TOKEN_CLIENTE"
```

**Respuesta:**
```json
[
  {
    "id": 1,
    "origin": "La Habana",
    "destination": "Viñales",
    "departure_time": "2026-05-15T08:00:00",
    "arrival_time": "2026-05-15T10:30:00",
    "price_per_seat": 15.00,
    "available_seats": 12,
    "status": "scheduled"
  }
]
```

### 5.2 Ver mapa de asientos
```bash
curl -X GET "http://localhost:8000/trips/1/seats" \
  -H "Authorization: Bearer $TOKEN_CLIENTE"
```

**Respuesta:**
```json
{
  "trip_id": 1,
  "total_seats": 12,
  "available_seats": 12,
  "seats": [
    {"number": 1, "available": true, "status": "free"},
    {"number": 2, "available": true, "status": "free"},
    {"number": 3, "available": true, "status": "free"},
    ...
    {"number": 12, "available": true, "status": "free"}
  ]
}
```

### 5.3 Hacer reserva (asiento individual)
```bash
curl -X POST "http://localhost:8000/reservations/" \
  -H "Authorization: Bearer $TOKEN_CLIENTE" \
  -H "Content-Type: application/json" \
  -d '{
    "trip_id": 1,
    "seat_number": 7,
    "passenger_name": "Pedro Martínez",
    "passenger_phone": "5355555555",
    "passenger_email": "pedro@gmail.com",
    "is_full_rental": false,
    "notes": "Voy con mochila grande"
  }'
```

**Respuesta:**
```json
{
  "id": 1,
  "trip_id": 1,
  "user_id": 1,
  "seat_number": 7,
  "passenger_name": "Pedro Martínez",
  "passenger_phone": "5355555555",
  "passenger_email": "pedro@gmail.com",
  "status": "pending_payment",
  "payment_status": "unpaid",
  "total_price": 15.00,
  "notes": "Voy con mochila grande",
  "is_full_rental": false,
  "created_at": "2026-05-10T15:00:00",
  "confirmed_at": null
}
```

### 5.4 Ver mis reservas
```bash
curl -X GET "http://localhost:8000/reservations/my-reservations" \
  -H "Authorization: Bearer $TOKEN_CLIENTE"
```

---

## 6️⃣ CONDUCTOR - PANEL DE CONTROL

### 6.1 Ver mis viajes de hoy
```bash
TOKEN_CONDUCTOR="token_del_conductor"

curl -X GET "http://localhost:8000/driver/my-trips-today" \
  -H "Authorization: Bearer $TOKEN_CONDUCTOR"
```

**Respuesta:**
```json
[
  {
    "id": 1,
    "origin": "La Habana",
    "destination": "Viñales",
    "departure_time": "2026-05-15T08:00:00",
    "arrival_time": "2026-05-15T10:30:00",
    "status": "scheduled",
    "van": {
      "brand": "Hyundai",
      "model": "H350",
      "license_plate": "HAB123456",
      "capacity": 12
    },
    "total_confirmed": 1,
    "total_paid": 0,
    "total_collected": 0.00
  }
]
```

### 6.2 Ver detalle del viaje con pasajeros
```bash
curl -X GET "http://localhost:8000/driver/trip/1/detail" \
  -H "Authorization: Bearer $TOKEN_CONDUCTOR"
```

**Respuesta:**
```json
{
  "trip": {
    "id": 1,
    "origin": "La Habana",
    "destination": "Viñales",
    "departure_time": "2026-05-15T08:00:00",
    "arrival_time": "2026-05-15T10:30:00",
    "status": "scheduled",
    "pickup_points": "Parque Central, Hotel Nacional, Plaza",
    "notes": "Viaje directo"
  },
  "van": {
    "brand": "Hyundai",
    "model": "H350",
    "license_plate": "HAB123456",
    "capacity": 12,
    "has_ac": true,
    "has_wifi": false
  },
  "passengers": [
    {
      "reservation_id": 1,
      "passenger_name": "Pedro Martínez",
      "passenger_phone": "5355555555",
      "seat_number": 7,
      "payment_status": "unpaid",
      "check_in_status": "pending",
      "total_price": 15.00,
      "notes": "Voy con mochila grande"
    }
  ],
  "summary": {
    "total_confirmed": 1,
    "total_paid": 0,
    "total_unpaid": 1,
    "total_collected": 0.00
  }
}
```

### 6.3 Iniciar viaje
```bash
curl -X POST "http://localhost:8000/driver/trip/1/start" \
  -H "Authorization: Bearer $TOKEN_CONDUCTOR" \
  -H "Content-Type: application/json"
```

### 6.4 Hacer check-in a un pasajero
```bash
curl -X POST "http://localhost:8000/driver/passenger/1/check-in" \
  -H "Authorization: Bearer $TOKEN_CONDUCTOR" \
  -H "Content-Type: application/json"
```

**Respuesta:**
```json
{
  "id": 1,
  "reservation_id": 1,
  "check_in_status": "checked_in",
  "payment_status": "unpaid",
  "checked_in_at": "2026-05-15T08:05:00",
  "paid_at": null,
  "notes": null
}
```

### 6.5 Registrar pago en efectivo
```bash
curl -X POST "http://localhost:8000/driver/passenger/1/mark-paid" \
  -H "Authorization: Bearer $TOKEN_CONDUCTOR" \
  -H "Content-Type: application/json"
```

**Respuesta:**
```json
{
  "message": "Pago registrado exitosamente",
  "reservation_id": 1,
  "amount": 15.00,
  "payment_status": "paid"
}
```

### 6.6 Completar viaje
```bash
curl -X POST "http://localhost:8000/driver/trip/1/complete" \
  -H "Authorization: Bearer $TOKEN_CONDUCTOR" \
  -H "Content-Type: application/json"
```

**Respuesta:**
```json
{
  "trip_id": 1,
  "origin": "La Habana",
  "destination": "Viñales",
  "departure_time": "2026-05-15T08:00:00",
  "arrival_time": "2026-05-15T10:30:00",
  "real_departure_time": "2026-05-15T08:05:00",
  "real_arrival_time": "2026-05-15T10:35:00",
  "total_passengers_confirmed": 1,
  "total_passengers_boarded": 1,
  "total_no_shows": 0,
  "total_amount_collected": 15.00,
  "total_expected_amount": 15.00
}
```

---

## 7️⃣ ADMINISTRACIÓN - DASHBOARD

### 7.1 Ver estadísticas del día
```bash
curl -X GET "http://localhost:8000/admin/dashboard-stats" \
  -H "Authorization: Bearer $ADMIN_TOKEN"
```

**Respuesta:**
```json
{
  "trips_today": 2,
  "pending_confirmation": 0,
  "daily_income": 30.00,
  "occupancy_rate": 58.3,
  "total_confirmed_today": 2,
  "upcoming_trips": [
    {
      "id": 2,
      "route": "Matanzas → Cárdenas",
      "departure": "14:00",
      "status": "scheduled"
    }
  ]
}
```

### 7.2 Ver documentos próximos a vencer
```bash
curl -X GET "http://localhost:8000/admin/documents-expiring?days=30" \
  -H "Authorization: Bearer $ADMIN_TOKEN"
```

### 7.3 Listar todas las reservas
```bash
curl -X GET "http://localhost:8000/admin/all-reservations?skip=0&limit=50" \
  -H "Authorization: Bearer $ADMIN_TOKEN"
```

---

## 🔄 FLUJO COMPLETO DE UN DÍA

**8:00 AM** - Conductor Carlos ve sus viajes del día
```bash
GET /driver/my-trips-today
```

**8:30 AM** - Passengers empiezan a llegar
```bash
# Para cada pasajero:
POST /driver/passenger/{id}/check-in
```

**8:45 AM** - Primer pasajero paga en efectivo
```bash
POST /driver/passenger/1/mark-paid
```

**9:00 AM** - Carlos inicia el viaje (ya no se pueden sumar pasajeros)
```bash
POST /driver/trip/1/start
```

**10:45 AM** - Llega a destino
```bash
POST /driver/trip/1/complete
```

**Fin del día** - Admin revisa estadísticas
```bash
GET /admin/dashboard-stats
```

---

## ⚠️ CASOS DE ERROR

### Error: "El asiento ya está ocupado"
```json
{
  "detail": "El asiento 7 ya está ocupado"
}
```
**Solución:** Ver mapa de asientos y elegir otro

### Error: "Usuario desactivado"
```json
{
  "detail": "Usuario desactivado"
}
```
**Solución:** Contactar al admin para reactivación

### Error: "No tienes permisos de administrador"
```json
{
  "detail": "No tienes permisos de administrador"
}
```
**Solución:** Usar token de admin o pedir al admin el acceso

### Error: "Token expirado"
```json
{
  "detail": "No se pudieron validar las credenciales"
}
```
**Solución:** Hacer login nuevamente

---

**¡Listo! Ya tienes todos los ejemplos para usar la API completa de RutaCuba!**
