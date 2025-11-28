"""
Servicio para generar recomendaciones específicas para empleadores/administradores.
Estas recomendaciones son explícitas, objetivas y orientadas a la acción empresarial.
"""
from typing import Dict, List


class EmployerRecommendationsService:
    """Servicio para generar recomendaciones empresariales basadas en resultados de evaluación"""
    
    def get_recommendations_by_dimension(self, dimension_name: str, risk_level: str) -> List[str]:
        """
        Obtiene recomendaciones específicas para empleadores por dimensión y nivel de riesgo
        
        Args:
            dimension_name: Nombre de la dimensión
            risk_level: Nivel de riesgo (BAJO, MEDIO, ALTO)
        
        Returns:
            Lista de recomendaciones orientadas a la acción empresarial
        """
        # Diccionario completo de recomendaciones por dimensión y nivel
        recommendations = {
            'Carga y ritmo de trabajo': {
                'ALTO': [
                    "**ACCIÓN URGENTE**: Realizar auditoría inmediata de distribución de cargas laborales. Redistribuir tareas sobrecargadas.",
                    "Implementar sistema de monitoreo de horas trabajadas con alertas automáticas cuando se excedan límites saludables.",
                    "Evaluar necesidad de contratación de personal adicional o redistribución de responsabilidades entre equipos.",
                    "Establecer pausas obligatorias y controlar su cumplimiento efectivo durante la jornada laboral.",
                    "Revisar y ajustar plazos de entrega realistas en consulta con los equipos ejecutores.",
                    "Capacitar a supervisores en identificación temprana de señales de sobrecarga laboral."
                ],
                'MEDIO': [
                    "Monitorear semanalmente la carga de trabajo mediante reportes de avance y encuestas rápidas.",
                    "Capacitar a líderes de equipo en gestión eficiente del tiempo y priorización de tareas.",
                    "Implementar canales de comunicación directa para reportar situaciones de sobrecarga antes de que escalen.",
                    "Utilizar herramientas de gestión de proyectos para visibilizar cuellos de botella y optimizar flujos.",
                    "Establecer reuniones mensuales de revisión de cargas con cada equipo."
                ],
                'BAJO': [
                    "**MANTENER**: El equilibrio actual en distribución de tareas es adecuado. Documentar las prácticas exitosas.",
                    "Continuar monitoreando preventivamente mediante indicadores de carga laboral.",
                    "Reconocer y compartir las buenas prácticas de gestión del tiempo con otras áreas.",
                    "Mantener comunicación abierta para detectar cambios antes de que se conviertan en problemas."
                ]
            },
            'Desarrollo de competencias': {
                'ALTO': [
                    "**ACCIÓN URGENTE**: Diseñar plan de capacitación anual con presupuesto asignado y metas claras de desarrollo por puesto.",
                    "Establecer alianzas con instituciones educativas y plataformas de formación online.",
                    "Implementar programa de mentoría interna donde colaboradores experimentados guíen a nuevos o menos capacitados.",
                    "Crear planes de carrera individualizados que muestren caminos de crecimiento concretos.",
                    "Asignar horas laborales específicas para formación sin afectar la productividad.",
                    "Establecer sistema de certificación y reconocimiento de nuevas competencias adquiridas."
                ],
                'MEDIO': [
                    "Realizar diagnóstico formal de necesidades de capacitación por área y puesto.",
                    "Programar cursos trimestrales de actualización profesional relevantes al sector.",
                    "Facilitar participación en seminarios, webinars y conferencias del sector (virtual o presencial).",
                    "Implementar sistema de reconocimiento económico o simbólico al completar capacitaciones.",
                    "Crear biblioteca digital de recursos de aprendizaje accesible para todo el personal."
                ],
                'BAJO': [
                    "**MANTENER**: Los programas de capacitación actuales están funcionando bien. Continuar con el enfoque actual.",
                    "Documentar y compartir las mejores prácticas de desarrollo con toda la organización.",
                    "Reconocer públicamente a quienes participan activamente en su formación continua.",
                    "Mantener el presupuesto y tiempo destinado a capacitación."
                ]
            },
            'Liderazgo': {
                'ALTO': [
                    "**ACCIÓN URGENTE**: Implementar evaluación 360° obligatoria para todos los supervisores y mandos medios.",
                    "Contratar programa intensivo de formación en liderazgo, inteligencia emocional y gestión de personas.",
                    "Establecer canal anónimo de retroalimentación sobre estilo de liderazgo con seguimiento garantizado.",
                    "Revisar perfiles de puesto de líderes y actualizar competencias requeridas.",
                    "Considerar coaching ejecutivo externo para líderes con evaluaciones críticas.",
                    "Establecer consecuencias claras para liderazgos tóxicos o contraproducentes."
                ],
                'MEDIO': [
                    "Ofrecer talleres mensuales de habilidades de liderazgo efectivo y comunicación asertiva.",
                    "Crear espacios estructurados de retroalimentación bidireccional líder-equipo.",
                    "Implementar coaching grupal para líderes de equipos similares.",
                    "Promover modelo de liderazgo participativo mediante reconocimientos y buenos ejemplos.",
                    "Establecer indicadores de clima laboral por equipo para medir impacto del liderazgo."
                ],
                'BAJO': [
                    "**MANTENER**: El liderazgo actual es positivo. Reconocer y visibilizar estas buenas prácticas.",
                    "Documentar el estilo de liderazgo exitoso para replicarlo en otras áreas.",
                    "Invitar a líderes destacados a compartir sus estrategias con otros supervisores.",
                    "Mantener los programas de desarrollo y seguimiento de líderes."
                ]
            },
            'Margen de acción y control': {
                'ALTO': [
                    "**ACCIÓN URGENTE**: Mapear decisiones que pueden ser delegadas sin riesgo y establecer protocolos claros.",
                    "Capacitar a supervisores en empowerment y confianza en el equipo, reduciendo microgestión.",
                    "Definir por escrito niveles de autoridad para cada puesto y comunicarlos claramente.",
                    "Crear comités de participación donde empleados opinen sobre decisiones que les afectan.",
                    "Implementar sistema de sugerencias con respuestas obligatorias de la gerencia.",
                    "Revisar causas de la centralización excesiva y establecer plan de descentralización gradual."
                ],
                'MEDIO': [
                    "Ampliar gradualmente los márgenes de decisión autónoma del personal operativo.",
                    "Establecer mecanismos de consulta antes de implementar cambios importantes en procesos.",
                    "Promover participación activa en la planificación de tareas y métodos de trabajo.",
                    "Capacitar a líderes en delegación efectiva y confianza en el equipo.",
                    "Reconocer iniciativas y decisiones acertadas tomadas por el personal."
                ],
                'BAJO': [
                    "**MANTENER**: Los niveles de autonomía actuales están bien balanceados. Continuar con esta práctica.",
                    "Documentar las prácticas exitosas de empoderamiento para nuevas áreas.",
                    "Reconocer a supervisores que fomentan la toma de decisiones descentralizada.",
                    "Mantener comunicación abierta sobre límites y responsabilidades."
                ]
            },
            'Organización del trabajo': {
                'ALTO': [
                    "**ACCIÓN URGENTE**: Contratar auditoría externa de procesos para identificar ineficiencias críticas.",
                    "Rediseñar procesos confusos o redundantes mediante talleres participativos con el personal.",
                    "Implementar sistema de gestión documental digital accesible y organizado.",
                    "Clarificar roles y responsabilidades con matrices RACI (Responsable, Aprobador, Consultado, Informado).",
                    "Establecer reuniones semanales de coordinación obligatorias entre áreas interdependientes.",
                    "Actualizar y publicar manuales de procedimientos en formato accesible y entendible."
                ],
                'MEDIO': [
                    "Revisar y actualizar procedimientos operativos estándar semestralmente.",
                    "Implementar herramientas colaborativas (Trello, Asana, Monday) para mejorar coordinación.",
                    "Facilitar espacios inter-departamentales para resolver dependencias y mejorar flujos.",
                    "Optimizar canales de comunicación interna eliminando redundancias.",
                    "Capacitar en uso efectivo de herramientas organizacionales."
                ],
                'BAJO': [
                    "**MANTENER**: La organización actual es clara y eficiente. Continuar con estas prácticas.",
                    "Documentar procesos exitosos como estándares para nuevas áreas.",
                    "Compartir mejores prácticas organizacionales en reuniones generales.",
                    "Mantener actualizada la documentación de procesos."
                ]
            },
            'Recuperación': {
                'ALTO': [
                    "**ACCIÓN URGENTE**: Auditar cumplimiento real de horarios, pausas y descansos legales. Sancionar incumplimientos.",
                    "Implementar política de desconexión digital obligatoria fuera de horario (correos, mensajes, llamadas).",
                    "Contratar especialista en ergonomía para revisar espacios de descanso y pausas activas.",
                    "Monitorear y limitar horas extra a casos excepcionales con autorización expresa.",
                    "Crear espacios físicos adecuados y cómodos específicamente para descanso del personal.",
                    "Establecer indicadores de uso de vacaciones y perseguir a quienes no las tomen."
                ],
                'MEDIO': [
                    "Promover activamente campañas de uso completo de vacaciones anuales.",
                    "Mejorar zonas de descanso con mobiliario confortable y amenities básicos.",
                    "Implementar programa de pausas activas con instructor o videos guía.",
                    "Evaluar viabilidad de horarios flexibles o modelos híbridos de trabajo.",
                    "Monitorear cargas que impidan descansos efectivos."
                ],
                'BAJO': [
                    "**MANTENER**: Las políticas de descanso y recuperación están funcionando bien.",
                    "Continuar promoviendo cultura de equilibrio trabajo-descanso.",
                    "Reconocer a supervisores que respetan horarios y descansos del personal.",
                    "Mantener espacios de descanso en buenas condiciones."
                ]
            },
            'Soporte y apoyo': {
                'ALTO': [
                    "**ACCIÓN URGENTE**: Implementar Programa de Asistencia al Empleado (EAP) con servicio psicológico confidencial.",
                    "Contratar facilitador externo para talleres de construcción de equipos y mejora de relaciones.",
                    "Capacitar obligatoriamente a supervisores en escucha activa, empatía y apoyo emocional básico.",
                    "Establecer sistema de 'buddy' donde cada nuevo empleado tenga un compañero asignado de apoyo.",
                    "Crear espacios formales e informales de convivencia para fortalecer vínculos.",
                    "Implementar encuestas anónimas trimestrales sobre clima de apoyo y compañerismo."
                ],
                'MEDIO': [
                    "Promover cultura de colaboración mediante reconocimientos a trabajo en equipo.",
                    "Facilitar actividades de integración periódicas (almuerzos, celebraciones, actividades recreativas).",
                    "Implementar sistema de reconocimiento entre pares para visibilizar apoyos mutuos.",
                    "Ofrecer talleres de comunicación efectiva y resolución de conflictos.",
                    "Crear canales informales de comunicación para fortalecer relaciones."
                ],
                'BAJO': [
                    "**MANTENER**: El clima de apoyo y colaboración es positivo. Continuar fomentándolo.",
                    "Reconocer y celebrar públicamente ejemplos de trabajo en equipo exitoso.",
                    "Documentar y compartir prácticas que fomentan el apoyo mutuo.",
                    "Mantener espacios de convivencia y fortalecimiento de vínculos."
                ]
            },
            'Acoso discriminatorio': {
                'ALTO': [
                    "**ACCIÓN URGENTE Y LEGAL**: Implementar protocolo escrito de prevención y sanción del acoso discriminatorio INMEDIATAMENTE.",
                    "Investigar exhaustivamente cualquier denuncia con seriedad y garantizar confidencialidad y protección a denunciantes.",
                    "Capacitación obligatoria certificada para TODO el personal en diversidad, inclusión y no discriminación.",
                    "Establecer sanciones disciplinarias severas (hasta despido justificado) para conductas discriminatorias probadas.",
                    "Crear Comité de Ética y Convivencia con representación diversa y poder de decisión.",
                    "Contratar asesoría legal externa especializada en derechos laborales y antidiscriminación.",
                    "Publicar política de cero tolerancia visible en toda la empresa."
                ],
                'MEDIO': [
                    "Reforzar comunicación constante sobre política de cero tolerancia a discriminación.",
                    "Ofrecer capacitación semestral obligatoria en respeto, diversidad e inclusión.",
                    "Establecer canales múltiples (buzón, correo, presencial) y anónimos para reportar incidentes.",
                    "Promover campaña visible de cultura organizacional inclusiva y diversa.",
                    "Monitorear clima laboral con enfoque específico en percepción de discriminación."
                ],
                'BAJO': [
                    "**MANTENER**: El ambiente inclusivo actual debe preservarse. Continuar con políticas de respeto.",
                    "Reconocer públicamente el compromiso organizacional con la no discriminación.",
                    "Mantener capacitaciones preventivas anuales.",
                    "Celebrar la diversidad del equipo de forma visible."
                ]
            },
            'Acoso laboral': {
                'ALTO': [
                    "**ACCIÓN URGENTE Y LEGAL**: Activar protocolo de intervención inmediata. Investigar denuncias con seriedad absoluta.",
                    "Realizar auditoría profunda del clima laboral con enfoque en hostigamiento y maltrato.",
                    "Implementar múltiples canales anónimos de denuncia con seguimiento garantizado y plazos definidos.",
                    "Capacitar obligatoriamente a TODO el personal en prevención del acoso laboral y mobbing.",
                    "Establecer consecuencias disciplinarias ejemplares (suspensión, despido) para acosadores identificados.",
                    "Ofrecer apoyo psicológico profesional gratuito a víctimas de acoso.",
                    "Contratar auditoría externa independiente para evaluar situación real."
                ],
                'MEDIO': [
                    "Fortalecer y comunicar ampliamente políticas de convivencia laboral respetuosa.",
                    "Capacitar a líderes en detección temprana de señales de acoso y cómo intervenir.",
                    "Promover cultura de comunicación asertiva y resolución constructiva de conflictos.",
                    "Realizar campañas trimestrales de sensibilización sobre acoso laboral.",
                    "Monitorear indicadores de rotación, ausentismo y clima por área."
                ],
                'BAJO': [
                    "**MANTENER**: El ambiente laboral respetuoso actual debe preservarse.",
                    "Continuar con políticas de prevención y mantener canales de denuncia activos.",
                    "Reconocer las buenas prácticas de convivencia respetuosa.",
                    "Mantener capacitación preventiva anual."
                ]
            },
            'Acoso sexual': {
                'ALTO': [
                    "**ACCIÓN URGENTE Y LEGAL CRÍTICA**: Implementar protocolo específico de prevención y atención del acoso sexual HOY.",
                    "Capacitación obligatoria y certificada para TODO el personal sobre consentimiento, límites y conductas inapropiadas.",
                    "Garantizar confidencialidad ABSOLUTA y protección contra represalias para denunciantes.",
                    "Establecer sanciones disciplinarias SEVERAS incluyendo despido inmediato para casos probados.",
                    "Contratar consultoría externa especializada en prevención y atención del acoso sexual.",
                    "Crear espacios físicos seguros y múltiples mecanismos de denuncia accesibles 24/7.",
                    "Documentar todas las acciones tomadas y mantener registro para auditorías legales.",
                    "Revisar y eliminar cualquier política o práctica que normalice conductas inapropiadas."
                ],
                'MEDIO': [
                    "Reforzar continuamente política de cero tolerancia mediante comunicación constante.",
                    "Capacitar específicamente sobre límites profesionales, lenguaje apropiado y respeto corporal.",
                    "Promover cultura organizacional de respeto integral y profesionalismo.",
                    "Establecer protocolos claros de actuación ante sospechas o reportes.",
                    "Monitorear clima laboral con preguntas específicas sobre seguridad y respeto."
                ],
                'BAJO': [
                    "**MANTENER**: El ambiente laboral profesional y respetuoso debe preservarse activamente.",
                    "Continuar con cultura de respeto y políticas preventivas.",
                    "Reconocer el ambiente laboral seguro y profesional logrado.",
                    "Mantener capacitaciones anuales preventivas."
                ]
            },
            'Adicción al trabajo': {
                'ALTO': [
                    "**ACCIÓN URGENTE**: Implementar políticas corporativas estrictas contra presentismo y glorificación del exceso de trabajo.",
                    "Establecer límites tecnológicos (bloqueo de correos/sistemas fuera de horario) y culturales de disponibilidad.",
                    "Auditar cargas de trabajo reales vs. planeadas para identificar origen del exceso.",
                    "Promover activamente uso obligatorio de vacaciones y días de descanso sin penalización implícita.",
                    "Ofrecer programa de equilibrio vida-trabajo con apoyo psicológico especializado.",
                    "Capacitar y responsabilizar a supervisores que fomentan o normalizan el exceso de trabajo.",
                    "Reconocer y premiar EFICIENCIA sobre horas trabajadas."
                ],
                'MEDIO': [
                    "Promover cultura organizacional que valore eficiencia y resultados sobre horas presenciales.",
                    "Implementar desconexión digital obligatoria con sanciones para quienes incumplan.",
                    "Ofrecer talleres sobre gestión del tiempo, priorización y delegación efectiva.",
                    "Evaluar si cargas de trabajo son realistas y ajustarlas si es necesario.",
                    "Visibilizar casos de éxito de balance trabajo-vida personal."
                ],
                'BAJO': [
                    "**MANTENER**: El equilibrio trabajo-vida personal es saludable. Continuar promociéndolo.",
                    "Reconocer y premiar explícitamente la desconexión laboral saludable.",
                    "Documentar y compartir buenas prácticas de balance.",
                    "Mantener políticas de desconexión vigentes."
                ]
            },
            'Condiciones del trabajo': {
                'ALTO': [
                    "**ACCIÓN URGENTE Y LEGAL**: Contratar auditoría profesional de seguridad y salud ocupacional INMEDIATAMENTE.",
                    "Invertir presupuesto urgente en mejoras de infraestructura, equipamiento y condiciones físicas.",
                    "Garantizar cumplimiento ESTRICTO de todas las normativas de seguridad laboral vigentes.",
                    "Proveer equipos de protección personal adecuados y de calidad sin costo para empleados.",
                    "Activar Comité de Seguridad y Salud Ocupacional con reuniones mensuales obligatorias.",
                    "Contratar asesoría técnica externa para identificar, evaluar y mitigar riesgos ocupacionales.",
                    "Establecer plan de mejoras con cronograma y presupuesto asignado.",
                    "Documentar todas las acciones para cumplimiento legal y auditorías."
                ],
                'MEDIO': [
                    "Realizar inspecciones trimestrales programadas de condiciones laborales.",
                    "Actualizar y mantener equipos, herramientas y mobiliario de trabajo.",
                    "Capacitar regularmente en uso correcto de equipos y medidas de seguridad.",
                    "Mejorar ergonomía de puestos de trabajo (sillas, iluminación, ventilación).",
                    "Implementar sistema de reporte de condiciones inseguras con respuesta rápida."
                ],
                'BAJO': [
                    "**MANTENER**: Las condiciones físicas actuales son adecuadas. Continuar con mantenimiento.",
                    "Mantener programa de mantenimiento preventivo de instalaciones y equipos.",
                    "Reconocer y comunicar el compromiso con la seguridad y salud laboral.",
                    "Continuar cumpliendo normativas de seguridad."
                ]
            },
            'Doble presencia (laboral-familiar)': {
                'ALTO': [
                    "**ACCIÓN URGENTE**: Implementar políticas de flexibilidad horaria real y efectiva INMEDIATAMENTE.",
                    "Establecer opciones formales de teletrabajo o trabajo híbrido con criterios claros.",
                    "Crear programa de apoyo para cuidado de dependientes (niños, adultos mayores, personas con discapacidad).",
                    "Ofrecer permisos especiales pagados para emergencias o responsabilidades familiares críticas.",
                    "Revisar cargas laborales que sistemáticamente interfieren con responsabilidades familiares.",
                    "Promover activamente cultura organizacional que valore y respete la vida personal y familiar.",
                    "Establecer convenios con guarderías, centros de cuidado o subsidios para apoyo familiar."
                ],
                'MEDIO': [
                    "Ampliar opciones de flexibilidad horaria (entrada/salida flexible dentro de rangos).",
                    "Facilitar ajustes temporales de horario para necesidades familiares específicas.",
                    "Ofrecer beneficios orientados a conciliación (días adicionales, horarios reducidos temporales).",
                    "Capacitar a líderes en comprensión y empatía hacia responsabilidades familiares del personal.",
                    "Evaluar posibilidad de trabajo remoto parcial o por días específicos."
                ],
                'BAJO': [
                    "**MANTENER**: Las políticas de conciliación actuales están funcionando. Continuar con ellas.",
                    "Reconocer y comunicar el compromiso organizacional con el balance trabajo-familia.",
                    "Mantener flexibilidad y comprensión hacia necesidades familiares.",
                    "Documentar buenas prácticas de conciliación para compartir."
                ]
            },
            'Estabilidad laboral percibida': {
                'ALTO': [
                    "**ACCIÓN URGENTE**: Comunicar de forma transparente, frecuente y honesta sobre situación y perspectivas de la empresa.",
                    "Revisar tipos de contratos y priorizar estabilidad contractual real (indefinidos vs. temporales sin justificación).",
                    "Reducir drásticamente contratación temporal a menos que sea estrictamente necesaria por naturaleza del trabajo.",
                    "Crear y comunicar planes de carrera claros con oportunidades de desarrollo a largo plazo.",
                    "Implementar reuniones trimestrales ALL-HANDS donde se actualice sobre situación empresarial.",
                    "Ofrecer capacitación continua que mejore empleabilidad interna y demuestre inversión en el personal.",
                    "Reconocer y premiar antigüedad y lealtad de forma visible."
                ],
                'MEDIO': [
                    "Mejorar frecuencia y calidad de comunicación organizacional sobre futuro y proyectos.",
                    "Establecer compromisos explícitos y cumplibles con el personal.",
                    "Promover contratación estable sobre temporal cuando sea posible.",
                    "Reconocer y valorar públicamente la permanencia de empleados leales.",
                    "Crear espacios de diálogo sobre inquietudes laborales."
                ],
                'BAJO': [
                    "**MANTENER**: La estabilidad laboral percibida es positiva. Continuar con comunicación transparente.",
                    "Reconocer el compromiso mutuo entre empresa y empleados.",
                    "Mantener políticas de estabilidad y desarrollo a largo plazo.",
                    "Continuar comunicando visión y proyectos futuros."
                ]
            },
            'Salud auto percibida': {
                'ALTO': [
                    "**ACCIÓN URGENTE**: Implementar programa integral de salud ocupacional con recursos específicos asignados.",
                    "Ofrecer chequeos médicos preventivos anuales gratuitos para todo el personal.",
                    "Establecer convenios con centros médicos para atención preferencial y descuentos.",
                    "Crear programa estructurado de prevención de enfermedades laborales específicas del sector.",
                    "Garantizar licencias médicas adecuadas SIN presión explícita o implícita por reintegro prematuro.",
                    "Implementar programa de bienestar integral (físico, mental, nutricional) con profesionales especializados.",
                    "Evaluar factores laborales que puedan estar afectando la salud y mitigarlos.",
                    "Ofrecer subsidio o reembolso parcial para gastos médicos no cubiertos por seguro."
                ],
                'MEDIO': [
                    "Promover hábitos saludables con campañas educativas sobre nutrición, ejercicio y prevención.",
                    "Ofrecer pausas activas estructuradas y facilitar acceso a actividades deportivas.",
                    "Facilitar acceso a servicios de salud preventiva (vacunación, chequeos básicos).",
                    "Crear campañas periódicas de promoción de la salud (días de la salud, ferias).",
                    "Mejorar condiciones que impactan salud (ergonomía, iluminación, ventilación)."
                ],
                'BAJO': [
                    "**MANTENER**: Los programas de bienestar y salud actuales están funcionando bien.",
                    "Continuar promoviendo estilos de vida saludables.",
                    "Reconocer y comunicar el compromiso con la salud integral del personal.",
                    "Mantener beneficios de salud vigentes."
                ]
            }
        }
        
        # Obtener recomendaciones de la dimensión
        dimension_recs = recommendations.get(dimension_name, {})
        return dimension_recs.get(risk_level, [
            f"Evaluar la situación de '{dimension_name}' con nivel '{risk_level}' y tomar acciones apropiadas."
        ])
    
    def get_general_recommendations_by_level(self, risk_level: str) -> List[str]:
        """
        Obtiene recomendaciones generales para empleadores según el nivel de riesgo predominante
        
        Args:
            risk_level: Nivel de riesgo predominante (BAJO, MEDIO, ALTO)
        
        Returns:
            Lista de recomendaciones generales empresariales
        """
        general_recommendations = {
            'ALTO': [
                "**PRIORIDAD MÁXIMA**: Su empresa presenta niveles de riesgo psicosocial ALTO que requieren intervención inmediata. Esto no solo afecta el bienestar del personal, sino también la productividad y puede generar responsabilidades legales.",
                "Establezca un Comité de Intervención Psicosocial con presupuesto asignado y autoridad para implementar cambios urgentes.",
                "Considere contratar consultoría externa especializada en riesgos psicosociales para obtener perspectiva objetiva y planes de acción profesionales.",
                "Implemente un sistema de seguimiento mensual de indicadores clave (ausentismo, rotación, productividad, clima) para medir impacto de las intervenciones.",
                "Comunique abiertamente al personal las acciones que se están tomando. La transparencia generará confianza y colaboración.",
                "Priorice las dimensiones con mayor riesgo según los resultados específicos de sus evaluaciones.",
                "Asegure cumplimiento legal estricto de normativas laborales, de seguridad y salud ocupacional para evitar sanciones."
            ],
            'MEDIO': [
                "Su empresa presenta niveles de riesgo MEDIO que, si bien no son críticos, requieren atención proactiva para evitar escalamiento.",
                "Implemente plan de mejora continua con objetivos trimestrales específicos y medibles para reducir riesgos identificados.",
                "Fortalezca los canales de comunicación bidireccional entre gerencia y personal para detectar problemas tempranamente.",
                "Invierta en capacitación de mandos medios y supervisores, ya que el liderazgo efectivo es clave para gestionar riesgos psicosociales.",
                "Evalúe periódicamente (semestral o anualmente) para monitorear evolución y efectividad de acciones implementadas.",
                "Reconozca y refuerce las áreas o equipos con bajo riesgo para mantener buenas prácticas.",
                "Considere implementar programas de bienestar integral (físico, mental, social) como inversión preventiva."
            ],
            'BAJO': [
                "**FELICITACIONES**: Su empresa presenta niveles de riesgo psicosocial BAJO, lo cual indica un ambiente laboral saludable y condiciones favorables.",
                "Mantenga las prácticas actuales que han generado estos resultados positivos. Documente y sistematice las buenas prácticas para preservarlas.",
                "No baje la guardia: continúe evaluando periódicamente para detectar cambios tempranamente antes de que escalen.",
                "Considere ser referente en su sector compartiendo sus mejores prácticas con cámaras empresariales o asociaciones.",
                "Reconozca públicamente a los líderes y equipos que han contribuido a este ambiente laboral positivo.",
                "Invierta en mantener y mejorar continuamente las condiciones laborales como estrategia de atracción y retención de talento.",
                "Monitoree dimensiones específicas que, aunque en nivel bajo, puedan tener oportunidades de mejora marginal."
            ]
        }
        
        return general_recommendations.get(risk_level, [
            "Evalúe los resultados específicos de su empresa y tome acciones apropiadas según los niveles de riesgo identificados."
        ])

