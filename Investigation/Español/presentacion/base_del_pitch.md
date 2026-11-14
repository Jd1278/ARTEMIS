# Base de investigación para el pitch de ASTROGUARD

**Actualización de estado:** el repositorio usa actualmente el nombre ARTEMIS HEALTH y difiere el modo offline completo. El guion histórico de esta página debe ajustarse al [informe 004](../informes/004_revision_repositorio_artemis.md) antes de presentarse; la versión examinada contiene preparación de datos y un esqueleto de aplicación, no el flujo completo construido.

**Borrador promocional más reciente:** [guion comercial editable v0.1](guion_comercial_editable.md), redactado después de la serie 005–011 y basado en el corte técnico 80be128. Esta página conserva el planteamiento histórico.

**Fecha:** 14 de noviembre de 2026. **Versión:** 1.0. Derivada del [informe 001](../informes/001_cuidado_biologico_y_psicologico.md).

## Mensaje central

ASTROGUARD propone ayudar al astronauta a comprender y dar seguimiento a su salud física y bienestar mediante registros, tendencias y explicaciones, incluso bajo condiciones de comunicación limitada si la arquitectura local se implementa y verifica.

## Cadena del argumento

1. **Contexto documentado:** NASA identifica peligros físicos, psicológicos y operativos del vuelo espacial. [F01](https://www.nasa.gov/hrp/hazards/)
2. **Problema operativo documentado:** los sistemas médicos a bordo afrontan posibles interrupciones de comunicación y recursos limitados. [F02](https://www.nasa.gov/reference/medical-operations-and-clinical-care/)
3. **Necesidad propuesta:** disponer de información personal comprensible y accesible para el seguimiento cotidiano.
4. **Solución propuesta:** reunir mediciones, autoinformes, gráficas y avisos explicados conforme al alcance de 48 horas.
5. **Beneficio por evaluar:** mejorar comprensión y continuidad del registro. La prevención de complicaciones es una aspiración que necesita evidencia clínica.

## Afirmaciones para la presentación

| Formulación defendible | Estado | Evidencia necesaria adicional |
| --- | --- | --- |
| El aislamiento y el confinamiento pueden afectar bienestar y desempeño. | Evidencia de contexto: [F06](https://www.nasa.gov/directorates/esdmd/hhp/behavioral-health-risk/). | No atribuir esos efectos a toda tripulación. |
| El seguimiento del sueño y la fatiga es pertinente para explorar el bienestar. | Evidencia de contexto [F07](https://www.nasa.gov/reference/risk-from-inadequate-sleep-and-irregular-schedules/) e inferencia de diseño. | Selección y revisión de instrumentos. |
| Proponemos reunir registros físicos y autoinformes en una interfaz. | Alcance de producto. | Capturas y demostración antes de decir «lo hace». |
| La aplicación funciona sin internet externo. | Pendiente de prueba. | Arquitectura, condiciones y resultado de desconexión documentados. |
| El panel facilita comprender los datos. | Hipótesis. | Prueba de comprensión con usuarios. |
| ASTROGUARD previene enfermedades o reduce el estrés. | No respaldado para el producto. | Estudios específicos; no utilizar como resultado de la hackathon. |

## Guion preliminar de aproximadamente un minuto

En una misión espacial, el seguimiento de la salud debe continuar aun cuando el apoyo desde la Tierra esté limitado. NASA estudia riesgos que incluyen cambios físicos, aislamiento y alteraciones del sueño.

Nuestro equipo propone ASTROGUARD: una herramienta para reunir indicadores disponibles y autoinformes de bienestar, mostrar su evolución y explicar cambios en el historial personal.

Para la hackathon, planteamos un prototipo centrado en registrar, consultar y comprender la información, distinguiendo datos públicos de escenarios simulados. El siguiente paso será demostrar ese flujo y evaluar su comprensión y continuidad de uso.

Buscamos apoyar una mayor autonomía de seguimiento. La integración de sensores y la validación especializada permitirán investigar después su utilidad real para el cuidado de astronautas.

## Material que falta antes de cerrar el pitch

- Relación de funciones realmente construidas y pruebas superadas.
- Capturas o video del flujo integrado, con procedencia de los datos visible.
- Revisión de pertinencia por un especialista; no afirmar que ya ocurrió.
- Una prueba breve de comprensión y registro de sus resultados.
- Requisitos vigentes del desafío y duración real del pitch. Las siete diapositivas y el video de 30 segundos aparecen en el documento interno; no se verificaron aquí como reglas actuales del evento.

## Evidencia complementaria sobre gravedad alterada

El [informe 002](../informes/002_riesgos_microgravedad_y_gravedad_parcial.md) permite explicar que huesos, músculos, circulación, visión y equilibrio pueden verse afectados durante el vuelo y las transiciones de gravedad. La microgravedad orbital corresponde a caída libre conjunta, no a desaparición de la atracción gravitatoria. [F12](https://www.nasa.gov/centers-and-facilities/glenn/what-is-microgravity/)

Como ejemplo concreto, Gabel y colaboradores estudiaron 17 astronautas y observaron recuperación incompleta de densidad mineral ósea total de tibia en nueve al año del retorno. Conservar el tamaño de la cohorte y el plazo; no presentar el hallazgo como daño permanente ni como incidencia universal. [F14](https://pmc.ncbi.nlm.nih.gov/articles/PMC9247070/)

El vínculo propuesto con ASTROGUARD es organizar el seguimiento y explicar sus límites. La app no mide huesos, diagnostica alteraciones oculares ni determina aptitud operativa a partir del pulso. Para Luna y Marte, diferenciar expectativas de gravedad parcial de resultados humanos ya observados en órbita. [F18](https://ntrs.nasa.gov/citations/20210019591)

## Medicina aeroespacial como contexto del proyecto

El [informe 003](../informes/003_medicina_aeroespacial_y_aplicaciones.md) explica que la medicina aeroespacial adapta prevención, atención y seguimiento a las exposiciones y restricciones del vuelo. El lugar propuesto de ASTROGUARD es apoyar información e historial dentro de ese proceso, con resultados propios todavía por evaluar.

Los ejemplos de investigación incluyen ecografía guiada, ejercicio en vuelo y gravedad artificial en reposo inclinado. Distinguir estas categorías evita presentar una intervención experimental como atención establecida o como validación del software. Para la presentación puede usarse el argumento: «La medicina aeroespacial necesita continuidad de información antes, durante y después del vuelo; proponemos investigar una herramienta que facilite esa continuidad y su comprensión».

## Transparencia de esta preparación

Se utilizó asistencia de IA para buscar fuentes, organizar la revisión y redactar borradores. No se generaron datos clínicos ni se validó el producto. El equipo debe revisar el contenido y ajustar el guion a la implementación que pueda demostrar.
