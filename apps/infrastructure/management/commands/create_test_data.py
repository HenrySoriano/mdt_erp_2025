"""
Script para crear datos de prueba en el sistema
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.infrastructure.models import Company, Employee
from datetime import date

User = get_user_model()


class Command(BaseCommand):
    help = 'Crea datos de prueba para el sistema'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creando datos de prueba...')
        
        # Establecer contraseña para superusuario
        try:
            admin = User.objects.get(email='admin@test.com')
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(self.style.SUCCESS(f'✓ Contraseña establecida para {admin.email}'))
        except User.DoesNotExist:
            admin = User.objects.create_superuser(
                email='admin@test.com',
                password='admin123'
            )
            self.stdout.write(self.style.SUCCESS(f'✓ Superusuario creado: {admin.email}'))
        
        # Crear admin de empresa
        company_admin, created = User.objects.get_or_create(
            email='admin.empresa@test.com',
            defaults={
                'role': User.Role.COMPANY_ADMIN,
                'is_staff': True
            }
        )
        if created:
            company_admin.set_password('admin123')
            company_admin.save()
            self.stdout.write(self.style.SUCCESS(f'✓ Admin de empresa creado: {company_admin.email}'))
        
        # Crear empresa
        company, created = Company.objects.get_or_create(
            ruc='1234567890001',
            defaults={
                'name': 'Empresa Demo S.A.',
                'address': 'Av. Principal 123',
                'phone': '0999999999',
                'email': 'contacto@empresademo.com',
                'city': 'Quito',
                'province': 'Pichincha',
                'admin': company_admin
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Empresa creada: {company.name}'))
        
        # Crear empleado de prueba
        employee_user, created = User.objects.get_or_create(
            email='empleado@test.com',
            defaults={
                'role': User.Role.EMPLOYEE
            }
        )
        if created:
            employee_user.set_password('empleado123')
            employee_user.save()
            self.stdout.write(self.style.SUCCESS(f'✓ Usuario empleado creado: {employee_user.email}'))
        
        employee, created = Employee.objects.get_or_create(
            identification='1234567890',
            defaults={
                'user': employee_user,
                'company': company,
                'first_name': 'Juan',
                'last_name': 'Pérez',
                'date_of_birth': date(1990, 1, 1),
                'gender': Employee.Gender.MASCULINO,
                'ethnicity': Employee.Ethnicity.MESTIZO,
                'area': 'Tecnología',
                'position': 'Desarrollador',
                'education_level': Employee.EducationLevel.UNIVERSITARIO,
                'years_of_experience': 5,
                'province': 'Pichincha',
                'city': 'Quito'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Empleado creado: {employee.full_name}'))
        
        self.stdout.write(self.style.SUCCESS('\n=== Datos de prueba creados exitosamente ==='))
        self.stdout.write(self.style.SUCCESS('\nCredenciales de acceso:'))
        self.stdout.write(self.style.SUCCESS('Superusuario: admin@test.com / admin123'))
        self.stdout.write(self.style.SUCCESS('Admin Empresa: admin.empresa@test.com / admin123'))
        self.stdout.write(self.style.SUCCESS('Empleado: empleado@test.com / empleado123'))
