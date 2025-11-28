# 🚀 COMANDOS PARA EJECUTAR LA APLICACIÓN

## ⚡ INICIO RÁPIDO

### 1. Verificar que todo está correcto:
```powershell
.\venv\Scripts\python.exe manage.py check
```

### 2. Aplicar migraciones (si es necesario):
```powershell
.\venv\Scripts\python.exe manage.py migrate
```

### 3. Iniciar el servidor:
```powershell
.\venv\Scripts\python.exe manage.py runserver
```

### 4. Abrir en el navegador:
```
http://127.0.0.1:8000/login/
```

---

## 📋 COMANDOS COMPLETOS

### Verificar el proyecto:
```powershell
.\venv\Scripts\python.exe manage.py check
```

### Aplicar migraciones:
```powershell
.\venv\Scripts\python.exe manage.py migrate
```

### Crear superusuario (si no existe):
```powershell
.\venv\Scripts\python.exe manage.py createsuperuser
```

### Iniciar servidor de desarrollo:
```powershell
.\venv\Scripts\python.exe manage.py runserver
```

### Iniciar servidor en puerto específico:
```powershell
.\venv\Scripts\python.exe manage.py runserver 8000
```

### Iniciar servidor accesible desde red local:
```powershell
.\venv\Scripts\python.exe manage.py runserver 0.0.0.0:8000
```

### Compilar CSS de Tailwind (si haces cambios):
```powershell
.\venv\Scripts\python.exe manage.py tailwind start
```

---

## 🔧 COMANDOS ÚTILES

### Ver todas las migraciones pendientes:
```powershell
.\venv\Scripts\python.exe manage.py showmigrations
```

### Crear migraciones (si cambiaste modelos):
```powershell
.\venv\Scripts\python.exe manage.py makemigrations
```

### Abrir shell de Django:
```powershell
.\venv\Scripts\python.exe manage.py shell
```

### Recolectar archivos estáticos (producción):
```powershell
.\venv\Scripts\python.exe manage.py collectstatic
```

### Ejecutar script de encriptación de contraseñas:
```powershell
.\venv\Scripts\python.exe scripts\encrypt_existing_passwords.py
```

---

## 🌐 ACCESO A LA APLICACIÓN

**URL Local:**
```
http://127.0.0.1:8000/login/
```

**Credenciales por defecto:**
- Email: `admin@test.com`
- Password: `admin123`

---

## 🛑 DETENER EL SERVIDOR

Presiona `Ctrl + C` en la terminal donde está corriendo el servidor.

---

## 📝 NOTAS IMPORTANTES

1. **No necesitas activar el entorno virtual** si usas `.\venv\Scripts\python.exe` directamente
2. **El servidor se ejecuta en segundo plano** si usas `is_background: true`
3. **Para ver logs en tiempo real**, ejecuta el servidor en primer plano
4. **Si cambias código Python**, el servidor se recarga automáticamente
5. **Si cambias templates HTML**, recarga la página en el navegador

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### Error: "Port 8000 is already in use"
```powershell
# Usar otro puerto
.\venv\Scripts\python.exe manage.py runserver 8001
```

### Error: "Module not found"
```powershell
# Instalar dependencias
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Error: "No migrations to apply"
```powershell
# Crear migraciones primero
.\venv\Scripts\python.exe manage.py makemigrations
.\venv\Scripts\python.exe manage.py migrate
```

---

## ✅ VERIFICACIÓN RÁPIDA

Ejecuta estos comandos en orden:

```powershell
# 1. Verificar proyecto
.\venv\Scripts\python.exe manage.py check

# 2. Aplicar migraciones
.\venv\Scripts\python.exe manage.py migrate

# 3. Iniciar servidor
.\venv\Scripts\python.exe manage.py runserver
```

**Resultado esperado:**
```
System check identified no issues (0 silenced).
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

¡Listo para ejecutar! 🚀

