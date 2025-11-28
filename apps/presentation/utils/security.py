"""
Utilidades de seguridad para validación y sanitización de inputs
"""
import re
from django.core.exceptions import ValidationError
from django.utils.html import escape
from django.utils.safestring import mark_safe


def sanitize_string(value, max_length=255):
    """
    Sanitiza un string eliminando caracteres peligrosos
    """
    if not isinstance(value, str):
        value = str(value)
    
    # Eliminar caracteres de control y null bytes
    value = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', value)
    
    # Limitar longitud
    if len(value) > max_length:
        value = value[:max_length]
    
    return value.strip()


def validate_integer(value, min_value=None, max_value=None):
    """
    Valida y convierte un valor a entero de forma segura
    """
    try:
        int_value = int(value)
        
        if min_value is not None and int_value < min_value:
            raise ValidationError(f'El valor debe ser mayor o igual a {min_value}')
        
        if max_value is not None and int_value > max_value:
            raise ValidationError(f'El valor debe ser menor o igual a {max_value}')
        
        return int_value
    except (ValueError, TypeError):
        raise ValidationError('El valor debe ser un número entero válido')


def validate_year(value, min_year=2000, max_year=2100):
    """
    Valida un año de forma segura
    """
    year = validate_integer(value, min_value=min_year, max_value=max_year)
    return year


def sanitize_email(email):
    """
    Valida y sanitiza un email
    """
    if not email:
        return None
    
    email = sanitize_string(email, max_length=254)
    
    # Validar formato básico de email
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        raise ValidationError('Formato de email inválido')
    
    return email.lower()


def sanitize_sql_like_pattern(pattern):
    """
    Escapa caracteres especiales para uso seguro en consultas LIKE
    """
    if not pattern:
        return ''
    
    # Escapar caracteres especiales de SQL LIKE
    pattern = pattern.replace('\\', '\\\\')
    pattern = pattern.replace('%', '\\%')
    pattern = pattern.replace('_', '\\_')
    
    return sanitize_string(pattern)


def escape_html(value):
    """
    Escapa HTML para prevenir XSS
    """
    if value is None:
        return ''
    return escape(str(value))


def validate_company_access(user, company):
    """
    Valida que un usuario tenga acceso a una empresa específica
    """
    from apps.infrastructure.models import CustomUser
    
    # Superusuarios tienen acceso a todo
    if user.is_superuser or user.role == CustomUser.Role.SUPERUSER:
        return True
    
    # Verificar que el usuario administre esta empresa
    if user.role == CustomUser.Role.COMPANY_ADMIN:
        return company in user.managed_companies.all()
    
    return False


def validate_employee_access(user, employee):
    """
    Valida que un usuario tenga acceso a un empleado específico
    """
    from apps.infrastructure.models import CustomUser
    
    # Superusuarios tienen acceso a todo
    if user.is_superuser or user.role == CustomUser.Role.SUPERUSER:
        return True
    
    # Administradores solo pueden acceder a empleados de sus empresas
    if user.role == CustomUser.Role.COMPANY_ADMIN:
        return employee.company in user.managed_companies.all()
    
    # Empleados solo pueden acceder a su propia información
    if user.role == CustomUser.Role.EMPLOYEE:
        return hasattr(user, 'employee') and user.employee == employee
    
    return False

