from django.db import models
from django.utils.translation import gettext_lazy as _
from .user import CustomUser


class Company(models.Model):
    """Modelo para representar una empresa"""
    name = models.CharField(_('Nombre'), max_length=200)
    ruc = models.CharField(_('RUC'), max_length=13, unique=True)
    address = models.TextField(_('Dirección'))
    phone = models.CharField(_('Teléfono'), max_length=20)
    email = models.EmailField(_('Email'))
    city = models.CharField(_('Ciudad'), max_length=100)
    province = models.CharField(_('Provincia'), max_length=100)
    admin = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_companies',
        limit_choices_to={'role': CustomUser.Role.COMPANY_ADMIN}
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Empresa')
        verbose_name_plural = _('Empresas')
        ordering = ['name']

    def __str__(self):
        return self.name


class Employee(models.Model):
    """Modelo para representar un empleado con datos sociodemográficos"""
    
    class EducationLevel(models.TextChoices):
        PRIMARIA = 'PRIMARIA', _('Primaria')
        SECUNDARIA = 'SECUNDARIA', _('Secundaria')
        TECNICO = 'TECNICO', _('Técnico')
        UNIVERSITARIO = 'UNIVERSITARIO', _('Universitario')
        POSTGRADO = 'POSTGRADO', _('Postgrado')

    class Ethnicity(models.TextChoices):
        MESTIZO = 'MESTIZO', _('Mestizo')
        INDIGENA = 'INDIGENA', _('Indígena')
        AFROECUATORIANO = 'AFROECUATORIANO', _('Afroecuatoriano')
        BLANCO = 'BLANCO', _('Blanco')
        MONTUBIO = 'MONTUBIO', _('Montubio')
        OTRO = 'OTRO', _('Otro')

    class Gender(models.TextChoices):
        MASCULINO = 'M', _('Masculino')
        FEMENINO = 'F', _('Femenino')
        OTRO = 'O', _('Otro')
    
    class AgeRange(models.TextChoices):
        DIECISEIS_VEINTICUATRO = '16_24', _('16-24 años')
        VEINTICINCO_TREINTAYCUATRO = '25_34', _('25-34 años')
        TREINTAYCINCO_CUARENTAYTRES = '35_43', _('35-43 años')
        CUARENTAYCUATRO_CINCUENTAYDOS = '44_52', _('44-52 años')
        CINCUENTAYTRES_MAS = '53_MAS', _('53 años o más')
    
    class ExperienceRange(models.TextChoices):
        CERO_DOS = '0_2', _('0-2 años')
        TRES_DIEZ = '3_10', _('3-10 años')
        ONCE_VEINTE = '11_20', _('11-20 años')
        VEINTIUNO_MAS = '21_MAS', _('21 años o más')
    
    class WorkAreaERP(models.TextChoices):
        ADMINISTRATIVA = 'ADMINISTRATIVA', _('Administrativa')
        OPERATIVA = 'OPERATIVA', _('Operativa')
        COMERCIAL = 'COMERCIAL', _('Comercial')
        LOGISTICA = 'LOGISTICA', _('Logística')
        PRODUCCION = 'PRODUCCION', _('Producción')
        TRANSFORMACION = 'TRANSFORMACION', _('Transformación')
        SOPORTE = 'SOPORTE', _('Soporte')
        TECNOLOGIA_INNOVACION = 'TECNOLOGIA_INNOVACION', _('Tecnología e Innovación')

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='employee_profile'
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='employees'
    )
    
    # Datos personales
    first_name = models.CharField(_('Nombres'), max_length=100)
    last_name = models.CharField(_('Apellidos'), max_length=100)
    identification = models.CharField(_('Cédula'), max_length=10, unique=True)
    date_of_birth = models.DateField(_('Fecha de nacimiento'))
    gender = models.CharField(_('Sexo'), max_length=1, choices=Gender.choices)
    ethnicity = models.CharField(_('Auto-identificación étnica'), max_length=20, choices=Ethnicity.choices)
    
    # Datos laborales
    area = models.CharField(_('Área de trabajo (Texto libre)'), max_length=100, help_text='Nombre del área según la empresa')
    work_area_erp = models.CharField(
        _('Área de Trabajo ERP'), 
        max_length=30, 
        choices=WorkAreaERP.choices,
        default='ADMINISTRATIVA',
        help_text='Área según clasificación del cuestionario MDT (para comparación con evaluaciones)'
    )
    position = models.CharField(_('Cargo'), max_length=100)
    education_level = models.CharField(_('Nivel de instrucción'), max_length=20, choices=EducationLevel.choices)
    hire_date = models.DateField(
        _('Fecha de ingreso a la empresa'), 
        help_text='La antigüedad se calculará automáticamente desde esta fecha',
        default='2020-01-01'  # Fecha por defecto para empleados existentes
    )
    
    # Datos de ubicación
    province = models.CharField(_('Provincia'), max_length=100)
    city = models.CharField(_('Ciudad'), max_length=100)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Empleado')
        verbose_name_plural = _('Empleados')
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self):
        """Calcula la edad actual del empleado"""
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
    
    @property
    def years_of_experience(self):
        """Calcula los años de experiencia/antigüedad desde la fecha de ingreso"""
        from datetime import date
        today = date.today()
        years = today.year - self.hire_date.year - (
            (today.month, today.day) < (self.hire_date.month, self.hire_date.day)
        )
        return max(0, years)  # No puede ser negativo
    
    @property
    def age_range(self):
        """
        Calcula el rango de edad basándose en la edad actual.
        Usa los mismos rangos que el modelo Evaluation para consistencia.
        """
        age = self.age
        if 16 <= age <= 24:
            return '16-24'
        elif 25 <= age <= 34:
            return '25-34'
        elif 35 <= age <= 43:
            return '35-43'
        elif 44 <= age <= 52:
            return '44-52'
        elif age >= 53:
            return '53+'
        else:
            return None  # Menor de 16 años
    
    def get_age_range_display(self):
        """Devuelve la representación legible del rango de edad"""
        age_range = self.age_range
        age_range_labels = {
            '16-24': '16-24 años',
            '25-34': '25-34 años',
            '35-43': '35-43 años',
            '44-52': '44-52 años',
            '53+': 'Igual o superior a 53 años'
        }
        return age_range_labels.get(age_range, 'No definido')
    
    @property
    def experience_range(self):
        """
        Calcula el rango de antigüedad/experiencia basándose en years_of_experience.
        Usa los mismos rangos que el modelo Evaluation para consistencia.
        """
        years = self.years_of_experience
        if 0 <= years <= 2:
            return '0-2'
        elif 3 <= years <= 10:
            return '3-10'
        elif 11 <= years <= 20:
            return '11-20'
        elif years >= 21:
            return '21+'
        else:
            return None
    
    def get_experience_range_display(self):
        """Devuelve la representación legible del rango de experiencia"""
        exp_range = self.experience_range
        exp_range_labels = {
            '0-2': '0-2 años',
            '3-10': '3-10 años',
            '11-20': '11-20 años',
            '21+': 'Igual o superior a 21 años'
        }
        return exp_range_labels.get(exp_range, 'No definido')