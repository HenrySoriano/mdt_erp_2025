#!/bin/bash
# Script de despliegue automatizado para PythonAnywhere (Bash)
# Ejecutar en la consola web de PythonAnywhere después de subir el código

set -e  # Salir si hay algún error

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funciones de utilidad
print_header() {
    echo -e "\n${BLUE}============================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}============================================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Detectar directorio base
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$BASE_DIR"

# Obtener usuario de PythonAnywhere
PA_USERNAME="${USER:-$(whoami)}"

print_header "🚀 DESPLIEGUE AUTOMATIZADO - PYTHONANYWHERE"

# ============================================
# 1. VERIFICACIÓN DE ENTORNO
# ============================================
print_header "1. VERIFICACIÓN DE ENTORNO"

print_success "Usuario detectado: $PA_USERNAME"
print_success "Directorio base: $BASE_DIR"

# Verificar Python
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

print_info "Python $PYTHON_VERSION"

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 10 ]); then
    print_error "Se requiere Python 3.10 o superior"
    exit 1
fi

# Verificar que manage.py existe
if [ ! -f "manage.py" ]; then
    print_error "No se encontró manage.py. ¿Estás en el directorio correcto?"
    exit 1
fi

print_success "Estructura del proyecto verificada"

# ============================================
# 2. VERIFICACIÓN DE VARIABLES DE ENTORNO
# ============================================
print_header "2. VERIFICACIÓN DE VARIABLES DE ENTORNO"

MISSING_VARS=()

check_var() {
    if [ -z "${!1}" ]; then
        MISSING_VARS+=("$1")
        print_error "$1: NO CONFIGURADA"
        return 1
    else
        if [[ "$1" == *"PASSWORD"* ]] || [[ "$1" == *"SECRET"* ]] || [[ "$1" == *"KEY"* ]]; then
            DISPLAY_VALUE="********************"
        else
            DISPLAY_VALUE="${!1}"
        fi
        print_success "$1: $DISPLAY_VALUE"
        return 0
    fi
}

check_var "DJANGO_SECRET_KEY" || true
check_var "DB_NAME" || true
check_var "DB_USER" || true
check_var "DB_PASSWORD" || true
check_var "DB_HOST" || true

if [ ${#MISSING_VARS[@]} -gt 0 ]; then
    print_warning "\n⚠️  Variables de entorno faltantes:"
    for var in "${MISSING_VARS[@]}"; do
        echo "   - $var"
    done
    
    echo ""
    echo "Configura las variables de entorno antes de continuar:"
    echo "export DJANGO_SECRET_KEY='tu-secret-key'"
    echo "export DB_NAME='tuusuario\$default'"
    echo "export DB_USER='tuusuario'"
    echo "export DB_PASSWORD='tu-password'"
    echo "export DB_HOST='tuusuario.mysql.pythonanywhere-services.com'"
    
    read -p "¿Continuar de todos modos? (s/n): " respuesta
    if [ "$respuesta" != "s" ]; then
        print_error "Despliegue cancelado. Configura las variables primero."
        exit 1
    fi
fi

# Verificar DEBUG
if [ "${DJANGO_DEBUG:-False}" = "True" ]; then
    print_warning "DEBUG está activado. Debe estar en False para producción."
    read -p "¿Continuar? (s/n): " respuesta
    if [ "$respuesta" != "s" ]; then
        exit 1
    fi
else
    print_success "DEBUG está desactivado (correcto para producción)"
fi

# ============================================
# 3. INSTALACIÓN DE DEPENDENCIAS
# ============================================
print_header "3. INSTALACIÓN DE DEPENDENCIAS"

if [ ! -f "requirements.txt" ]; then
    print_error "No se encontró requirements.txt"
    exit 1
fi

print_info "Instalando dependencias desde requirements.txt..."
if pip3.${PYTHON_MINOR} install --user -r requirements.txt; then
    print_success "Dependencias instaladas correctamente"
else
    print_error "Error al instalar dependencias"
    read -p "¿Continuar de todos modos? (s/n): " respuesta
    if [ "$respuesta" != "s" ]; then
        exit 1
    fi
fi

# Verificar Playwright (opcional)
print_info "Verificando Playwright..."
if python3 -c "import playwright" 2>/dev/null; then
    print_success "Playwright está instalado"
    print_info "Instalando navegadores de Playwright..."
    playwright install chromium || true
    print_success "Navegadores de Playwright instalados"
else
    print_warning "Playwright no está instalado (opcional para generación de PDF/PPT)"
fi

# ============================================
# 4. CONFIGURACIÓN DE DJANGO
# ============================================
print_header "4. CONFIGURACIÓN DE DJANGO"

print_info "Verificando configuración de Django..."
if python3.${PYTHON_MINOR} manage.py check --deploy; then
    print_success "Configuración de Django verificada"
else
    print_warning "Advertencias en la configuración. Revisa los mensajes anteriores."
fi

# ============================================
# 5. MIGRACIONES DE BASE DE DATOS
# ============================================
print_header "5. MIGRACIONES DE BASE DE DATOS"

print_info "Aplicando migraciones..."
if python3.${PYTHON_MINOR} manage.py migrate; then
    print_success "Migraciones aplicadas correctamente"
else
    print_error "Error al aplicar migraciones"
    read -p "¿Continuar de todos modos? (s/n): " respuesta
    if [ "$respuesta" != "s" ]; then
        exit 1
    fi
fi

# Verificar migraciones pendientes
print_info "Verificando migraciones pendientes..."
if python3.${PYTHON_MINOR} manage.py showmigrations | grep -q "\[ \]"; then
    print_warning "Hay migraciones pendientes. Revisa el output anterior."
else
    print_success "Todas las migraciones están aplicadas"
fi

# ============================================
# 6. CARGAR DATOS INICIALES (OPCIONAL)
# ============================================
print_header "6. DATOS INICIALES"

read -p "¿Cargar datos iniciales (dimensions y questions)? (s/n): " respuesta
if [ "$respuesta" = "s" ]; then
    for fixture in "apps/infrastructure/fixtures/dimensions.json" "apps/infrastructure/fixtures/questions.json"; do
        if [ -f "$fixture" ]; then
            print_info "Cargando $fixture..."
            if python3.${PYTHON_MINOR} manage.py loaddata "$fixture" 2>&1 | grep -q "UNIQUE\|already exists"; then
                print_warning "$fixture ya existe (ignorado)"
            elif python3.${PYTHON_MINOR} manage.py loaddata "$fixture"; then
                print_success "$fixture cargado correctamente"
            else
                print_error "Error al cargar $fixture"
            fi
        else
            print_warning "No se encontró $fixture"
        fi
    done
fi

# ============================================
# 7. CREAR SUPERUSUARIO (OPCIONAL)
# ============================================
print_header "7. SUPERUSUARIO"

read -p "¿Crear superusuario? (s/n): " respuesta
if [ "$respuesta" = "s" ]; then
    print_info "Ejecutando createsuperuser..."
    print_info "(Sigue las instrucciones en pantalla)"
    python3.${PYTHON_MINOR} manage.py createsuperuser || true
    print_success "Superusuario creado (o ya existía)"
else
    print_info "Omitiendo creación de superusuario"
fi

# ============================================
# 8. ARCHIVOS ESTÁTICOS
# ============================================
print_header "8. ARCHIVOS ESTÁTICOS"

STATIC_ROOT="$BASE_DIR/staticfiles"
print_info "STATIC_ROOT: $STATIC_ROOT"

print_info "Recopilando archivos estáticos..."
if python3.${PYTHON_MINOR} manage.py collectstatic --noinput; then
    print_success "Archivos estáticos recopilados correctamente"
    if [ -d "$STATIC_ROOT" ]; then
        FILE_COUNT=$(find "$STATIC_ROOT" -type f | wc -l)
        print_info "Total de archivos estáticos: $FILE_COUNT"
    fi
else
    print_error "Error al recopilar archivos estáticos"
    print_warning "Asegúrate de ejecutar 'collectstatic' manualmente"
fi

# ============================================
# 9. VERIFICACIÓN FINAL
# ============================================
print_header "9. VERIFICACIÓN FINAL"

print_info "Verificando que la aplicación puede iniciar..."
if python3.${PYTHON_MINOR} manage.py check; then
    print_success "La aplicación puede iniciar correctamente"
else
    print_error "Error al verificar la aplicación"
fi

# ============================================
# 10. INSTRUCCIONES FINALES
# ============================================
print_header "✅ DESPLIEGUE COMPLETADO"

echo -e "${BLUE}Próximos pasos:${NC}"
echo "1. Configura la aplicación web en PythonAnywhere:"
echo "   - Ve a la pestaña 'Web'"
echo "   - Haz clic en 'Add a new web app' o edita la existente"
echo "   - Selecciona 'Manual configuration'"
echo "   - Selecciona Python 3.10"
echo ""
echo "2. Configura el archivo WSGI:"
echo "   Edita el archivo WSGI y agrega:"
echo "   import os"
echo "   import sys"
echo "   path = '/home/$PA_USERNAME/mdt_erp_2025'"
echo "   if path not in sys.path:"
echo "       sys.path.append(path)"
echo "   os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'"
echo "   from django.core.wsgi import get_wsgi_application"
echo "   application = get_wsgi_application()"
echo ""
echo "3. Configura rutas estáticas:"
echo "   - URL: /static/"
echo "   - Directory: /home/$PA_USERNAME/mdt_erp_2025/staticfiles"
echo ""
echo "4. Reinicia la aplicación web:"
echo "   - Haz clic en el botón verde 'Reload'"
echo ""
echo "5. Verifica que el sitio funciona:"
echo "   - Abre: https://$PA_USERNAME.pythonanywhere.com"

print_header "🎉 ¡DESPLIEGUE FINALIZADO!"

