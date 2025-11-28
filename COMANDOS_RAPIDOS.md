# ⚡ COMANDOS RÁPIDOS PARA PROBAR LA APLICACIÓN

## 🎯 SOLUCIÓN AL PROBLEMA DE POWERSHELL

**Problema**: PowerShell bloquea scripts `.ps1` por seguridad.

**Solución**: Usar Python directamente **SIN activar el entorno virtual**.

---

## ✅ COMANDOS QUE FUNCIONAN (SIN ACTIVAR)

### 1. Verificar el proyecto:
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

### 4. Cargar datos iniciales (si es necesario):
```powershell
.\venv\Scripts\python.exe scripts\create_superuser_and_load_data.py
```

---

## 🔄 ALTERNATIVA: Cambiar Política de Ejecución (Solo esta sesión)

Si prefieres activar el entorno, ejecuta primero:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\venv\Scripts\Activate.ps1
```

Luego puedes usar:
```powershell
python manage.py check
python manage.py runserver
```

**Nota**: Esta política solo afecta la sesión actual de PowerShell.

---

## 🚀 INICIO RÁPIDO (Recomendado)

### Terminal 1 - Verificar y ejecutar servidor:
```powershell
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py runserver
```

### Terminal 2 - Tailwind (solo si necesitas recompilar CSS):
```powershell
.\venv\Scripts\python.exe manage.py tailwind start
```

---

## 🌐 ACCESO A LA APLICACIÓN

- **URL**: http://127.0.0.1:8000/login/
- **Usuario**: admin@test.com
- **Contraseña**: admin123

---

## 📝 NOTA IMPORTANTE

**No necesitas activar el entorno virtual** si usas la ruta completa `.\venv\Scripts\python.exe`. Esto funciona perfectamente y evita problemas con las políticas de PowerShell.

---

## ✅ VERIFICACIÓN RÁPIDA

Ejecuta este comando para verificar que todo funciona:

```powershell
.\venv\Scripts\python.exe manage.py check
```

**Resultado esperado**: `System check identified no issues (0 silenced).`


