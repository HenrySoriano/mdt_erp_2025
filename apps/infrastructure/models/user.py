from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from apps.presentation.utils.encryption import encrypt_password, decrypt_password

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        SUPERUSER = 'SUPERUSER', _('Superuser')
        COMPANY_ADMIN = 'COMPANY_ADMIN', _('Company Admin')
        EMPLOYEE = 'EMPLOYEE', _('Employee')

    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.EMPLOYEE)
    stored_password = models.CharField(_('Contraseña almacenada'), max_length=500, blank=True, null=True, 
                                       help_text='Contraseña encriptada para referencia del administrador')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    def set_stored_password(self, password):
        """
        Encripta y guarda una contraseña en stored_password
        """
        if password:
            self.stored_password = encrypt_password(password)
        else:
            self.stored_password = None
    
    def get_stored_password(self, user=None):
        """
        Desencripta y retorna la contraseña almacenada
        Solo permite desencriptar si el usuario es superusuario
        
        Args:
            user: Usuario que solicita la contraseña (debe ser superusuario)
            
        Returns:
            String con la contraseña desencriptada o None
        """
        if not self.stored_password:
            return None
        
        # Solo superusuarios pueden ver contraseñas
        if user and (user.is_superuser or user.role == self.Role.SUPERUSER):
            try:
                return decrypt_password(self.stored_password)
            except Exception:
                # Si falla la desencriptación, retornar None
                return None
        
        return None


@receiver(pre_save, sender=CustomUser)
def encrypt_stored_password(sender, instance, **kwargs):
    """
    Signal para encriptar stored_password antes de guardar
    Solo encripta si el valor cambió y no está ya encriptado
    """
    if instance.stored_password:
        # Verificar si ya está encriptado (los valores encriptados son más largos y tienen formato específico)
        # Si tiene menos de 50 caracteres, probablemente no está encriptado
        if len(instance.stored_password) < 50:
            # Intentar encriptar solo si parece ser texto plano
            try:
                # Verificar si puede ser desencriptado (ya está encriptado)
                decrypt_password(instance.stored_password)
            except:
                # No está encriptado, encriptarlo
                instance.set_stored_password(instance.stored_password)

