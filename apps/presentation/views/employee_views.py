from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.core.exceptions import ValidationError
from datetime import datetime
import json
from apps.infrastructure.models import Employee, Evaluation, Question, Response, RiskResult, EvaluationPeriod, Dimension
from apps.application.services.risk_calculator import RiskCalculatorService
from apps.application.services.recommendations_service import RecommendationsService
from apps.presentation.utils.ecuador_data import PROVINCIAS_ECUADOR, CIUDADES_POR_PROVINCIA, get_todas_las_ciudades
from apps.presentation.utils.security import validate_year
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
    
    # Buscar período activo para la empresa
    active_period = EvaluationPeriod.objects.filter(
        company=employee.company,
        is_active=True,
        year=current_year
    ).first()
    
    # Verificar si ya tiene una evaluación para el período activo
    current_evaluation = None
    if active_period:
        current_evaluation = Evaluation.objects.filter(
            employee=employee,
            evaluation_period=active_period
        ).first()
    
    # Obtener evaluaciones completadas
    completed_evaluations = Evaluation.objects.filter(
        employee=employee,
        status=Evaluation.Status.COMPLETED
    ).order_by('-year')
    
    # Verificar si puede crear nueva evaluación (hay período activo y no tiene evaluación completada o puede editar)
    can_create_new = False
    if active_period:
        today = timezone.now().date()
        if active_period.start_date <= today <= active_period.end_date:
            if not current_evaluation:
                can_create_new = True
            elif current_evaluation.is_complete and current_evaluation.can_edit():
                can_create_new = True
    
    context = {
        'employee': employee,
        'current_year': current_year,
        'current_evaluation': current_evaluation,
        'completed_evaluations': completed_evaluations,
        'has_current_evaluation': current_evaluation is not None,
        'can_start_evaluation': current_evaluation is None or current_evaluation.status == Evaluation.Status.DRAFT,
        'active_period': active_period,
        'can_create_new': can_create_new,
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
    
    # Buscar período activo para la empresa
    active_period = EvaluationPeriod.objects.filter(
        company=employee.company,
        is_active=True,
        year=current_year
    ).first()
    
    if not active_period:
        messages.error(request, 'No hay un período de evaluación activo para tu empresa. Contacta al administrador.')
        return redirect('employee_dashboard')
    
    # Verificar que la fecha actual esté dentro del período
    today = timezone.now().date()
    if today < active_period.start_date or today > active_period.end_date:
        messages.error(request, f'El período de evaluación está cerrado. Período: {active_period.start_date} - {active_period.end_date}')
        return redirect('employee_dashboard')
    
    # Buscar evaluación existente para este período o crear una nueva
    evaluation = Evaluation.objects.filter(
        employee=employee,
        evaluation_period=active_period
    ).first()
    
    if evaluation:
        if evaluation.is_complete and not evaluation.can_edit():
            messages.info(request, 'Ya completaste la evaluación para este período y alcanzaste el límite de ediciones.')
            return redirect('view_evaluation_results', evaluation_id=evaluation.id)
        return redirect('take_evaluation', evaluation_id=evaluation.id)
    
    # Crear nueva evaluación para este período
    evaluation = Evaluation.objects.create(
        employee=employee,
        year=current_year,
        evaluation_period=active_period,
        status=Evaluation.Status.DRAFT
    )
    
    messages.success(request, f'Evaluación iniciada para el período {active_period.name}. Puedes guardar tu progreso en cualquier momento.')
    
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
    
    # Si está completada pero puede editar, permitir acceso
    if evaluation.is_complete and not evaluation.can_edit():
        messages.info(request, 'Esta evaluación ya fue completada y has alcanzado el límite de ediciones.')
        return redirect('view_evaluation_results', evaluation_id=evaluation.id)
    
    # Si está completada pero puede editar, mostrar mensaje
    if evaluation.is_complete and evaluation.can_edit():
        remaining = evaluation.get_remaining_edits()
        messages.warning(request, f'Estás editando una evaluación completada. Te quedan {remaining} ediciones restantes.')
    
    questions = Question.objects.all().order_by('number')
    
    # Obtener respuestas existentes
    existing_responses = {
        r.question_id: r.answer 
        for r in Response.objects.filter(evaluation=evaluation)
    }
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        # Manejar aceptación de confidencialidad
        if action == 'accept_confidentiality':
            evaluation.confidentiality_accepted = True
            evaluation.save()
            return redirect('take_evaluation', evaluation_id=evaluation.id)
        
        # Verificar si puede editar (si está completada)
        if evaluation.is_complete and not evaluation.can_edit():
            messages.error(request, f'Has alcanzado el límite de 3 ediciones. No puedes modificar esta evaluación.')
            return redirect('view_evaluation_results', evaluation_id=evaluation.id)
        
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
            
            # Guardar aceptación de confidencialidad si viene
            if 'confidentiality_accepted' in request.POST:
                evaluation.confidentiality_accepted = True
            
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
            
            elif action == 'preview_results':
                # Verificar si es una petición AJAX (fetch)
                is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.headers.get('Content-Type', '').startswith('application/json')
                
                # Guardar todas las respuestas primero
                for question in questions:
                    answer_key = f'question_{question.id}'
                    if answer_key in request.POST:
                        answer = int(request.POST[answer_key])
                        Response.objects.update_or_create(
                            evaluation=evaluation,
                            question=question,
                            defaults={'answer': answer}
                        )
                
                # Verificar que todas las preguntas estén respondidas
                total_questions = questions.count()
                answered_question_ids = set(Response.objects.filter(evaluation=evaluation).values_list('question_id', flat=True))
                all_question_ids = set(questions.values_list('id', flat=True))
                missing_question_ids = all_question_ids - answered_question_ids
                answered_questions = len(answered_question_ids)
                
                if answered_questions < total_questions or missing_question_ids:
                    # Identificar preguntas faltantes
                    missing_questions = Question.objects.filter(id__in=missing_question_ids).order_by('number')
                    missing_numbers = [q.number for q in missing_questions]
                    missing_list = ", ".join(map(str, missing_numbers[:10])) + ("..." if len(missing_numbers) > 10 else "")
                    
                    error_message = f'Debes responder todas las preguntas antes de ver los resultados. Respondidas: {answered_questions}/{total_questions}. Preguntas faltantes: {missing_list}'
                    
                    if is_ajax:
                        return JsonResponse({
                            'success': False,
                            'error': error_message,
                            'missing_questions': missing_numbers
                        }, status=400)
                    else:
                        messages.error(request, error_message)
                        return redirect('take_evaluation', evaluation_id=evaluation.id)
                
                # Si ya está completada, recalcular resultados y marcar como DRAFT para permitir reenvío
                was_complete = evaluation.is_complete
                was_confidentiality_accepted = evaluation.confidentiality_accepted
                original_edit_count = evaluation.edit_count
                
                if was_complete:
                    # Si ya está completada, recalcular resultados y marcar como DRAFT temporalmente
                    # para que aparezca el botón de enviar en la vista de resultados
                    try:
                        calculator = RiskCalculatorService()
                        calculator.calculate_evaluation_risk(evaluation)
                        
                        # Marcar como DRAFT temporalmente para permitir reenvío desde resultados
                        evaluation.status = Evaluation.Status.DRAFT
                        evaluation.save()
                        
                        # Guardar en sesión que esta evaluación estaba originalmente completada
                        # para poder incrementar el contador cuando se envíe
                        request.session[f'eval_{evaluation.id}_was_complete'] = True
                        request.session[f'eval_{evaluation.id}_original_edit_count'] = original_edit_count
                        
                        if is_ajax:
                            return JsonResponse({
                                'success': True,
                                'redirect_url': reverse('view_evaluation_results', args=[evaluation.id])
                            })
                        return redirect('view_evaluation_results', evaluation_id=evaluation.id)
                    except ValueError as e:
                        # Error de validación con mensaje específico
                        error_message = str(e)
                        if is_ajax:
                            return JsonResponse({
                                'success': False,
                                'error': f'Error al calcular resultados: {error_message}'
                            }, status=400)
                        messages.error(request, f'Error al calcular resultados: {error_message}')
                        return redirect('take_evaluation', evaluation_id=evaluation.id)
                    except Exception as e:
                        import traceback
                        import logging
                        logger = logging.getLogger(__name__)
                        error_detail = traceback.format_exc()
                        logger.error(f'Error al recalcular resultados para evaluación {evaluation.id}: {str(e)}\n{error_detail}')
                        error_message = str(e) if str(e) else 'Error desconocido al calcular resultados'
                        if is_ajax:
                            return JsonResponse({
                                'success': False,
                                'error': f'Error al calcular resultados: {error_message}. Por favor, verifica que todas las preguntas estén respondidas correctamente.'
                            }, status=500)
                        messages.error(request, f'Error al calcular resultados: {error_message}. Por favor, verifica que todas las preguntas estén respondidas correctamente.')
                        return redirect('take_evaluation', evaluation_id=evaluation.id)
                
                # Si no está completada, calcular riesgos temporalmente para vista previa
                # Necesitamos marcar temporalmente como completada para calcular, luego revertir
                evaluation.status = Evaluation.Status.COMPLETED
                if not evaluation.confidentiality_accepted:
                    evaluation.confidentiality_accepted = True  # Temporal para calcular
                evaluation.save()
                
                try:
                    calculator = RiskCalculatorService()
                    calculator.calculate_evaluation_risk(evaluation)
                except ValueError as e:
                    # Error de validación con mensaje específico (preguntas faltantes, etc.)
                    evaluation.status = Evaluation.Status.DRAFT
                    evaluation.confidentiality_accepted = was_confidentiality_accepted
                    evaluation.save()
                    # Mostrar el mensaje específico del error
                    error_message = str(e)
                    if is_ajax:
                        return JsonResponse({
                            'success': False,
                            'error': f'Error al calcular resultados: {error_message}'
                        }, status=400)
                    messages.error(request, f'Error al calcular resultados: {error_message}')
                    return redirect('take_evaluation', evaluation_id=evaluation.id)
                except Exception as e:
                    # Otros errores
                    evaluation.status = Evaluation.Status.DRAFT
                    evaluation.confidentiality_accepted = was_confidentiality_accepted
                    evaluation.save()
                    import traceback
                    import logging
                    logger = logging.getLogger(__name__)
                    error_detail = traceback.format_exc()
                    logger.error(f'Error al calcular resultados para evaluación {evaluation.id}: {str(e)}\n{error_detail}')
                    # Mostrar el mensaje del error si es descriptivo, sino mostrar genérico
                    error_message = str(e) if str(e) else 'Error desconocido al calcular resultados'
                    if is_ajax:
                        return JsonResponse({
                            'success': False,
                            'error': f'Error al calcular resultados: {error_message}. Por favor, verifica que todas las preguntas estén respondidas correctamente.'
                        }, status=500)
                    messages.error(request, f'Error al calcular resultados: {error_message}. Por favor, verifica que todas las preguntas estén respondidas correctamente.')
                    return redirect('take_evaluation', evaluation_id=evaluation.id)
                
                # Revertir el estado para permitir edición (modo preview)
                evaluation.status = Evaluation.Status.DRAFT
                evaluation.confidentiality_accepted = was_confidentiality_accepted
                evaluation.save()
                
                # Redirigir a vista de resultados en modo preview
                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'redirect_url': reverse('view_evaluation_results', args=[evaluation.id])
                    })
                return redirect('view_evaluation_results', evaluation_id=evaluation.id)
            
            elif action == 'submit':
                # Guardar todas las respuestas primero
                for question in questions:
                    answer_key = f'question_{question.id}'
                    if answer_key in request.POST:
                        answer = int(request.POST[answer_key])
                        Response.objects.update_or_create(
                            evaluation=evaluation,
                            question=question,
                            defaults={'answer': answer}
                        )
                
                # Verificar que todas las preguntas estén respondidas
                total_questions = questions.count()
                answered_questions = Response.objects.filter(evaluation=evaluation).count()
                
                if answered_questions < total_questions:
                    # Identificar preguntas faltantes
                    answered_question_ids = set(Response.objects.filter(evaluation=evaluation).values_list('question_id', flat=True))
                    all_question_ids = set(questions.values_list('id', flat=True))
                    missing_question_ids = all_question_ids - answered_question_ids
                    missing_questions = Question.objects.filter(id__in=missing_question_ids).order_by('number')
                    missing_numbers = [q.number for q in missing_questions]
                    
                    messages.error(request, f'Debes responder todas las preguntas. Respondidas: {answered_questions}/{total_questions}. Preguntas faltantes: {", ".join(map(str, missing_numbers[:10]))}{"..." if len(missing_numbers) > 10 else ""}')
                    return redirect('take_evaluation', evaluation_id=evaluation.id)
                elif not evaluation.confidentiality_accepted:
                    messages.error(request, 'Debes aceptar la certificación de confidencialidad antes de enviar.')
                    return redirect('take_evaluation', evaluation_id=evaluation.id)
                else:
                    # Verificar si esta evaluación estaba originalmente completada (modo edición)
                    was_complete_before = request.session.get(f'eval_{evaluation.id}_was_complete', False)
                    original_edit_count = request.session.get(f'eval_{evaluation.id}_original_edit_count', 0)
                    
                    # Si estaba completada antes o está completada ahora, incrementar contador de ediciones
                    if was_complete_before or evaluation.is_complete:
                        if was_complete_before:
                            evaluation.edit_count = original_edit_count + 1
                        else:
                            evaluation.edit_count += 1
                        evaluation.last_edited_at = datetime.now()
                    
                    # Marcar como completada
                    evaluation.status = Evaluation.Status.COMPLETED
                    if not evaluation.date_completed:
                        evaluation.date_completed = datetime.now()
                    evaluation.save()
                    
                    # Limpiar variables de sesión si existen
                    if f'eval_{evaluation.id}_was_complete' in request.session:
                        del request.session[f'eval_{evaluation.id}_was_complete']
                    if f'eval_{evaluation.id}_original_edit_count' in request.session:
                        del request.session[f'eval_{evaluation.id}_original_edit_count']
                    
                    # Calcular riesgos
                    try:
                        calculator = RiskCalculatorService()
                        calculator.calculate_evaluation_risk(evaluation)
                    except ValueError as e:
                        # Error de validación con mensaje específico
                        messages.error(request, f'Error al calcular resultados: {str(e)}')
                        return redirect('take_evaluation', evaluation_id=evaluation.id)
                    except Exception as e:
                        # Otros errores
                        import traceback
                        import logging
                        logger = logging.getLogger(__name__)
                        error_detail = traceback.format_exc()
                        logger.error(f'Error al calcular resultados al enviar evaluación {evaluation.id}: {str(e)}\n{error_detail}')
                        error_message = str(e) if str(e) else 'Error desconocido al calcular resultados'
                        messages.error(request, f'Error al calcular resultados: {error_message}. Por favor, verifica que todas las preguntas estén respondidas correctamente.')
                        return redirect('take_evaluation', evaluation_id=evaluation.id)
                    
                    if evaluation.edit_count > 0:
                        remaining = evaluation.get_remaining_edits()
                        messages.success(request, f'¡Evaluación actualizada exitosamente! Te quedan {remaining} ediciones restantes.')
                    else:
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
def submit_evaluation_from_results(request, evaluation_id):
    """Enviar evaluación definitivamente desde la página de resultados"""
    try:
        employee = request.user.employee_profile
    except Employee.DoesNotExist:
        messages.error(request, 'No tienes un perfil de empleado asociado')
        return redirect('login')
    
    evaluation = get_object_or_404(
        Evaluation,
        id=evaluation_id,
        employee=employee
    )
    
    # Verificar que no esté ya completada (a menos que sea una re-edición)
    if evaluation.is_complete:
        # Verificar si hay una sesión que indique que estaba en modo preview
        was_in_preview = request.session.get(f'eval_{evaluation.id}_was_complete', False)
        if not was_in_preview:
            messages.info(request, 'Esta evaluación ya fue enviada.')
            return redirect('view_evaluation_results', evaluation_id=evaluation.id)
    
    # Verificar que todas las preguntas estén respondidas
    questions = Question.objects.all()
    total_questions = questions.count()
    answered_question_ids = set(Response.objects.filter(evaluation=evaluation).values_list('question_id', flat=True))
    all_question_ids = set(questions.values_list('id', flat=True))
    missing_question_ids = all_question_ids - answered_question_ids
    answered_questions = len(answered_question_ids)
    
    if answered_questions < total_questions or missing_question_ids:
        missing_questions = Question.objects.filter(id__in=missing_question_ids).order_by('number')
        missing_numbers = [q.number for q in missing_questions]
        missing_list = ", ".join(map(str, missing_numbers[:10])) + ("..." if len(missing_numbers) > 10 else "")
        messages.error(request, f'Debes responder todas las preguntas antes de enviar. Respondidas: {answered_questions}/{total_questions}. Preguntas faltantes: {missing_list}')
        return redirect('take_evaluation', evaluation_id=evaluation.id)
    
    # Verificar confidencialidad
    if not evaluation.confidentiality_accepted:
        messages.error(request, 'Debes aceptar la certificación de confidencialidad antes de enviar.')
        return redirect('take_evaluation', evaluation_id=evaluation.id)
    
    # Verificar si esta evaluación estaba originalmente completada (modo edición)
    was_complete_before = request.session.get(f'eval_{evaluation.id}_was_complete', False)
    original_edit_count = request.session.get(f'eval_{evaluation.id}_original_edit_count', 0)
    
    with transaction.atomic():
        # Si estaba completada antes, incrementar contador de ediciones
        if was_complete_before:
            evaluation.edit_count = original_edit_count + 1
            evaluation.last_edited_at = datetime.now()
        
        # Marcar como completada
        evaluation.status = Evaluation.Status.COMPLETED
        if not evaluation.date_completed:
            evaluation.date_completed = datetime.now()
        evaluation.save()
        
        # Limpiar variables de sesión
        if f'eval_{evaluation.id}_was_complete' in request.session:
            del request.session[f'eval_{evaluation.id}_was_complete']
        if f'eval_{evaluation.id}_original_edit_count' in request.session:
            del request.session[f'eval_{evaluation.id}_original_edit_count']
        
        # Calcular riesgos
        try:
            calculator = RiskCalculatorService()
            calculator.calculate_evaluation_risk(evaluation)
        except ValueError as e:
            messages.error(request, f'Error al calcular resultados: {str(e)}')
            return redirect('take_evaluation', evaluation_id=evaluation.id)
        except Exception as e:
            import traceback
            import logging
            logger = logging.getLogger(__name__)
            error_detail = traceback.format_exc()
            logger.error(f'Error al calcular resultados al enviar evaluación {evaluation.id}: {str(e)}\n{error_detail}')
            error_message = str(e) if str(e) else 'Error desconocido al calcular resultados'
            messages.error(request, f'Error al calcular resultados: {error_message}. Por favor, verifica que todas las preguntas estén respondidas correctamente.')
            return redirect('take_evaluation', evaluation_id=evaluation.id)
    
    messages.success(request, '¡Evaluación enviada exitosamente!')
    return redirect('view_evaluation_results', evaluation_id=evaluation.id)


@login_required
def view_evaluation_results(request, evaluation_id):
    """Ver resultados de una evaluación completada o en preview"""
    try:
        employee = request.user.employee_profile
    except Employee.DoesNotExist:
        messages.error(request, 'No tienes un perfil de empleado asociado')
        return redirect('login')
    
    # Permitir ver resultados incluso si está en DRAFT (para preview)
    evaluation = get_object_or_404(
        Evaluation,
        id=evaluation_id,
        employee=employee
    )
    
    # Si está en DRAFT y no tiene resultados calculados, redirigir al formulario
    if evaluation.status == Evaluation.Status.DRAFT:
        risk_results_count = RiskResult.objects.filter(evaluation=evaluation).count()
        if risk_results_count == 0:
            messages.info(request, 'Primero debes completar la evaluación para ver los resultados.')
            return redirect('take_evaluation', evaluation_id=evaluation.id)
    
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
    
    # Obtener recomendaciones médicas ocupacionales por dimensión
    medical_recommendations = {}
    for result in risk_results:
        medical_recommendations[result.dimension.name] = recommendations_service.get_medical_recommendations(
            result.dimension.name,
            result.risk_level
        )
    
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
        'medical_recommendations': medical_recommendations,
        'risk_counts': risk_counts,
        'high_risk_results': high_risk_results,
        'medium_risk_results': medium_risk_results,
        'completed_evaluations': completed_evaluations,
    }
    
    return render(request, 'employee/evaluation_results.html', context)


@login_required
def compare_evaluations(request):
    """Comparar evaluaciones específicas (por fecha o año)"""
    try:
        employee = request.user.employee_profile
    except Employee.DoesNotExist:
        messages.error(request, 'No tienes un perfil de empleado asociado')
        return redirect('login')
    
    # Obtener todas las evaluaciones completadas con información detallada
    completed_evaluations = Evaluation.objects.filter(
        employee=employee,
        status=Evaluation.Status.COMPLETED
    ).order_by('-date_completed', '-year')
    
    comparison_data = None
    eval1_selected = None
    eval2_selected = None
    
    if request.method == 'GET' and 'eval1' in request.GET and 'eval2' in request.GET:
        # Validar IDs de evaluaciones
        try:
            eval1_id = int(request.GET.get('eval1', 0))
            eval2_id = int(request.GET.get('eval2', 0))
            
            if eval1_id == eval2_id:
                messages.error(request, 'Debes seleccionar dos evaluaciones diferentes')
                return redirect('compare_evaluations')
            
            eval1_selected = get_object_or_404(Evaluation, id=eval1_id, employee=employee, status=Evaluation.Status.COMPLETED)
            eval2_selected = get_object_or_404(Evaluation, id=eval2_id, employee=employee, status=Evaluation.Status.COMPLETED)
            
        except (ValueError, TypeError):
            messages.error(request, 'IDs de evaluaciones inválidos')
            return redirect('compare_evaluations')
        
        try:
            calculator = RiskCalculatorService()
            comparison_data = calculator.compare_evaluations_by_id(eval1_selected.id, eval2_selected.id)
            
            # Agregar campos simplificados para el template
            if comparison_data:
                for dim in comparison_data['dimensions']:
                    dim['score1'] = dim.get('score1', 0)
                    dim['risk1'] = dim.get('risk1', '')
                    dim['score2'] = dim.get('score2', 0)
                    dim['risk2'] = dim.get('risk2', '')
        except ValueError as e:
            messages.error(request, str(e))
    
    context = {
        'employee': employee,
        'completed_evaluations': completed_evaluations,
        'comparison_data': comparison_data,
        'eval1_selected': eval1_selected,
        'eval2_selected': eval2_selected,
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
    
    # Obtener recomendaciones médicas ocupacionales por dimensión
    medical_recommendations = {}
    for result in risk_results:
        medical_recommendations[result.dimension.name] = recommendations_service.get_medical_recommendations(
            result.dimension.name,
            result.risk_level
        )
    
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
            
            # Agregar recomendaciones médico ocupacionales si existen
            med_recs = medical_recommendations.get(result.dimension.name, [])
            if med_recs:
                med_title_style = ParagraphStyle(
                    'MedTitle',
                    parent=styles['Heading3'],
                    fontSize=10,
                    textColor=colors.HexColor('#7c3aed'),
                    spaceAfter=4,
                    spaceBefore=8,
                    fontName='Helvetica-Bold'
                )
                med_title = Paragraph("Recomendaciones Médicas Ocupacionales:", med_title_style)
                elements.append(med_title)
                
                for med_rec in med_recs:
                    med_rec_para = Paragraph(f"• {med_rec}", normal_style)
                    elements.append(med_rec_para)
            
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
