"""
Script para cargar datos iniciales en MySQL
Ejecuta este script después de migrar a MySQL para cargar dimensiones y preguntas
"""
import os
import django
import sys

# Agregar el directorio raíz al path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management import call_command
from apps.infrastructure.models import Question, Dimension

def cargar_datos_iniciales():
    """Carga dimensiones y preguntas desde fixtures"""
    print("=" * 60)
    print("CARGANDO DATOS INICIALES EN MySQL")
    print("=" * 60)
    
    # Verificar estado actual
    print("\n1. Verificando estado actual...")
    dimensiones_count = Dimension.objects.count()
    preguntas_count = Question.objects.count()
    print(f"   Dimensiones: {dimensiones_count}")
    print(f"   Preguntas: {preguntas_count}")
    
    # Cargar dimensiones
    print("\n2. Cargando dimensiones...")
    try:
        call_command('loaddata', 'apps/infrastructure/fixtures/dimensions.json', verbosity=0)
        print("   ✅ Dimensiones cargadas")
    except Exception as e:
        print(f"   ⚠️  Advertencia al cargar dimensiones: {e}")
        # Continuar aunque haya errores de duplicados
    
    # Cargar preguntas
    print("\n3. Cargando preguntas...")
    try:
        call_command('loaddata', 'apps/infrastructure/fixtures/questions.json', verbosity=0)
        print("   ✅ Preguntas cargadas")
    except Exception as e:
        print(f"   ⚠️  Advertencia al cargar preguntas: {e}")
        # Continuar aunque haya errores de duplicados
    
    # Verificar resultado final
    print("\n4. Verificando resultado...")
    dimensiones_final = Dimension.objects.count()
    preguntas_final = Question.objects.count()
    
    print(f"   Dimensiones: {dimensiones_final}")
    print(f"   Preguntas: {preguntas_final}")
    
    if preguntas_final >= 58:
        print("\n" + "=" * 60)
        print("✅ Datos cargados exitosamente!")
        print("=" * 60)
        return True
    else:
        print("\n" + "=" * 60)
        print("⚠️  Se cargaron algunos datos, pero puede haber problemas")
        print(f"   Esperado: 58 preguntas, Encontrado: {preguntas_final}")
        print("=" * 60)
        return False

if __name__ == '__main__':
    cargar_datos_iniciales()

