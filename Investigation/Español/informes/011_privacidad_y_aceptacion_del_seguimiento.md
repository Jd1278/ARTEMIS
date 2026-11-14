# Privacidad y aceptación del seguimiento físico y psicológico

**Informe:** 011 · **Fecha:** 14 de noviembre de 2026 · **Versión:** 1.0  
**Investigación secuencial:** 7 de 7. **Estado:** investigación documental y diseño de evaluación concluidos; aceptación humana y cumplimiento integral no validados.

## Pregunta y conclusión

¿Cómo apoyar bienestar sin convertir el registro en vigilancia invasiva? La propuesta debe minimizar información, explicar finalidad y destinatarios, permitir un tratamiento diferenciado de datos sensibles y comprobar aceptación con usuarios. El consentimiento escrito no demuestra por sí solo confianza o comodidad; una política de acceso tampoco demuestra que se aplique correctamente.

La investigación comenzó después del cierre del informe 010. Se consultaron fuentes de operaciones médicas, protección de datos y seguridad técnica y se contrastaron con el alcance ficticio de la demo. No se recogieron respuestas emocionales reales ni datos personales de salud. Este documento no acredita cumplimiento jurídico ni determina una clasificación regulatoria del producto.

## Fundamento y fuentes

NASA contempla comunicaciones médicas y psicológicas privadas dentro de las operaciones. Eso respalda separar intimidad y coordinación operativa; no implica que todo dato de un tripulante deba mostrarse a todo el equipo. [NASA Medical Operations](https://www.nasa.gov/reference/6-0-medical-operations/).

En Colombia, la Ley 1581 incluye datos de salud entre los sensibles y establece reglas especiales para su tratamiento. Para una investigación que recolecte información real, el equipo debe determinar finalidad, responsables, autorización o fundamento aplicable y derechos, con su institución. No se presume una excepción por llamarse hackathon o por usar un alias. [Ley 1581 de 2012, compilación oficial](https://normograma.dian.gov.co/dian/compilacion/docs/ley_1581_2012.htm), [SIC, tratamiento de datos sensibles de salud](https://sedeelectronica.sic.gov.co/publicaciones/boletin-juridico/concepto/tratamiento-de-datos-sensibles-relativos-la-salud). La aplicación de otras jurisdicciones, transferencias y procedimientos institucionales no se resolvió en esta revisión.

OWASP recomienda mínimo privilegio, denegación por defecto y control de autorización por petición. Es una guía de implementación, no una certificación del proyecto. [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html).

Supabase documenta RLS como mecanismo de control de acceso a filas. Las claves o roles privilegiados pueden cambiar las garantías; una configuración escrita requiere pruebas con identidades apropiadas. [Supabase RLS](https://supabase.com/docs/guides/database/postgres/row-level-security).

## Separar los contextos de datos

| Contexto | Información propuesta | Tratamiento recomendado |
| --- | --- | --- |
| Demo pública | Perfiles y valores ficticios. | Impedir invitaciones a introducir expedientes reales; identificar simulación. |
| Prueba de interfaz | Código de participante, tareas, tiempos y errores sobre escenarios ficticios. | Evitar nombres, diagnósticos y preguntas sobre salud personal; consentimiento y retención definidos. |
| Investigación científica pública | Archivos de origen y datos desidentificados según términos. | Conservar atribución; no intentar identificar personas ni unir fuentes para hacerlo. |
| Uso futuro con personas reales | Mediciones y autoinformes potencialmente sensibles. | Gobernanza, autorización, acceso, conservación y evaluación institucional antes de recolectar. |

Un alias es seudonimización si alguien puede vincularlo con una persona; no debe anunciarse anonimato garantizado. En equipos pequeños también pueden identificar las fechas, roles y patrones. Publicar datos sensibles en un repositorio crea exposición e historial que no se revierte simplemente borrando una fila.

## Matriz de acceso propuesta

- **Persona:** acceso a su historial y explicación de finalidad y destinatarios.
- **Profesional autorizado:** acceso a lo necesario para la finalidad acordada, con trazabilidad.
- **Equipo de misión:** información operativa pertinente bajo protocolo; no ranking público de ánimo o estrés.
- **Investigador:** datos apropiados para el estudio y bajo sus condiciones; evitar acceso ilimitado por conveniencia.
- **Administrador técnico:** permisos mínimos y separación de funciones; no justificar lectura clínica general por administrar infraestructura.

Es un diseño futuro. En el esquema actual, el rol backend accede a datos de demo y no hay flujo completo de usuarios implementado. La separación `demo/research` no equivale a aislamiento entre usuarios reales. No se ha probado seguridad ni autorización integral.

## Aceptación psicológica como hipótesis

Se propone contrastar si explicar finalidad, permitir omitir preguntas y definir quién ve las respuestas mejora la aceptación. No se ha medido ese efecto. Evitar recompensas por reportar bajo estrés, sanciones por cansancio o presión para contestar «bien»: podrían distorsionar el registro. Esta es una recomendación de diseño, no un resultado experimental propio.

Las entrevistas de aceptación deben preguntar por escenarios: qué compartiría con un profesional, qué con compañeros, qué preferiría omitir y qué información necesita antes de decidir. Registrar razones y diferencias por rol. No pedir que la persona revele experiencias psicológicas para opinar sobre la interfaz.

## Consentimiento y gestión preparados

Antes de una sesión, el equipo debe concretar responsable/contacto institucional, finalidad, datos registrados, almacenamiento, personas con acceso, plazo de conservación y procedimiento de retirada o consulta. La grabación, si se plantea, requiere una decisión separada y explicación clara; por defecto puede hacerse una prueba sin grabar ni recoger salud real.

No se fija un plazo arbitrario de conservación como si fuera una obligación legal. Definirlo según finalidad y revisión institucional; documentar destrucción o anonimización cuando proceda. Una evaluación clínica o de salud sensible requiere que la institución determine la revisión ética aplicable.

## Cierre de la serie

La investigación documental y la propuesta de privacidad están cerradas. Quedan pendientes implementación, pruebas de permisos, revisión institucional y aceptación con personas. Con esto termina la séptima investigación en el orden solicitado. La siguiente tarea es el guion comercial, usando como hechos únicamente evidencia documentada y resultados realmente ejecutados.
