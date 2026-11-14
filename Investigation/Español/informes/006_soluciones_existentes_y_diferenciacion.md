# Soluciones existentes y diferenciación propuesta de ARTEMIS HEALTH

**Informe:** 006 · **Fecha:** 14 de noviembre de 2026 · **Versión:** 1.0  
**Investigación secuencial:** 2 de 7. **Estado:** comparación documental concluida.

## Pregunta y conclusión

¿Qué existe y qué puede aportar el proyecto? Ya hay soluciones de registro y apoyo a la salud de astronautas. **No es defendible presentar ARTEMIS HEALTH como el primer sistema que reúne datos de salud espacial.** El posicionamiento propuesto es un prototipo académico de seguimiento comprensible, trazabilidad y demostración reproducible para cuatro indicadores. Es una propuesta por evaluar, no una ventaja competitiva demostrada.

La investigación comenzó después del cierre documental del informe 005. Se buscaron fuentes de agencias y desarrolladores y una publicación científica. No se probaron los sistemas comparados, ni se solicitaron presupuestos, acceso o entrevistas. Ausencia de una función en una descripción pública significa «no comprobada», no «inexistente».

## Comparación de referentes

| Referente | Función documentada | Relación con ARTEMIS HEALTH | Madurez y límite |
| --- | --- | --- | --- |
| EveryWear, CNES/MEDES/ESA | Registro de información médica y científica en tablet, cuestionarios y comunicación privada; integración de dispositivos. | Es el referente funcional más cercano. La idea de unificar el registro ya existe. | Uso en misiones descrito por sus responsables; no se auditó el producto. |
| SpaceWear, descrito por ESA | Adquisición de datos mediante un monitor corporal. | Referente de instrumentación; una interfaz de seguimiento necesita distinguirse de un sensor. | Investigación y uso documentados en contexto orbital; no se verificaron prestaciones comerciales actuales. |
| Agentes de apoyo médico para exploración, Buras y Hilmers, 2025 | Concepto de agentes que apoyen al responsable médico cuando no hay consulta terrestre disponible. | Su alcance clínico es mucho mayor que el registro descriptivo de ARTEMIS. | Artículo conceptual, no prueba de eficacia de una solución clínica autónoma. |

EveryWear tiene documentación de arquitectura con app, servidor a bordo y servicios en tierra, además de registro, preprocesamiento y sincronización. Por ello ARTEMIS no debe atribuirse como novedad la combinación de movilidad, datos y seguimiento. [Marnat et al., IAC 2022, resumen en DLR](https://elib.dlr.de/191550/). MEDES describe su uso operativo y evolución con las misiones; esa es una declaración del desarrollador, no una comparación independiente de usabilidad. [MEDES](https://www.medes.fr/en/project/everywear-app/).

La descripción de SpaceWear confirma que también existe investigación sobre captura fisiológica portátil. ARTEMIS, en su alcance presente, no mide automáticamente variables ni sustituye dispositivos. [ESA, Health science in orbit](https://www.esa.int/Science_Exploration/Human_and_Robotic_Exploration/Health_science_in_orbit).

El artículo de Buras y Hilmers plantea características y un concepto de operaciones para agentes médicos. No justifica añadir diagnóstico por IA al MVP ni anunciar una autonomía que el proyecto no ha probado. [npj Microgravity, 2025, DOI 10.1038/s41526-025-00503-x](https://www.nature.com/articles/s41526-025-00503-x).

## Diferenciación que sí conviene investigar

1. **Comprensión:** explicar diferencias personales, datos faltantes y límites con claridad. Se demostrará mediante tareas de interpretación, no por cantidad de tarjetas.
2. **Trazabilidad visible:** que el usuario reconozca simulación, autoinforme y fuente pública. Hace falta comprobar que la interfaz conserva y comunica esos campos.
3. **Reproducibilidad educativa:** preparar escenarios públicos y verificables para enseñanza y evaluación. El repositorio aporta una base, pero faltan empaquetado y flujo integrado.
4. **Alcance acotado:** cuatro indicadores en vez de prometer cubrir toda la medicina espacial. Es una decisión de foco, no prueba de superioridad.

Estos atributos pueden coexistir en soluciones existentes. No se comprobó exclusividad, patentabilidad, menor coste, mayor precisión o ahorro de tiempo.

## Hipótesis de aplicación y mercado

Además de una demostración para la hackathon, podrían explorarse laboratorios universitarios, programas de formación y misiones análogas como contextos de evaluación. Son posibles interlocutores, no clientes confirmados. Para investigar viabilidad comercial deberán comprobarse necesidad, alternativas, autoridad de compra, integración, mantenimiento y disposición de pago. No se estimaron tamaño de mercado ni ingresos.

## Recomendación para el pitch

Usar: «Estamos desarrollando una experiencia de seguimiento explicable y trazable para investigar cómo presentar información física y de bienestar en contextos espaciales». Evitar «único», «primero», «superior a los sistemas NASA», «menor coste demostrado» o «asistente médico autónomo».

La revisión documental queda cerrada con un referente directo identificado y una propuesta de diferenciación verificable. Sigue pendiente comparar experiencias con usuarios y especialistas; no se inventó una ventaja para llenar esa ausencia.
