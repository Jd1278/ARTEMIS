# Bitácora de investigación de ASTROGUARD y ARTEMIS HEALTH

| Fecha | Cambio | Resultado y pendientes |
| --- | --- | --- |
| 2026-11-14 | Creación de la carpeta de investigación, índice, informe 001, registro de fuentes y base del pitch. | Revisión documental exploratoria completada. Conecta contexto biológico y psicológico con propuestas del MVP de 48 horas. Pendientes: revisión especializada, indicadores definitivos y pruebas del software. |
| 2026-11-14 | Informe 002 sobre microgravedad y gravedad parcial; fuentes F12–F19, índice y mensajes complementarios para el pitch. | Se distinguen mecanismos, riesgos, fases e incertidumbre de extrapolación. Se verificó el dato de recuperación ósea en un estudio de 17 astronautas. Sin descarga de datasets ni validación clínica del producto. |
| 2026-11-14 | Informe 003 sobre medicina aeroespacial, comparación con atención terrestre y aplicaciones de investigación; fuentes F20–F26. | Incluye ADUM, SPRINT, AGBRESA, Twins Study y recuperación ósea. Distingue implementación, análogos y límites de evidencia. Se actualizaron índice y base del pitch. |
| 2026-11-14 | Informe 004 y evidencia de revisión de Jd1278/ARTEMIS, commit 92cf0cf. | 112 archivos; dos pruebas y 46 controles aprobados; 4320 observaciones P0 sintéticas, 92 nulos. Se documenta nombre vigente ARTEMIS HEALTH, Supabase y offline diferido. Sin cambios remotos ni verificación de base remota. |

## Serie secuencial solicitada

1. Informe 005: revisión documental de necesidades cerrada antes de comenzar soluciones existentes. Pendiente contraste humano; no se simularon entrevistas. Se verificaron README y requisitos del nuevo commit 80be128.
2. Informe 006: comparación documental cerrada después del 005. EveryWear es referente directo; no se sostiene exclusividad ni superioridad del proyecto. Se continúa con indicadores.
3. Informe 007: fundamento de indicadores cerrado después del 006; no se validaron traducciones ni sensores. Se identifican decisiones de ingeniería y permisos de instrumentos. Se continúa con auditoría de datos.
4. Informe 008: auditoría acotada cerrada después del 007. Dos CSV OSDR contrastados con pivotes del repositorio sin diferencias; unidades HAPI y dos días TEPC verificados. NLSP y limpieza clínica completa pendientes; descargas solo en memoria. Se continúa con usabilidad.
5. Informe 009: investigación metodológica cerrada después del 008; protocolo y registro vacío preparados. No hubo participantes ni resultados humanos inventados. Se continúa con restricciones operativas.
6. Informe 010: restricciones y verificación local cerradas después del 009. En 80be128 pasan dos pruebas y 46 controles; health responde y rutas de producto devuelven 404. No hay verificación de Supabase u offline. Se continúa con privacidad.
7. Informe 011: privacidad y diseño de evaluación de aceptación cerrados después del 010. No se recolectó salud real ni se certificó cumplimiento. Finalizada la serie documental; a continuación se redacta el guion comercial editable.
8. Después del cierre del 011 se redactaron síntesis y guion comercial v0.1, con versiones principal y breve, apoyo visual y afirmaciones trazables. No se publicaron ni se enviaron a terceros.

## Decisiones de documentación

- Utilizar Markdown y enlaces relativos para facilitar revisión y publicación en GitHub.
- Mantener las fuentes cerca de las afirmaciones y un registro central de referencias.
- Diferenciar evidencia publicada, propuesta de diseño, hipótesis y resultados propios.
- Tratar el plan interno como especificación propuesta; no afirmar implementación a partir de su contenido.
- No incluir expedientes, datos de salud personales ni datasets completos en la documentación.
- Preparar los mensajes del pitch con límites explícitos; no afirmar prevención, eficacia clínica o mejora psicológica sin estudios.
- Diferenciar microgravedad orbital y gravedad parcial; no atribuir radiación, aislamiento o todo cambio de salud exclusivamente a la gravedad.
- Conservar los informes anteriores como antecedentes y fijar el estado técnico por commit: 92cf0cf en el informe 004 y 80be128 en la serie posterior. No presentar el diseño antiguo de SQLite/offline como función del repositorio actual.

La creación de esta carpeta no implica commit ni publicación remota. Los siguientes informes se incorporarán aquí durante el trabajo que se solicite en este proyecto; no hay una tarea automática programada.

## Ajuste posterior del guion

Por solicitud del usuario, el guion comercial v0.2 se redujo a una sola versión de 30 segundos y se actualizaron sus tiempos visuales e índices. La duración de voz sigue pendiente de ensayo.
