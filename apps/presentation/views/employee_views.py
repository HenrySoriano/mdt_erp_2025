from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse
from datetime import datetime
from apps.infrastructure.models import Employee, Evaluation, Question, Response, RiskResult
from apps.application.services.risk_calculator import RiskCalculatorService
from apps.application.services.recommendations_service import RecommendationsService
from apps.presentation.utils.ecuador_data import PROVINCIAS_ECUADOR, CIUDADES_POR_PROVINCIA, get_todas_las_ciudades
from django.utils import timezone


@login_required
def employee_dashboard(request):
    """Dashboard para empleados"""
    try:
        employee = request.user.employee_profile
    except Employee.DoesNotExist:
        messages.error(request, 'No tienes un perfil de empleado asociado')
        return redirect('login')
    
    current_year = datetime.now().year
    
    # Verificar si ya tiene una evaluación este año
    current_evaluation = Evaluation.objects.filter(
        employee=employee,
        year=current_year
    ).first()
    
    # Obtener evaluaciones completadas
    completed_evaluations = Evaluation.objects.filter(
        employee=employee,
        status=Evaluation.Status.COMPLETED
    ).order_by('-year')
    
    context = {
        'employee': employee,
        'current_year': current_year,
        'current_evaluation': current_evaluation,
        'completed_evaluations': completed_evaluations,
        'has_current_evaluation': current_evaluation is not None,
        'can_start_evaluation': current_evaluation is None or current_evaluation.status == Evaluation.Status.DRAFT,
    }
    
    return render(request, 'employee/dashboard.html', context)


@login_required
def start_evaluation(request):
    """Inicia o continúa una evaluación"""
    try:
        employee = request.user.employee_profile
    except Employee.DoesNotExist:
        messages.error(request, 'No tienes un perfil de empleado asociado')
        return redirect('login')
    
    current_year = datetime.now().year
    
    # Buscar evaluación existente o crear una nueva
    evaluation, created = Evaluation.objects.get_or_create(
        employee=employee,
        year=current_year,
        status=Evaluation.Status.DRAFT,
        defaults={'year': current_year}
    )
    
    if created:
        messages.success(request, 'Evaluación iniciada. Puedes guardar tu progreso en cualquier momento.')
    
    return redirect('take_evaluation', evaluation_id=evaluation.id)


@login_required
def take_evaluation(request, evaluation_id):
    """Formulario para tomar la evaluación"""
    try:
        employee = request.user.employee_profile
    except Employee.DoesNotExist:
        messages.error(request, 'No tienes un perfil de empleado asociado')
        return redirect('login')
    
    evaluation = get_object_or_404(Evaluation, id=evaluation_id, employee=employee)
    
    if evaluation.is_complete:
        messages.info(request, 'Esta evaluación ya fue completada')
        return redirect('view_evaluation_results', evaluation_id=evaluation.id)
    
    questions = Question.objects.all().order_by('number')
    
    # Obtener respuestas existentes
    existing_responses = {
        r.question_id: r.answer 
        for r in Response.objects.filter(evaluation=evaluation)
    }
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        with transaction.atomic():
            # Guardar datos generales
            if 'evaluation_date' in request.POST and request.POST['evaluation_date']:
                from datetime import datetime as dt
                evaluation.evaluation_date = dt.strptime(request.POST['evaluation_date'], '%Y-%m-%d').date()
            evaluation.province = request.POST.get('province', '')
            evaluation.city = request.POST.get('city', '')
            evaluation.work_area = request.POST.get('work_area', '')
            evaluation.education_level = request.POST.get('education_level', '')
            evaluation.experience_range = request.POST.get('experience_range', '')
            evaluation.age_range = request.POST.get('age_range', '')
            evaluation.ethnicity = request.POST.get('ethnicity', '')
            evaluation.gender = request.POST.get('gender', '')
            evaluation.save()
            
            # Guardar todas las respuestas
            for question in questions:
                answer_key = f'question_{question.id}'
                if answer_key in request.POST:
                    answer = int(request.POST[answer_key])
                    Response.objects.update_or_create(
                        evaluation=evaluation,
                        question=question,
                        defaults={'answer': answer}
                    )
            
            if action == 'save_draft':
                messages.success(request, 'Progreso guardado exitosamente')
                return redirect('employee_dashboard')
            
            elif action == 'submit':
                # Verificar que todas las preguntas estén respondidas
                total_questions = questions.count()
                answered_questions = Response.objects.filter(evaluation=evaluation).count()
                
                if answered_questions < total_questions:
                    messages.error(request, f'Debes responder todas las preguntas. Respondidas: {answered_questions}/{total_questions}')
                else:
                    # Marcar como completada
                    evaluation.status = Evaluation.Status.COMPLETED
                    evaluation.date_completed = datetime.now()
                    evaluation.save()
                    
                    # Calcular riesgos
                    calculator = RiskCalculatorService()
                    calculator.calculate_evaluation_risk(evaluation)
                    
                    messages.success(request, '¡Evaluación completada exitosamente!')
                    return redirect('view_evaluation_results', evaluation_id=evaluation.id)
    
    # Preparar datos de provincias y ciudades
    provincias = PROVINCIAS_ECUADOR
    todas_las_ciudades = get_todas_las_ciudades()
    
    # Si hay una provincia seleccionada, obtener sus ciudades
    provincia_seleccionada = evaluation.province or employee.province
    ciudades = CIUDADES_POR_PROVINCIA.get(provincia_seleccionada, todas_las_ciudades) if provincia_seleccionada else todas_las_ciudades
    
    # Preparar ciudades por provincia para JavaScript
    ciudades_por_provincia = {provincia: ciudades for provincia, ciudades in CIUDADES_POR_PROVINCIA.items()}
    
    context = {
        'evaluation': evaluation,
        'employee': employee,
        'questions': questions,
        'existing_responses': existing_responses,
        'completion_percentage': evaluation.completion_percentage,
        'provincias': provincias,
        'ciudades': ciudades,
        'ciudades_por_provincia': ciudades_por_provincia,
    }
    
    return render(request, 'employee/take_evaluation.html', context)


@login_required
def view_evaluation_results(request, evaluation_id):
    """Ver resultados de una evaluación completada"""
    try:
        employee = request.user.employee_profile
    except Employee.DoesNotExist:
        messages.error(request, 'No tienes un perfil de empleado asociado')
        return redirect('login')
    
    evaluation = get_object_or_404(
        Evaluation,
        id=evaluation_id,
        employee=employee,
        status=Evaluation.Status.COMPLETED
    )
    
    # Obtener resultados por dimensión
    risk_results = RiskResult.objects.filter(evaluation=evaluation).select_related('dimension').prefetch_related('dimension__questions').order_by('dimension__order')
    
    # Agregar número de preguntas por dimensión a cada resultado
    for result in risk_results:
        result.question_count = result.dimension.questions.count()
    
    # Calcular resumen
    calculator = RiskCalculatorService()
    summary = calculator.get_evaluation_summary(evaluation)
    
    # Obtener recomendaciones personalizadas (con género)
    recommendations_service = RecommendationsService()
    recommendations = recommendations_service.get_all_recommendations(risk_results, evaluation)
    
    # Contar dimensiones por nivel de riesgo
    risk_counts = {
        'BAJO': risk_results.filter(risk_level='BAJO').count(),
        'MEDIO': risk_results.filter(risk_level='MEDIO').count(),
        'ALTO': risk_results.filter(risk_level='ALTO').count(),
    }
    
    # Separar dimensiones por nivel para mejor visualización
    high_risk_results = list(risk_results.filter(risk_level='ALTO'))
    medium_risk_results = list(risk_results.filter(risk_level='MEDIO'))[:2]  # Solo las primeras 2
    
    # Obtener evaluaciones completadas para el botón de comparar
    completed_evaluations = Evaluation.objects.filter(
        employee=evaluation.employee,
        status=Evaluation.Status.COMPLETED
    ).exclude(id=evaluation.id)
    
    context = {
        'evaluation': evaluation,
        'employee': evaluation.employee,
        'risk_results': risk_results,
        'summary': summary,
        'recommendations': recommendations,
        'risk_counts': risk_counts,
        'high_risk_results': high_risk_results,
        'medium_risk_results': medium_risk_results,
        'completed_evaluations': completed_evaluations,
    }
    
    return render(request, 'employee/evaluation_results.html', context)


@login_required
def compare_evaluations(request):
    """Comparar evaluaciones de diferentes años"""
    try:
        employee = request.user.employee_profile
    except Employee.DoesNotExist:
        messages.error(request, 'No tienes un perfil de empleado asociado')
        return redirect('login')
    
    # Obtener años disponibles
    completed_evaluations = Evaluation.objects.filter(
        employee=employee,
        status=Evaluation.Status.COMPLETED
    ).order_by('-year')
    
    available_years = list(completed_evaluations.values_list('year', flat=True))
    
    comparison_data = None
    
    if request.method == 'GET' and 'year1' in request.GET and 'year2' in request.GET:
        # Validar años de forma segura
        try:
            year1 = validate_year(request.GET.get('year1', str(datetime.now().year)))
            year2 = validate_year(request.GET.get('year2', str(datetime.now().year)))
        except (ValueError, TypeError, KeyError, ValidationError):
            messages.error(request, 'Años inválidos para comparación')
            return redirect('compare_evaluations')
        
        try:
            calculator = RiskCalculatorService()
            comparison_data = calculator.compare_evaluations(employee.id, year1, year2)
        except ValueError as e:
            messages.error(request, str(e))
    
    context = {
        'employee': employee,
        'available_years': available_years,
        'comparison_data': comparison_data,
    }
    
    return render(request, 'employee/compare_evaluations.html', context)


@login_required
def download_evaluation_pdf(request, evaluation_id):
    """Genera y descarga un PDF con los resultados de la evaluación"""
    # Importar reportlab solo cuando se necesite
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
        from io import BytesIO
    except ImportError:
        messages.error(request, 'Error: La librería reportlab no está instalada correctamente.')
        return redirect('view_evaluation_results', evaluation_id=evaluation_id)
    
    try:
        employee = request.user.employee_profile
    except Employee.DoesNotExist:
        messages.error(request, 'No tienes un perfil de empleado asociado')
        return redirect('login')
    
    evaluation = get_object_or_404(
        Evaluation,
        id=evaluation_id,
        employee=employee,
        status=Evaluation.Status.COMPLETED
    )
    
    # Obtener resultados por dimensión
    risk_results = RiskResult.objects.filter(evaluation=evaluation).select_related('dimension').prefetch_related('dimension__questions').order_by('dimension__order')
    
    # Agregar número de preguntas por dimensión a cada resultado
    for result in risk_results:
        result.question_count = result.dimension.questions.count()
    
    # Calcular resumen
    calculator = RiskCalculatorService()
    summary = calculator.get_evaluation_summary(evaluation)
    
    # Obtener recomendaciones personalizadas (con género)
    recommendations_service = RecommendationsService()
    recommendations = recommendations_service.get_all_recommendations(risk_results, evaluation)
    
    # Contar dimensiones por nivel de riesgo
    risk_counts = {
        'BAJO': risk_results.filter(risk_level='BAJO').count(),
        'MEDIO': risk_results.filter(risk_level='MEDIO').count(),
        'ALTO': risk_results.filter(risk_level='ALTO').count(),
    }
    
    # Crear el PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1e3a8a'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#334155'),
        spaceAfter=8,
        spaceBefore=8,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#1f2937'),
        spaceAfter=6,
        alignment=TA_JUSTIFY
    )
    
    # Título
    title = Paragraph(f"Informe de Evaluación de Riesgo Psicosocial {evaluation.year}", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))
    
    # Información del empleado
    info_data = [
        ['Empleado:', employee.full_name],
        ['Empresa:', employee.company.name],
        ['Área:', employee.area],
        ['Fecha de Evaluación:', evaluation.date_completed.strftime('%d/%m/%Y') if evaluation.date_completed else 'N/A'],
        ['Año:', str(evaluation.year)],
    ]
    
    info_table = Table(info_data, colWidths=[2*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e0e7ff')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1e293b')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Resumen de riesgo general
    overall_risk = summary.get('overall_risk', 'MEDIO')
    risk_color = colors.HexColor('#10b981') if overall_risk == 'BAJO' else (colors.HexColor('#eab308') if overall_risk == 'MEDIO' else colors.HexColor('#ef4444'))
    
    summary_heading = Paragraph("Resumen General", heading_style)
    elements.append(summary_heading)
    
    summary_data = [
        ['Riesgo General:', overall_risk],
        ['Dimensiones con Bajo Riesgo:', str(risk_counts['BAJO'])],
        ['Dimensiones con Medio Riesgo:', str(risk_counts['MEDIO'])],
        ['Dimensiones con Alto Riesgo:', str(risk_counts['ALTO'])],
    ]
    
    summary_table = Table(summary_data, colWidths=[3*inch, 3*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f1f5f9')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1e293b')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (1, 0), (1, 0), risk_color),
        ('TEXTCOLOR', (1, 0), (1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Resultados por dimensión
    dimensions_heading = Paragraph("Resultados por Dimensión", heading_style)
    elements.append(dimensions_heading)
    
    # Encabezado de la tabla
    dimensions_header = [['Dimensión', 'Puntaje', 'Nivel de Riesgo']]
    
    # Datos de dimensiones
    dimensions_data = []
    for result in risk_results:
        risk_color_cell = colors.HexColor('#10b981') if result.risk_level == 'BAJO' else (colors.HexColor('#eab308') if result.risk_level == 'MEDIO' else colors.HexColor('#ef4444'))
        dimensions_data.append([
            result.dimension.name,
            str(result.score),
            result.risk_level
        ])
    
    # Crear tabla completa
    dimensions_table_data = dimensions_header + dimensions_data
    dimensions_table = Table(dimensions_table_data, colWidths=[3.5*inch, 1.5*inch, 1.5*inch])
    
    # Estilos de la tabla
    table_style = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
    ]
    
    # Colorear celdas de nivel de riesgo
    for i, result in enumerate(risk_results, start=1):
        risk_color_cell = colors.HexColor('#10b981') if result.risk_level == 'BAJO' else (colors.HexColor('#eab308') if result.risk_level == 'MEDIO' else colors.HexColor('#ef4444'))
        table_style.append(('BACKGROUND', (2, i), (2, i), risk_color_cell))
        table_style.append(('TEXTCOLOR', (2, i), (2, i), colors.white))
        table_style.append(('FONTNAME', (2, i), (2, i), 'Helvetica-Bold'))
    
    dimensions_table.setStyle(TableStyle(table_style))
    elements.append(dimensions_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Recomendaciones por dimensión
    recommendations_heading = Paragraph("Recomendaciones por Dimensión", heading_style)
    elements.append(recommendations_heading)
    
    for result in risk_results:
        dim_recs = recommendations.get(result.dimension.name, [])
        if dim_recs:
            # Color del título según nivel de riesgo
            risk_title_color = colors.HexColor('#059669') if result.risk_level == 'BAJO' else (colors.HexColor('#ca8a04') if result.risk_level == 'MEDIO' else colors.HexColor('#dc2626'))
            
            dim_title_style = ParagraphStyle(
                'DimTitle',
                parent=styles['Heading3'],
                fontSize=11,
                textColor=risk_title_color,
                spaceAfter=6,
                spaceBefore=10,
                fontName='Helvetica-Bold'
            )
            
            dim_title = Paragraph(f"{result.dimension.name} ({result.risk_level})", dim_title_style)
            elements.append(dim_title)
            
            for rec in dim_recs:
                rec_para = Paragraph(f"• {rec}", normal_style)
                elements.append(rec_para)
            
            elements.append(Spacer(1, 0.15*inch))
    
    # Mensaje general
    elements.append(Spacer(1, 0.2*inch))
    general_heading = Paragraph("Mensaje General", heading_style)
    elements.append(general_heading)
    
    if overall_risk == 'ALTO':
        general_message = "Esta evaluación identifica áreas donde podemos trabajar juntos para mejorar tu bienestar laboral. Cada dimensión tiene oportunidades de mejora que pueden abordarse de manera colaborativa. Considera conversar con tu supervisor/a o recursos humanos sobre estas áreas de manera constructiva, enfocándote en soluciones que beneficien a todos. Recuerda que tu bienestar es importante y que hay recursos disponibles para apoyarte en este proceso de mejora continua."
    elif overall_risk == 'MEDIO':
        general_message = "Tu evaluación muestra algunas áreas con oportunidades de mejora. Identifica las dimensiones específicas donde puedes trabajar en conjunto con tu equipo. Establece metas concretas y alcanzables para mejorar estas dimensiones de manera colaborativa. Busca apoyo y recursos disponibles para fortalecer estas áreas. El trabajo en equipo es clave para el éxito."
    else:
        general_message = "¡Felicitaciones! Tu evaluación muestra un buen equilibrio general. Continúa manteniendo este nivel y aprovecha las fortalezas identificadas. Aunque el riesgo general es bajo, mantén la atención en las dimensiones que pueden seguir mejorándose. El crecimiento continuo beneficia a todos."
    
    general_para = Paragraph(general_message, normal_style)
    elements.append(general_para)
    elements.append(Spacer(1, 0.3*inch))
    
    # Pie de página
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#64748b'),
        alignment=TA_CENTER
    )
    footer = Paragraph(f"Informe generado el {datetime.now().strftime('%d/%m/%Y a las %H:%M')} | Sistema de Evaluación de Riesgo Psicosocial", footer_style)
    elements.append(footer)
    
    # Construir PDF
    doc.build(elements)
    
    # Preparar respuesta
    buffer.seek(0)
    response = HttpResponse(buffer.read(), content_type='application/pdf')
    # Limpiar nombre del archivo de caracteres especiales
    safe_name = employee.full_name.replace(' ', '_').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('ñ', 'n')
    safe_name = ''.join(c for c in safe_name if c.isalnum() or c in ('_', '-'))
    filename = f"Evaluacion_Riesgo_Psicosocial_{evaluation.year}_{safe_name}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response
