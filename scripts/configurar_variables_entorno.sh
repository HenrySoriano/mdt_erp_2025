#!/bin/bash
# Script para configurar variables de entorno en PythonAnywhere
# Ejecutar antes del script de despliegue

set -e

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}============================================================${NC}"
echo -e "${BLUE}CONFIGURACIÓN DE VARIABLES DE ENTORNO${NC}"
echo -e "${BLUE}============================================================${NC}\n"

# Obtener usuario de PythonAnywhere
PA_USERNAME="${USER:-$(whoami)}"

echo -e "${YELLOW}Usuario detectado: $PA_USERNAME${NC}\n"

# Función para solicitar variable de entorno
ask_var() {
    local var_name=$1
    local description=$2
    local default_value=$3
    local is_secret=${4:-false}
    
    if [ -n "${!var_name}" ]; then
        if [ "$is_secret" = true ]; then
            echo -e "${GREEN}✓ $var_name ya está configurada${NC}"
        else
            echo -e "${GREEN}✓ $var_name = ${!var_name}${NC}"
        fi
        return 0
    fi
    
    if [ -n "$default_value" ]; then
        read -p "$description [$default_value]: " value
        value=${value:-$default_value}
    else
        read -p "$description: " value
    fi
    
    if [ -z "$value" ]; then
        echo -e "${YELLOW}⚠ $var_name no configurada (se omitirá)${NC}"
        return 1
    fi
    
    export $var_name="$value"
    echo -e "${GREEN}✓ $var_name configurada${NC}"
    return 0
}

# Generar SECRET_KEY si no existe
if [ -z "$DJANGO_SECRET_KEY" ]; then
    echo -e "\n${BLUE}Generando SECRET_KEY...${NC}"
    DJANGO_SECRET_KEY=$(python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
    export DJANGO_SECRET_KEY
    echo -e "${GREEN}✓ SECRET_KEY generada automáticamente${NC}"
fi

# Variables requeridas
echo -e "\n${BLUE}Configurando variables requeridas:${NC}\n"

ask_var "DJANGO_SECRET_KEY" "DJANGO_SECRET_KEY" "$DJANGO_SECRET_KEY" true
ask_var "DB_NAME" "Nombre de base de datos MySQL" "${PA_USERNAME}\$default"
ask_var "DB_USER" "Usuario de MySQL" "$PA_USERNAME"
ask_var "DB_PASSWORD" "Contraseña de MySQL" "" true
ask_var "DB_HOST" "Host MySQL" "${PA_USERNAME}.mysql.pythonanywhere-services.com"
ask_var "DB_PORT" "Puerto MySQL" "3306"

# Variables opcionales
echo -e "\n${BLUE}Configurando variables opcionales:${NC}\n"

ask_var "DJANGO_DEBUG" "DEBUG (False para producción)" "False"
ask_var "DJANGO_ALLOWED_HOSTS" "ALLOWED_HOSTS" "${PA_USERNAME}.pythonanywhere.com"
ask_var "DJANGO_CSRF_TRUSTED_ORIGINS" "CSRF_TRUSTED_ORIGINS" "https://${PA_USERNAME}.pythonanywhere.com"

# Email (opcional)
read -p "¿Configurar email? (s/n): " config_email
if [ "$config_email" = "s" ]; then
    ask_var "EMAIL_HOST" "Servidor SMTP" "smtp.gmail.com"
    ask_var "EMAIL_PORT" "Puerto SMTP" "587"
    ask_var "EMAIL_USE_TLS" "Usar TLS" "True"
    ask_var "EMAIL_HOST_USER" "Usuario de email" ""
    ask_var "EMAIL_HOST_PASSWORD" "Contraseña de email (App Password)" "" true
    ask_var "DEFAULT_FROM_EMAIL" "Email remitente" "noreply@tudominio.com"
fi

# Guardar en archivo .env (opcional)
echo -e "\n${BLUE}¿Guardar variables en archivo .env?${NC}"
read -p "(Esto creará un archivo .env en el directorio actual) (s/n): " save_env

if [ "$save_env" = "s" ]; then
    ENV_FILE=".env"
    cat > "$ENV_FILE" << EOF
# Variables de entorno para PythonAnywhere
# Generado automáticamente - NO SUBIR A GIT

# Django Core
DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY
DJANGO_DEBUG=$DJANGO_DEBUG
DJANGO_ALLOWED_HOSTS=$DJANGO_ALLOWED_HOSTS
DJANGO_CSRF_TRUSTED_ORIGINS=$DJANGO_CSRF_TRUSTED_ORIGINS

# Base de Datos
DB_NAME=$DB_NAME
DB_USER=$DB_USER
DB_PASSWORD=$DB_PASSWORD
DB_HOST=$DB_HOST
DB_PORT=$DB_PORT
EOF

    if [ -n "$EMAIL_HOST" ]; then
        cat >> "$ENV_FILE" << EOF

# Email
EMAIL_HOST=$EMAIL_HOST
EMAIL_PORT=$EMAIL_PORT
EMAIL_USE_TLS=$EMAIL_USE_TLS
EMAIL_HOST_USER=$EMAIL_HOST_USER
EMAIL_HOST_PASSWORD=$EMAIL_HOST_PASSWORD
DEFAULT_FROM_EMAIL=$DEFAULT_FROM_EMAIL
EOF
    fi

    echo -e "${GREEN}✓ Variables guardadas en $ENV_FILE${NC}"
    echo -e "${YELLOW}⚠ Recuerda: NO subir .env a Git${NC}"
fi

# Mostrar resumen
echo -e "\n${BLUE}============================================================${NC}"
echo -e "${BLUE}RESUMEN${NC}"
echo -e "${BLUE}============================================================${NC}\n"

echo -e "${GREEN}Variables configuradas:${NC}"
env | grep -E "^(DJANGO_|DB_|EMAIL_)" | sed 's/=.*/=***/' | sort

echo -e "\n${BLUE}Para usar estas variables en la sesión actual:${NC}"
echo "export DJANGO_SECRET_KEY='$DJANGO_SECRET_KEY'"
echo "export DB_NAME='$DB_NAME'"
echo "export DB_USER='$DB_USER'"
echo "export DB_PASSWORD='$DB_PASSWORD'"
echo "export DB_HOST='$DB_HOST'"
echo "export DB_PORT='$DB_PORT'"
echo "export DJANGO_DEBUG='$DJANGO_DEBUG'"
echo "export DJANGO_ALLOWED_HOSTS='$DJANGO_ALLOWED_HOSTS'"
echo "export DJANGO_CSRF_TRUSTED_ORIGINS='$DJANGO_CSRF_TRUSTED_ORIGINS'"

if [ -n "$EMAIL_HOST" ]; then
    echo "export EMAIL_HOST='$EMAIL_HOST'"
    echo "export EMAIL_PORT='$EMAIL_PORT'"
    echo "export EMAIL_USE_TLS='$EMAIL_USE_TLS'"
    echo "export EMAIL_HOST_USER='$EMAIL_HOST_USER'"
    echo "export EMAIL_HOST_PASSWORD='$EMAIL_HOST_PASSWORD'"
    echo "export DEFAULT_FROM_EMAIL='$DEFAULT_FROM_EMAIL'"
fi

echo -e "\n${BLUE}Para cargar desde .env (si se creó):${NC}"
echo "set -a"
echo "source .env"
echo "set +a"

echo -e "\n${GREEN}✓ Configuración completada${NC}\n"

