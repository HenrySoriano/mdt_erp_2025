# 🚀 Cómo Ejecutar el Proyecto en PowerShell

## ⚠️ Problema con Activate.ps1

En PowerShell, `activate.bat` no funciona y `Activate.ps1` puede estar bloqueado por políticas de seguridad.

## ✅ Soluciones Prácticas

### Opción 1: Usar Scripts PowerShell (RECOMENDADO)

He creado dos scripts para facilitar el inicio:

**Terminal 1 - Tailwind:**
```powershell
.\INICIAR_TAILWIND.ps1
```

**Terminal 2 - Servidor Django:**
```powershell
.\INICIAR_SERVIDOR.ps1
```

### Opción 2: Usar Comandos Directos (Sin Activar)

**Terminal 1 - Tailwind:**
```powershell
.\venv\Scripts\python.exe manage.py tailwind start
```

**Terminal 2 - Servidor Django:**
```powershell
.\venv\Scripts\python.exe manage.py runserver
```

### Opción 3: Usar CMD en lugar de PowerShell

Abre **CMD** (no PowerShell) y ejecuta:
```cmd
.\venv\Scripts\activate.bat
python manage.py tailwind start
```

Y en otra ventana CMD:
```cmd
.\venv\Scripts\activate.bat
python manage.py runserver
```

---

## 📋 Pasos Completos

### 1. Verificar que todo está listo
```powershell
.\venv\Scripts\python.exe manage.py check
```

### 2. Iniciar Tailwind (Terminal 1)
```powershell
.\INICIAR_TAILWIND.ps1
```
O directamente:
```powershell
.\venv\Scripts\python.exe manage.py tailwind start
```

### 3. Iniciar Servidor (Terminal 2)
```powershell
.\INICIAR_SERVIDOR.ps1
```
O directamente:
```powershell
.\venv\Scripts\python.exe manage.py runserver
```

### 4. Acceder a la aplicación
- URL: http://127.0.0.1:8000/login/
- Email: `admin@test.com`
- Password: `admin123`

---

## 🔧 Otros Comandos Útiles

### Migraciones
```powershell
.\venv\Scripts\python.exe manage.py migrate
```

### Cargar datos iniciales
```powershell
.\venv\Scripts\python.exe create_superuser_and_load_data.py
```

### Crear superusuario
```powershell
.\venv\Scripts\python.exe manage.py createsuperuser
```

### Verificar estado
```powershell
.\venv\Scripts\python.exe manage.py check
```

---

## 💡 Nota Importante

**No necesitas activar el entorno virtual** si usas la ruta completa `.\venv\Scripts\python.exe`. Esto funciona perfectamente y evita problemas con las políticas de PowerShell.

