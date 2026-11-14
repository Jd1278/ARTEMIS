# Usabilidad y comprensión del seguimiento de salud

**Informe:** 009 · **Fecha:** 14 de noviembre de 2026 · **Versión:** 1.0  
**Investigación secuencial:** 5 de 7. **Estado:** investigación metodológica concluida; pruebas con personas no realizadas.

## Pregunta y conclusión

¿Cómo comprobar que la persona entiende el panel y no confunde una observación descriptiva con un diagnóstico? Hay que observar tareas y explicaciones del usuario, además de medir errores y tiempo. Un diseño atractivo, un test automatizado o una opinión del desarrollador no demuestran comprensión humana.

La investigación comenzó después de cerrar el informe 008. Se consultaron fuentes primarias sobre evaluación y accesibilidad. No se reclutaron participantes ni se simularon respuestas. Se entrega un protocolo y un [registro vacío](../plantillas/009_registro_usabilidad.csv), no resultados de usabilidad.

## Fundamento metodológico

NIST describe evaluación con éxito de tareas, errores, tiempo y observaciones cualitativas para estudiar eficacia, eficiencia y satisfacción. Estos aspectos requieren usuarios, objetivos y contexto definidos. [NIST Usability Testing](https://www.nist.gov/programs-projects/usability-testing).

NASA describe pruebas iterativas con humanos para identificar problemas de operabilidad, carga e interfaces. El protocolo de la hackathon adapta esa lógica como investigación formativa; no es un proceso de certificación aeroespacial. [NASA Systems Engineering Processes](https://www.nasa.gov/reference/3-0-systems-engineering-processes-vol-2/).

WCAG 2.2 aporta criterios verificables de teclado, etiquetas, contraste y comunicación que no dependa solo del color. Superar una selección de controles no equivale a declarar conformidad completa. [W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/).

## Preguntas e hipótesis a evaluar

- ¿Reconoce el usuario qué valores son simulados y cuáles fueron introducidos manualmente?
- ¿Distingue dato faltante de valor cero y dato antiguo de medición actual?
- ¿Entiende que la comparación no es un diagnóstico y que el historial puede ser insuficiente?
- ¿Puede detectar que un registro no se guardó, sin perder el borrador?
- ¿Puede completar el flujo con teclado y en pantalla pequeña?

Las hipótesis son que procedencia visible y explicaciones reducen confusión y que un formulario breve limita carga. No se consideran confirmadas.

## Protocolo formativo listo para ejecutar

**Población:** invitar primero a usuarios adultos del contexto disponible y, por separado, a personal con experiencia médica o de operaciones. Un piloto propuesto de cinco a ocho personas sirve para encontrar problemas, no para estimar desempeño poblacional ni representar astronautas. Etiquetar experiencia y contexto sin recoger nombres o datos médicos.

**Condiciones:** consentimiento, posibilidad de retirar participación, escenarios ficticios y una versión fija de la interfaz. No inducir privación de sueño, estrés ni exposición física. Si solo hay maqueta, evaluar comprensión de esa maqueta y no persistencia del producto.

**Sesión:** explicar que se evalúa la herramienta, no al participante; dar una tarea sin señalar el control; observar; registrar ayudas; preguntar después qué entendió. Un moderador que explica el significado durante la tarea cambia la medición y debe dejarlo anotado.

| Tarea | Evidencia esperada | Error que importa |
| --- | --- | --- |
| T1. Identificar el último dato y su procedencia. | Valor, unidad, fecha y origen correctos. | Atribuir dato sintético a un astronauta real. |
| T2. Registrar un ejemplo ficticio. | Unidad y escala correctas; confirmar guardado solo si procede. | Entender «enviado» como «guardado» ante fallo. |
| T3. Leer una serie con huecos. | Explicar ausencia sin convertirla en cero o normalidad. | Interpretar falta de datos como buena salud. |
| T4. Interpretar comparación. | Reconocer referencia, periodo y carácter descriptivo. | Diagnóstico o certeza de seguridad atribuida al aviso. |
| T5. Cambiar perfil y origen. | Distinguir historiales y simulación de autoinforme. | Mezclar personas o fuentes. |
| T6. Recuperarse de fallo de conexión simulado. | Reconocer NO GUARDADO y recuperar borrador. | Creer que hay persistencia offline ya implementada. |

## Métricas y criterios propuestos

Registrar éxito sin ayuda, éxito con ayuda o fallo; tiempo por tarea; número y tipo de ayudas; errores; explicación textual; y facilidad percibida mediante una pregunta propia identificada como no validada. No etiquetar esa pregunta como SUS o NASA-TLX.

El objetivo inicial del proyecto puede conservarse como criterio de ingeniería: encontrar información principal en máximo dos pantallas. Cualquier tiempo objetivo se fija antes del estudio. Registrar denominadores, abandonos y tareas no ejecutables; no sustituir datos ausentes por cero.

Un error de interpretación médica o guardado debe investigarse antes de la demo. El promedio favorable de otras tareas no lo compensa. Para una muestra pequeña, informar frecuencias y casos concretos; no generalizar porcentajes de satisfacción a todos los astronautas.

## Revisión de accesibilidad preparada

Verificar navegación y foco de teclado, nombres de controles, errores asociados a campos, texto junto a estados, tabla equivalente a gráficas, zoom y adaptación a tamaños previstos. El contraste de texto normal tiene como referencia 4,5:1 en WCAG AA, con excepciones y condiciones que deben revisarse en el estándar. Contraste calculado en un token no acredita toda la aplicación.

## Cierre

Está terminado el fundamento, protocolo, tareas y formato de registro. Quedan pendientes una interfaz evaluable, consentimiento y sesiones reales. La frase correcta para la presentación es «preparamos cómo evaluar comprensión y facilidad de uso», no «validamos la experiencia con astronautas». Se continúa con restricciones operativas sin tratar esa validación humana como obtenida.
