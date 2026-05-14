# 🚀 ACTUALIZACIÓN RUTACUBA - NOTIFICACIONES WHATSAPP Y REPORTE DE VIAJES

## ¿QUÉ SE AGREGÓ?

### 1. ✅ NOTIFICACIONES POR WHATSAPP
- Cuando se crea una nueva reserva → Notificación al admin por WhatsApp
- Cuando se completa un viaje → Reporte financiero por WhatsApp
- Cuando se recibe un pago → Confirmación por WhatsApp

**Número admin:** +53 119975 (Cuba)

### 2. ✅ REPORTE FINANCIERO COMPLETO DE VIAJES
Al finalizar cada viaje se calcula automáticamente:

```
EJEMPLO DE REPORTE:
═════════════════════════════════════════════════════════
Viaje: La Habana → Viñales (Trip #5)
Distancia: 180 km
─────────────────────────────────────────────────────────
💰 DINERO RECAUDADO: $255.00 (7 pasajeros × $30 + 1 × $15)

🛢️ COMBUSTIBLE:
   - Consumo: 0.08 L/km
   - Distancia: 180 km
   - Total litros: 14.4 L
   - Precio por litro: $1.50
   - Costo total: $21.60

💵 DINERO DESPUÉS DE COMBUSTIBLE: $233.40

👨‍✈️ SALARIO CONDUCTOR (15% de $233.40): $35.01

📈 GANANCIA NETA DEL VIAJE: $198.39

═════════════════════════════════════════════════════════
```

---

## 📦 CAMBIOS EN EL CÓDIGO

### 1. requirements.txt
```
✅ Agregado: twilio==8.10.0
```

### 2. .env
```
Nuevos campos:
TWILIO_ACCOUNT_SID=tu_account_sid_aqui
TWILIO_AUTH_TOKEN=tu_auth_token_aqui
TWILIO_WHATSAPP_FROM=whatsapp:+1234567890
ADMIN_WHATSAPP_NUMBER=whatsapp:+53119975

DEFAULT_FUEL_CONSUMPTION_KM=0.08
DEFAULT_FUEL_PRICE=1.50
DRIVER_COMMISSION_PERCENTAGE=15
```

### 3. models.py
Agregados 3 campos a la tabla `trips`:
```python
distance_km          # Distancia en km
fuel_consumption_per_km  # Litros por km
fuel_price_per_liter    # Precio por litro
```

Nueva tabla `trip_reports`:
```python
# Contiene todos los cálculos financieros del viaje
money_collected
total_fuel_consumed
total_fuel_cost
driver_salary
net_profit
... (y más)
```

### 4. services.py
- Actualizado `create_reservation()` → Envía WhatsApp al crear reserva
- Actualizado `complete_trip()` → Calcula TripReport y envía WhatsApp

### 5. Archivo nuevo: whatsapp_service.py
- Clase `WhatsAppService` con métodos para enviar notificaciones

### 6. schemas.py
- Agregados campos a `TripCreate`
- Nuevo schema `TripReportResponse`

---

## 🔧 PASOS PARA INSTALAR

### PASO 1: Actualizar requirements.txt

```powershell
# En tu carpeta del proyecto
pip install -r requirements.txt --upgrade
```

### PASO 2: Obtener credenciales de Twilio

1. Abre: https://www.twilio.com
2. Regístrate (o inicia sesión)
3. Ve a Console
4. Copia tu **Account SID**
5. Copia tu **Auth Token**
6. Ve a Messaging → WhatsApp (Sandbox o comprado)
7. Copia el número **WHATSAPP_FROM**

### PASO 3: Configurar .env

```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=tu_token_aqui
TWILIO_WHATSAPP_FROM=whatsapp:+1987654321
ADMIN_WHATSAPP_NUMBER=whatsapp:+53119975

DEFAULT_FUEL_CONSUMPTION_KM=0.08
DEFAULT_FUEL_PRICE=1.50
DRIVER_COMMISSION_PERCENTAGE=15
```

### PASO 4: Reiniciar servidor

```powershell
# En PowerShell, presiona Ctrl+C para detener el servidor anterior

uvicorn main:app --reload
```

---

## 📱 CÓMO FUNCIONA WHATSAPP

### Notificación al crear reserva:

```
📱 WhatsApp que recibe el admin:

🎫 NUEVA RESERVA - RutaCuba

ID Reserva: #123
Pasajero: Pedro Martínez
Ruta: La Habana → Viñales
Salida: 15/05/2026 08:00
Precio: $15.00

⏰ Acción requerida: Confirmar pago
```

### Notificación al completar viaje:

```
📱 WhatsApp que recibe el admin:

✅ VIAJE COMPLETADO - RutaCuba

ID Viaje: #5
Ruta: La Habana → Viñales
Conductor: Carlos Rodríguez

📊 RESUMEN FINANCIERO:
💰 Dinero Recaudado: $255.00
🚐 Salario Conductor (15%): $35.01
📈 Ganancia Neta: $198.39
```

---

## 🗄️ CÁLCULO MATEMÁTICO

```
Paso 1: Dinero recaudado
money_collected = suma de todos los pagos

Paso 2: Costo de combustible
total_fuel_consumed = distance_km × fuel_consumption_per_km
total_fuel_cost = total_fuel_consumed × fuel_price_per_liter

Paso 3: Dinero después del combustible
money_after_fuel = money_collected - total_fuel_cost

Paso 4: Salario del conductor (15%)
driver_salary = money_after_fuel × 0.15

Paso 5: Ganancia neta
net_profit = money_collected - total_fuel_cost - driver_salary
```

### EJEMPLO PRÁCTICO:

```
Viaje: La Habana → Viñales
Distancia: 180 km
Pasajeros que pagaron: 8
Precio por asiento: $30

Paso 1: money_collected = 8 × $30 = $240

Paso 2: 
total_fuel_consumed = 180 × 0.08 = 14.4 L
total_fuel_cost = 14.4 × $1.50 = $21.60

Paso 3:
money_after_fuel = $240 - $21.60 = $218.40

Paso 4:
driver_salary = $218.40 × 0.15 = $32.76

Paso 5:
net_profit = $240 - $21.60 - $32.76 = $185.64
```

---

## 📊 NUEVOS ENDPOINTS

### Ver reporte de un viaje completado:

```
GET /admin/trip-report/{trip_id}

Respuesta:
{
  "id": 1,
  "trip_id": 5,
  "origin": "La Habana",
  "destination": "Viñales",
  "distance_km": 180.0,
  "total_passengers_boarded": 8,
  "money_collected": 240.00,
  "fuel_consumption_per_km": 0.08,
  "fuel_price_per_liter": 1.50,
  "total_fuel_consumed": 14.4,
  "total_fuel_cost": 21.60,
  "money_after_fuel": 218.40,
  "driver_salary": 32.76,
  "net_profit": 185.64
}
```

---

## ⚙️ CÓMO CREAR UN VIAJE CON DATOS DE COMBUSTIBLE

```powershell
# Ejemplo de POST /trips/

{
  "origin": "La Habana",
  "destination": "Viñales",
  "departure_time": "2026-05-15T08:00:00",
  "arrival_time": "2026-05-15T10:30:00",
  "price_per_seat": 30.00,
  "available_seats": 12,
  "van_id": 1,
  "driver_id": 2,
  "pickup_points": "Parque Central, Hotel Nacional",
  "notes": "Viaje directo",
  
  "distance_km": 180.0,                    # NUEVO
  "fuel_consumption_per_km": 0.08,        # NUEVO
  "fuel_price_per_liter": 1.50            # NUEVO
}
```

---

## 🧪 PRUEBA SIN TWILIO

Si no tienes Twilio configurado, el sistema:
1. ✅ Sigue funcionando normalmente
2. ⚠️ Muestra un aviso en la consola
3. 📝 NO envía WhatsApp (pero registra en logs)

**Mensaje que verás:**
```
⚠️ AVISO: Twilio no está configurado. Mensaje que se enviaría:
[contenido del mensaje]
```

---

## 🔐 SEGURIDAD

### Credenciales de Twilio
- Guarda `TWILIO_ACCOUNT_SID` y `TWILIO_AUTH_TOKEN` en .env
- **NUNCA** las compartas en repositorios públicos
- En producción, usa variables de entorno seguras

### Número de WhatsApp
- Se guarda en .env: `ADMIN_WHATSAPP_NUMBER`
- Puedes cambiar el número sin modificar el código
- Solo el admin recibe notificaciones

---

## 📈 FLUJO COMPLETO CON NUEVO SISTEMA

### 1. Cliente hace reserva
```
POST /reservations/
↓
✓ Reserva creada
↓
📱 WhatsApp al admin: "Nueva reserva #123"
```

### 2. Viaje inicia
```
POST /driver/trip/{id}/start
↓
✓ Viaje en progreso
```

### 3. Viaje se completa
```
POST /driver/trip/{id}/complete
↓
✓ Se calcula TripReport automáticamente
✓ Se guarda en BD
↓
📱 WhatsApp al admin con resumen financiero
```

### 4. Admin revisa reporte
```
GET /admin/trip-report/{trip_id}
↓
Ve todos los datos: dinero, combustible, salario, ganancia
```

---

## 🎯 RESUMEN DE ARCHIVOS ACTUALIZADOS

| Archivo | Cambios |
|---------|---------|
| requirements.txt | + twilio |
| .env | + 6 nuevas variables |
| config.py | + Configuración de Twilio |
| models.py | + 3 campos en Trip + tabla TripReport |
| schemas.py | + TripReportResponse |
| services.py | + NotificacionesWhatsApp en reserva y viaje completado |
| whatsapp_service.py | NUEVO - Servicio WhatsApp |

---

## ✅ CHECKLIST FINAL

- [ ] Descargué nuevo código
- [ ] Actualicé requirements.txt
- [ ] Instalé `pip install -r requirements.txt`
- [ ] Obtuve credenciales de Twilio
- [ ] Configuré .env con credenciales
- [ ] Ejecuté `uvicorn main:app --reload`
- [ ] Probé crear una reserva
- [ ] Recibí notificación en WhatsApp
- [ ] Completé un viaje
- [ ] Ví el reporte con cálculos

---

## 🆘 PROBLEMAS COMUNES

### ❌ "ModuleNotFoundError: No module named 'twilio'"
```powershell
pip install twilio
```

### ❌ "Twilio credentials are invalid"
- Verifica que copiaste correctamente de Twilio Console
- Usa "Account SID" (no API Key)
- Usa "Auth Token" (no API Secret)

### ❌ "WhatsApp message not sent"
- Verifica que el número tiene formato `whatsapp:+XXXXXXXXXX`
- El número debe ser el del sandbox o comprado
- En sandbox, el número necesita ser agregado primero

### ❌ "No recibo mensajes de WhatsApp"
- Verifica que el número `+53119975` es correcto
- En Twilio sandbox, el número debe estar verificado
- Checa los logs para ver si hay errores

---

## 📞 OPCIONES DE COMBUSTIBLE

### Configuración global en .env:
```env
DEFAULT_FUEL_CONSUMPTION_KM=0.08    # Litros por km
DEFAULT_FUEL_PRICE=1.50              # Precio por litro
```

### Configuración por viaje:
Al crear un viaje, puedes especificar:
```json
"distance_km": 180.0,
"fuel_consumption_per_km": 0.08,
"fuel_price_per_liter": 1.50
```

Si no especificas, usa los valores por defecto.

---

## 🚀 PRÓXIMOS PASOS

1. **Instala Twilio** - Regístrate en twilio.com
2. **Obtén credenciales** - Copia Account SID y Auth Token
3. **Configura .env** - Pega las credenciales
4. **Reinicia servidor** - `uvicorn main:app --reload`
5. **Prueba** - Crea una reserva y mira tu WhatsApp

---

**¡LISTO! Tu sistema ahora tiene notificaciones por WhatsApp y reportes financieros automáticos.** 🎉

**Versión:** 2.1.0 con WhatsApp y Trip Reports  
**Actualizado:** Mayo 2026  
**Estado:** Completamente Funcional
