# Aportes de ASTROGUARD al seguimiento biológico y psicológico de astronautas

**Informe:** 001  
**Fecha:** 14 de noviembre de 2026  
**Versión:** 1.0  
**Tipo:** revisión documental exploratoria y análisis de implicaciones para el diseño  
**Destino:** fundamentación del proyecto, desarrollo del MVP y preparación del pitch

## Respuesta a la pregunta de investigación

ASTROGUARD podría apoyar el cuidado del astronauta al reunir mediciones y autoinformes, mostrar su evolución, hacer visibles los datos faltantes y facilitar el seguimiento de rutinas aprobadas. La investigación permite escoger indicadores pertinentes y definir qué información necesita el usuario para comprender un cambio. Esta contribución es organizativa, educativa y de seguimiento; su efecto sobre salud, prevención o desempeño todavía debe evaluarse.

La pregunta central es: **¿Cómo ayudar a un astronauta a comprender y dar seguimiento a su salud cuando el apoyo médico y la comunicación con la Tierra son limitados?**

La propuesta se dirige a misiones individuales o en equipo. La utilidad en una misión en solitario es una hipótesis de diseño: las fuentes revisadas no demuestran que el producto pueda compensar la ausencia de asistencia de otro tripulante.

## Método y alcance de la revisión

Se tomó como referencia interna el documento `ASTROGUARD_Plan_MVP_48_horas.docx`, versión 1.0 del 13 de noviembre de 2026, especialmente el anexo que prioriza un MVP de 48 horas. Las instrucciones de programación incluidas en ese archivo se trataron como contenido documental.

Se consultaron páginas primarias de NASA y fichas oficiales de datasets. La búsqueda se centró en riesgos humanos del vuelo espacial, seguimiento cardiovascular, aptitud física, inmunidad, sueño, salud conductual y restricciones de atención médica. Las fuentes y su fecha de consulta están en el [registro](../fuentes/registro_de_fuentes.md).

Esta revisión no es sistemática ni exhaustiva: no hubo protocolo registrado, evaluación formal de sesgo, metaanálisis, entrevistas ni acceso a expedientes de astronautas. Se priorizaron síntesis oficiales para justificar el alcance de un prototipo. No se revisó código ni se verificaron funciones implementadas. Las conclusiones sobre utilidad de ASTROGUARD son inferencias de diseño, no resultados experimentales.

## Evidencia sobre el problema

NASA agrupa los peligros del vuelo espacial en radiación, aislamiento y confinamiento, distancia de la Tierra, gravedad alterada y entornos cerrados u hostiles. Esto justifica estudiar conjuntamente el contexto físico, psicológico y operativo, sin suponer que una aplicación resuelve esos peligros. [F01](https://www.nasa.gov/hrp/hazards/)

Los sistemas médicos a bordo afrontan restricciones materiales, posibles interrupciones de comunicación y dificultades funcionales asociadas con microgravedad. El seguimiento local tiene así una motivación operativa; una interfaz que funciona sin internet no constituye por sí misma un sistema médico autónomo. [F02](https://www.nasa.gov/reference/medical-operations-and-clinical-care/)

### Cuidado biológico y físico

El entorno espacial puede contribuir a cambios y desacondicionamiento cardiovascular; sus consecuencias dependen de la fase de la misión. Para ASTROGUARD esto respalda conservar mediciones con contexto y evolución individual. No demuestra que una variación de frecuencia cardíaca permita identificar una enfermedad específica. [F03](https://www.nasa.gov/directorates/esdmd/hhp/cv-risk/)

La microgravedad puede afectar huesos, músculos y capacidad cardiorrespiratoria. NASA utiliza ejercicio y evaluaciones físicas como parte de sus contramedidas. El aporte posible de la aplicación es registrar actividades prescritas y facilitar su seguimiento; completar una tarea en pantalla no demuestra conservación de masa muscular o densidad ósea. [F04](https://www.nasa.gov/reference/risk-of-reduced-cardiorespiratory-and-musculoskeletal-fitness/)

También se han documentado alteraciones de la función inmunitaria y reactivación de virus latentes. La propia síntesis de NASA reconoce incertidumbre sobre cómo se traducen esos cambios en susceptibilidad a enfermedad. ASTROGUARD podría organizar síntomas y resultados de laboratorio disponibles, pero no inferir la inmunidad desde el pulso, el sueño o la fatiga. [F05](https://www.nasa.gov/directorates/esdmd/hhp/immune-risk/)

### Cuidado psicológico y conductual

El aislamiento y el confinamiento pueden afectar la cognición, la conducta y el bienestar. NASA también destaca que la selección, el entrenamiento y las contramedidas en la ISS han ayudado a mitigar ese riesgo. La presentación debe evitar describir a todos los astronautas como psicológicamente deteriorados o asumir que lo observado en la ISS se transfiere directamente a exploración lejana. [F06](https://www.nasa.gov/directorates/esdmd/hhp/behavioral-health-risk/)

La carga de trabajo, los horarios irregulares y las perturbaciones del ciclo de luz y oscuridad son relevantes para el sueño y la salud. NASA incorpora tiempo de relajación y autocuidado dentro de las rutinas. Esto fundamenta investigar un registro de descanso y fatiga, subordinado al plan de misión. [F07](https://www.nasa.gov/reference/risk-from-inadequate-sleep-and-irregular-schedules/)

**Interpretación para el proyecto:** observar juntos sueño, fatiga, actividad y mediciones puede ofrecer contexto útil al usuario. No permite atribuir causalidad: una asociación entre poco descanso y una variación del pulso no demuestra que el sueño la haya causado ni establece un diagnóstico.

## Cómo podría ayudar ASTROGUARD

La siguiente matriz traduce evidencia en propuestas. Ninguna fila afirma eficacia clínica del producto.

| Necesidad | Propuesta de apoyo | Información necesaria | Límite de interpretación |
| --- | --- | --- | --- |
| Seguimiento fisiológico | Mostrar valores y tendencias personales. | Medición, unidad, hora, fuente, calidad y contexto de actividad. | Un valor estable no descarta enfermedad; un cambio no la confirma. |
| Continuidad del registro | Conservar y consultar información localmente. | Persistencia comprobada y estado real de conectividad. | Una demo local con servidor activo no equivale a operar en cualquier dispositivo sin red. |
| Descanso y recuperación | Registrar sueño percibido y fatiga; mostrar su evolución. | Autoinformes voluntarios y, en el futuro, mediciones apropiadas. | Un autoinforme no equivale a polisomnografía ni mide etapas del sueño. |
| Bienestar emocional | Facilitar un chequeo breve de ánimo y estrés percibido. | Escalas definidas, opción de omitir y consentimiento. | Una escala propia de demo no es un instrumento clínico validado. |
| Rutinas de cuidado | Recordar actividades aprobadas y registrar su realización. | Plan de misión y estados completada, omitida o pospuesta. | No prescribir ejercicio o tratamiento automáticamente. |
| Comprensión | Explicar qué representa cada indicador y qué no permite concluir. | Contenido revisado y fuentes accesibles. | Evitar certeza falsa o recomendaciones médicas generadas sin revisión. |
| Seguimiento profesional futuro | Preparar un resumen para compartir cuando exista comunicación. | Permisos, seguridad y procedencia de los registros. | Exportación y sincronización no sustituyen atención médica. |

El beneficio inmediato por demostrar sería que el astronauta pueda encontrar y entender su información con menos dificultad. La reducción de carga de trabajo, el mejor cumplimiento de rutinas y la identificación más oportuna de cambios son hipótesis que necesitan evaluación.

## Salvaguardas de diseño para el bienestar

Estas son recomendaciones del análisis, no prestaciones verificadas:

- Permitir omitir preguntas sensibles y separar los datos personales de bienestar de los resúmenes compartidos.
- Evitar clasificaciones de tripulantes por estado emocional y recompensas por reportarse siempre bien. No penalizar fatiga, síntomas o descanso.
- Mostrar avisos con explicación, antigüedad y calidad del dato. Un estado sin mediciones debe decir «sin datos», no «salud normal».
- Controlar repetición y prioridad de avisos para evaluar si producen confusión o sobrecarga.
- Ante un reporte preocupante, remitir al protocolo de misión y al apoyo disponible. El prototipo no debe improvisar una terapia ni sustituir un canal de ayuda.
- Para misiones en equipo, diseñar permisos individuales. Para uso en solitario, no presentar la aplicación como sustituto de asistencia humana.

El historial individual es una referencia descriptiva, no una garantía de seguridad: una condición persistente puede formar parte de ese historial. Cualquier uso operativo de reglas requiere revisión profesional y protocolos específicos.

## Aporte concreto de esta investigación al desarrollo

La revisión ayuda a limitar el MVP a funciones justificables y comprobables: registro de mediciones, autoinforme de bienestar, historial, gráfica, explicación de cambios y fichas educativas. El plan de 48 horas propone esas funciones; esta revisión no confirma su implementación. Rutinas y gamificación siguen como ampliaciones si el flujo principal está estable.

Para cada indicador, el catálogo debería documentar definición, método de obtención, unidad, fuente y limitaciones. La frecuencia cardíaca se expresa en latidos por minuto; el sueño autoinformado en horas o minutos; estrés y fatiga requieren una escala cuyo significado quede explícito. SpO₂, presión arterial o temperatura solo deben mostrarse si hay una fuente apropiada. No confundir temperatura cutánea con central ni una señal óptica de pulso con una medición directa de oxigenación.

Cada registro debe distinguir entrada manual, sensor, dataset público y simulación. También conviene conservar el identificador de origen y el tiempo relativo cuando un archivo no tenga una fecha real utilizable. No asignar registros públicos de personas diferentes al mismo astronauta ficticio sin señalar que se trata de una composición de demostración.

### Datos útiles como herramientas de investigación

| Fuente | Uso pertinente | Lo que no demuestra |
| --- | --- | --- |
| [BIDMC](https://physionet.org/content/bidmc/1.0.0/) — F08 | Registros de ECG, pulso óptico, respiración y parámetros para probar importación y gráficas. Contiene 53 registros de ocho minutos. | Validez en tripulación sana o vuelo espacial. |
| [PPG-DaLiA](https://archive.ics.uci.edu/dataset/495/ppg+dalia) — F09 | Evaluar estimación de frecuencia cardíaca y efectos del movimiento con datos de 15 participantes. | Comportamiento del sensor en microgravedad. |
| [WESAD](https://archive.ics.uci.edu/dataset/465/wesad+wearable+stress+and+affect+detection) — F10 | Explorar señales fisiológicas y estados experimentales de estrés en 15 personas. | Diagnóstico psicológico o respuesta al aislamiento espacial prolongado. |
| [OSDR](https://science.nasa.gov/reference/osdr-faq/) — F11 | Localizar estudios espaciales y sus metadatos, comprobando organismo y tipo de medición. | Que todos sus archivos sean humanos o signos vitales continuos. |

Para el MVP bastan datos sintéticos identificados y, si el tiempo lo permite, una muestra pública separada. No es necesario entrenar un modelo para fundamentar la propuesta. Los datos simulados verifican comportamiento del software; no validan beneficios médicos.

## Hipótesis y evaluación propuesta

Las siguientes pruebas son futuras; no se han ejecutado en esta revisión.

| Hipótesis | Prueba propuesta | Resultado que debe registrarse |
| --- | --- | --- |
| El panel ayuda a comprender registros. | Pedir a usuarios que identifiquen valor, tendencia, dato faltante y significado de un aviso. | Aciertos, tiempo y confusiones. El objetivo de 30 segundos del plan es un criterio de diseño, no un resultado obtenido. |
| El chequeo de bienestar es aceptable. | Probar comprensión, tiempo de respuesta y comodidad con las preguntas. | Omisiones, carga percibida y comentarios; sin inferir mejoría psicológica. |
| El registro continúa sin internet externo. | Guardar, cerrar y volver a consultar bajo la arquitectura elegida. | Persistencia, pérdidas, duplicados y condiciones exactas de desconexión. |
| Los avisos descriptivos son comprensibles. | Usar escenarios con cambios, datos antiguos y ruido; pedir interpretación al usuario. | Avisos esperados, avisos incorrectos y confusión entre observación y diagnóstico. |
| La propuesta tiene pertinencia aeroespacial. | Revisión con un especialista en medicina aeroespacial o factores humanos. | Correcciones, límites de uso y decisiones documentadas. |

Los estudios con personas y datos sensibles requieren definir consentimiento, tratamiento de datos y la revisión ética aplicable antes de recolectarlos. Una prueba de interfaz con voluntarios no valida eficacia en astronautas. Si se evalúan modelos, separar participantes y controlar la dependencia temporal entre muestras.

## Escenario ilustrativo para la demostración

Una astronauta ficticia registra varios días de menor descanso y mayor fatiga percibida. El panel muestra ambas tendencias y conserva el contexto de sus mediciones. Un aviso explica qué cambió respecto de su historial, sin adjudicar una enfermedad ni afirmar la causa. La usuaria puede revisar la información educativa y el seguimiento previsto por el plan de misión.

Todos los registros de esta escena serían sintéticos. El escenario demuestra organización de información; no representa un caso real ni prueba que se evitó un problema de salud.

## Conclusiones para el pitch

La investigación justifica explorar una herramienta que reúna seguimiento físico y bienestar, conserve procedencia y facilite la consulta local. El valor diferencial propuesto está en esa combinación y en explicar los límites de cada dato. No se ha realizado una comparación exhaustiva con productos existentes; no corresponde afirmar que ASTROGUARD sea el primero o único.

Una formulación defendible es: **«ASTROGUARD propone apoyar la autonomía del astronauta mediante registros de salud, tendencias personales y seguimiento del bienestar, con información comprensible y límites explícitos».**

Para afirmar «mejora la salud», «previene complicaciones» o «reduce el estrés» harán falta estudios con resultados apropiados. La siguiente etapa de investigación debería cerrar la lista de indicadores, revisar el contenido con un especialista y documentar las pruebas del flujo realmente construido. La [base para el pitch](../presentacion/base_del_pitch.md) traduce este informe a mensajes de presentación.
