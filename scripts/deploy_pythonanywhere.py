#!/usr/bin/env python3
"""
Script de despliegue automatizado para PythonAnywhere
Ejecutar en la consola web de PythonAnywhere después de subir el código
"""

import os
import sys
import subprocess
import getpass
from pathlib import Path

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

def run_command(command, check=True, capture_output=False):
    """Ejecuta un comando y retorna el resultado"""
    try:
        if capture_output:
            result = subprocess.run(
                command,
                shell=True,
                check=check,
                capture_output=True,
                text=True,
                cwd=BASE_DIR
            )
            return result.stdout.strip(), result.stderr.strip(), result.returncode
        else:
            result = subprocess.run(
                command,
                shell=True,
                check=check,
                cwd=BASE_DIR
            )
            return "", "", result.returncode
    except subprocess.CalledProcessError as e:
        return "", str(e), e.returncode

# Detectar directorio base
BASE_DIR = Path(__file__).resolve().parent.parent
os.chdir(BASE_DIR)

# Obtener usuario de PythonAnywhere
PA_USERNAME = os.environ.get('USER', getpass.getuser())

print_header("🚀 DESPLIEGUE AUTOMATIZADO - PYTHONANYWHERE")

# ============================================
# 1. VERIFICACIÓN DE ENTORNO
# ============================================
print_header("1. VERIFICACIÓN DE ENTORNO")

# Verificar que estamos en PythonAnywhere
if 'pythonanywhere.com' not in os.environ.get('HOME', ''):
    print_warning("No se detectó entorno de PythonAnywhere")
    respuesta = input("¿Continuar de todos modos? (s/n): ").lower()
    if respuesta != 's':
        print_error("Despliegue cancelado")
        sys.exit(1)

print_success(f"Usuario detectado: {PA_USERNAME}")
print_success(f"Directorio base: {BASE_DIR}")

# Verificar Python
python_version = sys.version_info
print_info(f"Python {python_version.major}.{python_version.minor}.{python_version.micro}")

if python_version.major != 3 or python_version.minor < 10:
    print_error("Se requiere Python 3.10 o superior")
    sys.exit(1)

# Verificar que manage.py existe
if not (BASE_DIR / 'manage.py').exists():
    print_error("No se encontró manage.py. ¿Estás en el directorio correcto?")
    sys.exit(1)

print_success("Estructura del proyecto verificada")

# ============================================
# 2. VERIFICACIÓN DE VARIABLES DE ENTORNO
# ============================================
print_header("2. VERIFICACIÓN DE VARIABLES DE ENTORNO")

required_vars = {
    'DJANGO_SECRET_KEY': 'Secret key de Django',
    'DB_NAME': f'Nombre de base de datos (ej: {PA_USERNAME}$default)',
    'DB_USER': 'Usuario de MySQL',
    'DB_PASSWORD': 'Contraseña de MySQL',
    'DB_HOST': f'Host MySQL (ej: {PA_USERNAME}.mysql.pythonanywhere-services.com)',
}

missing_vars = []
for var, description in required_vars.items():
    value = os.environ.get(var)
    if not value:
        missing_vars.append((var, description))
        print_error(f"{var}: NO CONFIGURADA")
    else:
        # Ocultar valores sensibles
        if 'PASSWORD' in var or 'SECRET' in var or 'KEY' in var:
            display_value = '*' * min(len(value), 20)
        else:
            display_value = value
        print_success(f"{var}: {display_value}")

if missing_vars:
    print_warning("\n⚠️  Variables de entorno faltantes:")
    for var, description in missing_vars:
        print(f"   - {var}: {description}")
    
    print("\nConfigura las variables de entorno antes de continuar:")
    print("export DJANGO_SECRET_KEY='tu-secret-key'")
    print("export DB_NAME='tuusuario$default'")
    print("export DB_USER='tuusuario'")
    print("export DB_PASSWORD='tu-password'")
    print("export DB_HOST='tuusuario.mysql.pythonanywhere-services.com'")
    
    respuesta = input("\n¿Continuar de todos modos? (s/n): ").lower()
    if respuesta != 's':
        print_error("Despliegue cancelado. Configura las variables primero.")
        sys.exit(1)

# Verificar DEBUG
debug = os.environ.get('DJANGO_DEBUG', 'False').lower()
if debug == 'true':
    print_warning("DEBUG está activado. Debe estar en False para producción.")
    respuesta = input("¿Continuar? (s/n): ").lower()
    if respuesta != 's':
        sys.exit(1)
else:
    print_success("DEBUG está desactivado (correcto para producción)")

# ============================================
# 3. INSTALACIÓN DE DEPENDENCIAS
# ============================================
print_header("3. INSTALACIÓN DE DEPENDENCIAS")

requirements_file = BASE_DIR / 'requirements.txt'
if not requirements_file.exists():
    print_error("No se encontró requirements.txt")
    sys.exit(1)

print_info("Instalando dependencias desde requirements.txt...")
stdout, stderr, code = run_command(
    f"pip3.{python_version.minor} install --user -r requirements.txt",
    check=False
)

if code == 0:
    print_success("Dependencias instaladas correctamente")
else:
    print_error(f"Error al instalar dependencias: {stderr}")
    respuesta = input("¿Continuar de todos modos? (s/n): ").lower()
    if respuesta != 's':
        sys.exit(1)

# Verificar Playwright (opcional)
print_info("Verificando Playwright...")
try:
    import playwright
    print_success("Playwright está instalado")
    print_info("Instalando navegadores de Playwright...")
    run_command("playwright install chromium", check=False)
    print_success("Navegadores de Playwright instalados")
except ImportError:
    print_warning("Playwright no está instalado (opcional para generación de PDF/PPT)")

# ============================================
# 4. CONFIGURACIÓN DE DJANGO
# ============================================
print_header("4. CONFIGURACIÓN DE DJANGO")

# Verificar configuración
print_info("Verificando configuración de Django...")
stdout, stderr, code = run_command(
    f"python3.{python_version.minor} manage.py check --deploy",
    check=False
)

if code == 0:
    print_success("Configuración de Django verificada")
else:
    print_warning(f"Advertencias en la configuración: {stderr}")
    print_info("Revisa los mensajes anteriores")

# ============================================
# 5. MIGRACIONES DE BASE DE DATOS
# ============================================
print_header("5. MIGRACIONES DE BASE DE DATOS")

print_info("Aplicando migraciones...")
stdout, stderr, code = run_command(
    f"python3.{python_version.minor} manage.py migrate",
    check=False
)

if code == 0:
    print_success("Migraciones aplicadas correctamente")
else:
    print_error(f"Error al aplicar migraciones: {stderr}")
    respuesta = input("¿Continuar de todos modos? (s/n): ").lower()
    if respuesta != 's':
        sys.exit(1)

# Verificar migraciones pendientes
print_info("Verificando migraciones pendientes...")
stdout, stderr, code = run_command(
    f"python3.{python_version.minor} manage.py showmigrations",
    check=False,
    capture_output=True
)

if '[ ]' in stdout:
    print_warning("Hay migraciones pendientes. Revisa el output anterior.")
else:
    print_success("Todas las migraciones están aplicadas")

# ============================================
# 6. CARGAR DATOS INICIALES (OPCIONAL)
# ============================================
print_header("6. DATOS INICIALES")

fixtures = [
    'apps/infrastructure/fixtures/dimensions.json',
    'apps/infrastructure/fixtures/questions.json',
]

respuesta = input("¿Cargar datos iniciales (dimensions y questions)? (s/n): ").lower()
if respuesta == 's':
    for fixture in fixtures:
        fixture_path = BASE_DIR / fixture
        if fixture_path.exists():
            print_info(f"Cargando {fixture}...")
            stdout, stderr, code = run_command(
                f"python3.{python_version.minor} manage.py loaddata {fixture}",
                check=False
            )
            if code == 0:
                print_success(f"{fixture} cargado correctamente")
            else:
                if 'UNIQUE constraint' in stderr or 'already exists' in stderr.lower():
                    print_warning(f"{fixture} ya existe (ignorado)")
                else:
                    print_error(f"Error al cargar {fixture}: {stderr}")
        else:
            print_warning(f"No se encontró {fixture}")

# ============================================
# 7. CREAR SUPERUSUARIO (OPCIONAL)
# ============================================
print_header("7. SUPERUSUARIO")

respuesta = input("¿Crear superusuario? (s/n): ").lower()
if respuesta == 's':
    print_info("Ejecutando createsuperuser...")
    print_info("(Sigue las instrucciones en pantalla)")
    run_command(
        f"python3.{python_version.minor} manage.py createsuperuser",
        check=False
    )
    print_success("Superusuario creado (o ya existía)")
else:
    print_info("Omitiendo creación de superusuario")

# ============================================
# 8. ARCHIVOS ESTÁTICOS
# ============================================
print_header("8. ARCHIVOS ESTÁTICOS")

# Verificar STATIC_ROOT
static_root = BASE_DIR / 'staticfiles'
print_info(f"STATIC_ROOT: {static_root}")

print_info("Recopilando archivos estáticos...")
stdout, stderr, code = run_command(
    f"python3.{python_version.minor} manage.py collectstatic --noinput",
    check=False
)

if code == 0:
    print_success("Archivos estáticos recopilados correctamente")
    if static_root.exists():
        file_count = len(list(static_root.rglob('*')))
        print_info(f"Total de archivos estáticos: {file_count}")
else:
    print_error(f"Error al recopilar archivos estáticos: {stderr}")
    print_warning("Asegúrate de ejecutar 'collectstatic' manualmente")

# ============================================
# 9. VERIFICACIÓN FINAL
# ============================================
print_header("9. VERIFICACIÓN FINAL")

# Verificar que la aplicación puede iniciar
print_info("Verificando que la aplicación puede iniciar...")
stdout, stderr, code = run_command(
    f"python3.{python_version.minor} manage.py check",
    check=False,
    capture_output=True
)

if code == 0:
    print_success("La aplicación puede iniciar correctamente")
else:
    print_error(f"Error al verificar la aplicación: {stderr}")

# ============================================
# 10. INSTRUCCIONES FINALES
# ============================================
print_header("✅ DESPLIEGUE COMPLETADO")

print_info("Próximos pasos:")
print("1. Configura la aplicación web en PythonAnywhere:")
print("   - Ve a la pestaña 'Web'")
print("   - Haz clic en 'Add a new web app' o edita la existente")
print("   - Selecciona 'Manual configuration'")
print("   - Selecciona Python 3.10")
print()
print("2. Configura el archivo WSGI:")
print("   Edita el archivo WSGI y agrega:")
print(f"   import os")
print(f"   import sys")
print(f"   path = '/home/{PA_USERNAME}/mdt_erp_2025'")
print(f"   if path not in sys.path:")
print(f"       sys.path.append(path)")
print(f"   os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'")
print(f"   from django.core.wsgi import get_wsgi_application")
print(f"   application = get_wsgi_application()")
print()
print("3. Configura rutas estáticas:")
print("   - URL: /static/")
print(f"   - Directory: /home/{PA_USERNAME}/mdt_erp_2025/staticfiles")
print()
print("4. Reinicia la aplicación web:")
print("   - Haz clic en el botón verde 'Reload'")
print()
print("5. Verifica que el sitio funciona:")
print(f"   - Abre: https://{PA_USERNAME}.pythonanywhere.com")

print_header("🎉 ¡DESPLIEGUE FINALIZADO!")

