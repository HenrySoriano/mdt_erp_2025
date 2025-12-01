"""
Servicio para calcular el riesgo psicosocial basado en las respuestas de la evaluación.
Implementa la lógica de negocio para el cálculo de puntajes y niveles de riesgo.
"""
from typing import Dict, List, Tuple
from apps.infrastructure.models import Evaluation, Dimension, Response, RiskResult, Question


class RiskCalculatorService:
    """
    Servicio para calcular los niveles de riesgo por dimensión.
    Aplica el principio Single Responsibility: solo se encarga del cálculo de riesgos.
    """
    
    def calculate_evaluation_risk(self, evaluation: Evaluation) -> Dict[str, any]:
        """
        Calcula el riesgo para todas las dimensiones de una evaluación.
        
        Args:
            evaluation: La evaluación a calcular
            
        Returns:
            Dict con los resultados por dimensión
        """
        if not evaluation.is_complete:
            raise ValueError("La evaluación debe estar completada para calcular el riesgo")
        
        results = {}
        dimensions = Dimension.objects.all()
        
        for dimension in dimensions:
            score, risk_level = self._calculate_dimension_risk(evaluation, dimension)
            
            # Guardar o actualizar el resultado
            risk_result, created = RiskResult.objects.update_or_create(
                evaluation=evaluation,
                dimension=dimension,
                defaults={
                    'score': score,
                    'risk_level': risk_level
                }
            )
            
            results[dimension.name] = {
                'score': score,
                'risk_level': risk_level,
                'dimension_id': dimension.id
            }
        
        return results
    
    def _calculate_dimension_risk(self, evaluation: Evaluation, dimension: Dimension) -> Tuple[int, str]:
        """
        Calcula el puntaje y nivel de riesgo para una dimensión específica.
        
        Args:
            evaluation: La evaluación
            dimension: La dimensión a calcular
            
        Returns:
            Tuple (score, risk_level)
        """
        # Obtener las preguntas de esta dimensión
        questions = dimension.questions.all()
        question_ids = list(questions.values_list('id', flat=True))
        
        if not question_ids:
            # Si la dimensión no tiene preguntas, retornar valores por defecto
            return 0, 'BAJO'
        
        # Obtener las respuestas para estas preguntas
        responses = Response.objects.filter(
            evaluation=evaluation,
            question_id__in=question_ids
        )
        
        # Verificar que todas las preguntas de la dimensión tengan respuesta
        answered_question_ids = set(responses.values_list('question_id', flat=True))
        missing_question_ids = set(question_ids) - answered_question_ids
        
        if missing_question_ids:
            missing_count = len(missing_question_ids)
            total_count = len(question_ids)
            raise ValueError(
                f"Faltan {missing_count} de {total_count} respuestas para la dimensión '{dimension.name}'. "
                f"Preguntas faltantes: {sorted(missing_question_ids)}"
            )
        
        # Calcular el puntaje total
        score = sum(response.answer for response in responses)
        
        # Verificar que el score esté en un rango válido
        if score == 0:
            raise ValueError(
                f"El puntaje calculado para la dimensión '{dimension.name}' es 0. "
                f"Esto indica que faltan respuestas o las respuestas no están guardadas correctamente."
            )
        
        # Determinar el nivel de riesgo
        risk_level = dimension.calculate_risk_level(score)
        
        # Verificar que se obtuvo un nivel de riesgo válido
        if risk_level == 'INDEFINIDO':
            raise ValueError(
                f"No se pudo determinar el nivel de riesgo para la dimensión '{dimension.name}' con puntaje {score}. "
                f"Rangos válidos: Bajo ({dimension.low_risk_min}-{dimension.low_risk_max}), "
                f"Medio ({dimension.medium_risk_min}-{dimension.medium_risk_max}), "
                f"Alto ({dimension.high_risk_min}-{dimension.high_risk_max})"
            )
        
        return score, risk_level
    
    def get_evaluation_summary(self, evaluation: Evaluation) -> Dict[str, any]:
        """
        Obtiene un resumen completo de la evaluación con todos los resultados.
        
        Args:
            evaluation: La evaluación
            
        Returns:
            Dict con el resumen completo, incluido el puntaje global y riesgo global correcto
        """
        risk_results = RiskResult.objects.filter(evaluation=evaluation).select_related('dimension')
        
        # Calcular puntaje global total (suma de los valores obtenidos en cada dimensión)
        global_score = self.calculate_global_score(evaluation)
        global_risk_level = self.calculate_global_risk_level(global_score)
        
        summary = {
            'employee': evaluation.employee.full_name,
            'year': evaluation.year,
            'completion_date': evaluation.date_completed,
            'dimensions': [],
            'overall_risk': global_risk_level,  # Ahora usa el cálculo global correcto
            'global_score': global_score,  # Puntaje total (58-232)
            'global_risk_level': global_risk_level  # Nivel basado en rangos MDT
        }
        
        for result in risk_results:
            summary['dimensions'].append({
                'name': result.dimension.name,
                'score': result.score,
                'risk_level': result.risk_level,
                'max_score': result.dimension.low_risk_max
            })
        
        return summary
    
    def calculate_global_score(self, evaluation: Evaluation) -> int:
        """
        Calcula el puntaje total global sumando los valores obtenidos en cada dimensión.
        Según el procedimiento MDT: el resultado global por empleado es la suma del valor 
        obtenido en cada dimensión.
        
        Args:
            evaluation: La evaluación
            
        Returns:
            Puntaje total (rango: 58-232)
        """
        # Obtener los resultados de riesgo por dimensión
        risk_results = RiskResult.objects.filter(evaluation=evaluation)
        
        # Sumar los puntajes de todas las dimensiones
        total_score = sum(result.score for result in risk_results)
        
        return total_score
    
    def calculate_global_risk_level(self, total_score: int) -> str:
        """
        Calcula el nivel de riesgo global basado en el puntaje total de las 58 preguntas.
        
        Rangos según MDT:
        - Riesgo Bajo: 175-232 puntos
        - Riesgo Medio: 117-174 puntos
        - Riesgo Alto: 58-116 puntos
        
        Args:
            total_score: Puntaje total
            
        Returns:
            Nivel de riesgo global ('BAJO', 'MEDIO', 'ALTO')
        """
        if 175 <= total_score <= 232:
            return 'BAJO'
        elif 117 <= total_score <= 174:
            return 'MEDIO'
        elif 58 <= total_score <= 116:
            return 'ALTO'
        else:
            return 'INDEFINIDO'
    
    def _calculate_overall_risk(self, risk_results) -> str:
        """
        DEPRECATED: Este método calcula basado en dimensiones, no en puntaje total.
        Usar calculate_global_risk_level() para el cálculo correcto según MDT.
        
        Calcula el nivel de riesgo general basado en todos los resultados.
        
        Args:
            risk_results: QuerySet de RiskResult
            
        Returns:
            Nivel de riesgo general ('BAJO', 'MEDIO', 'ALTO')
        """
        if not risk_results.exists():
            return 'INDEFINIDO'
        
        risk_counts = {
            'ALTO': 0,
            'MEDIO': 0,
            'BAJO': 0
        }
        
        for result in risk_results:
            risk_counts[result.risk_level] += 1
        
        total = sum(risk_counts.values())
        
        # Si más del 50% son de riesgo alto, el riesgo general es alto
        if risk_counts['ALTO'] / total > 0.5:
            return 'ALTO'
        # Si más del 50% son de riesgo medio o alto, el riesgo general es medio
        elif (risk_counts['ALTO'] + risk_counts['MEDIO']) / total > 0.5:
            return 'MEDIO'
        else:
            return 'BAJO'
    
    def compare_evaluations(self, employee_id: int, year1: int, year2: int) -> Dict[str, any]:
        """
        Compara dos evaluaciones del mismo empleado en diferentes años.
        
        Args:
            employee_id: ID del empleado
            year1: Primer año
            year2: Segundo año
            
        Returns:
            Dict con la comparativa
        """
        from apps.infrastructure.models import Employee
        
        employee = Employee.objects.get(id=employee_id)
        
        eval1 = Evaluation.objects.filter(
            employee=employee,
            year=year1,
            status=Evaluation.Status.COMPLETED
        ).first()
        
        eval2 = Evaluation.objects.filter(
            employee=employee,
            year=year2,
            status=Evaluation.Status.COMPLETED
        ).first()
        
        if not eval1 or not eval2:
            raise ValueError("No se encontraron evaluaciones completadas para ambos años")
        
        results1 = {r.dimension.name: r for r in eval1.risk_results.all()}
        results2 = {r.dimension.name: r for r in eval2.risk_results.all()}
        
        comparison = {
            'employee': employee.full_name,
            'year1': year1,
            'year2': year2,
            'dimensions': []
        }
        
        for dim_name in results1.keys():
            if dim_name in results2:
                r1 = results1[dim_name]
                r2 = results2[dim_name]
                
                comparison['dimensions'].append({
                    'name': dim_name,
                    f'score_{year1}': r1.score,
                    f'risk_{year1}': r1.risk_level,
                    f'score_{year2}': r2.score,
                    f'risk_{year2}': r2.risk_level,
                    'score_change': r2.score - r1.score,
                    'improved': r2.score > r1.score  # Mayor puntaje = mejor
                })
        
        return comparison
    
    def compare_evaluations_by_id(self, eval1_id: int, eval2_id: int) -> Dict[str, any]:
        """
        Compara dos evaluaciones específicas por sus IDs.
        
        Args:
            eval1_id: ID de la primera evaluación
            eval2_id: ID de la segunda evaluación
            
        Returns:
            Dict con la comparativa
        """
        eval1 = Evaluation.objects.get(id=eval1_id)
        eval2 = Evaluation.objects.get(id=eval2_id)
        
        if eval1.employee != eval2.employee:
            raise ValueError("Las evaluaciones deben ser del mismo empleado")
        
        if eval1.status != Evaluation.Status.COMPLETED or eval2.status != Evaluation.Status.COMPLETED:
            raise ValueError("Ambas evaluaciones deben estar completadas")
        
        results1 = {r.dimension.name: r for r in eval1.risk_results.all()}
        results2 = {r.dimension.name: r for r in eval2.risk_results.all()}
        
        # Formatear fecha para mostrar
        date1_str = eval1.date_completed.strftime('%d/%m/%Y') if eval1.date_completed else f'Año {eval1.year}'
        date2_str = eval2.date_completed.strftime('%d/%m/%Y') if eval2.date_completed else f'Año {eval2.year}'
        
        comparison = {
            'employee': eval1.employee.full_name,
            'eval1_id': eval1_id,
            'eval2_id': eval2_id,
            'eval1_label': f'{date1_str} (Año {eval1.year})',
            'eval2_label': f'{date2_str} (Año {eval2.year})',
            'dimensions': []
        }
        
        for dim_name in results1.keys():
            if dim_name in results2:
                r1 = results1[dim_name]
                r2 = results2[dim_name]
                
                comparison['dimensions'].append({
                    'name': dim_name,
                    'score1': r1.score,
                    'risk1': r1.risk_level,
                    'score2': r2.score,
                    'risk2': r2.risk_level,
                    'score_change': r2.score - r1.score,
                    'improved': r2.score > r1.score  # Mayor puntaje = mejor
                })
        
        return comparison
