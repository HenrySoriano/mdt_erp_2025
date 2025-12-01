"""
Configuración adicional para producción
Se carga automáticamente cuando DEBUG=False
"""
from .settings import *
import os
import logging
from logging.handlers import RotatingFileHandler

# ============================================
# EMAIL CONFIGURATION
# ============================================
# Configurar servidor SMTP para producción
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = get_env_variable('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = int(get_env_variable('EMAIL_PORT', default='587'))
EMAIL_USE_TLS = get_env_variable('EMAIL_USE_TLS', default='True').lower() == 'true'
EMAIL_HOST_USER = get_env_variable('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = get_env_variable('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = get_env_variable('DEFAULT_FROM_EMAIL', default='noreply@tudominio.com')
SERVER_EMAIL = get_env_variable('SERVER_EMAIL', default=DEFAULT_FROM_EMAIL)

# ============================================
# LOGGING CONFIGURATION
# ============================================
LOGGING_DIR = BASE_DIR / 'logs'
LOGGING_DIR.mkdir(exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGGING_DIR / 'django.log',
            'maxBytes': 1024 * 1024 * 15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGGING_DIR / 'django_errors.log',
            'maxBytes': 1024 * 1024 * 15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['error_file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['error_file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'apps': {
            'handlers': ['file', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# ============================================
# PERFORMANCE OPTIMIZATIONS
# ============================================
# Caché (opcional - descomentar si instalas Redis/Memcached)
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.redis.RedisCache',
#         'LOCATION': get_env_variable('REDIS_URL', default='redis://127.0.0.1:6379/1'),
#     }
# }

# ============================================
# SECURITY ADDITIONAL SETTINGS
# ============================================
# Timeout de sesión (8 horas)
SESSION_COOKIE_AGE = 28800
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# ============================================
# FILE UPLOAD SETTINGS
# ============================================
# Límite de tamaño de archivos subidos (10MB)
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB

# ============================================
# ADMIN CONFIGURATION
# ============================================
ADMINS = [
    ('Admin', get_env_variable('ADMIN_EMAIL', default='admin@tudominio.com')),
]

MANAGERS = ADMINS

