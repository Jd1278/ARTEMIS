# ARTEMIS HEALTH · Contenido de frames v1

Documento de estructura: indica qué va en cada apartado. No representa una aplicación implementada ni cambia las reglas del backend. Base normativa: `docs/requirements.md` y `docs/architecture.md`.

## Navegación y contexto persistente

Cuatro destinos P0: Resumen, Registrar, Historial y Aprender. Perfiles vive como selector global y panel de detalle; Análisis se integra en Resumen/Historial. Investigación es P1 y queda fuera de la navegación funcional inicial.

Todas las pantallas muestran marca, entorno DEMO, perfil ficticio activo y cursor de misión con fecha histórica. SIMULADO identifica el conjunto sintético; los registros manuales se identifican como AUTOINFORME. Seleccionar perfil conserva la ruta y reinicia filtros incompatibles. Los resultados siempre corresponden al perfil y al cursor seleccionados. No usar la fecha actual del equipo como día de misión.

## F00 · Selección de perfil / módulo Profiles

Entrada: primera apertura sin perfil seleccionado, o selector global.

| Apartado | Contenido |
| --- | --- |
| Encabezado | Logo, ARTEMIS HEALTH, frase corta y etiqueta DEMO |
| Introducción | «Explora la evolución de un perfil ficticio» y aviso de datos simulados |
| Perfiles | Seis opciones CM-01 a CM-06; ID y nombre recibido del backend, sin inventar biografías, retratos, edad o antecedentes |
| Acción | «Abrir resumen»; habilitada con perfil seleccionado |
| Pie | Alcance educativo y ausencia de uso clínico |

Estados: carga, seis perfiles disponibles, vacío y error con reintento. En móvil las opciones se apilan. API prevista: GET `/api/profiles`. RF-01, RNF-09.

## F01 · Resumen / Profiles + Observations + Analysis

| Apartado | Contenido |
| --- | --- |
| Cabecera | «Resumen de misión», perfil, DEMO/SIMULADO, cursor de día y fecha histórica |
| Acciones | «Registrar observación» como CTA principal; «Ver historial» secundario |
| Cuatro tarjetas | Sueño en h; fatiga 1–7; estrés 0–100; pulso de reposo en bpm |
| Dentro de tarjeta | Último valor disponible hasta el cursor, unidad, fecha de observación, día de misión, origen, captura y calidad; indicar cuando no hay observación del día seleccionado |
| Evolución | Selector de indicador, periodo, filtro de origen y gráfica temporal; marca del cursor; huecos para nulos; eje con unidad |
| Comparación | Valor, mediana previa, diferencia con unidad, días válidos usados, periodo y versión de regla recibidos del backend |
| Explicación | «Cómo se calcula» y mensaje de historial insuficiente cuando corresponde |
| Procedencia | Acceso al detalle de la observación y a la tabla equivalente |

En escritorio: cuatro tarjetas; gráfica a la izquierda y explicación a la derecha. Tablet: dos tarjetas por fila. Móvil: tarjetas apiladas y explicación después de la gráfica. Sin puntuación global, semáforos, diagnósticos ni alertas clínicas.

API prevista: GET `/api/indicators`, GET `/api/profiles/{id}/dashboard` y GET `/api/profiles/{id}/comparison?indicator=&at=`. La estructura exacta de respuestas y el parámetro de cursor del dashboard deben acordarse con backend; no asumir que existen. RF-02, RF-08 a RF-12.

## F02 · Registro / módulo Observations

| Apartado | Contenido |
| --- | --- |
| Contexto | «Registrar observación», perfil ficticio, entorno DEMO y aviso de que este registro será AUTOINFORME |
| Indicador | Selector de uno de los cuatro indicadores |
| Valor | Campo numérico con etiqueta persistente, unidad derivada y explicación de dominio |
| Escalas | Sueño 0–24 h; fatiga entera 1–7 con extremos 1 «Totalmente alerta» y 7 «Completamente exhausto, incapaz de funcionar eficazmente»; estrés 0–100 con extremos «Sin estrés percibido» / «Máximo estrés percibido»; pulso positivo en reposo |
| Momento | Fecha y hora con zona horaria explícita; convertir a ISO 8601 UTC para la API; día de misión derivado solo según contrato acordado |
| Contexto de medida | Visible y derivado del indicador: sleep_report, fatigue_report, stress_report o rest; etiqueta comprensible en español |
| Procedencia | AUTOINFORME, captura MANUAL; no permitir seleccionar synthetic desde el formulario |
| Revisión | Perfil, indicador, valor/unidad y momento antes de enviar |
| Acción | «Guardar observación»; estado pendiente e impedimento de doble envío |
| Resultado | Confirmación tras 200/201; en error conservar borrador durante la sesión y mostrar NO GUARDADO |

UUID generado una sola vez por intento lógico y conservado al reintentar el mismo contenido. Tras cambiar contenido de un registro conflictivo, resolver explícitamente el flujo con backend. 409: explicar conflicto y ofrecer revisar; 422: errores junto al campo y resumen accesible. Desconexión: conservar borrador en memoria durante la sesión, sin prometer recuperación tras cerrar/recargar ni almacenamiento offline.

API prevista: POST `/api/observations`. Campos y autorización se confirman con backend. Una maqueta puede mostrar los estados, pero no fingir persistencia. RF-03 a RF-06, RF-14 y RF-15.

## F03 · Historial / módulo Observations

| Apartado | Contenido |
| --- | --- |
| Filtros | Perfil global, indicador, fechas desde/hasta inclusivas y origen separado |
| Encabezado de resultados | Periodo, número de registros y contexto de origen |
| Visualización | Pestañas «Gráfica» y «Tabla» sobre el mismo conjunto filtrado |
| Tabla | Fecha/hora y zona, día de misión, indicador, valor/unidad, contexto, origen, captura y calidad |
| Nulos | «Sin dato válido»; nunca convertir null a cero |
| Detalle | Abrir F04 desde fila o punto seleccionado |
| Acciones | Aplicar/limpiar filtros y navegación de resultados si hace falta; exportar no forma parte de P0 |

Mantener orden temporal explícito. No limitar silenciosamente la gráfica a la página visible de tabla: indicar el alcance si hay paginación. En móvil tabla dentro de una región desplazable identificada, conservando encabezados y acceso al detalle; la página general no desborda.

API prevista: GET `/api/profiles/{id}/observations?indicator=&from=&to=`. Filtro de origen y paginación aún requieren acuerdo. RF-07, RF-08, RF-12.

## F04 · Detalle de observación / Observations + Analysis

Panel lateral en escritorio; diálogo de pantalla completa en móvil. Contiene valor válido o «Sin dato válido», unidad, fecha UTC y conversión local, día de misión, contexto, perfil, origen, captura y flags explicados. Procedencia desplegable: UUID, archivo, fila, lote y transformación/hash cuando el backend los exponga. `source_value` se muestra como «Valor original excluido del análisis» cuando corresponda, nunca como medición válida.

Bloque de comparación: mediana previa, diferencia, hasta 14 días válidos anteriores dentro de 30, mínimo siete; excluir día actual y futuro, elegir última observación válida de cada día. Comparar solo mismo perfil, indicador, contexto, unidad y origen. Si faltan datos, explicar sin fabricar una diferencia. Mostrar versión de regla y periodo recibidos del servidor. Cerrar con Escape, devolver foco al activador. RF-09 a RF-12, RNF-11 y RNF-12.

## F05 · Aprender / módulo Education

Vista de biblioteca con cuatro fichas: Sueño, Fatiga, Estrés percibido y Pulso en reposo. Cada tarjeta lleva nombre, unidad/escala, resumen y «Leer ficha». Detalle: qué representa, cómo registrar, límites del autoinforme o contexto de reposo, cómo leer la evolución, límites del producto y referencia revisada. No inventar citas, recomendaciones terapéuticas ni enlaces. Si el contenido revisado todavía no existe, mostrar estado editorial pendiente.

API prevista: GET `/api/education/{indicator}`. RF-13. No añadir chat médico, rutinas o FAQ como requisitos P0.

## F06 · Procedencia y alcance / vista transversal

Accesible desde el pie y desde detalles de datos. Contiene carácter ficticio de perfiles, origen de datos sintéticos, límites de los autoinformes, tratamiento de imputados/nulos, versión de transformación y reglas, aviso de uso educativo y declaración de IA con información comprobada. Mostrar documentación empaquetada o enlazada; no crear métricas nuevas. RF-12, RF-16.

## F07 · Investigación / módulo Research · P1

Frame documental reservado: lista de estudios, ficha de fuente/licencia y exploración de observaciones públicas en un namespace separado. No habilitar navegación ni cargar datos hasta auditar licencia, procedencia y contrato. No comparar datos ambientales históricos con exposición personal ni mezclar con la línea base demo. RF-17, diferido.

## F08 · Estados y componentes / revisión interna

Galería de botón, selector, campo, tarjeta de indicador, badge de procedencia, badge de calidad, tooltip, tabs, tabla, diálogo, skeleton y aviso. Presentar carga, vacío, nulo excluido, historial insuficiente, sin conexión, error de consulta, NO GUARDADO, guardando, 409 y 422. Acceso de desarrollo, fuera de navegación pública.

## Puerta de revisión

Revisar F00–F06 y F08 a 360×800, 768×1024 y 1440×900, teclado y zoom 200%. Verificar texto además de color, contraste, foco y ausencia de solapamientos. Los fixtures deben llevar rótulo «Vista de diseño · datos de ejemplo» además de las etiquetas del dominio. No presentar la maqueta como conectada.

La siguiente integración requiere acordar con backend: esquemas JSON, cursor y zona horaria de misión, filtro de origen, campos de comparación/procedencia, auth y errores. Los endpoints del documento de arquitectura son previstos, no evidencia de implementación.
