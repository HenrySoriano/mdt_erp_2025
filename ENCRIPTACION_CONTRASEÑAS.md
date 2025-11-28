# 🔐 ENCRIPTACIÓN DE CONTRASEÑAS IMPLEMENTADA

**Fecha:** 2025-11-27  
**Estado:** ✅ Implementado

---

## ✅ IMPLEMENTACIÓN COMPLETA

Se ha implementado encriptación de contraseñas usando **Fernet (symmetric encryption)** de la librería `cryptography`. Las contraseñas ahora se almacenan encriptadas en la base de datos y solo los **superusuarios** pueden verlas.

---

## 🔧 CAMBIOS REALIZADOS

### 1. ✅ Utilidades de Encriptación
**Archivo:** `apps/presentation/utils/encryption.py`

- `encrypt_password()` - Encripta contraseñas antes de guardar
- `decrypt_password()` - Desencripta contraseñas (solo para superusuarios)
- `generate_encryption_key()` - Genera nueva clave de encriptación
- `get_fernet()` - Obtiene instancia de Fernet con la clave

### 2. ✅ Modelo CustomUser Actualizado
**Archivo:** `apps/infrastructure/models/user.py`

- Método `set_stored_password()` - Encripta y guarda contraseñas
- Método `get_stored_password(user)` - Desencripta solo si el usuario es superusuario
- Signal `pre_save` - Encripta automáticamente antes de guardar
- Campo `stored_password` aumentado a 500 caracteres (para valores encriptados)

### 3. ✅ Formularios Actualizados
**Archivo:** `apps/presentation/forms.py`

- `CompanyForm` - Usa `set_stored_password()` en lugar de asignación directa
- `EmployeeForm` - Usa `set_stored_password()` en lugar de asignación directa

### 4. ✅ Vistas Actualizadas
**Archivo:** `apps/presentation/views/admin_views.py`

- `edit_company()` - Pasa contraseña desencriptada al template solo si es superusuario
- `edit_employee()` - Pasa contraseña desencriptada al template solo si es superusuario
- `employee_detail()` - Pasa contraseña desencriptada al template solo si es superusuario
- Todas las asignaciones de `stored_password` ahora usan `set_stored_password()`

### 5. ✅ Templates Actualizados
**Archivos:**
- `apps/presentation/templates/admin/company_form.html`
- `apps/presentation/templates/admin/employee_form.html`
- `apps/presentation/templates/admin/employee_detail.html`

**Cambios:**
- Solo muestran contraseñas si el usuario es superusuario
- Muestran mensaje de advertencia si no es superusuario
- Manejan errores de desencriptación

### 6. ✅ Script de Migración
**Archivo:** `scripts/encrypt_existing_passwords.py`

- Script para encriptar todas las contraseñas existentes en texto plano
- Detecta automáticamente si ya están encriptadas
- Reporta estadísticas del proceso

### 7. ✅ Dependencias
**Archivo:** `requirements.txt`

- Añadido `cryptography>=41.0.0`

---

## 📋 CONFIGURACIÓN REQUERIDA

### 1. Instalar dependencias:
```bash
pip install cryptography
```

### 2. Generar clave de encriptación:
```python
python -c "from apps.presentation.utils.encryption import generate_encryption_key; print(generate_encryption_key())"
```

### 3. Configurar variable de entorno:
```powershell
# Windows PowerShell
$env:ENCRYPTION_KEY="tu-clave-generada-aqui"

# Linux/Mac
export ENCRYPTION_KEY="tu-clave-generada-aqui"
```

**⚠️ IMPORTANTE:** 
- Guarda esta clave de forma segura
- Si pierdes la clave, NO podrás desencriptar las contraseñas existentes
- Usa la misma clave en todos los entornos (desarrollo, producción)

---

## 🚀 USO

### Encriptar contraseñas existentes:
```bash
python scripts/encrypt_existing_passwords.py
```

### En código:
```python
from apps.infrastructure.models import CustomUser

# Guardar contraseña (se encripta automáticamente)
user.set_stored_password("mi_contraseña")
user.save()

# Obtener contraseña (solo si eres superusuario)
password = user.get_stored_password(request.user)
if password:
    print(f"Contraseña: {password}")
else:
    print("No tienes permisos o no hay contraseña almacenada")
```

---

## 🔒 SEGURIDAD

### ✅ Ventajas:
1. **Contraseñas encriptadas** - No se almacenan en texto plano
2. **Acceso restringido** - Solo superusuarios pueden ver contraseñas
3. **Encriptación fuerte** - Usa Fernet (AES-128 en modo CBC)
4. **Clave externa** - La clave de encriptación no está en el código

### ⚠️ Consideraciones:
1. **Clave de encriptación** - Debe guardarse de forma segura
2. **Backup de clave** - Si se pierde, no se pueden recuperar contraseñas
3. **Rotación de claves** - Requiere re-encriptar todas las contraseñas

---

## 📝 NOTAS IMPORTANTES

1. **Primera ejecución:** Ejecuta `scripts/encrypt_existing_passwords.py` para encriptar contraseñas existentes
2. **Producción:** Configura `ENCRYPTION_KEY` como variable de entorno en producción
3. **Desarrollo:** Si no configuras `ENCRYPTION_KEY`, se generará una clave temporal (solo para desarrollo)
4. **Superusuarios:** Solo usuarios con `is_superuser=True` o `role='SUPERUSER'` pueden ver contraseñas

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### Error: "Clave de encriptación inválida"
- Verifica que `ENCRYPTION_KEY` esté configurada correctamente
- La clave debe ser una cadena base64 válida de 32 bytes

### Error: "No se puede desencriptar"
- Verifica que estés usando la misma clave con la que se encriptó
- Si cambiaste la clave, necesitas re-encriptar todas las contraseñas

### Las contraseñas no se muestran
- Verifica que el usuario sea superusuario (`is_superuser=True` o `role='SUPERUSER'`)
- Verifica que la contraseña esté almacenada (`stored_password` no está vacío)

---

## ✅ VERIFICACIÓN

Para verificar que todo funciona:

1. Crea un nuevo empleado o empresa
2. Verifica que la contraseña se guarde encriptada en la BD
3. Como superusuario, verifica que puedas ver la contraseña desencriptada
4. Como admin de empresa, verifica que NO puedas ver la contraseña

---

## 📚 REFERENCIAS

- [cryptography Fernet](https://cryptography.io/en/latest/fernet/)
- [Django Security Best Practices](https://docs.djangoproject.com/en/5.2/topics/security/)

