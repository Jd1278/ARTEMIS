# Restricciones operativas y verificación técnica del seguimiento

**Informe:** 010 · **Fecha:** 14 de noviembre de 2026 · **Versión:** 1.0  
**Investigación secuencial:** 6 de 7. **Estado:** revisión documental y comprobación local concluidas; integración remota y entorno espacial no evaluados.

## Pregunta y respuesta

¿Qué necesita el sistema cuando comunicación, datos o componentes fallan? Debe distinguir disponibilidad de interfaz, servicio, almacenamiento y enlace remoto. **La arquitectura actual depende de Supabase para persistir y no demuestra operación autónoma espacial.** Puede investigarse como prototipo conectado, con una transición posterior a almacenamiento local y sincronización si ese objetivo se mantiene.

El informe se inició después de cerrar el 009. Se fijó el commit `80be128b17b5046ecd267d5a0604bbc5c74f5444`, que incorpora identidad visual respecto del corte 004, pero conserva el esqueleto de API. Se revisaron requisitos y conexión y se ejecutaron pruebas en una copia aislada. No hubo acceso a una base remota ni escritura fuera de esa copia, salvo el archivo de evidencia de la investigación.

## Contexto de misión

El informe de NASA sobre ancho de banda para atención médica de exploración describe comunicación diferida y restricciones de evacuación y suministro. Esto motiva diseñar continuidad y autonomía; no permite equiparar una conexión terrestre lenta con toda la operación espacial. [NASA/TM-2019-220335](https://ntrs.nasa.gov/citations/20200001702).

La arquitectura del proyecto propone navegador → FastAPI → PostgreSQL/Supabase. Para conexiones de pool transaccional, la documentación de Supabase explica consideraciones de conexiones y prepared statements; esa configuración no elimina la necesidad de enlace al servicio. [Supabase, conexión a PostgreSQL](https://supabase.com/docs/guides/database/connecting-to-postgres).

## Resultado ejecutado en la versión examinada

La [evidencia JSON](../evidencias/010_operacion.json) conserva comandos, salida y respuestas de pruebas HTTP dentro del proceso, con Python 3.13.1:

| Comprobación | Resultado | Interpretación |
| --- | --- | --- |
| Dos pruebas de contrato y artefacto. | Aprobadas, salida 0. | Verifican datos, no el flujo de producto. |
| Validador del paquete. | 46 controles PASS, salida 0. | Consistencia con reglas del paquete, no validación clínica. |
| Datos P0. | 4.320 observaciones, seis perfiles sintéticos, 92 nulos. | Selección preparada para demo. |
| GET `/api/health`. | HTTP 200; `status=scaffold`, `database_checked=false`. | Responde el esqueleto; no asegura conectividad ni salud de la base. |
| GET `/api/profiles`, `/api/indicators` y panel de ejemplo. | HTTP 404. | Rutas de producto todavía no implementadas. |
| POST `/api/observations` con ejemplo ficticio. | HTTP 404. | No se realizó un guardado ni se contactó Supabase. |

Los 404 describen el estado actual; no son pruebas de aceptación aprobadas. El cliente fue TestClient de FastAPI, sin servidor público ni condiciones de red espacial. El frontend sigue reservado y ahora contiene logo y tokens visuales; eso no demuestra interacción funcional.

## Matriz de fallos a investigar

| Condición | Comportamiento exigible propuesto | Evidencia necesaria | Estado |
| --- | --- | --- | --- |
| API no disponible | Mensaje de indisponibilidad y borrador preservado según alcance. | Desconectar API durante una tarea y comprobar recuperación. | Pendiente de flujo integrado. |
| Supabase sin conexión | No confirmar guardado; conservar borrador durante sesión. | Simular timeout y verificar ausencia de confirmación falsa. | Pendiente; no se tocó base real. |
| Respuesta perdida después de escritura | Reintento idempotente con mismo UUID. | Comprobar una sola fila y conflicto ante contenido distinto. | Diseñado; no verificado remotamente. |
| Lectura antigua o faltante | Fecha visible, hueco o «no disponible». | Casos fijos y comparación tabla/gráfica. | Pendiente de interfaz. |
| Datos fuera de dominio o incompatibles | Rechazo explicado sin guardado parcial. | Pruebas API y SQL con entorno de prueba. | Restricciones escritas; falta prueba integrada. |
| Perfil/origen cambiado | No mezclar historiales ni referencias. | Ensayos con perfiles y fuentes distintos. | Contrato preparado; flujo pendiente. |
| Cierre o reinicio | Comprobar qué persiste y qué borrador puede perderse. | Reinicio controlado de cliente y servidor. | Pendiente; no prometer borrador durable. |

## Arquitectura frente a objetivo de autonomía

Conviene distinguir tres niveles:

1. **Demo conectada:** persiste en servicio remoto cuando hay conexión. Es el alcance presente, aún por integrar.
2. **Aplicación local con datos durables:** requiere base o almacenamiento local, copia de recursos, recuperación y pruebas; no basta un frontend servido localmente.
3. **Operación distribuida con demoras:** añade cola durable, sincronización, conflictos, auditoría, seguridad y procedimientos de operación. Es investigación futura, no capacidad existente.

La prioridad es terminar y medir el nivel elegido, no añadir microservicios ni simular un sistema certificado. Antes de anunciar offline deben probarse recarga, cierre, reinicio, reintentos y persistencia sin enlace externo.

## Decisiones propuestas y límites

Mantener la distinción «registro enviado» / «guardado confirmado»; registrar calidad, origen y tiempo; versionar comparaciones; no presentar datos del calendario ficticio como actuales. La configuración SQL y las políticas RLS escritas necesitan verificación en un entorno autorizado y no reemplazan controles en la API.

No se midieron rendimiento, consumo de energía, resistencia a radiación, precisión de sensores, usabilidad ni seguridad completa. No se instalaron dependencias, aplicaron migraciones o publicaron cambios. Estas comprobaciones no convierten el software en un sistema apto para vuelo.

## Cierre

La investigación operativa y las pruebas locales están terminadas para el commit fijado. La siguiente evidencia útil será un flujo completo guardado–consulta–reinicio y una prueba de fallo de enlace. Hasta entonces, el mensaje comercial debe hablar de desarrollo y de seguimiento propuesto, sin anunciar autonomía offline ni monitoreo en tiempo real implementado. Se continúa con privacidad y aceptación.

Fuentes técnicas: [requisitos](https://github.com/Jd1278/ARTEMIS/blob/80be128b17b5046ecd267d5a0604bbc5c74f5444/artemis-healt/docs/requirements.md), [entrada API](https://github.com/Jd1278/ARTEMIS/blob/80be128b17b5046ecd267d5a0604bbc5c74f5444/artemis-healt/src/artemis_health/main.py), [documentación Supabase](https://github.com/Jd1278/ARTEMIS/blob/80be128b17b5046ecd267d5a0604bbc5c74f5444/artemis-healt/docs/supabase.md).
