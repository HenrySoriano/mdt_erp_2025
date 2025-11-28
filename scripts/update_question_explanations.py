"""
Script para actualizar las explicaciones de las preguntas del cuestionario de riesgo psicosocial
"""

import os
import django
import sys
import codecs

# Fix para encoding en Windows
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.infrastructure.models import Question

# Diccionario con explicaciones detalladas para cada pregunta
explanations = {
    1: "Esta pregunta evalúa si la carga de trabajo que recibes de compañeros, usuarios o clientes es razonable y manejable. Ejemplo: Si un compañero te pide ayuda con una tarea urgente, ¿sientes que es algo que puedes hacer sin afectar tu trabajo normal?",
    
    2: "Evalúa tu nivel de autonomía para decidir la velocidad a la que trabajas. Ejemplo: ¿Puedes decidir si trabajar más rápido en la mañana y más tranquilo en la tarde, o alguien más controla constantemente tu ritmo?",
    
    3: "Mide si tus responsabilidades laborales te generan tensión o ansiedad. Ejemplo: ¿Al pensar en tus tareas del día siguiente, te sientes tranquilo o preocupado?",
    
    4: "Evalúa si el tiempo disponible en tu jornada es suficiente para completar tus tareas. Ejemplo: ¿Terminas tu día habiendo completado todo, o constantemente dejas cosas pendientes por falta de tiempo?",
    
    5: "Mide si tus habilidades actuales son adecuadas para tu puesto. Ejemplo: ¿Te sientes preparado para realizar las tareas que te asignan, o frecuentemente sientes que te falta conocimiento?",
    
    6: "Evalúa si existe aprendizaje colaborativo en tu equipo. Ejemplo: ¿Tus compañeros comparten tips, técnicas o conocimientos que te ayudan a mejorar en tu trabajo?",
    
    7: "Mide si la empresa invierte en tu desarrollo profesional. Ejemplo: ¿Te ofrecen cursos, talleres o capacitaciones para mejorar tus habilidades?",
    
    8: "Evalúa si recibes retroalimentación regular sobre tu desempeño. Ejemplo: ¿Tu jefe te dice cómo lo estás haciendo, qué puedes mejorar y qué estás haciendo bien?",
    
    9: "Mide si se reconoce y valora el buen desempeño. Ejemplo: Cuando logras un objetivo importante, ¿tu jefe o la empresa lo reconoce de alguna manera?",
    
    10: "Evalúa la apertura de tu jefe a nuevas ideas. Ejemplo: Si propones una forma diferente de hacer algo, ¿tu jefe lo considera o lo rechaza sin escuchar?",
    
    11: "Mide si los objetivos que te asignan son realistas. Ejemplo: ¿Las fechas límite que te dan son alcanzables, o siempre son demasiado ajustadas?",
    
    12: "Evalúa si tu jefe te apoya cuando tienes sobrecarga de trabajo. Ejemplo: Si tienes demasiadas tareas, ¿tu jefe redistribuye el trabajo o te deja solo?",
    
    13: "Mide la calidad de la comunicación con tu jefe. Ejemplo: ¿Tu jefe te explica claramente qué espera de ti y te da feedback útil?",
    
    14: "Evalúa si las decisiones importantes se toman de forma participativa. Ejemplo: Cuando hay cambios que afectan al equipo, ¿tu jefe consulta la opinión del grupo?",
    
    15: "Mide si existe un espacio seguro para expresar opiniones diferentes. Ejemplo: ¿Puedes decir que no estás de acuerdo con algo sin temor a represalias?",
    
    16: "Evalúa si se fomenta el trabajo en equipo. Ejemplo: ¿Puedes pedir ayuda a otros departamentos cuando la necesitas, o cada área trabaja aislada?",
    
    17: "Mide si tu opinión se considera al establecer plazos. Ejemplo: Cuando te asignan una tarea, ¿te preguntan cuánto tiempo necesitas o simplemente te imponen una fecha?",
    
    18: "Evalúa si puedes aportar ideas de mejora. Ejemplo: Si identificas una forma más eficiente de hacer algo, ¿puedes proponerla y es considerada?",
    
    19: "Mide la efectividad de los canales de comunicación. Ejemplo: ¿La información importante llega clara y a tiempo, o siempre hay confusión?",
    
    20: "Evalúa la transparencia organizacional. Ejemplo: ¿Te informan sobre cómo va la empresa, sus logros y desafíos?",
    
    21: "Mide si se hacen ajustes razonables para personas con discapacidad. Ejemplo: Si alguien tiene limitaciones físicas, ¿se adaptan sus tareas o espacios de trabajo?",
    
    22: "Evalúa si las reuniones son productivas y necesarias. Ejemplo: ¿Las reuniones tienen un propósito claro y ayudan a lograr objetivos, o son pérdida de tiempo?",
    
    23: "Mide la claridad de los objetivos organizacionales. Ejemplo: ¿Sabes exactamente qué se espera lograr en tu área y cómo medirlo?",
    
    24: "Evalúa si siempre tienes trabajo que hacer. Ejemplo: ¿Hay momentos en que no sabes qué hacer porque no hay tareas asignadas?",
    
    25: "Mide el nivel de fatiga al terminar la jornada. Ejemplo: Al salir del trabajo, ¿tienes energía para hacer otras actividades o llegas agotado?",
    
    26: "Evalúa si puedes tomar descansos breves. Ejemplo: ¿Puedes levantarte, estirarte o tomar un café cuando lo necesitas, o debes estar en tu puesto sin parar?",
    
    27: "Mide si tienes tiempo para reflexionar sobre tu trabajo. Ejemplo: ¿Puedes pensar en cómo mejorar tus procesos, o estás siempre apurado sin tiempo para analizar?",
    
    28: "Evalúa si el horario laboral se ajusta a tus necesidades. Ejemplo: ¿El horario te permite cumplir con tus responsabilidades personales y familiares?",
    
    29: "Mide la calidad de tu descanso nocturno. Ejemplo: ¿Duermes bien y despiertas descansado, o el trabajo te genera insomnio o cansancio constante?",
    
    30: "Evalúa si el trabajo promueve la colaboración. Ejemplo: ¿Las tareas están diseñadas para que trabajes con otros y se fomente el diálogo?",
    
    31: "Mide el clima laboral y las relaciones entre colegas. Ejemplo: ¿Te sientes cómodo con tus compañeros, hay buen ambiente y apoyo mutuo?",
    
    32: "Evalúa el apoyo a trabajadores en situaciones especiales. Ejemplo: Si alguien está enfermo o tiene una discapacidad temporal, ¿recibe el apoyo necesario?",
    
    33: "Mide la disponibilidad de soporte técnico y administrativo. Ejemplo: Cuando necesitas ayuda con sistemas, papeleos o recursos, ¿la recibes oportunamente?",
    
    34: "Evalúa el acceso a servicios de bienestar. Ejemplo: ¿Tienes acceso a médico, psicólogo o consejero cuando enfrentas problemas personales o laborales?",
    
    35: "Mide si existe discriminación por edad. Ejemplo: ¿Se trata igual a personas jóvenes y mayores, o hay preferencias o prejuicios por la edad?",
    
    36: "Evalúa si trabajas solo en horario laboral o también fuera de él. Ejemplo: ¿Las metas que te pones a ti mismo las cumples en tu horario, o trabajas en casa o fines de semana?",
    
    37: "Mide la percepción general del ambiente de trabajo. Ejemplo: ¿Disfrutas ir a trabajar y el ambiente es positivo, o hay tensión y conflictos constantes?",
    
    38: "Evalúa la equidad de género en oportunidades. Ejemplo: ¿Hombres y mujeres tienen las mismas posibilidades de ascenso, capacitación y reconocimiento?",
    
    39: "Mide el sentido de pertenencia y valoración. Ejemplo: ¿Sientes que eres parte importante del equipo y que tu trabajo es valorado?",
    
    40: "Evalúa la accesibilidad física para personas con discapacidad. Ejemplo: ¿Hay rampas, baños adaptados y espacios accesibles para personas con movilidad reducida?",
    
    41: "Mide la presencia de acoso laboral (mobbing). Ejemplo: ¿Estás libre de burlas, humillaciones, rumores o intentos de dañar tu reputación de forma repetida?",
    
    42: "Evalúa la seguridad laboral percibida. Ejemplo: A pesar de cambios en la empresa, ¿te sientes seguro de que tu trabajo no está en riesgo?",
    
    43: "Mide la presencia de acoso sexual. Ejemplo: ¿Estás libre de comentarios, insinuaciones o contacto físico de naturaleza sexual no deseado?",
    
    44: "Evalúa el impacto del trabajo en la salud. Ejemplo: ¿Tu trabajo te causa dolores de cabeza, estrés, ansiedad o problemas físicos?",
    
    45: "Mide la capacidad de desconexión laboral. Ejemplo: Cuando no estás trabajando, ¿puedes relajarte y olvidarte del trabajo, o sigues pensando en él?",
    
    46: "Evalúa la interferencia de problemas personales en el trabajo. Ejemplo: ¿Tus problemas familiares o personales afectan tu concentración y rendimiento laboral?",
    
    47: "Mide las condiciones de seguridad física. Ejemplo: ¿Las herramientas, equipos y espacios son seguros y no representan riesgo de accidentes?",
    
    48: "Evalúa la ausencia de acoso sexual en el ambiente laboral. Ejemplo: ¿El ambiente de trabajo está libre de situaciones incómodas de naturaleza sexual?",
    
    49: "Mide la flexibilidad para atender asuntos personales. Ejemplo: Si necesitas resolver algo personal urgente, ¿puedes hacerlo sin problemas?",
    
    50: "Evalúa la presencia de conflictos y rumores. Ejemplo: ¿Tu lugar de trabajo está libre de chismes, rumores maliciosos o conflictos estresantes?",
    
    51: "Mide el equilibrio trabajo-vida personal. Ejemplo: ¿Puedes separar claramente tu tiempo de trabajo de tu tiempo personal y familiar?",
    
    52: "Evalúa el orgullo de pertenencia a la organización. Ejemplo: ¿Te sientes orgulloso de decir dónde trabajas y de lo que hace tu empresa?",
    
    53: "Mide el respeto a la diversidad. Ejemplo: ¿Se respetan todas las creencias, orientaciones sexuales, nacionalidades y opiniones políticas?",
    
    54: "Evalúa el reconocimiento y motivación. Ejemplo: ¿Sientes que tu trabajo es importante y eso te motiva a seguir esforzándote?",
    
    55: "Mide la adicción al trabajo. Ejemplo: Cuando no estás trabajando, ¿te sientes culpable o ansioso por no estar siendo productivo?",
    
    56: "Evalúa la equidad en beneficios y espacios. Ejemplo: ¿Todos tienen acceso a los mismos espacios y beneficios, o hay privilegios para ciertos grupos?",
    
    57: "Mide la capacidad de desconexión mental. Ejemplo: En tu tiempo libre, ¿puedes hacer hobbies y actividades sin pensar en el trabajo?",
    
    58: "Evalúa la autopercepción de salud. Ejemplo: ¿Te sientes bien física y mentalmente, o notas que tu salud se ha deteriorado?"
}

# Actualizar cada pregunta con su explicación
print("Actualizando explicaciones de preguntas...")
updated_count = 0

for number, explanation in explanations.items():
    try:
        question = Question.objects.get(number=number)
        question.explanation = explanation
        question.save()
        updated_count += 1
        print(f"[OK] Pregunta {number} actualizada")
    except Question.DoesNotExist:
        print(f"[ERROR] Pregunta {number} no encontrada")

print(f"\n[COMPLETADO] Total de preguntas actualizadas: {updated_count}/58")
