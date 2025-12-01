"""
Configuración específica para PythonAnywhere
Este archivo se carga automáticamente cuando detecta PYTHONANYWHERE_DOMAIN
"""
from .settings import *
import os

# Obtener el nombre de usuario de PythonAnywhere
PA_USERNAME = os.environ.get('USER', '')

# Base de datos MySQL de PythonAnywhere
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', f'{PA_USERNAME}$default'),
        'USER': os.environ.get('DB_USER', PA_USERNAME),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('MYSQL_HOST', f'{PA_USERNAME}.mysql.pythonanywhere-services.com'),
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}

# Archivos estáticos
STATIC_ROOT = f'/home/{PA_USERNAME}/mdt_erp_2025/staticfiles'
STATIC_URL = '/static/'

# Archivos de media
MEDIA_ROOT = f'/home/{PA_USERNAME}/mdt_erp_2025/media'
MEDIA_URL = '/media/'

# Hosts permitidos
ALLOWED_HOSTS = [f'{PA_USERNAME}.pythonanywhere.com']

# Debug desactivado en producción
DEBUG = False

# Configuración de seguridad
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Strict'
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Strict'

# CSRF trusted origins
CSRF_TRUSTED_ORIGINS = [f'https://{PA_USERNAME}.pythonanywhere.com']

