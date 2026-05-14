# 🗄️ ESTRUCTURA DE LA BASE DE DATOS - RutaCuba

## Tablas creadas automáticamente

Cuando ejecutas la aplicación, se crean estas tablas en `rutacuba.db`:

---

## 1️⃣ TABLA: `users`
**Para:** Clientes, conductores y administradores

```
id          | INTEGER  | Clave primaria
phone       | STRING   | Número único, ej: 5355555555
email       | STRING   | Email único (opcional)
full_name   | STRING   | Nombre completo
hashed_password | STRING | Contraseña encriptada
role        | ENUM     | 'client', 'admin', 'driver'
is_active   | BOOLEAN  | True/False
created_at  | DATETIME | Fecha de creación
```

**Ejemplo de fila:**
```
id=1, phone=5355555555, full_name="Pedro Martínez", 
role="client", is_active=True
```

---

## 2️⃣ TABLA: `vans`
**Para:** Minivans/autobuses

```
id          | INTEGER  | Clave primaria
brand       | STRING   | Hyundai, Mercedes, etc
model       | STRING   | H350, Sprinter, etc
license_plate | STRING | HAB123456 (única)
capacity    | INTEGER  | Número de asientos
has_ac      | BOOLEAN  | Tiene aire acondicionado
has_wifi    | BOOLEAN  | Tiene WiFi
is_active   | BOOLEAN  | Está disponible
insurance_expiry | DATETIME | Cuándo vence el seguro
license_expiry | DATETIME | Cuándo vence la licencia
notes       | STRING   | Notas adicionales
photo_url   | STRING   | URL de foto (opcional)
created_at  | DATETIME | Fecha creación
updated_at  | DATETIME | Última actualización
```

**Ejemplo:**
```
id=1, brand="Hyundai", license_plate="HAB123456", 
capacity=12, has_ac=True, is_active=True
```

---

## 3️⃣ TABLA: `trips`
**Para:** Viajes programados

```
id          | INTEGER  | Clave primaria
origin      | STRING   | De dónde sale (ej: La Habana)
destination | STRING   | A dónde va (ej: Viñales)
departure_time | DATETIME | Cuándo sale
arrival_time | DATETIME | Cuándo llega (estimado)
price_per_seat | FLOAT  | Precio por asiento (ej: 15.00)
available_seats | INTEGER | Cuántos asientos hay
status      | ENUM     | 'scheduled', 'in_progress', 'completed', 'cancelled'
is_full_rental_allowed | BOOLEAN | Se puede alquilar completo
full_rental_price | FLOAT | Precio si alquilas todo
pickup_points | TEXT   | Puntos de recogida (JSON)
notes       | STRING   | Notas del admin
real_departure_time | DATETIME | Cuándo realmente salió
real_arrival_time | DATETIME | Cuándo realmente llegó
van_id      | INTEGER  | ID de la minivan (FK)
driver_id   | INTEGER  | ID del conductor (FK, opcional)
created_at  | DATETIME | Cuándo se creó
updated_at  | DATETIME | Última actualización
```

**Relaciones:**
- `van_id` → Apunta a tabla `vans`
- `driver_id` → Apunta a tabla `users`

---

## 4️⃣ TABLA: `reservations`
**Para:** Reservas de pasajeros

```
id          | INTEGER  | Clave primaria
seat_number | INTEGER  | Asiento reservado (NULL si es alquiler completo)
passenger_name | STRING | Nombre del pasajero
passenger_phone | STRING | Teléfono del pasajero
passenger_email | STRING | Email del pasajero
status      | ENUM     | 'pending_payment', 'confirmed', 'cancelled', 'completed', 'no_show'
payment_status | ENUM   | 'unpaid', 'paid'
total_price | FLOAT    | Precio total (ej: 15.00)
notes       | STRING   | Notas del pasajero
is_full_rental | BOOLEAN | Es alquiler completo
user_id     | INTEGER  | ID del usuario que hizo la reserva (FK)
trip_id     | INTEGER  | ID del viaje (FK)
created_at  | DATETIME | Cuándo se hizo la reserva
confirmed_at | DATETIME | Cuándo se confirmó (NULL si pendiente)
cancelled_at | DATETIME | Cuándo se canceló (NULL si activa)
```

**Estados posibles:**
- `pending_payment` - Reserva hecha, esperando pago
- `confirmed` - Pago confirmado
- `cancelled` - Cancelada por usuario o admin
- `completed` - Viaje completado
- `no_show` - Pasajero no se presentó

**Relaciones:**
- `user_id` → tabla `users`
- `trip_id` → tabla `trips`

---

## 5️⃣ TABLA: `check_ins`
**Para:** Estado de check-in y pago de cada pasajero

```
id          | INTEGER  | Clave primaria
check_in_status | ENUM | 'pending', 'checked_in', 'no_show'
payment_status | ENUM  | 'unpaid', 'paid'
checked_in_at | DATETIME | Cuándo abordó (NULL si no subió)
paid_at     | DATETIME | Cuándo pagó (NULL si no pagó)
paid_by_driver | BOOLEAN | ¿Lo marcó el conductor como pagado?
notes       | STRING   | Notas sobre este pasajero
reservation_id | INTEGER | ID de la reserva (FK)
created_at  | DATETIME | Cuándo se creó el registro
updated_at  | DATETIME | Última actualización
```

**Estados de check-in:**
- `pending` - No ha abordado
- `checked_in` - Ya está en la minivan
- `no_show` - No se presentó

**Relaciones:**
- `reservation_id` → tabla `reservations` (1 a 1)

---

## 6️⃣ TABLA: `trip_summaries`
**Para:** Resumen financiero de viajes completados

```
id          | INTEGER  | Clave primaria
trip_id     | INTEGER  | ID del viaje (FK)
total_passengers_confirmed | INTEGER | Pasajeros confirmados
total_passengers_boarded | INTEGER | Pasajeros que subieron
total_no_shows | INTEGER | Pasajeros que no se presentaron
total_amount_collected | FLOAT | Dinero recaudado
total_expected_amount | FLOAT | Dinero esperado
created_at  | DATETIME | Cuándo se completó el viaje
```

**Ejemplo:**
```
trip_id=1, total_passengers_confirmed=8,
total_passengers_boarded=7, total_no_shows=1,
total_amount_collected=105.00, total_expected_amount=120.00
```

---

## 📊 RELACIONES ENTRE TABLAS

```
users (1) ─── (N) reservations
  ↑                    │
  │                    └─── (1) trips
  │
  └─ (N) trips (como conductor)

vans (1) ─── (N) trips

trips (1) ─── (N) reservations ─── (1) check_ins

trips (1) ─── (1) trip_summaries
```

---

## 🔍 CONSULTAS SQL ÚTILES

### Ver todos los usuarios
```sql
SELECT id, phone, full_name, role FROM users;
```

### Ver todos los viajes de hoy
```sql
SELECT id, origin, destination, departure_time, status
FROM trips
WHERE DATE(departure_time) = DATE('now');
```

### Ver reservas de un viaje
```sql
SELECT passenger_name, seat_number, status, payment_status
FROM reservations
WHERE trip_id = 1;
```

### Ver viajes de un conductor
```sql
SELECT id, origin, destination, departure_time
FROM trips
WHERE driver_id = 2;
```

### Ver reservas pendientes de confirmación
```sql
SELECT id, passenger_name, trip_id, total_price
FROM reservations
WHERE status = 'pending_payment';
```

### Calcular ingresos del día
```sql
SELECT SUM(total_price) as total_ingresos
FROM reservations
WHERE DATE(created_at) = DATE('now')
AND status = 'confirmed';
```

---

## 💾 BACKUP Y RESTAURACIÓN

### Hacer backup
```bash
cp rutacuba.db rutacuba_backup_2026-05-10.db
```

### Restaurar desde backup
```bash
cp rutacuba_backup_2026-05-10.db rutacuba.db
```

### Ver la base de datos (SQLite)
```bash
# Abrir en terminal
sqlite3 rutacuba.db

# Ver tablas
.tables

# Ver estructura de una tabla
.schema users

# Ver datos
SELECT * FROM users;

# Salir
.quit
```

---

## ⚙️ CAMPOS ESPECIALES

### Enums (Enumeraciones)
Son campos que solo aceptan valores específicos:

**UserRole:**
- `client` - Cliente regular
- `admin` - Administrador
- `driver` - Conductor

**TripStatus:**
- `scheduled` - Programado
- `in_progress` - En progreso
- `completed` - Completado
- `cancelled` - Cancelado

**ReservationStatus:**
- `pending_payment` - Pendiente de pago
- `confirmed` - Confirmada
- `cancelled` - Cancelada
- `completed` - Completada
- `no_show` - No se presentó

**CheckInStatus:**
- `pending` - No ha abordado
- `checked_in` - Ha abordado
- `no_show` - No se presentó

**PaymentStatus:**
- `unpaid` - No pagado
- `paid` - Pagado

---

## 🔐 INTEGRIDAD DE DATOS

### Restricciones implementadas:
1. **Unique:** phone (no puede haber dos usuarios con el mismo teléfono)
2. **Unique:** email (no puede haber dos usuarios con el mismo email)
3. **Unique:** license_plate (no puede haber dos vans con la misma placa)
4. **Foreign Keys:** Todas las relaciones están vinculadas
5. **Cascada:** Si se elimina un viaje, se eliminan sus reservas

---

## 📈 CRECIMIENTO ESPERADO

Si tienes 1,000 viajes al mes:
- **users:** ~500-1,000 registros
- **vans:** 5-20 registros
- **trips:** ~1,000 registros
- **reservations:** ~6,000-8,000 registros (6-8 por viaje)
- **check_ins:** ~6,000-8,000 registros (1 por reserva)
- **trip_summaries:** ~1,000 registros

Total: ~14,500-17,000 registros (SQLite aguanta sin problemas)

Para producción con millones de datos, considera PostgreSQL.

---

**¡Listo! Ahora entiendes cómo funciona toda la base de datos.**
