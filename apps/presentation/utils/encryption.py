"""
Utilidades para encriptar y desencriptar contraseñas almacenadas
Usa Fernet (symmetric encryption) de cryptography
"""
import os
import base64
from cryptography.fernet import Fernet
from django.core.exceptions import ImproperlyConfigured


def get_encryption_key():
    """
    Obtiene la clave de encriptación desde variable de entorno
    Si no existe, genera una nueva (solo para desarrollo)
    """
    key = os.environ.get('ENCRYPTION_KEY')
    
    if not key:
        # En desarrollo, generar una clave temporal
        # EN PRODUCCIÓN DEBE CONFIGURARSE LA VARIABLE DE ENTORNO
        key = Fernet.generate_key().decode()
        print("ADVERTENCIA: Usando clave de encriptacion temporal. Configura ENCRYPTION_KEY en produccion.")
    
    # Asegurar que la clave tenga el formato correcto
    if isinstance(key, str):
        key = key.encode()
    
    return key


def get_fernet():
    """
    Retorna una instancia de Fernet con la clave de encriptación
    """
    key = get_encryption_key()
    
    # Validar que la clave sea válida para Fernet
    try:
        return Fernet(key)
    except Exception as e:
        raise ImproperlyConfigured(f"Clave de encriptación inválida: {e}")


def encrypt_password(password):
    """
    Encripta una contraseña usando Fernet
    
    Args:
        password: String con la contraseña en texto plano
        
    Returns:
        String con la contraseña encriptada (base64)
    """
    if not password:
        return None
    
    try:
        fernet = get_fernet()
        encrypted = fernet.encrypt(password.encode())
        # Retornar como string base64
        return encrypted.decode()
    except Exception as e:
        raise ValueError(f"Error al encriptar contraseña: {e}")


def decrypt_password(encrypted_password):
    """
    Desencripta una contraseña usando Fernet
    
    Args:
        encrypted_password: String con la contraseña encriptada (base64)
        
    Returns:
        String con la contraseña en texto plano
        
    Raises:
        ValueError: Si la contraseña no puede ser desencriptada
    """
    if not encrypted_password:
        return None
    
    try:
        fernet = get_fernet()
        decrypted = fernet.decrypt(encrypted_password.encode())
        return decrypted.decode()
    except Exception as e:
        raise ValueError(f"Error al desencriptar contraseña: {e}")


def generate_encryption_key():
    """
    Genera una nueva clave de encriptación Fernet
    Útil para generar la clave inicial
    """
    return Fernet.generate_key().decode()

