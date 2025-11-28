"""
Script para actualizar usuarios existentes que no tienen stored_password
Genera nuevas contraseñas y las guarda en stored_password
"""
import os
import django
import sys

# Fix encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.infrastructure.models import CustomUser
import secrets
import string

def generate_password():
    """Genera una contraseña segura"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(12))

# Obtener todos los usuarios que no tienen stored_password
users_without_password = CustomUser.objects.filter(
    stored_password__isnull=True
) | CustomUser.objects.filter(stored_password='')

print(f'Encontrados {users_without_password.count()} usuarios sin contraseña almacenada')
print('=' * 60)

updated_count = 0
skipped_count = 0

for user in users_without_password:
    # Verificar si el usuario es superusuario y tiene email conocido
    if user.is_superuser and user.email == 'admin@test.com':
        # Restaurar contraseña conocida del superusuario
        user.set_password('admin123')
        user.stored_password = 'admin123'
        user.save()
        updated_count += 1
        print(f'[{updated_count}] {user.email} ({user.get_role_display()}) - Contraseña restaurada: admin123')
    else:
        # Para otros usuarios, generar nueva contraseña
        new_password = generate_password()
        
        # Establecer la contraseña (hasheada para autenticación)
        user.set_password(new_password)
        
        # Guardar la contraseña en texto plano para referencia
        user.stored_password = new_password
        user.save()
        
        updated_count += 1
        print(f'[{updated_count}] {user.email} ({user.get_role_display()}) - Nueva contraseña: {new_password}')

print('=' * 60)
print(f'✅ {updated_count} usuarios actualizados exitosamente')
print('\nNota: Las contraseñas mostradas arriba son las nuevas contraseñas generadas.')
print('Los usuarios deberán usar estas contraseñas para iniciar sesión.')

