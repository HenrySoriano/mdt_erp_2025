from django import forms
from apps.infrastructure.models import Company, Employee, CustomUser
from apps.presentation.utils.ecuador_data import PROVINCIAS_ECUADOR, CIUDADES_POR_PROVINCIA
import secrets
import string


class CompanyForm(forms.ModelForm):
    admin_email = forms.EmailField(
        label='Email del Administrador',
        help_text='Se creará un usuario con este email para gestionar la empresa',
        widget=forms.EmailInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'})
    )
    admin_password = forms.CharField(
        label='Contraseña del Administrador',
        widget=forms.PasswordInput(attrs={'class': 'w-full px-4 py-2 pr-10 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'}),
        required=False,
        help_text='Si se deja vacío, se generará una contraseña automática'
    )
    
    class Meta:
        model = Company
        fields = ['name', 'ruc', 'address', 'phone', 'email', 'city', 'province', 'admin_email', 'admin_password']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'}),
            'ruc': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'}),
            'address': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent', 'rows': 3}),
            'phone': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'}),
            'city': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'}),
            'province': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Forzar que province y city sean Select fields
        self.fields['province'].widget = forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'})
        self.fields['city'].widget = forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'})
        
        # Convertir PROVINCIAS_ECUADOR a formato de choices
        provincia_choices = [('', 'Seleccione una provincia')]
        for provincia_tuple in PROVINCIAS_ECUADOR:
            if isinstance(provincia_tuple, tuple):
                provincia_choices.append(provincia_tuple)
            else:
                provincia_choices.append((provincia_tuple, provincia_tuple))
        self.fields['province'].choices = provincia_choices
        
        # Inicializar ciudades vacías
        self.fields['city'].choices = [('', 'Seleccione una ciudad')]
        
        if self.instance and self.instance.pk:
            if self.instance.admin:
                self.fields['admin_email'].initial = self.instance.admin.email
            self.fields['admin_password'].required = False
            self.fields['admin_password'].help_text = 'Dejar vacío para mantener la contraseña actual'
            
            # Si hay provincia seleccionada, cargar ciudades
            if self.instance.province:
                ciudades = CIUDADES_POR_PROVINCIA.get(self.instance.province, [])
                city_choices = [('', 'Seleccione una ciudad')]
                for ciudad in ciudades:
                    city_choices.append((ciudad, ciudad))
                self.fields['city'].choices = city_choices
    
    def generate_password(self):
        """Genera una contraseña segura de 12 caracteres"""
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for i in range(12))
    
    def save(self, commit=True):
        company = super().save(commit=False)
        admin_email = self.cleaned_data['admin_email']
        admin_password = self.cleaned_data.get('admin_password') or self.generate_password()
        
        if commit:
            # Crear o actualizar usuario admin
            admin_user, created = CustomUser.objects.get_or_create(
                email=admin_email,
                defaults={
                    'role': CustomUser.Role.COMPANY_ADMIN,
                    'is_staff': True,
                    'is_active': True
                }
            )
            if created or not admin_user.check_password(admin_password):
                admin_user.set_password(admin_password)
                admin_user.set_stored_password(admin_password)  # Encriptar y almacenar contraseña
                admin_user.role = CustomUser.Role.COMPANY_ADMIN
                admin_user.is_staff = True
                admin_user.save()
            elif not admin_user.stored_password:
                # Si el usuario existe pero no tiene contraseña almacenada, guardarla ahora
                admin_user.set_stored_password(admin_password)
                admin_user.save()
            
            company.admin = admin_user
            company.save()
            self.admin_password = admin_password  # Guardar para mostrar después
        
        return company


class EmployeeForm(forms.ModelForm):
    user_email = forms.EmailField(
        label='Email del Empleado',
        help_text='Se creará un usuario con este email para el empleado',
        widget=forms.EmailInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'})
    )
    user_password = forms.CharField(
        label='Contraseña del Empleado',
        widget=forms.PasswordInput(attrs={'class': 'w-full px-4 py-2 pr-10 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'}),
        required=False,
        help_text='Si se deja vacío, se generará una contraseña automática'
    )
    
    class Meta:
        model = Employee
        fields = [
            'company', 'first_name', 'last_name', 'identification', 
            'date_of_birth', 'gender', 'ethnicity', 'area', 'work_area_erp', 'position',
            'education_level', 'hire_date', 'province', 'city',
            'user_email', 'user_password'
        ]
        widgets = {
            'company': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'}),
            'first_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'}),
            'identification': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'}),
            'ethnicity': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'}),
            'area': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'}),
            'work_area_erp': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'}),
            'position': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'}),
            'education_level': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'}),
            'hire_date': forms.DateInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent', 'type': 'date'}),
            'province': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'}),
            'city': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filtrar empresas según el usuario
        if user:
            if user.is_superuser or user.role == CustomUser.Role.SUPERUSER:
                self.fields['company'].queryset = Company.objects.all()
            else:
                self.fields['company'].queryset = user.managed_companies.all()
        
        # Forzar que province y city sean Select fields
        self.fields['province'].widget = forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'})
        self.fields['city'].widget = forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'})
        
        # Convertir PROVINCIAS_ECUADOR a formato de choices
        provincia_choices = [('', 'Seleccione una provincia')]
        for provincia_tuple in PROVINCIAS_ECUADOR:
            if isinstance(provincia_tuple, tuple):
                provincia_choices.append(provincia_tuple)
            else:
                provincia_choices.append((provincia_tuple, provincia_tuple))
        self.fields['province'].choices = provincia_choices
        
        # Inicializar ciudades vacías
        self.fields['city'].choices = [('', 'Seleccione una ciudad')]
        
        # Si hay provincia seleccionada, cargar ciudades
        if self.instance and self.instance.pk and self.instance.province:
            ciudades = CIUDADES_POR_PROVINCIA.get(self.instance.province, [])
            city_choices = [('', 'Seleccione una ciudad')]
            for ciudad in ciudades:
                city_choices.append((ciudad, ciudad))
            self.fields['city'].choices = city_choices
        
        if self.instance and self.instance.pk:
            if self.instance.user:
                self.fields['user_email'].initial = self.instance.user.email
            self.fields['user_password'].required = False
            self.fields['user_password'].help_text = 'Dejar vacío para mantener la contraseña actual'
    
    def generate_password(self):
        """Genera una contraseña segura de 12 caracteres"""
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for i in range(12))
    
    def save(self, commit=True):
        employee = super().save(commit=False)
        user_email = self.cleaned_data['user_email']
        user_password = self.cleaned_data.get('user_password') or self.generate_password()
        
        if commit:
            # Crear o actualizar usuario empleado
            employee_user, created = CustomUser.objects.get_or_create(
                email=user_email,
                defaults={
                    'role': CustomUser.Role.EMPLOYEE,
                    'is_active': True
                }
            )
            if created or not employee_user.check_password(user_password):
                employee_user.set_password(user_password)
                employee_user.set_stored_password(user_password)  # Encriptar y almacenar contraseña
                employee_user.role = CustomUser.Role.EMPLOYEE
                employee_user.save()
            elif not employee_user.stored_password:
                # Si el usuario existe pero no tiene contraseña almacenada, guardarla ahora
                employee_user.set_stored_password(user_password)
                employee_user.save()
            
            employee.user = employee_user
            employee.save()
            self.user_password = user_password  # Guardar para mostrar después
        
        return employee


class BulkImportForm(forms.Form):
    excel_file = forms.FileField(
        label='Archivo Excel',
        help_text='Seleccione un archivo Excel (.xlsx) con los datos a importar',
        widget=forms.FileInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent', 'accept': '.xlsx'})
    )
    import_type = forms.ChoiceField(
        choices=[
            ('companies', 'Empresas'),
            ('employees', 'Empleados'),
            ('evaluations', 'Evaluaciones Históricas'),
        ],
        label='Tipo de Importación',
        widget=forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent'})
    )

