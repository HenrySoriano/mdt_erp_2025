from django.db import models
from django.utils.translation import gettext_lazy as _
from .company import Employee


class Dimension(models.Model):
    """Modelo para las 14 dimensiones de evaluación de riesgo psicosocial"""
    name = models.CharField(_('Nombre'), max_length=100, unique=True)
    description = models.TextField(_('Descripción'), blank=True)
    order = models.IntegerField(_('Orden'), unique=True)
    
    # Rangos de riesgo
    low_risk_min = models.IntegerField(_('Riesgo Bajo - Mínimo'))
    low_risk_max = models.IntegerField(_('Riesgo Bajo - Máximo'))
    medium_risk_min = models.IntegerField(_('Riesgo Medio - Mínimo'))
    medium_risk_max = models.IntegerField(_('Riesgo Medio - Máximo'))
    high_risk_min = models.IntegerField(_('Riesgo Alto - Mínimo'))
    high_risk_max = models.IntegerField(_('Riesgo Alto - Máximo'))
    
    class Meta:
        verbose_name = _('Dimensión')
        verbose_name_plural = _('Dimensiones')
        ordering = ['order']

    def __str__(self):
        return self.name

    def calculate_risk_level(self, score):
        """Calcula el nivel de riesgo basado en el puntaje"""
        if self.low_risk_min <= score <= self.low_risk_max:
            return 'BAJO'
        elif self.medium_risk_min <= score <= self.medium_risk_max:
            return 'MEDIO'
        elif self.high_risk_min <= score <= self.high_risk_max:
            return 'ALTO'
        return 'INDEFINIDO'


class Question(models.Model):
    """Modelo para las 58 preguntas del cuestionario"""
    dimension = models.ForeignKey(
        Dimension,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    number = models.IntegerField(_('Número de ítem'), unique=True)
    text = models.TextField(_('Texto de la pregunta'))
    explanation = models.TextField(_('Explicación de la pregunta'), blank=True, help_text='Explicación detallada con ejemplos para ayudar a entender la pregunta')
    
    class Meta:
        verbose_name = _('Pregunta')
        verbose_name_plural = _('Preguntas')
        ordering = ['number']

    def __str__(self):
        return f"Ítem {self.number}: {self.text[:50]}..."


class Evaluation(models.Model):
    """Modelo para una evaluación de riesgo psicosocial"""
    
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', _('Borrador')
        COMPLETED = 'COMPLETED', _('Completada')
    
    # Opciones para datos generales
    class WorkArea(models.TextChoices):
        ADMINISTRATIVA = 'ADMINISTRATIVA', _('Administrativa')
        OPERATIVA = 'OPERATIVA', _('Operativa')
        COMERCIAL = 'COMERCIAL', _('Comercial')
        LOGISTICA = 'LOGISTICA', _('Logística')
        PRODUCCION = 'PRODUCCION', _('Producción')
        TRANSFORMACION = 'TRANSFORMACION', _('Transformación')
        SOPORTE = 'SOPORTE', _('Soporte')
        TECNOLOGIA_INNOVACION = 'TECNOLOGIA_INNOVACION', _('Tecnología e Innovación')
    
    class EducationLevel(models.TextChoices):
        NINGUNO = 'NINGUNO', _('Ninguno')
        EDUCACION_BASICA = 'EDUCACION_BASICA', _('Educación básica')
        EDUCACION_MEDIA = 'EDUCACION_MEDIA', _('Educación media')
        BACHILLERATO = 'BACHILLERATO', _('Bachillerato')
        TECNICO_TECNOLOGICO = 'TECNICO_TECNOLOGICO', _('Técnico/Tecnológico')
        TERCER_NIVEL = 'TERCER_NIVEL', _('Tercer Nivel')
        CUARTO_NIVEL = 'CUARTO_NIVEL', _('Cuarto Nivel')
        OTRO = 'OTRO', _('Otro')
    
    class ExperienceRange(models.TextChoices):
        CERO_DOS = '0-2', _('0-2 años')
        TRES_DIEZ = '3-10', _('3-10 años')
        ONCE_VEINTE = '11-20', _('11-20 años')
        VEINTIUNO_MAS = '21+', _('Igual o superior a 21 años')
    
    class AgeRange(models.TextChoices):
        DIECISEIS_VEINTICUATRO = '16-24', _('16-24 años')
        VEINTICINCO_TREINTAYCUATRO = '25-34', _('25-34 años')
        TREINTAYCINCO_CUARENTAYTRES = '35-43', _('35-43 años')
        CUARENTAYCUATRO_CINCUENTAYDOS = '44-52', _('44-52 años')
        CINCUENTAYTRES_MAS = '53+', _('Igual o superior a 53 años')
    
    class Ethnicity(models.TextChoices):
        INDIGENA = 'INDIGENA', _('Indígena')
        AFRO_ECUATORIANO = 'AFRO_ECUATORIANO', _('Afro-ecuatoriano')
        MESTIZO = 'MESTIZO', _('Mestizo/a')
        MONTUBIO = 'MONTUBIO', _('Montubio/a')
        BLANCO = 'BLANCO', _('Blanco/a')
        OTRO = 'OTRO', _('Otro')
    
    class Gender(models.TextChoices):
        MASCULINO = 'M', _('Masculino')
        FEMENINO = 'F', _('Femenino')

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='evaluations'
    )
    status = models.CharField(
        _('Estado'),
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT
    )
    year = models.IntegerField(_('Año'))
    date_started = models.DateTimeField(_('Fecha de inicio'), auto_now_add=True)
    date_completed = models.DateTimeField(_('Fecha de finalización'), null=True, blank=True)
    
    # Datos generales para el informe
    evaluation_date = models.DateField(_('Fecha de evaluación'), null=True, blank=True)
    province = models.CharField(_('Provincia'), max_length=100, blank=True)
    city = models.CharField(_('Ciudad'), max_length=100, blank=True)
    work_area = models.CharField(_('Área de trabajo'), max_length=30, choices=WorkArea.choices, blank=True)
    education_level = models.CharField(_('Nivel más alto de instrucción'), max_length=30, choices=EducationLevel.choices, blank=True)
    experience_range = models.CharField(_('Antigüedad en la empresa'), max_length=10, choices=ExperienceRange.choices, blank=True)
    age_range = models.CharField(_('Edad del trabajador'), max_length=10, choices=AgeRange.choices, blank=True)
    ethnicity = models.CharField(_('Auto-identificación étnica'), max_length=20, choices=Ethnicity.choices, blank=True)
    gender = models.CharField(_('Género'), max_length=1, choices=Gender.choices, blank=True)
    
    class Meta:
        verbose_name = _('Evaluación')
        verbose_name_plural = _('Evaluaciones')
        ordering = ['-date_started']
        unique_together = ['employee', 'year', 'status']

    def __str__(self):
        return f"Evaluación {self.year} - {self.employee.full_name} ({self.get_status_display()})"

    @property
    def is_complete(self):
        return self.status == self.Status.COMPLETED

    @property
    def completion_percentage(self):
        """Calcula el porcentaje de completitud"""
        total_questions = Question.objects.count()
        answered_questions = self.responses.count()
        if total_questions == 0:
            return 0
        return (answered_questions / total_questions) * 100


class Response(models.Model):
    """Modelo para las respuestas individuales a cada pregunta"""
    
    class Answer(models.IntegerChoices):
        EN_DESACUERDO = 1, _('En desacuerdo')
        POCO_DE_ACUERDO = 2, _('Poco de acuerdo')
        PARCIALMENTE_DE_ACUERDO = 3, _('Parcialmente de acuerdo')
        COMPLETAMENTE_DE_ACUERDO = 4, _('Completamente de acuerdo')

    evaluation = models.ForeignKey(
        Evaluation,
        on_delete=models.CASCADE,
        related_name='responses'
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='responses'
    )
    answer = models.IntegerField(
        _('Respuesta'),
        choices=Answer.choices
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Respuesta')
        verbose_name_plural = _('Respuestas')
        unique_together = ['evaluation', 'question']

    def __str__(self):
        return f"Respuesta a Ítem {self.question.number}: {self.get_answer_display()}"


class RiskResult(models.Model):
    """Modelo para almacenar los resultados calculados por dimensión"""
    
    class RiskLevel(models.TextChoices):
        BAJO = 'BAJO', _('Riesgo Bajo')
        MEDIO = 'MEDIO', _('Riesgo Medio')
        ALTO = 'ALTO', _('Riesgo Alto')

    evaluation = models.ForeignKey(
        Evaluation,
        on_delete=models.CASCADE,
        related_name='risk_results'
    )
    dimension = models.ForeignKey(
        Dimension,
        on_delete=models.CASCADE,
        related_name='risk_results'
    )
    score = models.IntegerField(_('Puntaje'))
    risk_level = models.CharField(
        _('Nivel de riesgo'),
        max_length=10,
        choices=RiskLevel.choices
    )
    calculated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Resultado de Riesgo')
        verbose_name_plural = _('Resultados de Riesgo')
        unique_together = ['evaluation', 'dimension']

    def __str__(self):
        return f"{self.dimension.name}: {self.get_risk_level_display()} ({self.score})"
