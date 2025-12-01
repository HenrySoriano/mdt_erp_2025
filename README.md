# Sistema de Evaluación de Riesgo Psicosocial

Sistema web desarrollado en Django para la evaluación y gestión de riesgo psicosocial en empresas.

## 🚀 Inicio Rápido

### Desarrollo Local

1. **Activar entorno virtual:**
```bash
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Windows CMD
venv\Scripts\activate.bat
```

2. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

3. **Configurar base de datos:**
```bash
# Configurar variables de entorno (opcional)
$env:USE_MYSQL_LOCAL="True"
$env:DB_NAME="mdt_erp_dev"
$env:DB_USER="root"
$env:DB_PASSWORD=""

# Ejecutar migraciones
python manage.py migrate

# Cargar datos iniciales
python manage.py loaddata apps/infrastructure/fixtures/dimensions.json
python manage.py loaddata apps/infrastructure/fixtures/questions.json

# Crear superusuario
python manage.py createsuperuser
```

4. **Iniciar servidor:**
```bash
python manage.py runserver
```

5. **Acceder a la aplicación:**
- URL: http://127.0.0.1:8000
- Login: http://127.0.0.1:8000/login/

### Scripts de Desarrollo

- `scripts/iniciar_desarrollo.ps1` - Inicia servidor Django y Tailwind
- `scripts/crear_usuarios_iniciales.py` - Crea usuarios de prueba
- `scripts/cargar_datos_iniciales.py` - Carga datos iniciales

## 📦 Despliegue a Producción

### PythonAnywhere

Consulta la guía completa en: **`DESPLIEGUE_PRODUCCION.md`**

**Pasos rápidos:**
1. Subir código a PythonAnywhere
2. Configurar variables de entorno: `bash scripts/configurar_variables_entorno.sh`
3. Instalar dependencias: `pip3.10 install --user -r requirements.txt`
4. Ejecutar migraciones: `python3.10 manage.py migrate`
5. Recopilar estáticos: `python3.10 manage.py collectstatic --noinput`
6. Configurar Web App (WSGI y rutas estáticas)
7. Verificar: `python3.10 scripts/verificar_produccion.py`

### Variables de Entorno Requeridas

```bash
DJANGO_SECRET_KEY=...
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=tuusuario.pythonanywhere.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://tuusuario.pythonanywhere.com
DB_NAME=tuusuario$default
DB_USER=tuusuario
DB_PASSWORD=...
DB_HOST=tuusuario.mysql.pythonanywhere-services.com
DB_PORT=3306
```

## 📁 Estructura del Proyecto

```
mdt_erp_2025/
├── apps/
│   ├── infrastructure/     # Modelos y lógica de negocio
│   └── presentation/        # Vistas y templates
├── config/                  # Configuración Django
├── theme/                   # Tema Tailwind CSS
├── scripts/                 # Scripts de utilidad
├── manage.py               # Script de gestión Django
├── requirements.txt        # Dependencias Python
└── wsgi.py                 # Configuración WSGI para producción
```

## 🔧 Tecnologías

- **Backend:** Django 5.2.8
- **Base de Datos:** MySQL/MariaDB
- **Frontend:** Tailwind CSS
- **Generación de Documentos:** python-pptx, reportlab
- **Gráficos:** Chart.js
- **Automatización:** Playwright

## 📚 Documentación

- **Despliegue:** `DESPLIEGUE_PRODUCCION.md` - Guía completa de despliegue
- **Checklist:** `CHECKLIST_PRODUCCION_PYTHONANYWHERE.md` - Checklist de producción

## 🔐 Seguridad

- Contraseñas encriptadas con Fernet (cryptography)
- Variables de entorno para configuración sensible
- Configuración de seguridad habilitada en producción (SSL, CSRF, HSTS)
- Validación de acceso por empresa

## 📝 Licencia

Proyecto privado - Todos los derechos reservados

