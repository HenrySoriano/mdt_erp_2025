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
    
    def get_medical_recommendations(self, dimension_name: str, risk_level: str) -> List[str]:
        """
        Retorna recomendaciones médicas ocupacionales empáticas y específicas por dimensión y nivel de riesgo.
        Para nivel BAJO retorna mensaje de seguimiento positivo.
        """
        if risk_level == 'BAJO':
            return [
                '¡Excelente! Tu bienestar en esta área está en buen estado. Continúa manteniendo estos hábitos saludables y no olvides que el autocuidado es fundamental para tu salud a largo plazo.'
            ]
        
        # Recomendaciones médicas empáticas y específicas para nivel MEDIO y ALTO
        medical_recommendations = {
            'Carga y ritmo de trabajo': {
                'MEDIO': [
                    'Entendemos que la carga laboral puede estar generando tensión. Te recomendamos una evaluación médica ocupacional para identificar cómo el ritmo de trabajo está afectando tu bienestar físico y mental.',
                    'Es importante que implementes pausas activas cada 2 horas durante tu jornada. Estas pausas ayudan a prevenir fatiga muscular, dolores de espalda y tensión visual.',
                    'Si experimentas dolores de cabeza frecuentes, tensión en cuello u hombros, o dificultad para concentrarte, estos pueden ser signos de sobrecarga. Comparte estos síntomas con medicina ocupacional.',
                    'Considera llevar un registro diario de cómo te sientes al finalizar la jornada. Esto ayudará a identificar patrones y será útil para tu evaluación médica.'
                ],
                'ALTO': [
                    'La sobrecarga laboral puede tener un impacto significativo en tu salud. Es importante que solicites una evaluación médica ocupacional lo antes posible para prevenir consecuencias a largo plazo.',
                    'Si experimentas síntomas como insomnio, ansiedad, dolores musculares persistentes, o agotamiento extremo, estos son señales de alerta que requieren atención médica inmediata.',
                    'El estrés crónico por sobrecarga puede afectar tu sistema inmunológico y cardiovascular. Una evaluación psicológica ocupacional te ayudará a identificar estrategias de afrontamiento saludables.',
                    'No ignores síntomas como palpitaciones, presión en el pecho, o dificultad para desconectarte del trabajo. Estos pueden indicar que necesitas apoyo médico y ajustes en tu rutina laboral.',
                    'Recuerda que tu salud es lo más importante. Si sientes que la carga laboral está afectando tu vida personal o tu salud, busca apoyo profesional de inmediato.'
                ]
            },
            'Desarrollo de competencias': {
                'MEDIO': [
                    'Sentir que no tienes las oportunidades de desarrollo que necesitas puede generar frustración y estrés. Una evaluación médica ocupacional puede ayudarte a identificar cómo esta situación está afectando tu bienestar.',
                    'La falta de crecimiento profesional puede impactar tu autoestima y motivación. Es importante que hables con medicina ocupacional sobre cómo te sientes respecto a tu desarrollo profesional.',
                    'Si experimentas sentimientos de estancamiento, desmotivación o ansiedad relacionada con tu futuro profesional, estos son aspectos importantes a compartir en tu evaluación médica.',
                    'Considera que el desarrollo profesional es parte integral de tu bienestar. Buscar apoyo puede ayudarte a encontrar estrategias para manejar esta situación mientras se buscan soluciones.'
                ],
                'ALTO': [
                    'La falta de oportunidades de desarrollo puede tener un impacto significativo en tu salud mental y bienestar general. Es importante que solicites una evaluación médica ocupacional para abordar esta situación.',
                    'Si sientes que tu carrera está estancada y esto te genera ansiedad, depresión, o afecta tu autoestima, una evaluación psicológica ocupacional puede ayudarte a desarrollar estrategias de afrontamiento.',
                    'El estrés relacionado con el desarrollo profesional puede manifestarse en síntomas físicos como tensión muscular, problemas de sueño, o cambios en el apetito. No ignores estas señales.',
                    'Recuerda que tu bienestar profesional es importante. Si esta situación está afectando tu salud, es válido buscar apoyo y considerar opciones que promuevan tu crecimiento personal y profesional.'
                ]
            },
            'Liderazgo': {
                'MEDIO': [
                    'Las dificultades con el liderazgo o supervisión pueden generar estrés significativo. Una evaluación médica ocupacional puede ayudarte a identificar cómo estas relaciones están afectando tu bienestar.',
                    'Si sientes que no recibes el apoyo, reconocimiento o dirección que necesitas de tus superiores, esto puede impactar tu salud mental. Es importante compartir estas preocupaciones con medicina ocupacional.',
                    'El estrés relacionado con el liderazgo puede manifestarse en ansiedad antes de reuniones, dificultad para dormir, o tensión constante. Estos síntomas merecen atención médica.',
                    'Recuerda que tener un buen liderazgo es fundamental para tu bienestar laboral. Si esta situación te está afectando, buscar apoyo profesional puede ayudarte a desarrollar estrategias de manejo.'
                ],
                'ALTO': [
                    'Un liderazgo deficiente puede tener un impacto grave en tu salud física y mental. Es importante que solicites una evaluación médica ocupacional inmediata para prevenir consecuencias a largo plazo.',
                    'Si experimentas síntomas como ansiedad constante, miedo al trabajo, problemas digestivos relacionados con el estrés, o dificultad para concentrarte debido a la tensión con superiores, estos son signos de alerta.',
                    'Una evaluación psicológica ocupacional puede ayudarte a identificar cómo el liderazgo está afectando tu autoestima, motivación y bienestar general, y desarrollar estrategias de afrontamiento saludables.',
                    'El estrés crónico por problemas de liderazgo puede afectar tu sistema inmunológico y aumentar el riesgo de enfermedades. No ignores estos síntomas y busca apoyo médico de inmediato.',
                    'Tu bienestar es prioritario. Si la situación con el liderazgo está afectando significativamente tu salud, es importante que busques apoyo profesional y consideres todas las opciones disponibles para protegerte.'
                ]
            },
            'Margen de acción y control': {
                'MEDIO': [
                    'Sentir que no tienes control sobre tu trabajo puede generar frustración y estrés. Una evaluación médica ocupacional puede ayudarte a identificar cómo la falta de autonomía está afectando tu bienestar.',
                    'La sensación de falta de control puede impactar tu motivación y satisfacción laboral. Si experimentas sentimientos de impotencia o frustración constante, es importante compartirlos con medicina ocupacional.',
                    'El estrés por falta de autonomía puede manifestarse en tensión muscular, dolores de cabeza, o dificultad para relajarte después del trabajo. Estos síntomas merecen atención médica.',
                    'Recuerda que tener cierto grado de control sobre tu trabajo es importante para tu bienestar. Buscar apoyo puede ayudarte a desarrollar estrategias para manejar esta situación.'
                ],
                'ALTO': [
                    'La falta de control sobre tu trabajo puede tener un impacto significativo en tu salud mental y física. Es importante que solicites una evaluación médica ocupacional para abordar esta situación.',
                    'Si sientes que no tienes voz en las decisiones que afectan tu trabajo y esto te genera ansiedad, depresión, o afecta tu autoestima, una evaluación psicológica ocupacional puede ayudarte.',
                    'El estrés crónico por falta de autonomía puede manifestarse en síntomas como insomnio, problemas digestivos, tensión constante, o sentimientos de desesperanza. No ignores estas señales.',
                    'La falta de control puede hacerte sentir atrapado o sin opciones. Es importante que busques apoyo profesional para desarrollar estrategias de afrontamiento y explorar opciones que te den más autonomía.',
                    'Tu bienestar es importante. Si esta situación está afectando significativamente tu salud, busca apoyo médico y considera todas las opciones disponibles para mejorar tu situación laboral.'
                ]
            },
            'Organización del trabajo': {
                'MEDIO': [
                    'La falta de claridad en objetivos y organización puede generar confusión y estrés. Una evaluación médica ocupacional puede ayudarte a identificar cómo esta situación está afectando tu bienestar.',
                    'Si sientes que no tienes claridad sobre qué se espera de ti o cómo organizar tu trabajo, esto puede generar ansiedad y frustración. Es importante compartir estas preocupaciones con medicina ocupacional.',
                    'El estrés por desorganización puede manifestarse en dificultad para concentrarte, sensación de estar siempre atrasado, o tensión constante. Estos síntomas merecen atención médica.',
                    'Recuerda que tener claridad y organización en el trabajo es fundamental para tu bienestar. Buscar apoyo puede ayudarte a desarrollar estrategias para manejar esta situación mientras se buscan mejoras organizacionales.'
                ],
                'ALTO': [
                    'La desorganización y falta de claridad en el trabajo puede tener un impacto grave en tu salud mental y física. Es importante que solicites una evaluación médica ocupacional para abordar esta situación.',
                    'Si la falta de organización te genera ansiedad constante, sensación de estar siempre perdido, o afecta tu capacidad para realizar tu trabajo, una evaluación psicológica ocupacional puede ayudarte.',
                    'El estrés crónico por desorganización puede manifestarse en síntomas como insomnio, problemas de memoria, dificultad para tomar decisiones, o agotamiento mental. No ignores estas señales.',
                    'La falta de estructura puede hacerte sentir abrumado y sin control. Es importante que busques apoyo profesional para desarrollar estrategias de afrontamiento y explorar opciones que mejoren la organización.',
                    'Tu bienestar es prioritario. Si esta situación está afectando significativamente tu salud, busca apoyo médico y considera todas las opciones disponibles para mejorar tu entorno laboral.'
                ]
            },
            'Recuperación': {
                'MEDIO': [
                    'No tener suficiente tiempo para recuperarte del trabajo puede afectar tu salud física y mental. Una evaluación médica ocupacional puede ayudarte a identificar cómo la falta de descanso está impactando tu bienestar.',
                    'Si sientes que nunca te recuperas completamente del trabajo, experimentas fatiga constante, o tienes dificultad para desconectarte, estos son signos importantes a compartir con medicina ocupacional.',
                    'La falta de recuperación adecuada puede manifestarse en problemas de sueño, irritabilidad, dificultad para concentrarte, o dolores musculares persistentes. Estos síntomas merecen atención médica.',
                    'El descanso es fundamental para tu salud. Si sientes que no tienes tiempo suficiente para recuperarte, busca apoyo para desarrollar estrategias que te permitan desconectarte y descansar adecuadamente.'
                ],
                'ALTO': [
                    'La falta de recuperación puede tener consecuencias graves para tu salud. Es importante que solicites una evaluación médica ocupacional inmediata para prevenir el agotamiento y otras complicaciones.',
                    'Si experimentas agotamiento extremo, insomnio persistente, dificultad para funcionar en tu vida diaria, o síntomas físicos relacionados con la falta de descanso, estos son signos de alerta que requieren atención médica urgente.',
                    'El agotamiento crónico puede afectar tu sistema inmunológico, cardiovascular y mental. Una evaluación psicológica ocupacional puede ayudarte a identificar estrategias para mejorar tu recuperación.',
                    'La falta de recuperación puede llevarte al agotamiento profesional (burnout). No ignores estos síntomas y busca apoyo médico de inmediato para prevenir consecuencias a largo plazo.',
                    'Tu salud es lo más importante. Si sientes que no puedes recuperarte del trabajo y esto está afectando tu vida, busca apoyo profesional urgente y considera todas las opciones para proteger tu bienestar.'
                ]
            },
            'Soporte y apoyo': {
                'MEDIO': [
                    'Sentir que no tienes el apoyo que necesitas en el trabajo puede generar estrés y sensación de soledad. Una evaluación médica ocupacional puede ayudarte a identificar cómo esta situación está afectando tu bienestar.',
                    'Si sientes que no puedes contar con tus compañeros o superiores cuando lo necesitas, esto puede impactar tu salud mental. Es importante compartir estas preocupaciones con medicina ocupacional.',
                    'La falta de apoyo puede manifestarse en ansiedad, sentimientos de aislamiento, o dificultad para manejar situaciones estresantes en el trabajo. Estos síntomas merecen atención médica.',
                    'El apoyo social en el trabajo es fundamental para tu bienestar. Buscar ayuda puede ayudarte a desarrollar estrategias para manejar esta situación y encontrar formas de obtener el apoyo que necesitas.'
                ],
                'ALTO': [
                    'La falta de apoyo en el trabajo puede tener un impacto significativo en tu salud mental y física. Es importante que solicites una evaluación médica ocupacional para abordar esta situación.',
                    'Si sientes que estás completamente solo en el trabajo y esto te genera ansiedad, depresión, o afecta tu capacidad para realizar tu trabajo, una evaluación psicológica ocupacional puede ayudarte.',
                    'El estrés crónico por falta de apoyo puede manifestarse en síntomas como insomnio, problemas digestivos, sentimientos de desesperanza, o dificultad para manejar el estrés. No ignores estas señales.',
                    'Sentirte sin apoyo puede hacerte sentir vulnerable y estresado. Es importante que busques apoyo profesional para desarrollar estrategias de afrontamiento y explorar opciones que mejoren tu red de apoyo.',
                    'Tu bienestar es importante. Si esta situación está afectando significativamente tu salud, busca apoyo médico y considera todas las opciones disponibles para mejorar tu entorno laboral.'
                ]
            },
            'Acoso discriminatorio': {
                'MEDIO': [
                    'Experimentar discriminación en el trabajo puede tener un impacto profundo en tu bienestar. Una evaluación médica ocupacional inmediata puede ayudarte a identificar cómo esta situación está afectando tu salud física y mental.',
                    'Si has experimentado discriminación basada en género, edad, raza, orientación sexual, o cualquier otra característica, esto puede generar estrés significativo. Es importante compartir estas experiencias con medicina ocupacional.',
                    'La discriminación puede manifestarse en síntomas como ansiedad, depresión, baja autoestima, o dificultad para concentrarte. Estos síntomas merecen atención médica y apoyo profesional.',
                    'Nadie debería experimentar discriminación en el trabajo. Buscar apoyo médico y legal puede ayudarte a protegerte y desarrollar estrategias para manejar esta situación difícil.'
                ],
                'ALTO': [
                    'La discriminación en el trabajo puede tener consecuencias graves para tu salud. Es importante que solicites una evaluación médica ocupacional URGENTE para proteger tu bienestar y documentar el impacto.',
                    'Si experimentas discriminación constante y esto te genera ansiedad severa, depresión, síntomas de estrés postraumático, o afecta tu capacidad para trabajar, busca apoyo médico y psicológico inmediato.',
                    'La discriminación puede causar trauma psicológico. Una evaluación psicológica ocupacional urgente puede ayudarte a identificar el impacto y desarrollar estrategias de afrontamiento y protección.',
                    'No estás solo. Si experimentas discriminación, es importante que busques apoyo profesional, legal y médico. Documenta los incidentes y considera todas las opciones disponibles para protegerte.',
                    'Tu dignidad y bienestar son invaluables. Si la discriminación está afectando tu salud, busca ayuda urgente y considera todas las opciones para poner fin a esta situación.'
                ]
            },
            'Acoso laboral': {
                'MEDIO': [
                    'El acoso laboral puede tener un impacto significativo en tu salud. Una evaluación médica ocupacional inmediata puede ayudarte a identificar cómo esta situación está afectando tu bienestar físico y mental.',
                    'Si experimentas acoso en el trabajo, ya sea verbal, psicológico o de otro tipo, esto puede generar estrés, ansiedad y afectar tu autoestima. Es importante compartir estas experiencias con medicina ocupacional.',
                    'El acoso puede manifestarse en síntomas como insomnio, ansiedad constante, dificultad para concentrarte, o síntomas físicos relacionados con el estrés. Estos síntomas merecen atención médica inmediata.',
                    'Nadie merece ser acosado en el trabajo. Buscar apoyo médico, psicológico y legal puede ayudarte a protegerte y desarrollar estrategias para manejar esta situación difícil.'
                ],
                'ALTO': [
                    'El acoso laboral puede tener consecuencias graves para tu salud. Es importante que solicites una evaluación médica ocupacional URGENTE para proteger tu bienestar y documentar el impacto.',
                    'Si experimentas acoso constante y esto te genera ansiedad severa, depresión, síntomas de estrés postraumático, o afecta tu capacidad para trabajar, busca apoyo médico y psicológico inmediato.',
                    'El acoso puede causar trauma psicológico. Una evaluación psicológica ocupacional urgente puede ayudarte a identificar el impacto y desarrollar estrategias de afrontamiento y protección.',
                    'No estás solo. Si experimentas acoso, es importante que busques apoyo profesional, legal y médico de inmediato. Documenta los incidentes y activa los protocolos de protección disponibles.',
                    'Tu seguridad y bienestar son lo más importante. Si el acoso está afectando tu salud, busca ayuda urgente y considera todas las opciones para poner fin a esta situación y protegerte.'
                ]
            },
            'Acoso sexual': {
                'MEDIO': [
                    'El acoso sexual en el trabajo es una situación grave que puede tener un impacto profundo en tu salud. Una evaluación médica ocupacional inmediata puede ayudarte a identificar cómo esta situación está afectando tu bienestar.',
                    'Si has experimentado acoso sexual, esto puede generar trauma, ansiedad, depresión y afectar tu capacidad para trabajar. Es importante compartir estas experiencias con medicina ocupacional de forma segura y confidencial.',
                    'El acoso sexual puede manifestarse en síntomas como insomnio, pesadillas, ansiedad constante, dificultad para concentrarte, o síntomas físicos relacionados con el estrés. Estos síntomas merecen atención médica inmediata.',
                    'Nadie debería experimentar acoso sexual. Buscar apoyo médico, psicológico y legal puede ayudarte a protegerte y desarrollar estrategias para manejar esta situación extremadamente difícil.'
                ],
                'ALTO': [
                    'El acoso sexual en el trabajo puede tener consecuencias graves para tu salud física y mental. Es importante que solicites una evaluación médica ocupacional URGENTE para proteger tu bienestar y documentar el impacto.',
                    'Si experimentas acoso sexual constante y esto te genera ansiedad severa, depresión, síntomas de estrés postraumático, o afecta tu capacidad para trabajar, busca apoyo médico y psicológico inmediato.',
                    'El acoso sexual puede causar trauma psicológico severo. Una evaluación psicológica ocupacional urgente puede ayudarte a identificar el impacto y desarrollar estrategias de afrontamiento y protección.',
                    'No estás solo. Si experimentas acoso sexual, es crítico que busques apoyo profesional, legal y médico de inmediato. Documenta los incidentes y activa los protocolos de protección disponibles.',
                    'Tu seguridad, dignidad y bienestar son invaluables. Si el acoso sexual está afectando tu salud, busca ayuda urgente y considera todas las opciones para poner fin a esta situación y protegerte.'
                ]
            },
            'Adicción al trabajo': {
                'MEDIO': [
                    'Trabajar excesivamente puede afectar tu salud física y mental. Una evaluación médica ocupacional puede ayudarte a identificar cómo la adicción al trabajo está impactando tu bienestar.',
                    'Si sientes que no puedes desconectarte del trabajo, trabajas constantemente fuera del horario laboral, o sientes ansiedad cuando no estás trabajando, estos son signos importantes a compartir con medicina ocupacional.',
                    'La adicción al trabajo puede manifestarse en problemas de sueño, fatiga crónica, dificultad para relajarte, o problemas en tus relaciones personales. Estos síntomas merecen atención médica.',
                    'El equilibrio es fundamental para tu salud. Si sientes que el trabajo está consumiendo tu vida, busca apoyo para desarrollar estrategias que te permitan establecer límites saludables.'
                ],
                'ALTO': [
                    'La adicción al trabajo puede tener consecuencias graves para tu salud. Es importante que solicites una evaluación médica ocupacional para prevenir el agotamiento y otras complicaciones.',
                    'Si trabajas constantemente, no puedes desconectarte, experimentas agotamiento extremo, o el trabajo está afectando seriamente tu vida personal y salud, estos son signos de alerta que requieren atención médica urgente.',
                    'El trabajo excesivo puede llevar al agotamiento profesional (burnout) y afectar tu sistema cardiovascular, inmunológico y mental. Una evaluación psicológica ocupacional puede ayudarte a desarrollar estrategias para establecer límites saludables.',
                    'La adicción al trabajo puede hacerte sentir que tu valor está solo en el trabajo. Es importante que busques apoyo profesional para desarrollar un equilibrio saludable y prevenir consecuencias a largo plazo.',
                    'Tu bienestar es más importante que el trabajo. Si sientes que no puedes parar de trabajar y esto está afectando tu salud, busca apoyo médico urgente y considera todas las opciones para protegerte.'
                ]
            },
            'Condiciones del trabajo': {
                'MEDIO': [
                    'Las condiciones físicas del trabajo pueden afectar tu salud. Una evaluación médica ocupacional puede ayudarte a identificar cómo el entorno laboral está impactando tu bienestar físico.',
                    'Si experimentas molestias relacionadas con iluminación, ruido, temperatura, ergonomía del puesto, o condiciones físicas del espacio, estos son aspectos importantes a compartir con medicina ocupacional.',
                    'Las malas condiciones de trabajo pueden manifestarse en dolores musculares, problemas visuales, fatiga, o dificultad para concentrarte. Estos síntomas merecen atención médica y evaluación ergonómica.',
                    'Tu entorno laboral debe ser seguro y saludable. Si las condiciones físicas están afectando tu bienestar, busca apoyo para identificar mejoras necesarias y proteger tu salud.'
                ],
                'ALTO': [
                    'Las condiciones físicas deficientes del trabajo pueden tener consecuencias graves para tu salud. Es importante que solicites una evaluación médica ocupacional inmediata para identificar riesgos y prevenir lesiones.',
                    'Si experimentas dolores persistentes, problemas visuales severos, dificultad respiratoria, o cualquier síntoma físico relacionado con las condiciones del trabajo, estos son signos de alerta que requieren atención médica urgente.',
                    'Una evaluación ergonómica y de medicina del trabajo puede identificar riesgos específicos y ayudar a implementar medidas correctivas urgentes para proteger tu salud.',
                    'Las condiciones físicas peligrosas pueden causar lesiones permanentes. No ignores estos síntomas y busca apoyo médico de inmediato para documentar el impacto y protegerte.',
                    'Tu seguridad física es fundamental. Si las condiciones del trabajo están afectando tu salud, busca ayuda urgente y considera todas las opciones para mejorar tu entorno laboral y protegerte.'
                ]
            },
            'Doble presencia (laboral-familiar)': {
                'MEDIO': [
                    'Equilibrar trabajo y familia puede ser desafiante y afectar tu bienestar. Una evaluación médica ocupacional puede ayudarte a identificar cómo esta situación está impactando tu salud física y mental.',
                    'Si sientes que nunca tienes tiempo suficiente para tu familia, experimentas culpa constante, o el trabajo interfiere con tus responsabilidades familiares, estos son signos importantes a compartir con medicina ocupacional.',
                    'La doble presencia puede manifestarse en estrés constante, fatiga, dificultad para dormir, o problemas en tus relaciones familiares. Estos síntomas merecen atención médica.',
                    'El equilibrio entre trabajo y familia es fundamental para tu bienestar. Buscar apoyo puede ayudarte a desarrollar estrategias que te permitan manejar ambas responsabilidades de manera más saludable.'
                ],
                'ALTO': [
                    'La dificultad para equilibrar trabajo y familia puede tener consecuencias graves para tu salud. Es importante que solicites una evaluación médica ocupacional para abordar esta situación.',
                    'Si sientes que estás constantemente dividido entre trabajo y familia, experimentas agotamiento extremo, o esta situación está afectando seriamente tu salud y relaciones, estos son signos de alerta que requieren atención médica urgente.',
                    'El estrés crónico por doble presencia puede afectar tu sistema inmunológico, cardiovascular y mental. Una evaluación psicológica ocupacional puede ayudarte a desarrollar estrategias para mejorar el equilibrio.',
                    'La doble presencia puede hacerte sentir que nunca estás presente completamente en ningún lugar. Es importante que busques apoyo profesional para desarrollar límites saludables y prevenir consecuencias a largo plazo.',
                    'Tu bienestar y el de tu familia son importantes. Si esta situación está afectando significativamente tu salud, busca apoyo médico urgente y considera todas las opciones para mejorar el equilibrio.'
                ]
            },
            'Estabilidad laboral percibida': {
                'MEDIO': [
                    'Sentir inseguridad sobre tu empleo puede generar ansiedad y estrés significativo. Una evaluación médica ocupacional puede ayudarte a identificar cómo esta preocupación está afectando tu bienestar.',
                    'Si sientes preocupación constante sobre tu estabilidad laboral, esto puede impactar tu salud mental y generar síntomas como ansiedad, dificultad para dormir, o tensión constante. Es importante compartir estas preocupaciones con medicina ocupacional.',
                    'La inseguridad laboral puede manifestarse en síntomas físicos relacionados con el estrés, como problemas digestivos, tensión muscular, o dolores de cabeza. Estos síntomas merecen atención médica.',
                    'La estabilidad laboral es importante para tu bienestar. Buscar apoyo puede ayudarte a desarrollar estrategias para manejar esta incertidumbre y reducir su impacto en tu salud.'
                ],
                'ALTO': [
                    'La inseguridad laboral extrema puede tener un impacto significativo en tu salud. Es importante que solicites una evaluación médica ocupacional para abordar esta situación y prevenir consecuencias a largo plazo.',
                    'Si la preocupación sobre tu estabilidad laboral te genera ansiedad severa, depresión, insomnio persistente, o afecta tu capacidad para funcionar, estos son signos de alerta que requieren atención médica urgente.',
                    'El estrés crónico por inseguridad laboral puede afectar tu sistema inmunológico, cardiovascular y mental. Una evaluación psicológica ocupacional puede ayudarte a desarrollar estrategias de afrontamiento.',
                    'La incertidumbre constante puede hacerte sentir vulnerable y estresado. Es importante que busques apoyo profesional para desarrollar estrategias de afrontamiento y explorar opciones que te den más seguridad.',
                    'Tu bienestar es importante. Si la inseguridad laboral está afectando significativamente tu salud, busca apoyo médico y considera todas las opciones disponibles para mejorar tu situación.'
                ]
            },
            'Salud auto percibida': {
                'MEDIO': [
                    'Si percibes que tu salud no está en buen estado, es importante que busques una evaluación médica ocupacional para identificar factores laborales que puedan estar afectando tu bienestar.',
                    'Tu percepción de tu salud es importante. Si sientes que tu trabajo está afectando tu salud física o mental, comparte estas preocupaciones con medicina ocupacional para una evaluación completa.',
                    'Los síntomas que percibes, ya sean físicos o mentales, merecen atención médica. Una evaluación puede ayudarte a identificar la causa y desarrollar estrategias para mejorar tu bienestar.',
                    'No ignores tus preocupaciones sobre tu salud. Buscar apoyo médico puede ayudarte a identificar problemas temprano y prevenir complicaciones a largo plazo.'
                ],
                'ALTO': [
                    'Si percibes que tu salud está significativamente afectada, es importante que solicites una evaluación médica ocupacional urgente para identificar factores laborales y prevenir complicaciones.',
                    'Tu percepción de problemas de salud es válida y merece atención inmediata. Si sientes que tu trabajo está afectando seriamente tu salud, busca apoyo médico urgente.',
                    'Una evaluación médica completa puede ayudarte a identificar problemas de salud relacionados con el trabajo y desarrollar un plan de tratamiento y prevención.',
                    'No ignores síntomas persistentes o preocupaciones sobre tu salud. Buscar ayuda médica temprana puede prevenir complicaciones y ayudarte a proteger tu bienestar a largo plazo.',
                    'Tu salud es lo más importante. Si percibes que tu trabajo está afectando significativamente tu bienestar, busca apoyo médico urgente y considera todas las opciones para protegerte.'
                ]
            },
            'Reconocimiento y compensación': {
                'MEDIO': [
                    'Se recomienda evaluación médica ocupacional para identificar posibles factores de estrés relacionados con el reconocimiento laboral.',
                    'Considera implementar programas de reconocimiento y valoración del trabajo.',
                    'Se sugiere evaluación de factores psicosociales relacionados con la satisfacción laboral.'
                ],
                'ALTO': [
                    'Se requiere evaluación médica ocupacional para determinar el impacto de la falta de reconocimiento en la salud.',
                    'Se recomienda evaluación psicológica ocupacional para identificar factores de riesgo relacionados con valoración laboral.',
                    'Considera implementar medidas de intervención según evaluación médica ocupacional.'
                ]
            },
            'Equilibrio trabajo-vida': {
                'MEDIO': [
                    'Se recomienda evaluación médica ocupacional para identificar posibles factores de estrés relacionados con el equilibrio trabajo-vida.',
                    'Considera implementar programas de gestión del tiempo y bienestar personal.',
                    'Se sugiere evaluación de factores relacionados con el estrés crónico.'
                ],
                'ALTO': [
                    'Se requiere evaluación médica ocupacional inmediata para determinar el impacto del desequilibrio trabajo-vida en la salud.',
                    'Se recomienda evaluación psicológica ocupacional para identificar factores de riesgo relacionados con el equilibrio personal.',
                    'Considera implementar medidas de adaptación y apoyo según evaluación médica ocupacional.'
                ]
            },
            'Condiciones de trabajo': {
                'MEDIO': [
                    'Se recomienda evaluación médica ocupacional para identificar posibles factores de riesgo relacionados con las condiciones de trabajo.',
                    'Considera implementar mejoras en las condiciones físicas del entorno laboral.',
                    'Se sugiere evaluación ergonómica completa del puesto de trabajo.'
                ],
                'ALTO': [
                    'Se requiere evaluación médica ocupacional inmediata para determinar el impacto de las condiciones de trabajo en la salud.',
                    'Se recomienda evaluación de medicina del trabajo para identificar riesgos físicos y ergonómicos.',
                    'Considera implementar medidas correctivas urgentes según evaluación médica ocupacional.'
                ]
            },
            'Exposición a riesgos': {
                'MEDIO': [
                    'Se recomienda evaluación médica ocupacional para identificar posibles factores de riesgo relacionados con la exposición laboral.',
                    'Considera implementar medidas de protección personal y colectiva.',
                    'Se sugiere evaluación de riesgos ocupacionales específicos del puesto de trabajo.'
                ],
                'ALTO': [
                    'Se requiere evaluación médica ocupacional inmediata para determinar el impacto de la exposición a riesgos en la salud.',
                    'Se recomienda evaluación de medicina del trabajo para identificar riesgos específicos y su impacto.',
                    'Considera implementar medidas de control de riesgos urgentes según evaluación médica ocupacional.'
                ]
            },
            'Carga mental': {
                'MEDIO': [
                    'Se recomienda evaluación médica ocupacional para identificar posibles factores de estrés relacionados con la carga mental.',
                    'Considera implementar programas de gestión de la carga cognitiva.',
                    'Se sugiere evaluación de factores psicosociales relacionados con la demanda mental.'
                ],
                'ALTO': [
                    'Se requiere evaluación médica ocupacional inmediata para determinar el impacto de la carga mental en la salud.',
                    'Se recomienda evaluación psicológica ocupacional para identificar factores de riesgo relacionados con la sobrecarga cognitiva.',
                    'Considera implementar medidas de adaptación según evaluación médica ocupacional.'
                ]
            },
            'Interferencia en la relación trabajo-familia': {
                'MEDIO': [
                    'Se recomienda evaluación médica ocupacional para identificar posibles factores de estrés relacionados con la interferencia trabajo-familia.',
                    'Considera implementar programas de apoyo para el equilibrio personal.',
                    'Se sugiere evaluación de factores psicosociales relacionados con la conciliación familiar.'
                ],
                'ALTO': [
                    'Se requiere evaluación médica ocupacional para determinar el impacto de la interferencia trabajo-familia en la salud.',
                    'Se recomienda evaluación psicológica ocupacional para identificar factores de riesgo relacionados con la conciliación.',
                    'Considera implementar medidas de apoyo y adaptación según evaluación médica ocupacional.'
                ]
            },
            'Violencia laboral': {
                'MEDIO': [
                    'La violencia laboral puede tener un impacto profundo en tu salud. Una evaluación médica ocupacional inmediata puede ayudarte a identificar cómo esta situación está afectando tu bienestar físico y mental.',
                    'Si has experimentado violencia en el trabajo, ya sea física, verbal o psicológica, esto puede generar trauma, ansiedad y afectar tu capacidad para trabajar. Es importante compartir estas experiencias con medicina ocupacional.',
                    'La violencia puede manifestarse en síntomas como insomnio, pesadillas, ansiedad constante, dificultad para concentrarte, o síntomas físicos relacionados con el estrés. Estos síntomas merecen atención médica inmediata.',
                    'Nadie debería experimentar violencia en el trabajo. Buscar apoyo médico, psicológico y legal puede ayudarte a protegerte y desarrollar estrategias para manejar esta situación extremadamente difícil.'
                ],
                'ALTO': [
                    'La violencia laboral puede tener consecuencias graves para tu salud física y mental. Es importante que solicites una evaluación médica ocupacional URGENTE para proteger tu bienestar y documentar el impacto.',
                    'Si experimentas violencia constante y esto te genera ansiedad severa, depresión, síntomas de estrés postraumático, o afecta tu capacidad para trabajar, busca apoyo médico y psicológico inmediato.',
                    'La violencia puede causar trauma psicológico severo. Una evaluación psicológica ocupacional urgente puede ayudarte a identificar el impacto y desarrollar estrategias de afrontamiento y protección.',
                    'No estás solo. Si experimentas violencia, es crítico que busques apoyo profesional, legal y médico de inmediato. Documenta los incidentes y activa los protocolos de protección disponibles.',
                    'Tu seguridad y bienestar son lo más importante. Si la violencia está afectando tu salud, busca ayuda urgente y considera todas las opciones para poner fin a esta situación y protegerte.'
                ]
            }
        }
        
        # Buscar recomendaciones específicas para la dimensión y nivel
        dim_recs = medical_recommendations.get(dimension_name, {})
        if dim_recs and risk_level in dim_recs:
            return dim_recs[risk_level]
        
        # Recomendaciones por defecto empáticas si no hay específicas para esta dimensión
        default_recommendations = {
            'MEDIO': [
                f'Entendemos que esta situación puede estar afectando tu bienestar. Te recomendamos una evaluación médica ocupacional para identificar cómo {dimension_name.lower()} está impactando tu salud física y mental.',
                'Es importante que compartas cualquier síntoma o preocupación que tengas con medicina ocupacional. Tu bienestar es nuestra prioridad.',
                'Buscar apoyo profesional puede ayudarte a desarrollar estrategias para manejar esta situación y proteger tu salud.'
            ],
            'ALTO': [
                f'Esta situación puede tener un impacto significativo en tu salud. Es importante que solicites una evaluación médica ocupacional urgente para identificar cómo {dimension_name.lower()} está afectando tu bienestar.',
                'Si experimentas síntomas físicos o psicológicos relacionados con esta situación, estos son signos de alerta que requieren atención médica inmediata.',
                'Tu salud es lo más importante. No ignores los síntomas y busca apoyo profesional urgente para protegerte y desarrollar estrategias de afrontamiento.',
                'Una evaluación médica y psicológica ocupacional puede ayudarte a identificar el impacto y desarrollar un plan para proteger tu bienestar.'
            ]
        }
        
        return default_recommendations.get(risk_level, [
            'Te recomendamos una evaluación médica ocupacional para identificar posibles factores de riesgo y proteger tu bienestar.',
            'Tu salud es importante. Si tienes preocupaciones sobre cómo esta situación está afectando tu bienestar, busca apoyo profesional.'
        ])
    
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
