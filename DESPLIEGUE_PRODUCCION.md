# 🚀 Guía de Despliegue a Producción - PythonAnywhere

## 📋 Pre-requisitos

1. ✅ Cuenta de PythonAnywhere creada
2. ✅ Base de datos MySQL creada en PythonAnywhere
3. ✅ Código del proyecto listo para producción
4. ✅ Variables de entorno preparadas

---

## 🔧 Paso 1: Subir Código a PythonAnywhere

### Opción A: Usando Git (Recomendado)
```bash
# En la consola web de PythonAnywhere
cd ~
git clone https://github.com/tu-usuario/tu-repositorio.git mdt_erp_2025
cd mdt_erp_2025
```

### Opción B: Subir manualmente
1. Comprime el proyecto (excluyendo `venv/`, `__pycache__/`, `db.sqlite3`, `.env`)
2. Sube el archivo ZIP a PythonAnywhere
3. Descomprime en `~/mdt_erp_2025`

---

## 🔐 Paso 2: Configurar Variables de Entorno

### Opción A: Usando el script interactivo
```bash
cd ~/mdt_erp_2025
bash scripts/configurar_variables_entorno.sh
```

### Opción B: Manualmente
```bash
# Generar SECRET_KEY
python3.10 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Generar ENCRYPTION_KEY
python3.10 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode('utf-8'))"

# Configurar variables (reemplaza 'tuusuario' con tu usuario)
export DJANGO_SECRET_KEY='tu-secret-key-generado'
export DJANGO_DEBUG='False'
export DJANGO_ALLOWED_HOSTS='tuusuario.pythonanywhere.com'
export DJANGO_CSRF_TRUSTED_ORIGINS='https://tuusuario.pythonanywhere.com'
export DB_NAME='tuusuario$default'
export DB_USER='tuusuario'
export DB_PASSWORD='tu-password-mysql'
export DB_HOST='tuusuario.mysql.pythonanywhere-services.com'
export DB_PORT='3306'
```

**⚠️ IMPORTANTE:** Para que las variables persistan, guárdalas en `~/.bashrc` o crea un archivo `.env`:

```bash
# Crear archivo .env
nano ~/mdt_erp_2025/.env
# Pega las variables en formato KEY=value
# Guarda con Ctrl+O, Enter, Ctrl+X
```

---

## 📦 Paso 3: Instalar Dependencias

```bash
cd ~/mdt_erp_2025
pip3.10 install --user -r requirements.txt
```

**Nota sobre Playwright:**
- Playwright puede no funcionar en el plan gratuito de PythonAnywhere
- Si necesitas Playwright, considera el plan Beginner ($5/mes)
- Para instalar: `playwright install chromium` (solo si tienes plan pago)

---

## 🗄️ Paso 4: Configurar Base de Datos

### 4.1 Crear base de datos MySQL
1. Ve a la pestaña "Databases" en PythonAnywhere
2. Crea una base de datos MySQL
3. Anota el nombre (será `tuusuario$default`)

### 4.2 Ejecutar migraciones
```bash
cd ~/mdt_erp_2025
python3.10 manage.py migrate
```

### 4.3 Cargar datos iniciales (si aplica)
```bash
python3.10 manage.py loaddata apps/infrastructure/fixtures/dimensions.json
python3.10 manage.py loaddata apps/infrastructure/fixtures/questions.json
```

### 4.4 Crear superusuario
```bash
python3.10 manage.py createsuperuser
```

---

## 📁 Paso 5: Configurar Archivos Estáticos

```bash
cd ~/mdt_erp_2025
python3.10 manage.py collectstatic --noinput
```

Esto creará los archivos estáticos en `~/mdt_erp_2025/staticfiles`

---

## 🌐 Paso 6: Configurar Web App

1. Ve a la pestaña **"Web"** en PythonAnywhere
2. Haz clic en **"Add a new web app"** (si es primera vez) o edita la existente
3. Selecciona **"Manual configuration"** → **"Python 3.10"**

### 6.1 Configurar WSGI
1. Haz clic en el enlace del archivo WSGI
2. Reemplaza TODO el contenido con:

```python
import os
import sys

path = '/home/tuusuario/mdt_erp_2025'  # ⚠️ CAMBIA 'tuusuario' por tu usuario
if path not in sys.path:
    sys.path.append(path)

os.chdir(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

# Cargar variables de entorno desde .env si existe
from pathlib import Path
env_file = Path(path) / '.env'
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

3. Guarda el archivo

### 6.2 Configurar Rutas Estáticas
En la sección **"Static files"** de la Web App:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/tuusuario/mdt_erp_2025/staticfiles` |
| `/media/` | `/home/tuusuario/mdt_erp_2025/media` |

⚠️ **CAMBIA 'tuusuario' por tu usuario de PythonAnywhere**

---

## ✅ Paso 7: Verificar y Reiniciar

1. Haz clic en el botón verde **"Reload"** en la pestaña Web
2. Espera unos segundos
3. Accede a tu sitio: `https://tuusuario.pythonanywhere.com`

---

## 🧪 Paso 8: Verificación Post-Despliegue

### Checklist de Verificación:
- [ ] El sitio carga sin errores
- [ ] Login funciona correctamente
- [ ] Archivos estáticos se cargan (CSS, JS, imágenes)
- [ ] HTTPS funciona (certificado SSL automático)
- [ ] No hay errores en la consola del navegador
- [ ] Dashboard carga correctamente
- [ ] Crear/editar empresas funciona
- [ ] Crear/editar empleados funciona
- [ ] Evaluaciones funcionan
- [ ] Generación de PDF funciona
- [ ] Generación de PowerPoint funciona (si Playwright está disponible)

### Verificar Logs:
```bash
# Ver logs de errores
tail -f ~/mdt_erp_2025/logs/django_errors.log

# Ver logs generales
tail -f ~/mdt_erp_2025/logs/django.log
```

---

## 🔄 Actualizaciones Futuras

### Cuando hagas cambios en el código:
```bash
cd ~/mdt_erp_2025
git pull  # Si usas Git
# O sube los archivos nuevos manualmente

# Si hay nuevas migraciones
python3.10 manage.py migrate

# Si hay cambios en archivos estáticos
python3.10 manage.py collectstatic --noinput

# Reiniciar aplicación
# Ve a la pestaña Web → Haz clic en "Reload"
```

---

## 🐛 Solución de Problemas Comunes

### Error: "ModuleNotFoundError"
```bash
pip3.10 install --user nombre-del-modulo
```

### Error: "Static files not found"
```bash
python3.10 manage.py collectstatic --noinput
# Verifica que las rutas estén configuradas en Web App
```

### Error: "Database connection failed"
- Verifica variables de entorno (`DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`)
- Verifica que la base de datos exista en PythonAnywhere
- Verifica credenciales en la pestaña "Databases"

### Error 500: Internal Server Error
- Revisa logs: `tail -f ~/mdt_erp_2025/logs/django_errors.log`
- Verifica que `DEBUG=False` en producción
- Verifica que todas las variables de entorno estén configuradas
- Revisa la configuración de WSGI

### Error: "CSRF verification failed"
- Verifica `DJANGO_CSRF_TRUSTED_ORIGINS` incluye `https://tuusuario.pythonanywhere.com`
- Verifica que `CSRF_COOKIE_SECURE=True` en producción

---

## 📞 Soporte

Si encuentras problemas:
1. Revisa los logs en `~/mdt_erp_2025/logs/`
2. Revisa los logs de PythonAnywhere en la pestaña "Web" → "Error log"
3. Verifica que todas las variables de entorno estén configuradas
4. Verifica que la base de datos esté accesible

---

## ✅ Checklist Final

- [ ] Código subido a PythonAnywhere
- [ ] Variables de entorno configuradas
- [ ] Dependencias instaladas
- [ ] Base de datos configurada y migraciones ejecutadas
- [ ] Superusuario creado
- [ ] Archivos estáticos recopilados
- [ ] Web App configurada (WSGI y rutas estáticas)
- [ ] Aplicación reiniciada
- [ ] Sitio accesible y funcionando
- [ ] Todas las funcionalidades probadas

---

**¡Despliegue completado! 🎉**


