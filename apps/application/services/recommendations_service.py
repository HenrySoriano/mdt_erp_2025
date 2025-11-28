"""
Servicio para generar recomendaciones personalizadas basadas en los resultados de evaluación.
Incluye personalización por género y felicitaciones para niveles bajos de riesgo.
Las recomendaciones son equilibradas, empáticas y conciliatorias, sin culpar a nadie.
"""
from typing import Dict, List, Optional
from apps.infrastructure.models import RiskResult, Evaluation


class RecommendationsService:
    """Servicio para generar recomendaciones personalizadas por dimensión, nivel de riesgo y género"""
    
    def _get_gender_suffix(self, gender: Optional[str]) -> tuple:
        """
        Retorna sufijos de género para personalizar mensajes.
        Returns: (tú, eres, tienes, estás, tu, tengas, puedes, mereces)
        """
        if gender == 'F':
            return ('tú', 'eres', 'tienes', 'estás', 'tu', 'tengas', 'puedes', 'mereces')
        else:  # M o None (default masculino)
            return ('tú', 'eres', 'tienes', 'estás', 'tu', 'tengas', 'puedes', 'mereces')
    
    def _get_congratulations(self, dimension_name: str, gender: Optional[str] = None) -> List[str]:
        """Genera felicitaciones personalizadas por género para nivel BAJO"""
        tu, eres, tienes, estas, tu_pos, tengas, puedes, mereces = self._get_gender_suffix(gender)
        
        congratulations_by_dimension = {
            'Carga y ritmo de trabajo': [
                f'¡Felicitaciones! {tu.capitalize()} {tienes} una excelente gestión de {tu_pos} carga de trabajo. Esto demuestra que {eres} capaz de mantener un equilibrio saludable entre productividad y bienestar.',
                f'Es admirable cómo {eres} capaz de organizar {tu_pos} tareas de manera eficiente. Continúa con este excelente desempeño.',
                f'{tu.capitalize()} {estas} siendo un ejemplo para {tu_pos} compañeros. Considera compartir {tu_pos} estrategias de organización con el equipo.'
            ],
            'Desarrollo de competencias': [
                f'¡Excelente! {tu.capitalize()} {tienes} acceso a buenas oportunidades de desarrollo profesional. Aprovecha al máximo las capacitaciones disponibles.',
                f'Es destacable cómo {eres} proactivo/a en {tu_pos} crecimiento profesional. Continúa buscando nuevas habilidades que te ayuden a avanzar.',
                f'{tu.capitalize()} {tienes} el potencial para ser mentor/a de otros compañeros. Compartir {tu_pos} conocimientos fortalecerá al equipo.'
            ],
            'Liderazgo': [
                f'¡Muy bien! {tu.capitalize()} {tienes} un buen liderazgo y apoyo de {tu_pos} superiores. Aprovecha esta relación positiva para {tu_pos} desarrollo.',
                f'Es positivo que {tengas} una comunicación abierta con {tu_pos} supervisor/a. Mantén esta relación constructiva.',
                f'{tu.capitalize()} {estas} aprovechando bien las oportunidades de feedback y orientación. Esto te ayudará a crecer profesionalmente.'
            ],
            'Margen de acción y control': [
                f'¡Felicitaciones! {tu.capitalize()} {tienes} buen control sobre {tu_pos} trabajo. Esta autonomía te permite ser más eficiente y creativo/a.',
                f'Es excelente que {tengas} la capacidad de tomar decisiones informadas. Continúa buscando formas de mejorar {tu_pos} procesos.',
                f'{tu.capitalize()} {estas} demostrando responsabilidad y proactividad. Comparte {tu_pos} ideas de mejora con el equipo.'
            ],
            'Organización del trabajo': [
                f'¡Excelente! {tu.capitalize()} {tienes} un trabajo bien organizado con objetivos claros. Esto te ayuda a ser más productivo/a.',
                f'Es destacable cómo {eres} capaz de trabajar en un ambiente estructurado. Continúa contribuyendo a mantener esta organización.',
                f'{tu.capitalize()} {estas} aprovechando bien la claridad de objetivos para establecer prioridades. Sigue así.'
            ],
            'Recuperación': [
                f'¡Muy bien! {tu.capitalize()} {tienes} buenas oportunidades de descanso y recuperación. Mantener este equilibrio es fundamental para {tu_pos} bienestar.',
                f'Es positivo que {tengas} tiempo para desconectarte completamente del trabajo. Esto contribuye a {tu_pos} salud física y mental.',
                f'{tu.capitalize()} {estas} priorizando correctamente {tu_pos} bienestar. Continúa cuidando {tu_pos} salud.'
            ],
            'Soporte y apoyo': [
                f'¡Excelente! {tu.capitalize()} {tienes} buen apoyo social y técnico en {tu_pos} trabajo. Aprovecha estos recursos cuando los necesites.',
                f'Es positivo que {tengas} relaciones constructivas con {tu_pos} compañeros y superiores. Mantén esta red de apoyo.',
                f'{tu.capitalize()} {estas} siendo un apoyo para otros cuando lo necesitan. Esto fortalece el trabajo en equipo.'
            ],
            'Otros puntos importantes': [
                f'¡Felicitaciones! En general, {tu.capitalize()} {estas} manejando bien los aspectos adicionales de {tu_pos} trabajo. Mantén este equilibrio.',
                f'Es destacable cómo {eres} consciente de {tu_pos} bienestar. Continúa siendo proactivo/a en buscar ayuda cuando la necesites.',
                f'{tu.capitalize()} {estas} aprovechando bien los recursos disponibles. Esto te ayuda a mantener {tu_pos} salud y bienestar.'
            ],
            'Ambiente físico': [
                f'¡Muy bien! {tu.capitalize()} {tienes} un ambiente físico de trabajo adecuado. Mantén las condiciones que favorecen {tu_pos} bienestar.',
                f'Es positivo que {tengas} un espacio de trabajo cómodo y seguro. Continúa cuidando {tu_pos} entorno laboral.',
                f'{tu.capitalize()} {estas} trabajando en condiciones favorables. Esto contribuye a {tu_pos} productividad y salud.'
            ],
            'Reconocimiento y compensación': [
                f'¡Excelente! {tu.capitalize()} {tienes} un buen nivel de reconocimiento y valoración. Esto es importante para {tu_pos} motivación.',
                f'Es destacable cómo {eres} capaz de comunicar {tu_pos} valor y contribuciones. Continúa aprovechando las oportunidades de reconocimiento.',
                f'{tu.capitalize()} {estas} siendo reconocido/a por {tu_pos} trabajo. Esto fortalece {tu_pos} satisfacción laboral.'
            ],
            'Claridad de rol': [
                f'¡Felicitaciones! {tu.capitalize()} {tienes} claridad sobre {tu_pos} responsabilidades y rol. Esto te ayuda a ser más efectivo/a.',
                f'Es excelente que {tengas} objetivos y prioridades claras. Aprovecha esta claridad para mejorar {tu_pos} desempeño.',
                f'{tu.capitalize()} {estas} trabajando con un rol bien definido. Continúa comunicando cualquier cambio en {tu_pos} responsabilidades.'
            ],
            'Doble presencia (laboral-familiar)': [
                f'¡Excelente! {tu.capitalize()} {tienes} un buen equilibrio entre trabajo y vida familiar. Mantener este balance es fundamental.',
                f'Es destacable cómo {eres} capaz de establecer límites claros entre {tu_pos} vida laboral y personal. Sigue priorizando {tu_pos} familia.',
                f'{tu.capitalize()} {estas} manejando bien {tu_pos} responsabilidades laborales y familiares. Esto contribuye a {tu_pos} bienestar integral.'
            ],
            'Estabilidad laboral percibida': [
                f'¡Muy bien! {tu.capitalize()} {tienes} una percepción positiva de estabilidad laboral. Esto contribuye a {tu_pos} bienestar y productividad.',
                f'Es positivo que {tengas} seguridad en {tu_pos} empleo. Aprovecha esta estabilidad para planificar {tu_pos} futuro profesional.',
                f'{tu.capitalize()} {estas} desarrollando {tu_pos} habilidades para mantener {tu_pos} valor en la organización. Continúa así.'
            ],
            'Salud auto percibida': [
                f'¡Felicitaciones! {tu.capitalize()} {tienes} una percepción positiva de {tu_pos} salud. Continúa cuidando {tu_pos} bienestar físico y mental.',
                f'Es excelente que {tengas} hábitos saludables. Mantén el ejercicio, alimentación balanceada y descanso adecuado.',
                f'{tu.capitalize()} {estas} priorizando correctamente {tu_pos} salud. Realiza chequeos médicos regulares para mantener este bienestar.'
            ]
        }
        
        return congratulations_by_dimension.get(dimension_name, [
            f'¡Felicitaciones! {tu.capitalize()} {tienes} excelentes resultados en {dimension_name}. Continúa manteniendo este nivel.',
            f'Es destacable cómo {eres} capaz de mantener este equilibrio. Aprovecha las fortalezas identificadas en esta área.'
        ])
    
    def _get_recommendations_medium(self, dimension_name: str, gender: Optional[str] = None) -> List[str]:
        """Genera recomendaciones equilibradas y conciliatorias para nivel MEDIO"""
        tu, eres, tienes, estas, tu_pos, tengas, puedes, mereces = self._get_gender_suffix(gender)
        
        recommendations_by_dimension = {
            'Carga y ritmo de trabajo': [
                f'En esta dimensión hay oportunidades de mejora. Considera priorizar las tareas más importantes para optimizar {tu_pos} tiempo.',
                f'Podría ser útil establecer una comunicación abierta con {tu_pos} supervisor/a sobre {tu_pos} capacidad de trabajo diaria.',
                f'Explora técnicas de gestión del tiempo que se adapten a {tu_pos} estilo de trabajo para mejorar la eficiencia.',
                f'Recuerda que es válido solicitar apoyo cuando lo necesites. El trabajo en equipo beneficia a todos.'
            ],
            'Desarrollo de competencias': [
                f'Hay oportunidades para fortalecer {tu_pos} desarrollo profesional. Identifica áreas donde te gustaría crecer.',
                f'Considera solicitar feedback constructivo a {tu_pos} supervisor/a sobre {tu_pos} desempeño y áreas de crecimiento.',
                f'Investiga capacitaciones o cursos que puedan complementar {tu_pos} habilidades actuales.',
                f'Participa activamente en las oportunidades de desarrollo que ofrece la organización.'
            ],
            'Liderazgo': [
                f'Esta dimensión puede fortalecerse con mejor comunicación. Busca momentos para compartir {tu_pos} necesidades de manera constructiva.',
                f'Considera solicitar reuniones periódicas con {tu_pos} supervisor/a para alinear expectativas y recibir orientación.',
                f'Cuando identifiques oportunidades de mejora, propón soluciones colaborativas que beneficien al equipo.',
                f'Busca desarrollar habilidades de comunicación que te ayuden a expresar {tu_pos} ideas de manera efectiva.'
            ],
            'Margen de acción y control': [
                f'Hay espacio para aumentar {tu_pos} autonomía. Identifica áreas donde {puedes} tomar más decisiones.',
                f'Propón mejoras en procesos que conozcas bien, compartiendo {tu_pos} experiencia con el equipo.',
                f'Solicita información adicional sobre objetivos y expectativas para tomar decisiones más informadas.',
                f'Comunica de manera constructiva cómo mayor autonomía podría mejorar {tu_pos} efectividad.'
            ],
            'Organización del trabajo': [
                f'Esta dimensión puede mejorarse con mejor comunicación. Busca clarificar objetivos y procesos con {tu_pos} equipo.',
                f'Considera solicitar reuniones para alinear expectativas y objetivos con {tu_pos} supervisor/a.',
                f'Propón mejoras en la comunicación del equipo de manera colaborativa.',
                f'Documenta procesos exitosos para ayudar a mejorar la organización general del área.'
            ],
            'Recuperación': [
                f'Es importante cuidar {tu_pos} equilibrio trabajo-vida personal. Busca espacios para descansar y desconectarte.',
                f'Establece límites saludables entre {tu_pos} tiempo de trabajo y personal. El descanso mejora la productividad.',
                f'Practica técnicas de relajación y desconexión después del trabajo para mejorar {tu_pos} bienestar.',
                f'Asegúrate de tomar {tu_pos} descansos completos durante la jornada laboral para mantener {tu_pos} energía.'
            ],
            'Soporte y apoyo': [
                f'El apoyo mutuo fortalece el equipo. Busca fortalecer {tu_pos} relaciones con compañeros y superiores.',
                f'No dudes en solicitar ayuda cuando la necesites. El trabajo colaborativo beneficia a todos.',
                f'Participa activamente en actividades de equipo para construir una red de apoyo mutuo.',
                f'Comunica {tu_pos} necesidades de apoyo de manera clara y constructiva.'
            ],
            'Otros puntos importantes': [
                f'Hay algunos aspectos que pueden mejorarse. Identifica áreas específicas donde {puedes} trabajar en conjunto con el equipo.',
                f'Si sientes que algunos aspectos afectan {tu_pos} bienestar, busca apoyo profesional o conversa con recursos humanos.',
                f'Establece metas concretas y alcanzables para mejorar las áreas que identificaste.',
                f'Comunica {tu_pos} preocupaciones de manera constructiva, enfocándote en soluciones colaborativas.'
            ],
            'Ambiente físico': [
                f'El ambiente físico puede mejorarse. Identifica aspectos específicos que afectan {tu_pos} comodidad y bienestar.',
                f'Considera comunicar de manera constructiva las mejoras que podrían beneficiar a todo el equipo.',
                f'Documenta situaciones específicas del ambiente físico que podrían mejorarse.',
                f'Propón soluciones prácticas que beneficien tanto a {tu_pos} como al equipo en general.'
            ],
            'Reconocimiento y compensación': [
                f'El reconocimiento es importante para la motivación. Busca oportunidades para compartir {tu_pos} logros de manera constructiva.',
                f'Comunica {tu_pos} contribuciones y logros a {tu_pos} supervisor/a de manera regular y profesional.',
                f'Solicita feedback sobre {tu_pos} desempeño para entender cómo {puedes} seguir creciendo.',
                f'Considera proponer un sistema de reconocimiento que beneficie a todo el equipo.'
            ],
            'Claridad de rol': [
                f'{tu_pos.capitalize()} rol puede clarificarse mejor. Busca momentos para alinear expectativas con {tu_pos} supervisor/a.',
                f'Si no {tienes} una descripción de puesto actualizada, solicítala de manera constructiva.',
                f'Pide reuniones periódicas para alinear expectativas sobre {tu_pos} responsabilidades.',
                f'Documenta situaciones donde mayor claridad podría mejorar {tu_pos} efectividad.'
            ],
            'Doble presencia (laboral-familiar)': [
                f'El equilibrio trabajo-familia es importante. Busca más tiempo para {tu_pos} vida personal y familiar.',
                f'Establece límites saludables: evita trabajar en casa constantemente. {tu_pos.capitalize()} familia merece {tu_pos} atención.',
                f'Comunica a {tu_pos} familia y trabajo sobre la importancia de mantener este equilibrio para todos.',
                f'Practica desconexión completa del trabajo en {tu_pos} tiempo personal para recargar energías.'
            ],
            'Estabilidad laboral percibida': [
                f'{tu_pos.capitalize()} percepción de estabilidad puede mejorarse. Busca clarificar {tu_pos} situación laboral con {tu_pos} supervisor/a.',
                f'Solicita información sobre {tu_pos} futuro en la organización de manera constructiva.',
                f'Desarrolla habilidades adicionales que aumenten {tu_pos} valor para la organización.',
                f'Mantén un perfil profesional actualizado que refleje {tu_pos} crecimiento y contribuciones.'
            ],
            'Salud auto percibida': [
                f'Es importante priorizar {tu_pos} bienestar físico y mental. Considera realizar un chequeo médico regular.',
                f'Establece hábitos saludables: ejercicio regular, alimentación balanceada y descanso adecuado.',
                f'Si sientes que {tu_pos} salud se está afectando, busca apoyo profesional o conversa con recursos humanos.',
                f'Recuerda que cuidar {tu_pos} salud es fundamental para {tu_pos} bienestar y productividad a largo plazo.'
            ]
        }
        
        return recommendations_by_dimension.get(dimension_name, [
            f'Esta dimensión tiene oportunidades de mejora. Identifica áreas específicas donde {puedes} trabajar en conjunto con el equipo.',
            f'Busca apoyo y recursos disponibles para fortalecer esta área de manera colaborativa.',
            f'Establece metas concretas y alcanzables para mejorar esta dimensión.'
        ])
    
    def _get_recommendations_high(self, dimension_name: str, gender: Optional[str] = None) -> List[str]:
        """Genera recomendaciones equilibradas y conciliatorias para nivel ALTO - enfocadas en soluciones colaborativas"""
        tu, eres, tienes, estas, tu_pos, tengas, puedes, mereces = self._get_gender_suffix(gender)
        
        recommendations_by_dimension = {
            'Carga y ritmo de trabajo': [
                f'Esta dimensión requiere atención. Considera establecer una comunicación abierta con {tu_pos} supervisor/a sobre la distribución de tareas.',
                f'Es importante encontrar un equilibrio saludable. Prioriza {tu_pos} bienestar y comunica {tu_pos} necesidades de manera constructiva.',
                f'Explora junto con {tu_pos} equipo formas de optimizar procesos y redistribuir responsabilidades de manera equitativa.',
                f'Practica técnicas de gestión del estrés y considera solicitar apoyo cuando lo necesites. El trabajo en equipo es clave.',
                f'Documenta {tu_pos} carga de trabajo de manera objetiva para tener una base de conversación constructiva con {tu_pos} supervisor/a.'
            ],
            'Desarrollo de competencias': [
                f'Hay oportunidades para fortalecer {tu_pos} desarrollo profesional. Considera solicitar un plan de desarrollo conjunto con {tu_pos} supervisor/a.',
                f'Explora capacitaciones tanto internas como externas que puedan complementar {tu_pos} habilidades actuales.',
                f'Propón proyectos que te permitan aprender nuevas competencias y demostrar {tu_pos} potencial de crecimiento.',
                f'Establece metas de aprendizaje a corto y mediano plazo que puedas compartir con {tu_pos} supervisor/a.',
                f'Busca oportunidades de mentoría o aprendizaje colaborativo dentro de la organización.'
            ],
            'Liderazgo': [
                f'Esta dimensión puede mejorarse con mejor comunicación. Busca momentos para compartir {tu_pos} necesidades de manera constructiva.',
                f'Considera solicitar reuniones periódicas con {tu_pos} supervisor/a para alinear expectativas y recibir orientación.',
                f'Si sientes que necesitas más apoyo, busca recursos humanos como mediador para facilitar la comunicación.',
                f'Explora oportunidades de desarrollo de liderazgo que puedan beneficiar tanto a {tu_pos} como al equipo.',
                f'Establece límites saludables y comunica expectativas de manera respetuosa y constructiva.'
            ],
            'Margen de acción y control': [
                f'Hay oportunidades para aumentar {tu_pos} autonomía. Solicita información adicional sobre objetivos y propósito de {tu_pos} tareas.',
                f'Propón formas específicas en las que mayor autonomía podría mejorar {tu_pos} efectividad sin comprometer resultados.',
                f'Busca espacios para tomar decisiones sobre aspectos que conoces bien, demostrando {tu_pos} capacidad de responsabilidad.',
                f'Comunica de manera constructiva cómo mayor control podría mejorar {tu_pos} motivación y productividad.',
                f'Trabaja junto con {tu_pos} supervisor/a para identificar áreas donde {puedes} tener más autonomía gradualmente.'
            ],
            'Organización del trabajo': [
                f'Esta dimensión puede mejorarse con mejor comunicación y organización. Busca clarificar objetivos, roles y responsabilidades con el equipo.',
                f'Propón un plan de organización colaborativo con objetivos claros y plazos definidos que beneficie a todos.',
                f'Documenta procesos y mejoras que podrían ayudar a toda el área de manera constructiva.',
                f'Solicita reuniones para alinear expectativas y objetivos de manera que todos estén en la misma página.',
                f'Busca apoyo en recursos humanos si necesitas ayuda para facilitar mejoras organizacionales.'
            ],
            'Recuperación': [
                f'Es importante priorizar {tu_pos} descanso y recuperación. Establece límites saludables entre trabajo y vida personal.',
                f'Evita trabajar horas extras constantemente. El descanso adecuado mejora la productividad y el bienestar a largo plazo.',
                f'Considera conversar con {tu_pos} supervisor/a sobre la importancia del equilibrio trabajo-vida para mantener la productividad.',
                f'Practica técnicas de desconexión completa del trabajo en {tu_pos} tiempo libre para recargar energías.',
                f'Recuerda que cuidar {tu_pos} bienestar es fundamental para {tu_pos} efectividad y satisfacción laboral.'
            ],
            'Soporte y apoyo': [
                f'El apoyo mutuo es fundamental. Busca construir relaciones positivas con compañeros y superiores.',
                f'No tengas miedo de solicitar ayuda cuando la necesites. El trabajo colaborativo beneficia a todos.',
                f'Participa activamente en actividades de equipo para fortalecer {tu_pos} red de apoyo.',
                f'Si necesitas más apoyo, considera buscar recursos humanos como facilitador para mejorar la comunicación.',
                f'Comunica {tu_pos} necesidades de apoyo de manera constructiva, enfocándote en cómo puede beneficiar al equipo.'
            ],
            'Otros puntos importantes': [
                f'Hay varios aspectos que requieren atención. Identifica áreas específicas donde {puedes} trabajar en conjunto con el equipo.',
                f'Busca apoyo profesional si sientes que algunos aspectos afectan {tu_pos} bienestar. Recursos humanos puede guiarte.',
                f'Documenta situaciones específicas de manera objetiva para tener una base de conversación constructiva.',
                f'Considera conversar con recursos humanos sobre {tu_pos} preocupaciones de manera que puedan facilitar soluciones.',
                f'Enfócate en soluciones colaborativas que beneficien tanto a {tu_pos} como a la organización.'
            ],
            'Ambiente físico': [
                f'El ambiente físico puede mejorarse. Documenta aspectos específicos que afectan {tu_pos} comodidad y bienestar.',
                f'Solicita mejoras en las condiciones físicas de manera constructiva, enfocándote en beneficios para todo el equipo.',
                f'Si hay riesgos de seguridad, repórtalos inmediatamente para proteger a todos.',
                f'Propón soluciones prácticas que mejoren las condiciones para {tu_pos} y {tu_pos} compañeros.',
                f'Busca apoyo en recursos humanos o seguridad laboral si necesitas ayuda para facilitar mejoras.'
            ],
            'Reconocimiento y compensación': [
                f'El reconocimiento es importante para la motivación. Documenta {tu_pos} logros y contribuciones de manera profesional.',
                f'Solicita reuniones de feedback para entender cómo {puedes} seguir creciendo y ser reconocido/a.',
                f'Comunica {tu_pos} valor y contribuciones de manera constructiva y profesional.',
                f'Considera proponer un sistema de reconocimiento que beneficie a todo el equipo.',
                f'Busca oportunidades donde {tu_pos} trabajo pueda ser más visible y valorado de manera justa.'
            ],
            'Claridad de rol': [
                f'{tu_pos.capitalize()} rol necesita mayor claridad. Solicita una descripción clara de {tu_pos} puesto y responsabilidades.',
                f'Pide reuniones regulares para clarificar expectativas y objetivos de manera que todos estén alineados.',
                f'Documenta situaciones donde la falta de claridad afecta {tu_pos} trabajo de manera objetiva.',
                f'Trabaja junto con {tu_pos} supervisor/a para definir objetivos y responsabilidades claras.',
                f'Busca apoyo en recursos humanos si necesitas ayuda para facilitar la clarificación de roles.'
            ],
            'Doble presencia (laboral-familiar)': [
                f'Es importante establecer límites saludables entre trabajo y vida personal. Prioriza {tu_pos} equilibrio para {tu_pos} bienestar.',
                f'Evita llevar trabajo a casa constantemente. El descanso adecuado mejora {tu_pos} productividad y satisfacción.',
                f'Considera conversar con {tu_pos} supervisor/a sobre la importancia de mantener este equilibrio para todos.',
                f'Practica desconexión completa del trabajo en {tu_pos} tiempo personal para recargar energías.',
                f'Recuerda que cuidar {tu_pos} vida personal y familiar es fundamental para {tu_pos} bienestar integral.'
            ],
            'Estabilidad laboral percibida': [
                f'Si sientes inseguridad sobre {tu_pos} empleo, considera solicitar una reunión con {tu_pos} supervisor/a para clarificar {tu_pos} situación.',
                f'Documenta {tu_pos} desempeño y contribuciones de manera profesional para tener evidencia de {tu_pos} valor.',
                f'Desarrolla habilidades adicionales que aumenten {tu_pos} valor para la organización.',
                f'Busca apoyo profesional si la ansiedad afecta {tu_pos} bienestar. Recursos humanos puede guiarte.',
                f'Mantén un perfil profesional actualizado que refleje {tu_pos} crecimiento y compromiso con la organización.'
            ],
            'Salud auto percibida': [
                f'Es importante priorizar {tu_pos} salud. Considera realizar un chequeo médico para evaluar {tu_pos} estado de salud.',
                f'Si {tu_pos} salud se está afectando, conversa con recursos humanos sobre posibles ajustes en {tu_pos} trabajo.',
                f'Establece hábitos saludables: ejercicio regular, alimentación balanceada y descanso adecuado.',
                f'Busca apoyo psicológico si sientes que {tu_pos} salud mental se está afectando. Es válido pedir ayuda.',
                f'Recuerda que cuidar {tu_pos} salud es fundamental. El trabajo no debe comprometer {tu_pos} bienestar.'
            ]
        }
        
        return recommendations_by_dimension.get(dimension_name, [
            f'Esta dimensión requiere atención. Identifica áreas específicas donde {puedes} trabajar en conjunto con el equipo.',
            f'Busca apoyo y recursos disponibles para abordar esta situación de manera constructiva.',
            f'Documenta situaciones específicas de manera objetiva para tener una base de conversación colaborativa.',
            f'Enfócate en soluciones que beneficien tanto a {tu_pos} como a la organización.'
        ])
    
    def get_recommendations(self, risk_result: RiskResult, gender: Optional[str] = None) -> List[str]:
        """
        Obtiene recomendaciones personalizadas para una dimensión específica.
        
        Args:
            risk_result: El resultado de riesgo de una dimensión
            gender: Género del empleado ('M' o 'F') para personalizar mensajes
            
        Returns:
            Lista de recomendaciones personalizadas, equilibradas y conciliatorias
        """
        dimension_name = risk_result.dimension.name
        risk_level = risk_result.risk_level
        
        if risk_level == 'BAJO':
            return self._get_congratulations(dimension_name, gender)
        elif risk_level == 'MEDIO':
            return self._get_recommendations_medium(dimension_name, gender)
        else:  # ALTO
            return self._get_recommendations_high(dimension_name, gender)
    
    def get_all_recommendations(self, risk_results, evaluation: Optional[Evaluation] = None) -> Dict[str, List[str]]:
        """
        Obtiene recomendaciones para todas las dimensiones, personalizadas por género.
        
        Args:
            risk_results: QuerySet de RiskResult
            evaluation: Objeto Evaluation para obtener el género del empleado
            
        Returns:
            Dict con dimension_name como clave y lista de recomendaciones como valor
        """
        # Obtener género de la evaluación si está disponible
        gender = None
        if evaluation:
            gender = evaluation.gender
            # Si no hay género en la evaluación, intentar obtenerlo del empleado
            if not gender and hasattr(evaluation, 'employee'):
                if hasattr(evaluation.employee, 'gender'):
                    gender = evaluation.employee.gender
        
        all_recommendations = {}
        for result in risk_results:
            all_recommendations[result.dimension.name] = self.get_recommendations(result, gender)
        return all_recommendations
