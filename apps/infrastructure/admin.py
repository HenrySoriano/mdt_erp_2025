from django.contrib import admin
from apps.infrastructure.models import (
    CustomUser, Company, Employee, Dimension, Question, 
    Evaluation, Response, RiskResult, EvaluationPeriod
)


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'role', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('email',)
    ordering = ('-date_joined',)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'ruc', 'city', 'province', 'admin', 'created_at')
    list_filter = ('province', 'city')
    search_fields = ('name', 'ruc')
    ordering = ('name',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'identification', 'company', 'area', 'position', 'created_at')
    list_filter = ('company', 'area', 'education_level', 'gender')
    search_fields = ('first_name', 'last_name', 'identification')
    ordering = ('last_name', 'first_name')


@admin.register(Dimension)
class DimensionAdmin(admin.ModelAdmin):
    list_display = ('order', 'name', 'low_risk_range', 'medium_risk_range', 'high_risk_range')
    ordering = ('order',)
    
    def low_risk_range(self, obj):
        return f"{obj.low_risk_min}-{obj.low_risk_max}"
    low_risk_range.short_description = 'Rango Bajo'
    
    def medium_risk_range(self, obj):
        return f"{obj.medium_risk_min}-{obj.medium_risk_max}"
    medium_risk_range.short_description = 'Rango Medio'
    
    def high_risk_range(self, obj):
        return f"{obj.high_risk_min}-{obj.high_risk_max}"
    high_risk_range.short_description = 'Rango Alto'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('number', 'dimension', 'text_preview')
    list_filter = ('dimension',)
    search_fields = ('text',)
    ordering = ('number',)
    
    def text_preview(self, obj):
        return obj.text[:100] + '...' if len(obj.text) > 100 else obj.text
    text_preview.short_description = 'Pregunta'


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('employee', 'year', 'status', 'date_started', 'date_completed', 'completion_percentage')
    list_filter = ('status', 'year')
    search_fields = ('employee__first_name', 'employee__last_name')
    ordering = ('-date_started',)
    
    def completion_percentage(self, obj):
        return f"{obj.completion_percentage:.0f}%"
    completion_percentage.short_description = 'Completitud'


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('evaluation', 'question', 'answer', 'created_at')
    list_filter = ('answer',)
    search_fields = ('evaluation__employee__first_name', 'evaluation__employee__last_name')
    ordering = ('-created_at',)


@admin.register(RiskResult)
class RiskResultAdmin(admin.ModelAdmin):
    list_display = ('evaluation', 'dimension', 'score', 'risk_level', 'calculated_at')
    list_filter = ('risk_level', 'dimension')
    search_fields = ('evaluation__employee__first_name', 'evaluation__employee__last_name')
    ordering = ('-calculated_at',)


@admin.register(EvaluationPeriod)
class EvaluationPeriodAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'start_date', 'end_date', 'is_active', 'year', 'duration_days_display')
    list_filter = ('is_active', 'year', 'company')
    search_fields = ('name', 'company__name')
    ordering = ('-start_date',)
    date_hierarchy = 'start_date'
    
    fieldsets = (
        ('Información General', {
            'fields': ('company', 'name', 'year')
        }),
        ('Fechas', {
            'fields': ('start_date', 'end_date', 'is_active')
        }),
    )
    
    def duration_days_display(self, obj):
        return f"{obj.duration_days} días"
    duration_days_display.short_description = 'Duración'
