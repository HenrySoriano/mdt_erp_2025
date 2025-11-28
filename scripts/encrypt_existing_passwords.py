"""
Script para encriptar todas las contraseñas existentes en stored_password
Ejecutar una vez después de implementar la encriptación
"""
import os
import sys
import django

# Añadir el directorio raíz al path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.infrastructure.models import CustomUser
from apps.presentation.utils.encryption import encrypt_password, decrypt_password

def encrypt_existing_passwords():
    """
    Encripta todas las contraseñas que están en texto plano
    """
    print("=" * 60)
    print("ENCRIPTANDO CONTRASEÑAS EXISTENTES")
    print("=" * 60)
    
    users = CustomUser.objects.filter(stored_password__isnull=False).exclude(stored_password='')
    total = users.count()
    encrypted_count = 0
    already_encrypted = 0
    error_count = 0
    
    print(f"\nEncontrados {total} usuarios con contraseñas almacenadas\n")
    
    for user in users:
        try:
            # Intentar desencriptar para ver si ya está encriptada
            try:
                decrypted = decrypt_password(user.stored_password)
                # Si puede desencriptar, ya está encriptada
                already_encrypted += 1
                print(f"[OK] {user.email}: Ya esta encriptada")
            except:
                # No está encriptada, encriptarla
                encrypted = encrypt_password(user.stored_password)
                user.stored_password = encrypted
                user.save()
                encrypted_count += 1
                print(f"[OK] {user.email}: Encriptada exitosamente")
        except Exception as e:
            error_count += 1
            print(f"[ERROR] {user.email}: Error - {e}")
    
    print("\n" + "=" * 60)
    print("RESUMEN:")
    print(f"  Total procesados: {total}")
    print(f"  Encriptadas: {encrypted_count}")
    print(f"  Ya encriptadas: {already_encrypted}")
    print(f"  Errores: {error_count}")
    print("=" * 60)

if __name__ == '__main__':
    encrypt_existing_passwords()

