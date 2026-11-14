# Auditoría de procedencia y transformaciones de los datasets

**Informe:** 008 · **Fecha:** 14 de noviembre de 2026 · **Versión:** 1.0  
**Investigación secuencial:** 4 de 7. **Estado:** auditoría acotada concluida; límites de cobertura explícitos.

## Alcance y conclusión

Se cerró el informe 007 antes de iniciar esta auditoría. Se examinó el commit `80be128b17b5046ecd267d5a0604bbc5c74f5444`, se consultaron fuentes primarias y se descargaron en memoria dos CSV públicos de OSDR para contrastar su pivote con las copias del repositorio. No se modificaron datos del proyecto ni se ejecutó el pipeline que los sobrescribe. Los agregados de verificación están en el [anexo JSON](../evidencias/008_auditoria_fuentes.json); no se añaden a GitHub copias nuevas de mediciones individuales.

**Resultado:** la procedencia de los dos archivos OSDR pudo contrastarse hasta el pivote conservado; las unidades de radiación se comprobaron en HAPI. Eso no valida todas las correcciones clínicas, toda la serie ambiental ni la fuente NLSP. La fuente P0 del producto sigue siendo sintética.

## Cadena de procedencia revisada

| Grupo | Cadena identificada | Comprobación realizada | Límite |
| --- | --- | --- | --- |
| Simulación diaria | `generate_raw.py` → `clean.py` → adaptador `prepare_demo.py`. | Código, etiquetas y exclusión de derivados/imputados; recuentos del informe 004 como antecedente. | Parecerse a una distribución publicada no crea pacientes reales ni valida predicción. |
| OSD-569, hemograma | CSV largo público → pivote ancho → limpieza → tabla de laboratorio. | Descarga HTTP 200, 553 filas fuente; pivote de 28 registros idéntico a la copia conservada en columnas y valores. | La limpieza posterior requiere valoración clínica de correcciones y referencias. |
| OSD-575, panel metabólico | CSV largo público → pivote ancho → limpieza. | Descarga HTTP 200, 531 filas fuente; pivote de 28 registros idéntico al conservado. | No equivale a validar todos los datos derivados. |
| TEPC | Tasas HAPI e intervalos → resumen diario → escalado/imputación → calendario simulado. | Metadatos y dos jornadas de muestreo en el servicio original. | No se recalcularon los 180 días ni una dosis personal. |
| NLSP | Archivos atribuidos a UTMB Campaign 1 → limpieza y resumen. | Revisión de archivos y documentación del repositorio. | El enlace del portal no fue recuperable; no hubo contraste externo independiente. |

Los pivotes OSDR comparados usaron sujeto, sexo, punto temporal y analito, con el mismo procedimiento de `fetch_osdr.py`. No hubo claves de analito duplicadas en esos dos archivos actuales. La igualdad del pivote no acredita causalidad, diagnóstico ni representatividad poblacional.

## Fuentes originales verificadas

- [OSD-569](https://osdr.nasa.gov/bio/repo/data/studies/OSD-569), archivo `LSDS-7_Complete_Blood_Count_CBC.upload_SUBMITTED.csv` obtenido por la URL de descarga del script.
- [OSD-575](https://osdr.nasa.gov/bio/repo/data/studies/OSD-575), archivo `LSDS-8_Comprehensive_Metabolic_Panel_CMP.upload_SUBMITTED.csv` obtenido del mismo servicio.
- [HAPI metadata ISS_DOSANL_TEPC](https://cdaweb.gsfc.nasa.gov/hapi/info?id=ISS_DOSANL_TEPC): `DOSE` en µGy/min, `DOSE_EQ60` en µSv/min e intervalo en minutos. Son tasas y deben integrarse con su intervalo; no son directamente dosis diarias.
- [NLSP, campaña declarada](https://nlsp.nasa.gov/explore/data/details/6eaf1654-72d4-5d71-a9dd-a02e674c6473?dataType=MISSIONS): accesibilidad y autenticidad externa no comprobadas en esta revisión.
- [Términos OSDR](https://science.nasa.gov/reference/osdr-help-terms-and-conditions/): remiten a política de información y solicitan citas bibliográficas específicas de cada estudio. Descargar públicamente no sustituye documentar términos y atribución.

## Hallazgos de transformación

**P0:** el producto selecciona cuatro indicadores, conserva procedencia y convierte los imputados marcados en nulos para análisis. La copia sintética anterior contenía 4.320 observaciones y 92 nulos. Estos resultados se comprueban nuevamente en la investigación operativa posterior; no se presenta el CSV fuente como datos de vuelo.

**Información futura:** `clean.py` interpola bidireccionalmente y utiliza días 8–21 para la referencia de la misión. Es útil como transformación retrospectiva explicada, pero no para demostrar que un sistema detectó un cambio temprano sin información posterior. El P0 evita incorporar esos resultados derivados. El límite de interpolación por dirección tampoco demuestra por sí solo que todo hueco original tenga longitud total menor o igual a dos.

**Radiación:** `clean_radiation.py` usa ventana centrada y mediana global para imputar, escala cobertura parcial y reasigna fechas. No todo valor de la serie final es una medición directa. La combinación de valor medido, escalado e imputado debe conservar etiquetas separadas. La dosis equivalente ambiental del instrumento no se transforma automáticamente en dosis efectiva individual o porcentaje personal de un límite de carrera.

**Duplicados TEPC:** el descargador deduplica por minuto, no por registro completo. En la muestra del 1 de marzo de 2017 hubo 1.440 tiempos únicos y ningún duplicado; el 6 de abril hubo 1.351 registros y 90 tiempos repetidos, coincidentes en esta muestra con la deduplicación por minuto. Esa coincidencia en dos jornadas no demuestra que truncar timestamps sea correcto para cualquier intervalo o versión del servicio. Antes de recalcular toda la serie, definir identidad y política para duplicados con valores distintos.

**Laboratorio:** correcciones de columnas, valores calculados e intervalos de referencia deben conservar indicador de dato derivado y justificación clínica. Un registro llamado «raw» que ya fue pivotado es una copia transformada; conviene mantener también hash del archivo realmente descargado.

## Condiciones para aceptar cada grupo

1. **Demo P0:** aceptable para probar software si se identifica como simulación y se conservan nulos y origen; no sirve como eficacia médica.
2. **OSDR en vista científica:** procedencia al pivote respaldada; antes de ampliar su uso, cerrar cita del estudio, términos, reglas de limpieza y revisión de derivaciones.
3. **TEPC en vista científica:** usar como ambiente histórico con calidad explícita. Quedan pendientes recálculo completo, definición de duplicados y validación especializada de magnitudes e interpretación.
4. **NLSP:** mantener como material con trazabilidad declarada hasta contrastar descarga, archivos, permisos y transformaciones con el portal o custodio.
5. **Integrado:** no usar filas repetidas por tripulante como muestras independientes ni como fuente única para entrenamiento o inferencia clínica.

## Reproducibilidad y cierre

El anexo registra URLs exactas, SHA-256, tamaños, filas, metodología y resultados de comparación. Los hashes corresponden a descargas del 14 de noviembre de 2026; una actualización del origen requiere un nuevo corte. La revisión anterior verificó hashes de blobs Git, evitando cambios de saltos de línea de Windows.

La auditoría acotada está concluida: hay respaldo adicional de procedencia y una lista concreta de asuntos no resueltos. No se afirma que todas las fuentes o transformaciones hayan superado una auditoría científica completa. Puede continuar la investigación de usabilidad con una separación clara entre datos de demostración y evidencia clínica.
