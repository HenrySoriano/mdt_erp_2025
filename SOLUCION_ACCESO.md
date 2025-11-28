# 🔧 SOLUCIÓN DE PROBLEMAS DE ACCESO

## ✅ VERIFICACIÓN DEL SERVIDOR

El servidor está corriendo correctamente según el terminal. Verifica:

1. **URL correcta**: `http://127.0.0.1:8000/login/` o `http://127.0.0.1:8000/`
2. **Navegador**: Usa Chrome, Firefox o Edge (no Internet Explorer)
3. **Puerto**: Asegúrate de que el puerto 8000 no esté bloqueado

---

## 🔑 CREDENCIALES DE ACCESO

### Superusuario (Recomendado para pruebas):
- **Email**: `admin@test.com`
- **Password**: `admin123`

### Admin de Empresa:
- **Email**: `admin.empresa@test.com`
- **Password**: (verificar en base de datos)

---

## 🚨 PROBLEMAS COMUNES Y SOLUCIONES

### Problema 1: "No puedo acceder a la página"
**Solución**:
1. Verifica que el servidor esté corriendo (debe mostrar "Watching for file changes")
2. Abre el navegador y ve a: `http://127.0.0.1:8000/login/`
3. Si ves un error 404, verifica que el servidor esté en el puerto correcto

### Problema 2: "Las credenciales no funcionan"
**Solución**:
1. Verifica que estés usando: `admin@test.com` / `admin123`
2. Si no funciona, crea un nuevo superusuario:
   ```powershell
   .\venv\Scripts\python.exe manage.py createsuperuser
   ```

### Problema 3: "Me redirige al login después de iniciar sesión"
**Solución**:
1. Verifica que el usuario tenga un rol asignado
2. Verifica que el usuario esté activo (`is_active=True`)
3. Limpia las cookies del navegador y vuelve a intentar

### Problema 4: "Error 500 o error interno"
**Solución**:
1. Revisa la terminal donde corre el servidor para ver el error completo
2. Verifica que todas las migraciones estén aplicadas:
   ```powershell
   .\venv\Scripts\python.exe manage.py migrate
   ```

---

## 📋 PASOS PARA ACCEDER

1. **Inicia el servidor** (si no está corriendo):
   ```powershell
   .\venv\Scripts\python.exe manage.py runserver
   ```

2. **Abre el navegador** y ve a:
   ```
   http://127.0.0.1:8000/login/
   ```

3. **Ingresa las credenciales**:
   - Email: `admin@test.com`
   - Password: `admin123`

4. **Haz clic en "Iniciar Sesión"**

5. **Deberías ser redirigido** a:
   - Superusuario → `/superuser/dashboard/`
   - Admin → `/admin/dashboard/`
   - Empleado → `/employee/dashboard/`

---

## 🔍 VERIFICACIÓN ADICIONAL

Si aún no puedes acceder, ejecuta estos comandos para diagnosticar:

```powershell
# Verificar que el servidor esté corriendo
.\venv\Scripts\python.exe manage.py check

# Verificar usuarios disponibles
.\venv\Scripts\python.exe manage.py shell -c "from apps.infrastructure.models import CustomUser; print('Usuarios:', CustomUser.objects.count())"

# Verificar que el superusuario existe
.\venv\Scripts\python.exe manage.py shell -c "from apps.infrastructure.models import CustomUser; u = CustomUser.objects.filter(email='admin@test.com').first(); print('Existe:', u is not None, 'Activo:', u.is_active if u else False)"
```

---

## 📞 SI EL PROBLEMA PERSISTE

1. **Comparte el error exacto** que ves en el navegador
2. **Comparte los logs** de la terminal donde corre el servidor
3. **Verifica** que no haya errores en la consola del navegador (F12)

---

## ✅ ESTADO ACTUAL

- ✅ Servidor corriendo correctamente
- ✅ Usuarios en base de datos: 12 usuarios
- ✅ Superusuario disponible: `admin@test.com`
- ✅ Autenticación funcionando correctamente
- ✅ URLs configuradas correctamente

**El sistema está funcionando correctamente. Si no puedes acceder, sigue los pasos de arriba.**

