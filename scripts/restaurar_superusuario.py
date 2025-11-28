"""
Script para restaurar la contraseña del superusuario a admin123
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

# Buscar superusuario
admin = CustomUser.objects.filter(email='admin@test.com').first()

if admin:
    admin.set_password('admin123')
    admin.stored_password = 'admin123'
    admin.save()
    print('✅ Contraseña del superusuario restaurada exitosamente')
    print(f'   Email: {admin.email}')
    print(f'   Contraseña: admin123')
else:
    print('❌ No se encontró el superusuario admin@test.com')

