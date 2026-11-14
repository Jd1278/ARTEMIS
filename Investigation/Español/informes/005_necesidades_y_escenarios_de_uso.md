# Necesidades de seguimiento de salud y escenarios de uso

**Informe:** 005 · **Fecha:** 14 de noviembre de 2026 · **Versión:** 1.0  
**Investigación secuencial:** 1 de 7. **Estado:** revisión documental concluida; contraste con personas pendiente.

## Pregunta y respuesta

¿Qué necesidades del astronauta y del equipo médico justifican ARTEMIS HEALTH? La evidencia respalda investigar continuidad de información, comprensión del estado registrado y apoyo al seguimiento bajo restricciones de misión. No demuestra que la interfaz propuesta ya satisfaga esas necesidades. El producto debe priorizar registros claros, procedencia, antigüedad, contexto y límites de interpretación antes que una puntuación global de salud.

## Método y fuentes

Se consultaron documentación primaria de NASA sobre atención médica y conceptos de apoyo a decisiones, y el manual de integración humana. Se contrastaron con los requisitos de ARTEMIS HEALTH del commit `80be128b17b5046ecd267d5a0604bbc5c74f5444`, posterior al corte del informe 004. El README y los requisitos siguen indicando implementación funcional pendiente. No se entrevistó ni contactó a astronautas, médicos o integrantes del equipo. Los perfiles siguientes son hipótesis de diseño, no testimonios.

- [NASA Clinical Decision Support — Concepts of Operation](https://ntrs.nasa.gov/citations/20205008731): necesidad de autonomía y sistemas de información ante restricciones de tiempo, recursos y evacuación. Es una visión de sistema médico, más amplia que nuestro MVP.
- [NASA Health and Medical Care](https://www.nasa.gov/reference/3-0-health-and-medical-care/): la capacidad médica se adapta a misión, destino y recursos; no hay una única solución universal.
- [NASA Human Integration Design Handbook](https://www.nasa.gov/organizations/ochmo/human-integration-design-handbook/): diseño humano a partir de lecciones y criterios de integración. Su consulta no certifica conformidad.
- [Requisitos del producto fijados](https://github.com/Jd1278/ARTEMIS/blob/80be128b17b5046ecd267d5a0604bbc5c74f5444/artemis-healt/docs/requirements.md): fuente de alcance, no evidencia clínica ni de demanda comercial.

## Usuarios y necesidades propuestas

| Usuario hipotético | Trabajo que busca realizar | Necesidad a contrastar | Consecuencia de diseño |
| --- | --- | --- | --- |
| Tripulante | Registrar y consultar su seguimiento cotidiano. | Saber qué dato existe, de cuándo es y qué significa el cambio. | Entrada breve, historial y explicación con unidades. |
| Responsable médico de tripulación | Organizar información para seguir el protocolo. | Distinguir medición, autoinforme, faltante y simulación. | Procedencia visible y separación de contextos. |
| Profesional en tierra | Revisar información autorizada cuando esté disponible. | Entender secuencia, calidad y condiciones de captura. | Exportación futura trazable; no asumir transmisión implementada. |
| Investigador o evaluador de demo | Explorar datos y comprender límites. | Separar estudios reales de perfiles ficticios. | Espacios demo e investigación distintos. |

La documentación operativa existente no prueba que los usuarios carezcan hoy de herramientas. El problema propuesto es estudiar una experiencia de seguimiento comprensible; no se debe afirmar que los astronautas están sin atención médica.

## Escenarios prioritarios

**Chequeo diario.** Una persona selecciona el perfil ficticio y un día de misión, registra sueño, fatiga y estrés y consulta pulso si hay un dato apropiado. El sistema debe explicar escalas y no convertir autoinformes en mediciones de sensor.

**Consulta de cambio.** La persona observa una diferencia y necesita conocer la referencia, los días utilizados y la calidad. Una variación descriptiva no es una enfermedad. Si no hay suficientes datos compatibles, el resultado útil es «historial insuficiente».

**Fallo de guardado.** La persona intenta registrar mientras falla la conexión a Supabase. La interfaz debe conservar el borrador durante la sesión y mostrar NO GUARDADO. El alcance vigente difiere persistencia offline completa; abrir una página local no resuelve esa dependencia.

**Revisión científica.** Un evaluador consulta un estudio real en una vista separada, sin asignar sus resultados al perfil ficticio. Esa vista es P1, no función probada.

**Uso individual o en equipo.** La consulta individual requiere claridad con mínima carga. El trabajo en equipo añade permisos y responsabilidades; no justifica publicar estados emocionales de compañeros. El desempeño en misión solitaria no ha sido estudiado para este producto.

## Decisiones y criterios derivados

1. Priorizar cuatro indicadores y un flujo pequeño de registro y consulta.
2. Mostrar fecha y fase de misión, origen, unidad y calidad en cada contexto de lectura.
3. Evitar confirmaciones de guardado si no hubo persistencia real.
4. Mantener separados los datos sintéticos, autoinformados y públicos en comparaciones.
5. Presentar fichas educativas con límites y una ruta hacia el protocolo establecido; no recomendaciones clínicas autónomas.

Son requisitos propuestos que necesitan verificación técnica y aceptación del usuario, no beneficios medidos. El valor para el profesional médico seguirá siendo hipotético hasta contrastar qué datos necesita y en qué formato.

## Guía de entrevista preparada

Sesión propuesta de 20–30 minutos, con consentimiento, sin pedir expedientes ni información personal de salud. Comenzar por tareas reales antes de mostrar la solución:

1. ¿Cómo registra y revisa hoy información relevante durante una operación o simulación?
2. ¿Qué información necesita para interpretar una variación y cuál suele faltar?
3. ¿Qué parte del registro consume más esfuerzo o genera confusión?
4. ¿Qué cambia durante una pérdida de comunicación o una transición operativa?
5. ¿Qué datos de bienestar consideraría privados y con quién aceptaría compartirlos?
6. Ante un ejemplo ficticio, ¿qué entiende por dato antiguo, imputado y cambio respecto del historial?
7. ¿Qué tendría que demostrar esta herramienta para resultar útil, y qué le impediría utilizarla?

Registrar observación o cita consentida, rol general, contexto y decisión derivada. Separar opinión de una tarea observada. Una entrevista con personal de un análogo o un estudiante no representa automáticamente a astronautas.

## Cierre y pendientes

La revisión documental y el mapa de necesidades están terminados. Falta validación humana: necesidades prioritarias, frecuencia aceptable de registro, carga percibida y formato de revisión médica. No hay evidencia de adopción, ahorro de tiempo ni disposición de compra. Esta conclusión permite continuar con soluciones existentes sin presentar entrevistas inexistentes como trabajo realizado.
