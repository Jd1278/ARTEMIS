# Estado del repositorio ARTEMIS y de su investigación

**Informe:** 004  
**Fecha:** 14 de noviembre de 2026  
**Versión:** 1.0  
**Repositorio:** [Jd1278/ARTEMIS](https://github.com/Jd1278/ARTEMIS)  
**Rama y versión examinadas:** `main`, commit `92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698`  
**Tipo:** revisión documental y técnica con comprobaciones locales de datos

## Resultado principal

ARTEMIS contiene una base de investigación y preparación técnica para **ARTEMIS HEALTH**, el nombre vigente que su documentación da al proyecto anteriormente llamado ASTROGUARD. El avance verificable está en la especificación, la organización modular, la generación y adaptación de datos, el esquema PostgreSQL y pruebas acotadas. El flujo completo de aplicación —formulario, persistencia por API, historial y panel— todavía no está implementado en la versión examinada. El propio README reconoce este estado. [R01](https://github.com/Jd1278/ARTEMIS/blob/92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698/README.md), [R02](https://github.com/Jd1278/ARTEMIS/blob/92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698/artemis-healt/README.md)

La línea central de investigación del paquete es el seguimiento diario de sueño, fatiga, estrés y pulso, con material complementario de laboratorio, radiación ambiental y análogos de reposo en cama. Disponer de esos datos y scripts no demuestra predicción de enfermedad ni eficacia clínica del producto.

## Alcance y método de la revisión

Se utilizó el conector GitHub para consultar metadatos, árbol completo, archivos, ramas, commits, pull requests y ejecuciones de Actions. Se obtuvo una copia aislada del mismo commit para inspeccionar el documento Word, revisar scripts y ejecutar controles de lectura. No se modificó el repositorio remoto, no se aplicaron migraciones ni se utilizaron credenciales de Supabase.

Se revisaron los README, requisitos, arquitectura, revisión de datos, documentación de Supabase, auditoría, diccionario, fuentes y declaración de IA; el contenido textual y tablas del DOCX; código de entrada, conexión, preparación y pruebas; y las operaciones pertinentes de los scripts del paquete de datos. No se hizo una auditoría clínica independiente de cada transformación ni se volvió a descargar cada fuente NASA para contrastarla con el repositorio.

Los enlaces de evidencia están fijados al commit para que el informe siga siendo reproducible aunque cambie `main`. Los resultados y límites de ejecución están en el [anexo de verificación](../evidencias/004_verificacion_repositorio.json).

## Qué contiene

El árbol examinado incluye **112 archivos versionados**, de los cuales **14 son `.gitkeep`**: marcadores para conservar directorios, no funcionalidades. El árbol devuelto por GitHub no estaba truncado.

| Ubicación | Contenido observado | Interpretación |
| --- | --- | --- |
| `README.md` | Identidad, enlaces y estado del proyecto. | Punto de entrada; reconoce funciones pendientes. |
| `ARTEMIS_HEALTH_Requisitos_y_revision_datasets.docx` | Alcance, RF/RNF, evaluación de datasets y criterios de aceptación. | Documento fuente; algunas decisiones fueron modificadas después en Markdown. |
| `artemis-healt/docs/` | Requisitos vigentes, arquitectura, diseño, auditoría de datos, revisión y Supabase. | Principal documentación técnica del producto. |
| `artemis-healt/src/artemis_health/` | Entrada FastAPI, conexión PostgreSQL y módulos reservados. | Esqueleto de aplicación; solo se declara una ruta de negocio mínima. |
| `artemis-healt/frontend/` | Directorios reservados y un archivo de tokens CSS. | No contiene todavía una aplicación React compilable, componentes ni manifiesto de dependencias frontend. |
| `artemis-healt/migrations/` | Esquema SQL, restricciones, índices, roles y políticas RLS. | Capa de datos preparada en código; despliegue remoto no verificado. |
| `artemis-healt/scripts/` | Adaptador P0, migración, carga, verificación y exportación SQL. | Herramientas concretas de preparación y administración. |
| `artemis-healt/data/demo/` | Observaciones JSON y manifiesto con hashes. | Artefacto sintético empaquetado para el producto. |
| `artemis-healt/tests/` | Dos pruebas automatizadas y directorios reservados. | Cobertura de contrato y artefacto; no del flujo completo. |
| `artemis-sleep-dataset/` | Fuentes conservadas, tablas procesadas, referencias y scripts. | Paquete de investigación de datos, más amplio que su nombre referido al sueño. |

[Árbol de la versión examinada](https://github.com/Jd1278/ARTEMIS/tree/92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698).

## Qué se ha realizado según el historial

La consulta devolvió tres commits alcanzables en `main`, todos del 14 de noviembre de 2026. Horas convertidas a Bogotá, UTC−5:

| Hora | Commit | Avance documentado |
| --- | --- | --- |
| 08:59:29 | `5d77f4c` | Creación inicial del repositorio. |
| 11:44:51 | `a5a8142` | Incorporación principal con estructura y referencia a Supabase y Vercel. |
| 11:52:16 | `92cf0cf` | Integración de los dos historiales iniciales y ajuste del README. |

El último es un merge con dos padres. La comparación que devuelve GitHub para ese commit muestra un cambio pequeño del README; no debe contarse como otra implementación completa. Un mensaje de «primer despliegue» tampoco demuestra funcionamiento en producción. [Historial](https://github.com/Jd1278/ARTEMIS/commits/92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698), [merge examinado](https://github.com/Jd1278/ARTEMIS/commit/92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698).

Se encontró una rama, `main`; la consulta de pull requests devolvió cero y Actions registró cero ejecuciones. Esto no excluye trabajo fuera de GitHub ni pruebas manuales. El historial corto y concentrado no permite reconstruir todas las etapas previas del desarrollo.

## Qué investiga el paquete de datos

### Seguimiento diario simulado

El paquete genera una misión ficticia de seis tripulantes durante 180 días. Incluye descanso, fatiga Samn–Perelli, estrés, carga de trabajo, ánimo, atención/PVT y pulso en reposo. Las distribuciones y eventos están programados; sus etiquetas de anomalía son parte del generador, no descubrimientos de una IA ni eventos clínicos reales. [R03](https://github.com/Jd1278/ARTEMIS/blob/92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698/artemis-sleep-dataset/README.md)

La bibliografía del paquete cita estudios de sueño en la ISS, pruebas de vigilancia y escalas de fatiga para fundamentar parámetros. Esa calibración sirve para diseñar una simulación plausible, pero no valida la representación de todas las personas o misiones. Las referencias del paquete se conservaron como referencias declaradas; esta revisión no revalidó uno por uno sus umbrales. [R04](https://github.com/Jd1278/ARTEMIS/blob/92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698/artemis-sleep-dataset/docs/SOURCES.md)

### Laboratorio de Inspiration4

Se conservan tablas atribuidas a NASA OSDR OSD-569 y OSD-575, relativas a hemograma y panel metabólico, además de transformaciones y laboratorios sintéticos calibrados con esos valores. La documentación identifica cuatro participantes y siete puntos pre/post de una misión de tres días. No respalda alertas diarias para una misión de seis meses. Los resultados sintéticos derivados siguen siendo sintéticos. [R03](https://github.com/Jd1278/ARTEMIS/blob/92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698/artemis-sleep-dataset/README.md), [R04](https://github.com/Jd1278/ARTEMIS/blob/92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698/artemis-sleep-dataset/docs/SOURCES.md)

### Radiación ambiental histórica

El paquete atribuye su serie a ISS_DOSANL_TEPC, NASA CDAWeb, con fechas de 2017. La agrega por día, rellena o escala determinados registros y la incorpora a un calendario ficticio, repitiéndola por tripulante. No son mediciones personales de esos perfiles ni exposición contemporánea. La comparación con un límite de carrera que aparece en el paquete fuente no se adopta como resultado médico individual. [R05](https://github.com/Jd1278/ARTEMIS/blob/92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698/artemis-sleep-dataset/docs/CLEANING_REPORT.md), [R06](https://github.com/Jd1278/ARTEMIS/blob/92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698/artemis-healt/docs/review.md)

### Reposo en cama como análogo terrestre

Hay datos atribuidos a NASA Life Sciences Portal, campaña UTMB 1: actigrafía, WinSCAT y tolerancia a inclinación, con tres sujetos. Permiten explorar sueño, cognición y respuesta cardiovascular bajo un análogo, conservando sesiones y fases. No son vuelos espaciales. El paquete documenta correcciones de metadatos y exclusión de un archivo de pulso por duplicar presión diastólica; esta revisión constató esa documentación y la ausencia del campo en el producto procesado, sin reauditar el portal original. [R04](https://github.com/Jd1278/ARTEMIS/blob/92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698/artemis-sleep-dataset/docs/SOURCES.md), [R05](https://github.com/Jd1278/ARTEMIS/blob/92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698/artemis-sleep-dataset/docs/CLEANING_REPORT.md)

## Recuentos comprobados y selección del MVP

El CSV integrado tiene **20.080 filas**. La distribución que se comprobó conserva las etiquetas del propio paquete:

| Etiqueta | Filas | Significado declarado |
| --- | ---: | --- |
| `simulated` | 12.960 | Variables de seguimiento diario sintético, incluidas derivadas. |
| `simulated_from_real` | 588 | Laboratorio sintético calibrado con referencias reales. |
| `real_nasa_cdaweb` | 4.320 | Variables ambientales históricas repetidas por perfil. |
| `real_nasa_osdr` | 1.064 | Resultados de laboratorio de Inspiration4 procesados. |
| `real_nasa_lsda` | 1.148 | Variables del análogo terrestre. |

Contar filas no equivale a contar participantes, mediciones independientes ni días de exposición. Tampoco las etiquetas certifican por sí mismas la trazabilidad externa.

La aplicación P0 usa una selección más estrecha: **1.080 registros diarios fuente** se convierten en **4.320 observaciones**, una por indicador, perfil y día. Todas tienen `origin_type=synthetic`; hay seis perfiles y cuatro indicadores:

| Indicador | Unidad o escala | Observaciones | Valores excluidos del análisis |
| --- | --- | ---: | ---: |
| Sueño autoinformado | Horas | 1.080 | 0 |
| Fatiga | Samn–Perelli, 1–7 | 1.080 | 7 |
| Estrés percibido | 0–100 | 1.080 | 32 |
| Pulso en reposo | Latidos por minuto | 1.080 | 53 |
| **Total** | | **4.320** | **92** |

El adaptador asigna UUID deterministas, conserva archivo y fila de origen y convierte los valores imputados o fuera de dominio marcados en `value=null`, manteniendo `source_value`. No incorpora el `risk_score`, semáforos ni etiquetas de anomalía del paquete como conclusiones del producto. [R07](https://github.com/Jd1278/ARTEMIS/blob/92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698/artemis-healt/scripts/prepare_demo.py), [R08](https://github.com/Jd1278/ARTEMIS/blob/92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698/artemis-healt/data/demo/manifest.json)

## Qué está implementado y qué sigue propuesto

| Componente | Evidencia actual | Estado que puede comunicarse |
| --- | --- | --- |
| Preparación P0 | Adaptador, JSON, manifiesto y pruebas. | Implementado y comprobado localmente en esta revisión. |
| Datos de investigación | CSV/JSON, fuentes y scripts. | Disponibles; autenticidad y transformaciones requieren auditoría externa antes de conclusiones científicas. |
| API | `/api/health` devuelve `status=scaffold` y `database_checked=false`. | Esqueleto, no flujo de salud operativo. |
| Base de datos | SQL y scripts de migración/carga/verificación. | Preparados; conexión, migración y permisos remotos no verificados aquí. |
| Frontend | Directorios reservados y tokens CSS. | Pendiente de implementación. |
| Registro, historial y comparación | Contratos escritos en arquitectura y requisitos. | Especificados; sin endpoints funcionales correspondientes. |
| Fichas y vista científica | Módulos reservados. | Propuestas pendientes. |
| IA clínica | No se encontró modelo entrenado ni pipeline de inferencia desplegado. | Fuera del alcance P0. |
| Despliegue | URL de Vercel en metadatos y mensaje de commit. | Declarado; no validado como aplicación funcional. |

[R09 — entrada de API](https://github.com/Jd1278/ARTEMIS/blob/92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698/artemis-healt/src/artemis_health/main.py), [R10 — arquitectura](https://github.com/Jd1278/ARTEMIS/blob/92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698/artemis-healt/docs/architecture.md), [R11 — migración](https://github.com/Jd1278/ARTEMIS/blob/92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698/artemis-healt/migrations/001_initial.sql).

Los requisitos proponen una mediana histórica causal y separación por perfil, contexto y origen. La configuración SQL de esa regla no es su implementación de análisis. Las políticas RLS del esquema tampoco demuestran autenticación ni autorización completa de la futura API.

## Comprobaciones realizadas

En una copia aislada del commit, con Python **3.13.1**:

- `python -m unittest discover -s tests -v`, desde `artemis-healt`: **dos pruebas aprobadas**, código de salida 0.
- `python scripts/validate.py`, desde `artemis-sleep-dataset`: **46 controles PASS**, código de salida 0.
- Recuento independiente de CSV y observaciones, perfiles, indicadores, identificadores y nulos.
- Coincidencia del hash del JSON P0 con su manifiesto y coincidencia semántica entre `build()` y el JSON empaquetado.
- Comprobación de los **12 hashes** de la auditoría contra los bytes originales de Git: todos coinciden. Se usaron los blobs porque la conversión local de saltos de línea en Windows cambia hashes de archivos de trabajo.
- Importación del módulo de entrada y consulta directa de sus rutas y función de salud: confirma el esqueleto. No fue una prueba HTTP ni una prueba de base de datos.

No se ejecutó `run_all.sh`, que regenera fuentes y salidas. No se instalaron dependencias, no se aplicó SQL y no se verificó Supabase. La herramienta web no pudo recuperar la URL Vercel declarada ni `/api/health`; esto no prueba por sí solo que el despliegue esté caído.

Los controles de calibración comprueban consistencia y parecido con supuestos del generador; no son sensibilidad diagnóstica, eficacia clínica ni evaluación de usuarios. Aprobarlos no implica que el producto completo funcione.

## Inconsistencias y límites que conviene resolver

1. **Requisitos históricos distintos.** El DOCX mantiene SQLite y operación local sin internet, mientras `docs/requirements.md` establece PostgreSQL/Supabase y difiere offline completo. El README designa los requisitos Markdown como vigentes. Antes del pitch, marcar el Word como antecedente o actualizarlo. [R12](https://github.com/Jd1278/ARTEMIS/blob/92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698/artemis-healt/docs/requirements.md)
2. **Recuento documental desactualizado.** El diccionario indica 14.612 filas, frente a las 20.080 verificadas en el integrado. Corregir la cifra y conservar fecha/versionado. [R13](https://github.com/Jd1278/ARTEMIS/blob/92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698/artemis-sleep-dataset/docs/DATA_DICTIONARY.md)
3. **La revisión del validador quedó atrás del código.** `docs/review.md` dice que no garantiza salida distinta de cero; la versión examinada incluye `sys.exit(1 if errors else 0)`. No repetir el hallazgo antiguo como fallo actual. [R14](https://github.com/Jd1278/ARTEMIS/blob/92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698/artemis-sleep-dataset/scripts/validate.py)
4. **Información futura en la referencia heredada.** `clean.py` utiliza días 8–21 como referencia global e interpola bidireccionalmente. Esas transformaciones no sirven sin ajustes para simular decisiones tempranas sin información futura. El P0 evita adoptar sus resultados derivados y excluye imputados. [R15](https://github.com/Jd1278/ARTEMIS/blob/92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698/artemis-sleep-dataset/scripts/clean.py)
5. **Persistencia remota sin evidencia suficiente.** La guía incluye tanto pasos pendientes como una ejecución manual de migración reportada por el usuario, aún no comprobada. Falta evidencia de tablas, carga, reintentos y permisos. [R16](https://github.com/Jd1278/ARTEMIS/blob/92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698/artemis-healt/docs/supabase.md)
6. **Permisos y atribución.** No se encontró archivo LICENSE en el árbol ni licencia identificada en metadatos. Las referencias de datos no equivalen a licencia del código o autorización para toda redistribución. Documentar condiciones de cada fuente y decidir licencia del material propio.
7. **Declaración de IA incompleta.** Hay descripción detallada del trabajo asistido en datos, pero quedan entradas por completar para web, función de IA y presentación. El informe no verificó identidades de herramientas ni revisiones humanas declaradas. [R17](https://github.com/Jd1278/ARTEMIS/blob/92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698/artemis-sleep-dataset/docs/AI_USAGE.md)

## Cómo integrar la investigación que estamos produciendo

Al corte examinado, el repositorio remoto **no contiene la carpeta `investigacion/` ni los informes 001–004 de este trabajo**. Permanecen preparados en el espacio local del usuario. No confundir el manifiesto remoto de limpieza de antiguos archivos ASTROGUARD con una eliminación de estos informes locales: son ubicaciones y evidencias distintas.

Se recomienda incorporar `investigacion/` en la raíz, junto a los dos paquetes actuales, y enlazar su índice desde el README principal. Mantener:

- Los informes 001–003 como antecedentes científicos, conservando su fecha y el nombre utilizado entonces.
- El informe 004 como corte técnico del repositorio, con commit y evidencia de pruebas.
- Un registro de fuentes científicas separado de referencias técnicas del repositorio.
- Una bitácora que explique el cambio ASTROGUARD → ARTEMIS HEALTH y la decisión de persistencia.
- Evidencias futuras de implementación y pruebas, sin sustituir los resultados históricos por estados más recientes sin versión.

Primero conviene corregir las contradicciones documentales; después implementar y probar el flujo P0; finalmente actualizar el pitch con capturas y resultados reales. Las fuentes públicas de investigación deben seguir separadas de perfiles ficticios y registros manuales.

## Conclusión para presentar el avance

Una formulación respaldada es: **«ARTEMIS HEALTH cuenta con una especificación revisada, un paquete de investigación y una selección de datos sintéticos trazables para cuatro indicadores. Verificamos las pruebas de datos; el siguiente hito es integrar y demostrar el flujo de aplicación con persistencia».**

No hay evidencia suficiente en este corte para anunciar una aplicación médica operativa, entrenamiento clínico, prevención demostrada o autonomía sin conexión. Este informe describe la versión fijada; los avances posteriores requieren un nuevo corte.
