# 🔐 CONFIGURAR ENCRIPTACIÓN DE CONTRASEÑAS

## ✅ ENCRIPTACIÓN COMPLETADA

**Resultado del script:**
- ✅ **12 contraseñas encriptadas exitosamente**
- ✅ **0 errores**
- ✅ Todas las contraseñas existentes ahora están encriptadas

---

## 🔑 CONFIGURAR CLAVE DE ENCRIPTACIÓN PERMANENTE

### ⚠️ IMPORTANTE:
Actualmente se está usando una **clave temporal** generada automáticamente. Para producción, debes configurar una clave permanente.

### 1. Generar Clave de Encriptación:

Ejecuta este comando para generar una clave:
```powershell
.\venv\Scripts\python.exe -c "from apps.presentation.utils.encryption import generate_encryption_key; print(generate_encryption_key())"
```

### 2. Configurar Variable de Entorno:

#### En Desarrollo (Windows PowerShell):
```powershell
$env:ENCRYPTION_KEY="tu-clave-generada-aqui"
```

#### En Producción:
Configura la variable de entorno `ENCRYPTION_KEY` en tu servidor/hosting.

---

## ⚠️ ADVERTENCIA CRÍTICA

**Si cambias la clave de encriptación:**
- ❌ **NO podrás desencriptar las contraseñas existentes**
- ✅ Las nuevas contraseñas se encriptarán con la nueva clave
- ⚠️ Las contraseñas antiguas quedarán inaccesibles

**Recomendación:**
- Usa la misma clave en desarrollo y producción
- Guarda la clave de forma segura
- Si pierdes la clave, necesitarás resetear todas las contraseñas

---

## ✅ VERIFICAR ENCRIPTACIÓN

### Verificar en la Base de Datos:
Las contraseñas encriptadas tienen estas características:
- Son cadenas largas (más de 50 caracteres)
- Contienen caracteres base64 (A-Z, a-z, 0-9, +, /, =)
- Ejemplo: `gAAAAABl...` (mucho más largo)

### Verificar en la Aplicación:
1. Inicia sesión como superusuario
2. Ve a **Empleados** > Selecciona un empleado
3. Deberías ver la contraseña desencriptada
4. Si no aparece, verifica que:
   - Estás logueado como superusuario
   - La clave de encriptación está configurada correctamente

---

## 🔄 RE-ENCRIPTAR CON NUEVA CLAVE

Si necesitas cambiar la clave de encriptación:

1. **Configura la nueva clave:**
   ```powershell
   $env:ENCRYPTION_KEY="nueva-clave-aqui"
   ```

2. **Ejecuta el script de encriptación nuevamente:**
   ```powershell
   .\venv\Scripts\python.exe scripts\encrypt_existing_passwords.py
   ```

3. **El script detectará automáticamente:**
   - Contraseñas encriptadas con la clave antigua (las re-encriptará)
   - Contraseñas ya encriptadas con la nueva clave (las dejará igual)

---

## 📋 RESUMEN

✅ **Estado Actual:**
- 12 contraseñas encriptadas
- Usando clave temporal (funciona en desarrollo)
- Listo para usar

⚠️ **Para Producción:**
- Genera una clave permanente
- Configúrala como variable de entorno
- Guárdala de forma segura

---

## 🎯 SIGUIENTE PASO

**Opcional:** Genera y configura una clave permanente para producción:

```powershell
# Generar clave
.\venv\Scripts\python.exe -c "from apps.presentation.utils.encryption import generate_encryption_key; print(generate_encryption_key())"

# Configurar (copia la clave generada)
$env:ENCRYPTION_KEY="clave-generada-aqui"
```

¡Las contraseñas están encriptadas y seguras! 🔒

