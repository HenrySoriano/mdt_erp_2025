# ✅ Solución para PowerShell - Activación del Entorno Virtual

## 🔴 Problema Identificado

Cuando ejecutas `activate.bat` o `ACTIVAR_ENTORNO.bat` en PowerShell, el mensaje dice "activado" pero **NO se activa realmente** porque los scripts `.bat` se ejecutan en un subproceso separado.

## ✅ Soluciones que Funcionan

### Opción 1: Script PowerShell Personalizado (RECOMENDADO)

He creado `activar.ps1` que funciona correctamente:

```powershell
. .\activar.ps1
```

**Nota:** El punto (`.`) al inicio es importante - significa "ejecutar en el contexto actual"

Después de esto, verás `(venv)` en tu prompt y podrás usar:
```powershell
python manage.py runserver
python manage.py tailwind start
```

### Opción 2: Usar Comandos Directos (MÁS SIMPLE - Sin Activar)

**No necesitas activar el entorno** si usas la ruta completa:

**Terminal 1 - Tailwind:**
```powershell
.\venv\Scripts\python.exe manage.py tailwind start
```

**Terminal 2 - Servidor Django:**
```powershell
.\venv\Scripts\python.exe manage.py runserver
```

### Opción 3: Cambiar Política y Usar Activate.ps1 Original

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\venv\Scripts\Activate.ps1
```

Si esto funciona, verás `(venv)` en tu prompt.

### Opción 4: Usar CMD en lugar de PowerShell

Abre **CMD** (no PowerShell):
```cmd
.\venv\Scripts\activate.bat
python manage.py runserver
```

---

## 🎯 Recomendación

**Para desarrollo diario, usa la Opción 2** (comandos directos). Es más simple y evita problemas con políticas de PowerShell.

---

## 📋 Ejemplo Completo de Uso

### Iniciar el Proyecto (2 terminales)

**Terminal 1:**
```powershell
.\venv\Scripts\python.exe manage.py tailwind start
```

**Terminal 2:**
```powershell
.\venv\Scripts\python.exe manage.py runserver
```

**Acceder:** http://127.0.0.1:8000/login/

---

## 🔍 Verificar si el Entorno está Activo

Ejecuta esto para verificar:
```powershell
$env:VIRTUAL_ENV
```

Si muestra la ruta al venv, está activado. Si está vacío, no está activado.

---

## 💡 Nota Final

**No es necesario activar el entorno virtual** si usas `.\venv\Scripts\python.exe` directamente. Ambos métodos funcionan igual de bien.
