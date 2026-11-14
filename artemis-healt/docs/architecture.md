# Arquitectura monolítica modular
Un despliegue FastAPI sirve /api y archivos estáticos React. PostgreSQL en Supabase compartida, con tablas propiedad de cada módulo, migraciones ordenadas y transacciones por caso de uso. No usar peticiones HTTP entre módulos ni bases separadas. Router → servicio → repositorio; análisis consulta el servicio de observaciones. Platform contiene configuración, conexión y errores comunes, no reglas de negocio.

Profiles posee profiles; Observations posee observations e import_batches; Analysis posee notices y rule_versions; Education posee fichas empaquetadas; Research posee studies y research_observations P1. Las claves de perfil son obligatorias. La base no se distribuye con datos personales.

Contrato API a implementar: GET /api/profiles; GET /api/indicators; GET /api/profiles/{id}/dashboard; POST /api/observations; GET /api/profiles/{id}/observations?indicator=&from=&to=; GET /api/profiles/{id}/comparison?indicator=&at=; GET /api/education/{indicator}. Creación 201, repetición idéntica 200, UUID conflictivo 409, validación 422. Fechas ISO 8601 UTC; filtros inclusivos. IDs UUID para captura y deterministas para importación. Error con code, message, fields, request_id.

No inventar lockfiles: al implementar frontend resolver versiones y fijarlas junto con el entorno Python probado. Para desarrollo pueden funcionar Vite y API como dos procesos; en entrega solo existe el servidor monolítico. Navegación SPA deberá incorporar fallback de rutas antes de publicar.

