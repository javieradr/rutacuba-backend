# 🔧 COMANDOS POWERSHELL - ACTUALIZACIÓN RUTACUBA WHATSAPP

## 📋 REQUISITOS

Debes tener:
- ✅ Proyecto anterior instalado y funcionando
- ✅ Python 3.11+
- ✅ VS Code abierto con el proyecto

---

## 🚀 PASO 1: ACTUALIZAR ARCHIVOS

Abre PowerShell como administrador en tu carpeta del proyecto:

```powershell
cd $env:USERPROFILE\Desktop\rutacuba_backend
```

---

## 📥 PASO 2: DESCARGAR/COPIAR ARCHIVOS ACTUALIZADOS

### Opción A: Si tienes los archivos en una carpeta de descargas

```powershell
# Copiar archivos actualizados
Copy-Item "$env:USERPROFILE\Downloads\models.py" . -Force
Copy-Item "$env:USERPROFILE\Downloads\schemas.py" . -Force
Copy-Item "$env:USERPROFILE\Downloads\services.py" . -Force
Copy-Item "$env:USERPROFILE\Downloads\config.py" . -Force
Copy-Item "$env:USERPROFILE\Downloads\requirements.txt" . -Force
Copy-Item "$env:USERPROFILE\Downloads\.env" . -Force

# NUEVO: Copiar archivo de WhatsApp
Copy-Item "$env:USERPROFILE\Downloads\whatsapp_service.py" . -Force
```

### Opción B: Si están en otra ruta

```powershell
# Ajusta la ruta según donde estén tus archivos
Copy-Item "C:\ruta\a\tus\archivos\*.py" .
```

---

## ✅ PASO 3: VERIFICAR QUE SE COPIARON

```powershell
# Lista todos los archivos Python
ls *.py

# Verifica que ves estos NUEVOS/ACTUALIZADOS:
# - whatsapp_service.py (NUEVO)
# - models.py (actualizado)
# - services.py (actualizado)
# - schemas.py (actualizado)
```

---

## 📦 PASO 4: INSTALAR NUEVA DEPENDENCIA (Twilio)

```powershell
# Activar ambiente virtual si no está activado
.\venv\Scripts\Activate.ps1

# Actualizar requirements
pip install -r requirements.txt --upgrade
```

Verás mucho texto. Espera a que termine. Debe decir algo como:

```
Successfully installed twilio-8.10.0
```

---

## ✨ PASO 5: CONFIGURAR TWILIO

### 5a. Obtener credenciales (5 minutos)

1. Abre un navegador: https://www.twilio.com
2. Haz clic en **Sign Up** (registra una cuenta gratis)
3. Completa el formulario
4. Verifica tu email
5. Abre Twilio Console: https://console.twilio.com/
6. En el lado izquierdo, busca **Account Info**
7. Copia estos dos valores:
   - **Account SID** (empieza con AC)
   - **Auth Token** (cadena larga de caracteres)

8. Guarda ambos en un bloc de notas temporal

### 5b. Configurar WhatsApp en Twilio (opcional pero recomendado)

Para TESTING (sandbox):
```
Número FROM: whatsapp:+14155238886 (Twilio test)
Número TO: whatsapp:+53119975 (Tu número)
```

Para PRODUCCIÓN (comprar número):
```
Número FROM: whatsapp:+1234567890 (Tu número comprado)
Número TO: whatsapp:+53119975 (Destino)
```

Por ahora, usa el sandbox de Twilio.

---

## 🔐 PASO 6: ACTUALIZAR .env

En VS Code:

1. Abre el archivo `.env`
2. Reemplaza con esto:

```env
DATABASE_URL=sqlite:///./rutacuba.db
SECRET_KEY=tu-clave-secreta-muy-larga-y-aleatoria-2024-cambiar-en-produccion
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
FRONTEND_URL=http://localhost:3000

# TWILIO - WhatsApp Configuration
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=tu_auth_token_aqui_es_largo
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
ADMIN_WHATSAPP_NUMBER=whatsapp:+53119975

# Trip Configuration
DEFAULT_FUEL_CONSUMPTION_KM=0.08
DEFAULT_FUEL_PRICE=1.50
DRIVER_COMMISSION_PERCENTAGE=15
```

3. Reemplaza:
   - `TWILIO_ACCOUNT_SID` con tu Account SID
   - `TWILIO_AUTH_TOKEN` con tu Auth Token

4. Presiona **Ctrl + S** para guardar

---

## 🚀 PASO 7: REINICIAR SERVIDOR

En la terminal de VS Code (o PowerShell):

```powershell
# Si el servidor está corriendo, presiona Ctrl + C para detenerlo

# Espera 2 segundos

# Reinicia
uvicorn main:app --reload
```

Deberías ver:

```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

---

## 🧪 PASO 8: PROBAR TODO

### Test 1: Verificar que importa Twilio

En OTRA terminal PowerShell:

```powershell
cd $env:USERPROFILE\Desktop\rutacuba_backend

.\venv\Scripts\Activate.ps1

python -c "import twilio; print('✓ Twilio OK')"
```

Debe mostrar: `✓ Twilio OK`

---

### Test 2: Abrir documentación API

En el navegador:

```
http://localhost:8000/docs
```

---

### Test 3: Crear una reserva y probar WhatsApp

1. En la documentación, busca **POST /auth/register**
2. Registra un usuario nuevo:
```json
{
  "phone": "5351111111",
  "password": "prueba123",
  "full_name": "Usuario Prueba",
  "email": "prueba@test.com"
}
```
3. Copia el token que recibes

4. Autoriza en Swagger:
   - Click en botón **Authorize** arriba
   - Pega: `Bearer {tu_token_aqui}`

5. Busca **POST /reservations/**
6. Crea una reserva en un viaje existente

7. Si Twilio está configurado correctamente:
   - ✅ En la consola/terminal deberías ver: `✓ WhatsApp enviado: SM...`
   - ✅ En el admin deberías recibir un WhatsApp

---

## 📊 PASO 9: PROBAR REPORTE DE VIAJE

Para probar el reporte:

1. Asegúrate que un viaje tiene estos datos:
   ```json
   "distance_km": 180,
   "fuel_consumption_per_km": 0.08,
   "fuel_price_per_liter": 1.50
   ```

2. Completa el viaje:
   ```
   POST /driver/trip/{trip_id}/complete
   ```

3. Deberías recibir:
   - ✅ Notificación en WhatsApp con resumen
   - ✅ Reporte guardado en base de datos

---

## 🔄 PASO 10: VERIFICAR TODO FUNCIONA

Ejecuta estos comandos en PowerShell:

```powershell
# Verificar modelo
python -c "from models import TripReport; print('✓ TripReport model OK')"

# Verificar servicio WhatsApp
python -c "from whatsapp_service import WhatsAppService; print('✓ WhatsApp service OK')"

# Verificar Twilio
python -c "from twilio.rest import Client; print('✓ Twilio client OK')"
```

Todos deben mostrar `✓ ...OK`

---

## 💾 PASO 11: BACKUP

```powershell
# Hacer backup de la base de datos
Copy-Item rutacuba.db rutacuba_backup_$(Get-Date -Format 'yyyy-MM-dd_HHmmss').db

# Listar backups
ls rutacuba_backup_*.db
```

---

## 🎯 RESUMEN DE CAMBIOS

| Archivo | Cambio |
|---------|--------|
| requirements.txt | + twilio |
| .env | + 6 nuevas variables |
| config.py | + Twilio settings |
| models.py | + trip_reports tabla |
| services.py | + WhatsApp notifications |
| schemas.py | + TripReportResponse |
| whatsapp_service.py | ✨ NUEVO |

---

## 📱 SI NO RECIBISTE WHATSAPP

### Verificar logs en PowerShell

```powershell
# En la terminal donde corre uvicorn, busca:
# ✓ WhatsApp enviado: SMxxxxxxxx
# O
# ❌ Error enviando WhatsApp: ...
```

### Checklist:

- [ ] `TWILIO_ACCOUNT_SID` está en .env
- [ ] `TWILIO_AUTH_TOKEN` está en .env
- [ ] `TWILIO_WHATSAPP_FROM` es correcto
- [ ] `ADMIN_WHATSAPP_NUMBER` está en formato `whatsapp:+53119975`
- [ ] Twilio está en estado ACTIVE
- [ ] El número de destino está verificado en Twilio

---

## 🔄 COMANDO DIARIO RÁPIDO

Para empezar a trabajar cada día:

```powershell
# 1. Abre PowerShell en la carpeta
cd $env:USERPROFILE\Desktop\rutacuba_backend

# 2. Activa ambiente
.\venv\Scripts\Activate.ps1

# 3. Inicia servidor
uvicorn main:app --reload

# 4. En otra terminal, abre VS Code
code .

# 5. Abre navegador
# http://localhost:8000/docs
```

---

## 🆘 TROUBLESHOOTING

### Error: "twilio module not found"
```powershell
pip install twilio
```

### Error: "TWILIO_ACCOUNT_SID not found"
```powershell
# Verifica que .env existe
ls .env

# Si no existe, créalo con los valores correctos
```

### Error: "No se envía WhatsApp"
```powershell
# Verifica en los logs de uvicorn:
# Busca: "Twilio no está configurado" o "Error enviando"

# Si dice "no está configurado":
# - Edita .env
# - Cambia tu_account_sid_aqui → TU ACCOUNT SID REAL
# - Cambia tu_auth_token_aqui → TU AUTH TOKEN REAL
# - Guarda (Ctrl+S)
# - Reinicia servidor (Ctrl+C y luego uvicorn main:app --reload)
```

---

## ✅ COMANDO FINAL DE VERIFICACIÓN

```powershell
# Cuando todo esté listo, ejecuta esto:

$checks = @(
    "models.py",
    "services.py", 
    "whatsapp_service.py",
    "schemas.py",
    ".env"
)

foreach ($file in $checks) {
    if (Test-Path $file) {
        Write-Host "✓ $file existe" -ForegroundColor Green
    } else {
        Write-Host "✗ $file NO ENCONTRADO" -ForegroundColor Red
    }
}
```

---

## 🎉 ¡LISTO!

Ya tienes:
✅ Notificaciones por WhatsApp al crear reservas
✅ Reporte financiero al completar viajes
✅ Cálculo automático de gasto de combustible
✅ Cálculo automático de salario del conductor
✅ Ganancia neta del viaje

**Próximo paso:** Lee `ACTUALIZACION_WHATSAPP_REPORTES.md` para entender cómo funciona.

---

**¡Tu sistema RutaCuba está completamente actualizado!** 🚀
