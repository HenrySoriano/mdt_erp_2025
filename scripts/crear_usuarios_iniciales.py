"""
Script para crear usuarios iniciales de prueba
Ejecuta este script para crear superusuario, admin empresa y empleado
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

from apps.infrastructure.models import CustomUser, Company, Employee

def crear_usuarios_iniciales():
    """Crea los usuarios iniciales de prueba"""
    print("=" * 60)
    print("CREANDO USUARIOS INICIALES")
    print("=" * 60)
    
    # 1. Crear Superusuario
    print("\n1. Creando Superusuario...")
    try:
        superuser, created = CustomUser.objects.get_or_create(
            email='admin@test.com',
            defaults={
                'is_superuser': True,
                'is_staff': True,
                'is_active': True,
                'role': CustomUser.Role.SUPERUSER,
            }
        )
        if created:
            superuser.set_password('admin123')
            superuser.set_stored_password('admin123')
            superuser.save()
            print(f"   ✅ Superusuario creado: {superuser.email}")
        else:
            superuser.set_password('admin123')
            superuser.set_stored_password('admin123')
            superuser.is_superuser = True
            superuser.is_staff = True
            superuser.is_active = True
            superuser.role = CustomUser.Role.SUPERUSER
            superuser.save()
            print(f"   ✅ Superusuario actualizado: {superuser.email}")
    except Exception as e:
        print(f"   ❌ Error al crear superusuario: {e}")
        return False
    
    # 2. Crear Admin Empresa
    print("\n2. Creando Admin Empresa...")
    try:
        admin_empresa, created = CustomUser.objects.get_or_create(
            email='admin.empresa@test.com',
            defaults={
                'is_staff': True,
                'is_active': True,
                'role': CustomUser.Role.COMPANY_ADMIN,
            }
        )
        if created:
            admin_empresa.set_password('admin123')
            admin_empresa.set_stored_password('admin123')
            admin_empresa.save()
            print(f"   ✅ Admin Empresa creado: {admin_empresa.email}")
        else:
            admin_empresa.set_password('admin123')
            admin_empresa.set_stored_password('admin123')
            admin_empresa.is_staff = True
            admin_empresa.is_active = True
            admin_empresa.role = CustomUser.Role.COMPANY_ADMIN
            admin_empresa.save()
            print(f"   ✅ Admin Empresa actualizado: {admin_empresa.email}")
    except Exception as e:
        print(f"   ❌ Error al crear admin empresa: {e}")
        return False
    
    # 3. Crear Empresa de prueba (necesaria para el admin empresa)
    print("\n3. Creando Empresa de prueba...")
    try:
        empresa, created = Company.objects.get_or_create(
            name='Empresa de Prueba',
            defaults={
                'admin': admin_empresa,
                'ruc': '1234567890001',
                'address': 'Dirección de prueba',
                'phone': '0999999999',
                'email': 'contacto@empresa.com',
            }
        )
        if created:
            print(f"   ✅ Empresa creada: {empresa.name}")
        else:
            empresa.admin = admin_empresa
            empresa.save()
            print(f"   ✅ Empresa actualizada: {empresa.name}")
    except Exception as e:
        print(f"   ❌ Error al crear empresa: {e}")
        return False
    
    # 4. Crear Empleado
    print("\n4. Creando Empleado...")
    try:
        empleado_user, created = CustomUser.objects.get_or_create(
            email='empleado@test.com',
            defaults={
                'is_active': True,
                'role': CustomUser.Role.EMPLOYEE,
            }
        )
        if created:
            empleado_user.set_password('empleado123')
            empleado_user.set_stored_password('empleado123')
            empleado_user.save()
            print(f"   ✅ Usuario empleado creado: {empleado_user.email}")
        else:
            empleado_user.set_password('empleado123')
            empleado_user.set_stored_password('empleado123')
            empleado_user.is_active = True
            empleado_user.role = CustomUser.Role.EMPLOYEE
            empleado_user.save()
            print(f"   ✅ Usuario empleado actualizado: {empleado_user.email}")
        
        # Crear perfil de empleado
        from datetime import date, timedelta
        
        empleado, created = Employee.objects.get_or_create(
            user=empleado_user,
            defaults={
                'company': empresa,
                'first_name': 'Empleado',
                'last_name': 'Prueba',
                'identification': '1234567890',  # Cédula única
                'date_of_birth': date(1990, 1, 1),  # Fecha de nacimiento
                'hire_date': date(2020, 1, 1),  # Fecha de ingreso
                'position': 'Desarrollador',
                'area': 'Tecnología',
                'work_area_erp': 'TECNOLOGIA_INNOVACION',
                'gender': 'M',
                'education_level': 'UNIVERSITARIO',
                'ethnicity': 'MESTIZO',
                'province': 'Pichincha',
                'city': 'Quito',
            }
        )
        if created:
            print(f"   ✅ Perfil empleado creado: {empleado.first_name} {empleado.last_name}")
        else:
            empleado.company = empresa
            empleado.save()
            print(f"   ✅ Perfil empleado actualizado: {empleado.first_name} {empleado.last_name}")
    except Exception as e:
        print(f"   ❌ Error al crear empleado: {e}")
        return False
    
    # Resumen
    print("\n" + "=" * 60)
    print("RESUMEN")
    print("=" * 60)
    print("\nUsuarios creados:")
    print("  👤 Superusuario:")
    print("     Email: admin@test.com")
    print("     Contraseña: admin123")
    print("     Rol: SUPERUSER")
    print()
    print("  👤 Admin Empresa:")
    print("     Email: admin.empresa@test.com")
    print("     Contraseña: admin123")
    print("     Rol: COMPANY_ADMIN")
    print()
    print("  👤 Empleado:")
    print("     Email: empleado@test.com")
    print("     Contraseña: empleado123")
    print("     Rol: EMPLOYEE")
    print()
    print("=" * 60)
    print("✅ Usuarios creados exitosamente!")
    print("=" * 60)
    
    return True

if __name__ == '__main__':
    crear_usuarios_iniciales()

