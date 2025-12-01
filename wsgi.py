"""
Archivo WSGI para PythonAnywhere
Configura este archivo en la sección "WSGI configuration file" de tu Web App
"""
import os
import sys

# Ruta al proyecto (ajusta 'tuusuario' con tu nombre de usuario de PythonAnywhere)
path = '/home/tuusuario/mdt_erp_2025'
if path not in sys.path:
    sys.path.append(path)

# Cambiar al directorio del proyecto
os.chdir(path)

# Configurar Django settings module
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

# Importar aplicación WSGI de Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


