#!/usr/bin/env python3
"""
Script de verificación post-despliegue para PythonAnywhere
Ejecutar después del despliegue para verificar que todo funciona correctamente
"""

import os
import sys
import django
from pathlib import Path

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.conf import settings
from django.db import connection
from django.contrib.auth import get_user_model
from django.core.management import call_command

User = get_user_model()

# Colores para output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")

def print_success(text):
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")

def print_error(text):
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

def print_warning(text):
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")

def print_info(text):
    print(f"{Colors.OKCYAN}ℹ {text}{Colors.ENDC}")

def check_django_settings():
    """Verificar configuración de Django"""
    print_header("Verificando Configuración de Django")
    
    checks = []
    
    # DEBUG
    if settings.DEBUG:
        print_warning(f"DEBUG está activado: {settings.DEBUG} (debería ser False en producción)")
        checks.append(False)
    else:
        print_success(f"DEBUG está desactivado: {settings.DEBUG}")
        checks.append(True)
    
    # SECRET_KEY
    if settings.SECRET_KEY and len(settings.SECRET_KEY) > 20:
        print_success(f"SECRET_KEY configurada (longitud: {len(settings.SECRET_KEY)})")
        checks.append(True)
    else:
        print_error("SECRET_KEY no está configurada o es muy corta")
        checks.append(False)
    
    # ALLOWED_HOSTS
    if settings.ALLOWED_HOSTS:
        print_success(f"ALLOWED_HOSTS configurado: {', '.join(settings.ALLOWED_HOSTS)}")
        checks.append(True)
    else:
        print_error("ALLOWED_HOSTS está vacío")
        checks.append(False)
    
    # CSRF_TRUSTED_ORIGINS
    if hasattr(settings, 'CSRF_TRUSTED_ORIGINS') and settings.CSRF_TRUSTED_ORIGINS:
        print_success(f"CSRF_TRUSTED_ORIGINS configurado: {', '.join(settings.CSRF_TRUSTED_ORIGINS)}")
        checks.append(True)
    else:
        print_warning("CSRF_TRUSTED_ORIGINS no está configurado")
        checks.append(False)
    
    # Seguridad
    if not settings.DEBUG:
        security_settings = [
            ('SECURE_SSL_REDIRECT', getattr(settings, 'SECURE_SSL_REDIRECT', None)),
            ('SESSION_COOKIE_SECURE', getattr(settings, 'SESSION_COOKIE_SECURE', None)),
            ('CSRF_COOKIE_SECURE', getattr(settings, 'CSRF_COOKIE_SECURE', None)),
        ]
        for name, value in security_settings:
            if value:
                print_success(f"{name}: {value}")
            else:
                print_warning(f"{name} no está configurado")
    
    return all(checks)

def check_database():
    """Verificar conexión a base de datos"""
    print_header("Verificando Base de Datos")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result:
                print_success("Conexión a base de datos exitosa")
                
                # Verificar tablas principales
                cursor.execute("SHOW TABLES")
                tables = [row[0] for row in cursor.fetchall()]
                required_tables = [
                    'infrastructure_customuser',
                    'infrastructure_company',
                    'infrastructure_employee',
                    'infrastructure_dimension',
                    'infrastructure_question',
                    'presentation_evaluation',
                    'presentation_response',
                ]
                
                missing_tables = [t for t in required_tables if t not in tables]
                if missing_tables:
                    print_error(f"Tablas faltantes: {', '.join(missing_tables)}")
                    return False
                else:
                    print_success(f"Todas las tablas requeridas existen ({len(tables)} tablas totales)")
                    return True
    except Exception as e:
        print_error(f"Error al conectar con la base de datos: {e}")
        return False

def check_static_files():
    """Verificar archivos estáticos"""
    print_header("Verificando Archivos Estáticos")
    
    static_root = Path(settings.STATIC_ROOT)
    if static_root.exists():
        static_files = list(static_root.rglob('*'))
        file_count = len([f for f in static_files if f.is_file()])
        print_success(f"Directorio STATIC_ROOT existe: {static_root}")
        print_info(f"Archivos estáticos encontrados: {file_count}")
        return True
    else:
        print_warning(f"STATIC_ROOT no existe: {static_root}")
        print_info("Ejecuta: python3.10 manage.py collectstatic --noinput")
        return False

def check_users():
    """Verificar usuarios"""
    print_header("Verificando Usuarios")
    
    try:
        total_users = User.objects.count()
        superusers = User.objects.filter(is_superuser=True).count()
        
        print_success(f"Total de usuarios: {total_users}")
        print_success(f"Superusuarios: {superusers}")
        
        if superusers == 0:
            print_warning("No hay superusuarios. Crea uno con: python3.10 manage.py createsuperuser")
            return False
        
        return True
    except Exception as e:
        print_error(f"Error al verificar usuarios: {e}")
        return False

def check_migrations():
    """Verificar migraciones"""
    print_header("Verificando Migraciones")
    
    try:
        # Verificar migraciones pendientes
        from django.core.management import call_command
        from io import StringIO
        
        output = StringIO()
        call_command('showmigrations', '--plan', stdout=output)
        output.seek(0)
        migrations_output = output.read()
        
        if '[ ]' in migrations_output:
            print_warning("Hay migraciones pendientes")
            print_info("Ejecuta: python3.10 manage.py migrate")
            return False
        else:
            print_success("Todas las migraciones están aplicadas")
            return True
    except Exception as e:
        print_error(f"Error al verificar migraciones: {e}")
        return False

def main():
    """Ejecutar todas las verificaciones"""
    print_header("VERIFICACIÓN POST-DESPLEGUE - PythonAnywhere")
    
    results = []
    
    results.append(("Configuración Django", check_django_settings()))
    results.append(("Base de Datos", check_database()))
    results.append(("Archivos Estáticos", check_static_files()))
    results.append(("Usuarios", check_users()))
    results.append(("Migraciones", check_migrations()))
    
    # Resumen
    print_header("RESUMEN")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        if result:
            print_success(f"{name}: OK")
        else:
            print_error(f"{name}: FALLO")
    
    print(f"\n{Colors.BOLD}Resultado: {passed}/{total} verificaciones pasadas{Colors.ENDC}\n")
    
    if passed == total:
        print_success("¡Todas las verificaciones pasaron! El despliegue está completo.")
        return 0
    else:
        print_warning("Algunas verificaciones fallaron. Revisa los mensajes anteriores.")
        return 1

if __name__ == '__main__':
    sys.exit(main())


