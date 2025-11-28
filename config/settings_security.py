"""
Configuración de seguridad para producción
Importar estas configuraciones en settings.py cuando DEBUG=False
"""
import os
from django.core.exceptions import ImproperlyConfigured

def get_env_variable(var_name, default=None):
    """Obtiene una variable de entorno o lanza error si no existe"""
    try:
        return os.environ[var_name]
    except KeyError:
        if default is not None:
            return default
        error_msg = f"Set the {var_name} environment variable"
        raise ImproperlyConfigured(error_msg)


# SECURITY SETTINGS
SECURE_SSL_REDIRECT = True  # Redirigir HTTP a HTTPS (requiere SSL)
SESSION_COOKIE_SECURE = True  # Solo enviar cookies por HTTPS
CSRF_COOKIE_SECURE = True  # Solo enviar CSRF cookies por HTTPS
SECURE_BROWSER_XSS_FILTER = True  # Activar filtro XSS del navegador
SECURE_CONTENT_TYPE_NOSNIFF = True  # Prevenir MIME type sniffing
X_FRAME_OPTIONS = 'DENY'  # Prevenir clickjacking
SECURE_HSTS_SECONDS = 31536000  # 1 año
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Configuración de sesiones
SESSION_COOKIE_HTTPONLY = True  # Prevenir acceso a cookies via JavaScript
SESSION_COOKIE_SAMESITE = 'Strict'  # Prevenir CSRF

# Configuración de CSRF
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Strict'
CSRF_TRUSTED_ORIGINS = [
    # Añadir aquí los dominios permitidos
    # Ejemplo: 'https://tudominio.com',
]

# Headers de seguridad adicionales
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# Configuración de contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 12,  # Mínimo 12 caracteres
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Rate limiting (requiere django-ratelimit)
# RATELIMIT_ENABLE = True
# RATELIMIT_USE_CACHE = 'default'

# Logging de seguridad
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'security_file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': 'logs/security.log',
            'formatters': ['verbose'],
        },
    },
    'loggers': {
        'django.security': {
            'handlers': ['security_file'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}

