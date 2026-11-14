# Requisitos finales de ARTEMIS HEALTH

## Autoridad y objetivo
Esta especificación sustituye las anteriores ASTROGUARD y consolida ARTEMIS_HEALTH_Requisitos_y_revision_datasets.docx con la inspección del paquete local. Objetivo: registrar y comprender evolución personal de cuatro indicadores, con procedencia explícita y ejecución del servidor local o desplegado con acceso a Supabase. No entrenar modelos clínicos ni presentar puntuaciones de salud.

## Dataset y escalas definitivas
Fuente P0: crew_daily_log_clean.csv, seis perfiles ficticios, 180 días. Campos: resting_hr_bpm (bpm, reposo), sleep_duration_h (horas, sueño autoinformado), samn_perelli (entero 1–7, fatiga) y stress_vas (0–100, estrés percibido). Se conservan claves y escalas originales: no convertir fatiga ni estrés a 1–5. El formulario explicará extremos y carácter de autoinforme.

Generar un contrato longitudinal específico mediante scripts/prepare_demo.py. Cada fila incluye id, profile_id, indicator, value, unit, timestamp, mission_day, context, namespace, origin_type, capture_method, quality_flags, source_file, source_row y source_value. Los imputados o marcados fuera de dominio se conservan como source_value para auditoría, pero value=null. No interpolar ni usar esos valores en la mediana. Las filas fuente permanecen intactas.

Los campos baseline_*, status_*, overall_status, risk_score, event_label e is_anomaly no entran en el contrato del producto. Los últimos dos son etiquetas del generador, no resultados de predicción. El dataset integrado no se importa a P0. Datos de radiación histórica, laboratorio y análogos solo se consideran en research P1 tras verificar licencia y trazabilidad; fechas ambientales no equivalen a exposición personal.

## RF P0 y aceptación
Se conserva numeración del anexo entregado.
| ID | Requisito final y evidencia |
| --- | --- |
| RF-01 | Seleccionar uno de seis perfiles ficticios; panel DEMO y SIMULADO visible. |
| RF-02 | Mostrar cuatro indicadores con unidad, momento de misión, fecha, origen y calidad. |
| RF-03 | Registrar observación manual con UUID, perfil, indicador, unidad, hora y contexto. |
| RF-04 | Rechazar no finitos, unidades incompatibles y fechas inválidas; sueño 0–24, fatiga entera 1–7, estrés 0–100 y pulso positivo. Son dominios técnicos. |
| RF-05 | Persistir en PostgreSQL en Supabase y verificar recuperación tras reinicio. |
| RF-06 | Repetición idéntica no duplica; mismo UUID con distinto contenido devuelve 409. |
| RF-07 | Filtrar historial por perfil, indicador y periodo, en orden temporal. |
| RF-08 | Gráfica y tabla coinciden; null genera hueco, no cero ni línea interpolada. |
| RF-09 | Mediana de hasta 14 días anteriores dentro de 30 días, mínimo siete días válidos; excluir día actual y futuro. |
| RF-10 | Explicar mediana, diferencia, días usados y periodo; con menos de siete, historial insuficiente. |
| RF-11 | Mostrar variaciones descriptivas y versión de regla; ningún semáforo heredado del CSV. |
| RF-12 | Distinguir synthetic/user_report/public_dataset, import/manual, imputación y calidad por indicador. |
| RF-13 | Cuatro fichas educativas locales con límites y referencia revisada. |
| RF-14 | Consulta y registro con conexión a Supabase; ante desconexión informar indisponibilidad y conservar borrador durante la sesión. Offline completo diferido. |
| RF-15 | Ante error conservar borrador durante sesión y mostrar NO GUARDADO. |
| RF-16 | README, contrato, procedencia, versiones, declaración de IA y evidencias de pruebas. |

P1: RF-17 explorador científico separado; RF-18 rutinas educativas; RF-19 FAQ. Ninguno bloquea P0.

Comparaciones: mismo perfil, indicador, contexto, unidad y origen. synthetic y user_report no comparten línea base; los primeros registros manuales tendrán historial insuficiente. Por día usar la última observación válida. Estrés y fatiga se expresan en puntos, no porcentajes. El cursor temporal de demo permite revisar un día de misión: todo cálculo respeta ese cursor y no la fecha actual del computador. El P0 muestra diferencias sin umbrales de severidad.

## RNF y prueba
| ID | Requisito final y aceptación |
| --- | --- |
| RNF-01 | Último valor y origen accesibles en máximo dos pantallas. |
| RNF-02 | Teclado completo, foco visible, etiquetas, texto además de color; contraste objetivo 4.5:1 en texto normal. |
| RNF-03 | Revisar 360×800, 768×1024 y 1440×900 sin solapamientos. |
| RNF-04 | Panel local usable en menos de 3 s con 1000 observaciones; medir también el conjunto P0 completo y registrar equipo. |
| RNF-05 | Recursos visuales empaquetados; probar fallo de conexión con Supabase sin confirmar guardados. Sin almacenamiento offline en esta fase. |
| RNF-06 | Escritura atómica, IDs únicos y pruebas de fallo sin guardado parcial. |
| RNF-07 | Fuente, hash, fila, transformación y versión en manifiesto; público requiere licencia y URL comprobadas. |
| RNF-08 | Aislamiento demo/research y por origen en cada cálculo. |
| RNF-09 | Solo perfiles ficticios; demo no admite expedientes reales. |
| RNF-10 | Sin secretos ni administración abierta; validación en servidor. |
| RNF-11 | Cálculo verificable y explicación reproducible. |
| RNF-12 | Mantener nulos y flags; no borrar extremos originales ni presentar imputación como medición. |
| RNF-13 | Regeneración determinista y ejecución documentada en entorno limpio. |
| RNF-14 | Límites modulares, reglas versionadas y tokens visuales centralizados. |
| RNF-15 | Etiquetas de simulación, dato público o análogo según origen real del registro. |
| RNF-16 | Sin diagnósticos, terapias, clasificación normal/enfermo ni riesgo clínico. |

## Fases y responsables
I1 fuentes y auditoría; I2 datos y análisis; I3 backend; I4 frontend; I5 integración y QA; I6 diseño y pitch.
1. H0–H6: contratos, datos P0 y wireframes (I1, I2, I4, I5, I6); esqueleto API (I3).
2. H6–H12: PostgreSQL en Supabase, importación idempotente, selección de perfil y registro integrado (I2–I5).
3. H12–H16: historial, cálculo causal, estados y fichas (I2–I6); congelar alcance.
4. H16–H24: descanso escalonado y correcciones acotadas.
5. H24–H32: pruebas del anexo CA-01 a CA-10 y revisión visual; RF-17 solo si P0 pasa.
6. H32–H40: instalación, demo, documentación y pitch; I6 captura únicamente funciones comprobadas.
7. H40–H48: descanso, margen, verificación y entrega.

Terminado: todos los RF P0 y RNF aplicables aprobados, evidencia guardada, revisión cruzada y cero pérdidas de datos o éxitos ficticios. Estado actual: especificación y scaffolding; implementación funcional pendiente.

