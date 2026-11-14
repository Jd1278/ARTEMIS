# Capa de datos compartida

Estado: servidor MCP configurado para el proyecto qupghjvxflmkzasaubwb y autenticación OAuth completada. Codex confirma enabled y OAuth. Las herramientas deben cargarse en una sesión actualizada antes de inspeccionar el proyecto remoto y aplicar la migración. El esquema y los datos aún no se han aplicado ni verificado en remoto. PostgreSQL reemplaza SQLite como objetivo de persistencia; todo el equipo usa la misma base de desarrollo.

## Creación y aplicación
1. Conectar Supabase y seleccionar organización/proyecto. Para crear proyecto nuevo, confirmar región y cualquier coste antes de provisionar.
2. Obtener desde Connect una conexión directa o de pool en modo sesión para el operador de migraciones. Guardar DATABASE_ADMIN_URL únicamente en su entorno local.
3. Instalar dependencias: `pip install -e .`. Configurar las variables en el entorno del proceso: los scripts no leen .env automáticamente.
4. Ejecutar `python scripts/database.py migrate`, después `python scripts/database.py seed` y `python scripts/database.py verify` desde la raíz del proyecto.
5. Resultado esperado: seis perfiles, cuatro indicadores, 4320 observaciones sintéticas y 92 valores nulos. Repetir seed no debe duplicar. Un cambio del dataset con IDs existentes falla y revierte toda la transacción; requiere migración explícita, nunca sobrescritura silenciosa.

## Acceso de la aplicación
El esquema artemis es privado y no debe añadirse a los esquemas expuestos de Data API. anon y authenticated no acceden a estas tablas. Las políticas RLS permiten acceso al rol de grupo artemis_backend únicamente, con lectura de perfiles e indicadores y lectura/escritura de observaciones de demo según políticas.

Crear mediante administración un usuario PostgreSQL LOGIN dedicado, sin superusuario ni BYPASSRLS, miembro de artemis_backend. Su contraseña se genera y guarda fuera del repositorio. Ese usuario se utiliza en DATABASE_URL. El rol artemis_backend NOLOGIN no tiene contraseña y no es por sí solo un usuario de conexión. No usar postgres ni service_role en el navegador. El operador de migraciones usa permisos administrativos, fuera del runtime.

En Vercel usar la URL de Supavisor en modo transacción obtenida del panel para ese usuario, con TLS. El código desactiva prepared statements y cierra conexiones por operación. No ejecutar migraciones ni seed al arrancar una función. DATABASE_ADMIN_URL no se despliega. No existe acceso directo desde React: navegador → API → PostgreSQL.

RLS aquí protege frente a clientes públicos, no separa miembros del equipo que usan el backend. Antes de exponer endpoints de escritura, implementar autenticación y autorización en la API; hasta entonces mantener despliegue privado o demo de lectura. No repartir la contraseña administradora entre integrantes: invitarlos a la organización con permisos adecuados y coordinar migraciones por Git.

## Tablas
profiles: perfiles ficticios. indicators: unidades y dominios. observations: mediciones y calidad con claves foráneas. import_batches: hashes y trazabilidad. rule_versions: reglas descriptivas. notices: explicación y observaciones de referencia. schema_migrations: versión y checksum.

SQL impide valores no finitos, unidades/contextos incompatibles, escalas inválidas y valores de análisis no nulos marcados como imputados. Source_value conserva la cifra previa. Los datos públicos P1 tendrán su importador auditado; no se cargan con este seed.

## Verificación pendiente en remoto
El usuario informa que ejecutó `001_initial.sql` en SQL Editor. Falta comprobar el resultado remoto. Para cargar sin credenciales locales, ejecutar el archivo completo `scripts/sql/load_demo.sql` en SQL Editor. Se genera con `python scripts/export_seed_sql.py` a partir de los JSON empaquetados y sus hashes. La transacción verifica coincidencia de campos y conteos; repetirla no duplica ni sobrescribe. Resultado esperado: observations=4320, profiles=6, indicators=4, null_values=92.

La ejecución manual de la migración no registra por sí sola su checksum en schema_migrations. No ejecutar `database.py migrate` sobre ese esquema hasta reconciliar la migración manual con el esquema inspeccionado. Seed y verify pueden ejecutarse independientemente. No volver a ejecutar 001_initial.sql para cargar datos.

Aplicar migración y seed; ejecutar verify; repetir seed; probar rechazos de dominio y acceso denegado como anon/authenticated, y permisos del usuario backend. Los tests locales no sustituyen estas pruebas PostgreSQL.

Fuentes: https://supabase.com/docs/guides/database/connecting-to-postgres y https://supabase.com/docs/guides/database/postgres/row-level-security

