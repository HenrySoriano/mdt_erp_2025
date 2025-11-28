"""
Script para limpiar archivos no necesarios antes de subir a producción
Ejecutar con: python limpiar_produccion.py
"""
import os
import shutil

# Archivos y carpetas a eliminar
ARCHIVOS_ELIMINAR = [
    'debug_page.html',
    'Acción.docx',
    'apps/presentation/views/admin_views_pptx.py',
]

# Scripts de desarrollo (opcional: mover a carpeta scripts/)
SCRIPTS_DESARROLLO = [
    'create_superuser_and_load_data.py',
    'restaurar_superusuario.py',
    'update_question_explanations.py',
    'update_stored_passwords.py',
]

# Scripts de activación redundantes
SCRIPTS_REDUNDANTES = [
    'ACTIVAR_ENTORNO.bat',
    'ACTIVAR_ENTORNO.ps1',
    'activar.ps1',
]

# Fixtures duplicados
FIXTURES_DUPLICADOS = [
    'apps/infrastructure/fixtures/dimensions_updated.json',
    'apps/infrastructure/fixtures/questions_updated.json',
    'apps/infrastructure/fixtures/questions_final.json',
]

# Directorios vacíos DDD (opcional eliminar)
DIRECTORIOS_DDD_VACIOS = [
    'apps/domain/entities',
    'apps/domain/interfaces',
    'apps/infrastructure/repositories',
    'apps/application/use_cases',
]

def eliminar_archivo(ruta):
    """Elimina un archivo si existe"""
    if os.path.exists(ruta):
        try:
            os.remove(ruta)
            print(f"✅ Eliminado: {ruta}")
            return True
        except Exception as e:
            print(f"❌ Error al eliminar {ruta}: {e}")
            return False
    else:
        print(f"⚠️  No existe: {ruta}")
        return False

def eliminar_directorio(ruta):
    """Elimina un directorio si existe y está vacío"""
    if os.path.exists(ruta):
        try:
            # Verificar que solo tenga __init__.py vacío
            archivos = os.listdir(ruta)
            if len(archivos) == 1 and archivos[0] == '__init__.py':
                init_path = os.path.join(ruta, '__init__.py')
                with open(init_path, 'r') as f:
                    contenido = f.read().strip()
                if contenido == '':
                    os.remove(init_path)
                    os.rmdir(ruta)
                    print(f"✅ Eliminado directorio vacío: {ruta}")
                    return True
            print(f"⚠️  Directorio no está completamente vacío: {ruta}")
            return False
        except Exception as e:
            print(f"❌ Error al eliminar directorio {ruta}: {e}")
            return False
    else:
        print(f"⚠️  No existe: {ruta}")
        return False

def mover_a_scripts(ruta):
    """Mueve un archivo a la carpeta scripts/"""
    if not os.path.exists('scripts'):
        os.makedirs('scripts')
        print("📁 Creada carpeta scripts/")
    
    destino = os.path.join('scripts', os.path.basename(ruta))
    if os.path.exists(ruta):
        try:
            shutil.move(ruta, destino)
            print(f"✅ Movido a scripts/: {ruta}")
            return True
        except Exception as e:
            print(f"❌ Error al mover {ruta}: {e}")
            return False
    else:
        print(f"⚠️  No existe: {ruta}")
        return False

def main():
    print("=" * 60)
    print("🧹 LIMPIEZA PARA PRODUCCIÓN")
    print("=" * 60)
    print()
    
    # Confirmar acción
    respuesta = input("¿Deseas eliminar archivos obsoletos? (s/n): ").lower()
    if respuesta != 's':
        print("❌ Operación cancelada")
        return
    
    print("\n📋 ELIMINANDO ARCHIVOS OBSOLETOS...")
    print("-" * 60)
    eliminados = 0
    for archivo in ARCHIVOS_ELIMINAR:
        if eliminar_archivo(archivo):
            eliminados += 1
    
    print(f"\n✅ Eliminados {eliminados}/{len(ARCHIVOS_ELIMINAR)} archivos obsoletos")
    
    print("\n📋 ELIMINANDO FIXTURES DUPLICADOS...")
    print("-" * 60)
    eliminados_fixtures = 0
    for fixture in FIXTURES_DUPLICADOS:
        if eliminar_archivo(fixture):
            eliminados_fixtures += 1
    
    print(f"\n✅ Eliminados {eliminados_fixtures}/{len(FIXTURES_DUPLICADOS)} fixtures duplicados")
    
    print("\n📋 ELIMINANDO SCRIPTS REDUNDANTES...")
    print("-" * 60)
    respuesta_scripts = input("¿Eliminar scripts de activación redundantes? (s/n): ").lower()
    if respuesta_scripts == 's':
        eliminados_scripts = 0
        for script in SCRIPTS_REDUNDANTES:
            if eliminar_archivo(script):
                eliminados_scripts += 1
        print(f"\n✅ Eliminados {eliminados_scripts}/{len(SCRIPTS_REDUNDANTES)} scripts redundantes")
    
    print("\n📋 MOVIENDO SCRIPTS DE DESARROLLO...")
    print("-" * 60)
    respuesta_dev = input("¿Mover scripts de desarrollo a carpeta scripts/? (s/n): ").lower()
    if respuesta_dev == 's':
        movidos = 0
        for script in SCRIPTS_DESARROLLO:
            if mover_a_scripts(script):
                movidos += 1
        print(f"\n✅ Movidos {movidos}/{len(SCRIPTS_DESARROLLO)} scripts de desarrollo")
    
    print("\n📋 DIRECTORIOS DDD VACÍOS...")
    print("-" * 60)
    respuesta_ddd = input("¿Eliminar directorios DDD vacíos? (s/n): ").lower()
    if respuesta_ddd == 's':
        eliminados_ddd = 0
        for directorio in DIRECTORIOS_DDD_VACIOS:
            if eliminar_directorio(directorio):
                eliminados_ddd += 1
        print(f"\n✅ Eliminados {eliminados_ddd}/{len(DIRECTORIOS_DDD_VACIOS)} directorios DDD vacíos")
    
    print("\n" + "=" * 60)
    print("✅ LIMPIEZA COMPLETADA")
    print("=" * 60)
    print("\n⚠️  RECUERDA:")
    print("1. Verificar que el proyecto funcione: python manage.py check")
    print("2. Probar todas las funcionalidades principales")
    print("3. Revisar REVISION_PRODUCCION.md para más detalles")

if __name__ == '__main__':
    main()

