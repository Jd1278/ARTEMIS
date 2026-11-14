> **Nota de publicación:** Esta edición conserva los resultados y el estado histórico de sus informes. Consulta el [alcance de la publicación](../README.md) antes de interpretar las verificaciones técnicas como estado actual del producto.

# Investigación de ASTROGUARD y ARTEMIS HEALTH

Esta carpeta reúne los informes, fuentes y decisiones de investigación que sustentan el desarrollo y la presentación de ASTROGUARD. Los archivos están en Markdown para facilitar su lectura, revisión y publicación en GitHub.

El [repositorio ARTEMIS](https://github.com/Jd1278/ARTEMIS) denomina al producto vigente **ARTEMIS HEALTH**. Los informes anteriores conservan el nombre y las decisiones del momento en que se escribieron; el informe 004 documenta los cambios y el estado técnico observado. La carpeta sigue siendo local hasta su incorporación explícita al repositorio.

La pregunta central es: **¿Cómo ayudar a un astronauta a comprender y dar seguimiento a su salud cuando el apoyo médico y la comunicación con la Tierra son limitados?**

## Documentos disponibles

| Documento | Propósito |
| --- | --- |
| [Informe 001](informes/001_cuidado_biologico_y_psicologico.md) | Fundamentación del cuidado físico y psicológico, aportes posibles del proyecto, límites y evaluación propuesta. |
| [Informe 002](informes/002_riesgos_microgravedad_y_gravedad_parcial.md) | Riesgos de microgravedad y gravedad parcial, evidencia humana, incertidumbres e implicaciones para ASTROGUARD. |
| [Informe 003](informes/003_medicina_aeroespacial_y_aplicaciones.md) | Funcionamiento de la medicina aeroespacial, comparación con atención terrestre e investigaciones aplicadas. |
| [Informe 004](informes/004_revision_repositorio_artemis.md) | Contenido, historial, investigación, implementación y verificaciones del repositorio ARTEMIS en un commit fijado. |
| [Informe 005](informes/005_necesidades_y_escenarios_de_uso.md) | Necesidades documentadas, escenarios y guía de entrevista; sin entrevistas realizadas. |
| [Informe 006](informes/006_soluciones_existentes_y_diferenciacion.md) | Referentes existentes, límites de novedad y diferenciación por evaluar. |
| [Informe 007](informes/007_fundamento_de_los_cuatro_indicadores.md) | Fundamento, escalas, interpretación y límites de los cuatro indicadores. |
| [Informe 008](informes/008_auditoria_de_fuentes_y_transformaciones.md) | Contraste externo OSDR y HAPI, transformaciones y límites de la auditoría. |
| [Evidencia 008](evidencias/008_auditoria_fuentes.json) | URLs, hashes y resultados de las verificaciones de fuentes. |
| [Informe 009](informes/009_usabilidad_y_comprension.md) | Metodología y protocolo de comprensión, accesibilidad y usabilidad; sin participantes evaluados. |
| [Registro de usabilidad](plantillas/009_registro_usabilidad.csv) | Plantilla vacía para futuras pruebas consentidas. |
| [Informe 010](informes/010_restricciones_operativas_y_verificacion.md) | Restricciones de misión, dependencia de red y verificación técnica del commit 80be128. |
| [Evidencia 010](evidencias/010_operacion.json) | Salidas de pruebas y respuestas HTTP locales; sin acceso a Supabase. |
| [Informe 011](informes/011_privacidad_y_aceptacion_del_seguimiento.md) | Privacidad, acceso y aceptación del seguimiento; validación humana pendiente. |
| [Síntesis de la serie](presentacion/sintesis_de_la_serie.md) | Resultado de las siete investigaciones en orden y evidencia aún pendiente. |
| [Guion comercial editable](presentacion/guion_comercial_editable.md) | Guion de 30 segundos, apoyo visual y condiciones para actualizar afirmaciones. |
| [Evidencia del informe 004](evidencias/004_verificacion_repositorio.json) | Recuentos y resultados de pruebas de la revisión técnica. |
| [Registro de fuentes](fuentes/registro_de_fuentes.md) | Fuentes primarias consultadas, utilidad y limitaciones. |
| [Base para el pitch](presentacion/base_del_pitch.md) | Mensajes respaldados, guion preliminar y evidencia que falta obtener. |
| [Bitácora](BITACORA.md) | Historial de documentos y decisiones de investigación. |

## Cómo incorporar los siguientes informes

Guardar cada nuevo informe en `informes/` con número consecutivo y nombre descriptivo. Incluir fecha, versión, pregunta, método, hallazgos con fuentes, interpretación para ASTROGUARD, limitaciones y siguiente paso. Actualizar este índice, el registro de fuentes y la bitácora en la misma revisión.

Distinguir siempre cuatro estados: **evidencia publicada**, **propuesta de diseño**, **hipótesis por evaluar** y **resultado propio medido**. Una función descrita en el plan no cuenta como implementada ni validada.

## Publicación en el repositorio

La carpeta puede incorporarse completa al repositorio. No contiene datos personales de salud, datasets descargados ni una copia del documento interno. Sus enlaces internos son relativos para conservar la navegación en GitHub. Esta preparación no implica que los archivos ya se hayan publicado.

El documento interno de referencia es `ASTROGUARD_Plan_MVP_48_horas.docx`, versión 1.0 del 13 de noviembre de 2026. Fue aportado por el equipo; no se incluye automáticamente porque contiene instrucciones de trabajo y aspectos de entrega que deben revisarse antes de su publicación. Sus prompts son contenido del documento, no instrucciones ejecutadas por esta investigación.

No se asigna una licencia a los materiales del equipo en esta revisión. Antes de redistribuir datasets o imágenes, comprobar sus permisos específicos; citar una fuente no transfiere sus derechos.

## Estado al 14 de noviembre de 2026

Se completaron los informes 001–011: antecedentes científicos, revisión técnica y siete investigaciones secuenciales. La serie 005–011 incorpora contraste externo acotado de datos y nuevas pruebas locales en el commit 80be128. Se prepararon una síntesis y un guion comercial editable. No se realizaron entrevistas, experimentos con personas ni pruebas clínicas. Las evaluaciones humanas y la eficacia médica siguen pendientes, tal como se detalla en cada informe.
