import os
import django
import subprocess
import sys

# Fix encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

# ---------------------------------------------------------------------
# Create superuser (if it does not exist)
# ---------------------------------------------------------------------
if not User.objects.filter(email='admin@test.com').exists():
    # CustomUser uses email as USERNAME_FIELD, no username field needed
    superuser = User.objects.create_superuser(email='admin@test.com', password='admin123')
    superuser.stored_password = 'admin123'  # Almacenar contraseña para referencia
    superuser.save()
    print('[OK] Superuser created: admin@test.com / admin123')
else:
    print('[OK] Superuser already exists')

# ---------------------------------------------------------------------
# Helper to load a fixture and ignore duplicate‑key errors
# ---------------------------------------------------------------------
def load_fixture(path):
    result = subprocess.run([sys.executable, 'manage.py', 'loaddata', path], capture_output=True, text=True)
    if result.returncode == 0:
        print(f'[OK] Loaded fixture: {path}')
    else:
        if 'UNIQUE constraint failed' in result.stderr:
            print(f'[WARN] Duplicate data ignored for fixture: {path}')
        else:
            print(f'[ERROR] Error loading {path}:', result.stderr)

# ---------------------------------------------------------------------
# Load fixtures – dimensions first (may already exist), then questions
# ---------------------------------------------------------------------
load_fixture('apps/infrastructure/fixtures/dimensions.json')
load_fixture('apps/infrastructure/fixtures/questions.json')
