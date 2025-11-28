# 🚀 Guía de Inicio Rápido - MDT ERP 2025

## ⚠️ IMPORTANTE: Activación del Entorno Virtual

En Windows PowerShell, si obtienes un error de política de ejecución, usa una de estas opciones:

### Opción 1: Usar el archivo .bat (RECOMENDADO)
```cmd
.\venv\Scripts\activate.bat
```

O simplemente ejecuta:
```cmd
ACTIVAR_ENTORNO.bat
```

### Opción 2: Cambiar política de ejecución temporalmente (solo para esta sesión)
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\venv\Scripts\Activate.ps1
```

### Opción 3: Usar directamente python del venv (sin activar)
```powershell
.\venv\Scripts\python.exe manage.py runserver
.\venv\Scripts\python.exe manage.py tailwind start
```

---

## Pasos para Ejecutar el Proyecto

### 1️⃣ Activar Entorno Virtual
**Opción A (CMD o PowerShell con política cambiada):**
```cmd
.\venv\Scripts\activate.bat
```

**Opción B (PowerShell - cambiar política primero):**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\venv\Scripts\Activate.ps1
```

**Opción C (Sin activar - usar ruta completa):**
```powershell
.\venv\Scripts\python.exe manage.py [comando]
```

### 2️⃣ Aplicar Migraciones (solo primera vez o después de cambios)
```cmd
python manage.py migrate
```

### 3️⃣ Cargar Datos Iniciales (solo primera vez)
```cmd
python create_superuser_and_load_data.py
```

### 4️⃣ Iniciar Tailwind CSS (Terminal 1 - mantener abierta)
```cmd
python manage.py tailwind start
```
**Nota:** Mantén esta terminal abierta mientras desarrollas.

### 5️⃣ Iniciar Servidor Django (Terminal 2)
```cmd
python manage.py runserver
```

### 6️⃣ Acceder a la Aplicación
- **URL:** http://127.0.0.1:8000/login/
- **Credenciales:**
  - Email: `admin@test.com`
  - Password: `admin123`

### 7️⃣ Probar Funcionalidad Modal
- Haz clic en "📖 Explicación" en cualquier pregunta durante una evaluación

---

## 📝 Notas Importantes

- **Tailwind y Django deben ejecutarse en terminales separadas**
- Si cambias estilos CSS, Tailwind los compilará automáticamente
- La base de datos SQLite (`db.sqlite3`) ya contiene datos de prueba

---

## 🔧 Comandos Útiles

### Crear Superusuario Manualmente
```cmd
python manage.py createsuperuser
```

### Verificar Estado del Proyecto
```cmd
python manage.py check
```

### Compilar Tailwind para Producción
```cmd
python manage.py tailwind build
```

### Ver todas las opciones de Tailwind
```cmd
python manage.py tailwind --help
```

---

## ✅ Estado del Proyecto

- ✅ Entorno virtual configurado
- ✅ Rutas corregidas para nueva ubicación (C:\mdt_erp_2025)
- ✅ Python 3.12.8 configurado
- ✅ Dependencias instaladas
- ✅ Base de datos migrada
- ✅ Fixtures cargadas
- ✅ Superusuario creado

---

## 🐛 Solución de Problemas

### Error: "No se puede cargar el archivo Activate.ps1"
**Solución:** Usa `activate.bat` en lugar de `Activate.ps1`:
```cmd
.\venv\Scripts\activate.bat
```

### Error: "python no se reconoce como comando"
**Solución:** Asegúrate de haber activado el entorno virtual o usa la ruta completa:
```cmd
.\venv\Scripts\python.exe manage.py runserver
```
