"""
Script para hacer backup de la base de datos MySQL
Ejecutar diariamente o semanalmente según necesidad
"""
import os
import django
import sys
from datetime import datetime
import subprocess

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.conf import settings
from django.db import connection

def backup_database():
    """Crea un backup de la base de datos MySQL"""
    print("=" * 60)
    print("BACKUP DE BASE DE DATOS")
    print("=" * 60)
    
    # Obtener configuración de base de datos
    db_config = settings.DATABASES['default']
    
    if db_config['ENGINE'] != 'django.db.backends.mysql':
        print("❌ Este script solo funciona con MySQL")
        return False
    
    # Crear directorio de backups si no existe
    backup_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backups')
    os.makedirs(backup_dir, exist_ok=True)
    
    # Nombre del archivo de backup
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = os.path.join(backup_dir, f'backup_{timestamp}.sql')
    
    # Comando mysqldump
    cmd = [
        'mysqldump',
        f'--host={db_config["HOST"]}',
        f'--port={db_config["PORT"]}',
        f'--user={db_config["USER"]}',
        f'--password={db_config["PASSWORD"]}',
        '--single-transaction',
        '--routines',
        '--triggers',
        db_config['NAME'],
    ]
    
    print(f"\n📦 Creando backup de: {db_config['NAME']}")
    print(f"📁 Guardando en: {backup_file}")
    
    try:
        # Ejecutar mysqldump
        with open(backup_file, 'w', encoding='utf-8') as f:
            result = subprocess.run(
                cmd,
                stdout=f,
                stderr=subprocess.PIPE,
                text=True
            )
        
        if result.returncode == 0:
            file_size = os.path.getsize(backup_file) / (1024 * 1024)  # MB
            print(f"✅ Backup creado exitosamente")
            print(f"📊 Tamaño: {file_size:.2f} MB")
            
            # Comprimir backup (opcional)
            # Puedes usar gzip o 7zip aquí
            
            return True
        else:
            print(f"❌ Error al crear backup:")
            print(result.stderr)
            return False
            
    except FileNotFoundError:
        print("❌ mysqldump no encontrado. Asegúrate de tener MySQL instalado.")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def list_backups():
    """Lista todos los backups disponibles"""
    backup_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backups')
    
    if not os.path.exists(backup_dir):
        print("No hay directorio de backups")
        return
    
    backups = [f for f in os.listdir(backup_dir) if f.startswith('backup_') and f.endswith('.sql')]
    backups.sort(reverse=True)
    
    print("\n📋 Backups disponibles:")
    for backup in backups[:10]:  # Mostrar últimos 10
        file_path = os.path.join(backup_dir, backup)
        size = os.path.getsize(file_path) / (1024 * 1024)  # MB
        mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
        print(f"  - {backup} ({size:.2f} MB) - {mtime.strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'list':
        list_backups()
    else:
        backup_database()
        print("\n💡 Tip: Ejecuta 'python scripts/backup_database.py list' para ver backups")

