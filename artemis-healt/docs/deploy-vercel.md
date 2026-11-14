# Despliegue del código del equipo en Vercel

Base local actualizada mediante fast-forward a `origin/main`, commit `ba70824` (PR #1, frontend-p0 integrado). No se mezcló el frontend anterior. El respaldo completo del frontend y del Git anidado se guardó en `.local-backups/20261114-before-team-ba70824/` de la raíz del workspace, excluido de Git. No borrar este respaldo hasta revisar la versión nueva.

## Proyecto existente

Dominio indicado: https://artemis-two-pi.vercel.app. En el proyecto propietario de ese dominio, revisar Settings → Build and Deployment:

| Ajuste | Valor |
| --- | --- |
| Git repository | Jd1278/ARTEMIS |
| Production branch | main |
| Root Directory | artemis-healt |
| Framework Preset | FastAPI |
| Build Command | npm --prefix frontend ci && npm --prefix frontend run build |
| Output Directory | Sin override; no configurar frontend/dist como un proyecto Vite aislado |
| Node.js | 24.x, compatible con el Vite del lockfile |

`app.py` exporta el mismo objeto FastAPI del equipo y permite importar el layout `src/`. FastAPI sirve `/api` y el build React `frontend/dist`, con el fallback SPA existente. `vercel.json` configura el build y exige almacenamiento PostgreSQL; no se cambia a dos servicios.

La entrada de despliegue deniega POST/PUT/PATCH/DELETE con 403 READ_ONLY_DEMO. La aplicación local original del equipo conserva su lógica; la demo pública permanece en solo lectura hasta que exista autorización de escritura adecuada. No quitar esta barrera para habilitar escrituras anónimas.

`frontend/.env.production` fija `VITE_API_MODE=http`. Evita que el modo mock sea la selección implícita del build de producción. El cliente solicita `/api` del mismo origen; no necesita una clave de Supabase ni una URL administrativa en VITE_*.

## Variables del servidor

Configurar desde Vercel → Environment Variables, nunca en el navegador ni en Git:

- `DATABASE_URL`: conexión PostgreSQL/Supabase de ejecución, preferiblemente pooler compatible con serverless. Usar el secreto existente, no pegarlo en chats.
- `ARTEMIS_STORAGE=postgres` y `ARTEMIS_MODE=demo`: ya declarados como valores no secretos en vercel.json.

No habilitar SQLite en producción: el filesystem de la función no es almacenamiento persistente. No usar `/tmp` como sustituto de una base de datos persistente. No se ejecutan migraciones ni seeds de producción automáticamente; el equipo debe comprobar que el esquema y los perfiles ya existen antes de publicar. La configuración de la base de datos y su autorización se revisan por separado.

`.vercelignore` excluye secretos locales, venv, caches y archivos de la base local. Las credenciales administrativas permanecen fuera del frontend y del bundle público.

## Comprobaciones

Frontend: `npm ci`, `npm run typecheck`, `npm test`, `npm run build` desde frontend. Conservar las dependencias del equipo y su package-lock. El build advierte que el bundle principal supera 500 kB; no se cambió el diseño ni se hizo una optimización ajena al despliegue.

Backend: crear un venv, instalar requirements y ejecutar pytest. La prueba adicional `test_vercel_entrypoint.py` verifica que el adaptador mantiene OpenAPI, niega escrituras y, con dist presente, sirve raíz/rutas SPA sin convertir rutas API ni assets inexistentes en HTML.

Resultado local de esta preparación: typecheck correcto, 15 tests de frontend aprobados, build correcto con aviso de bundle >500 kB, y 21 tests de backend aprobados. Pytest informó 10 avisos de deprecación de Starlette/FastAPI, sin fallos. No se comprobó todavía el runtime de Vercel ni la conexión de Supabase en producción. La preview local usa una base separada `var/team-preview.db`, sin conectar ni migrar la base de producción.

Antes de producción, hacer un preview autenticado en el proyecto correcto y comprobar `/`, `/history`, `/api/health`, `/api/profiles`, assets, solicitudes reales del frontend y rechazo de POST. Confirmar la conexión de Supabase desde el servidor. Una compilación local correcta no demuestra que las variables o la base estén configuradas en Vercel.

## Estado del acceso

La CLI local de Vercel devolvió Logged out. No se modificaron ajustes remotos, secretos ni despliegues. No se hizo push ni se lanzó un deployment temporal. Para aplicar: iniciar sesión en la cuenta propietaria, revisar los ajustes anteriores, publicar los cambios preparados mediante el flujo Git del equipo y comprobar un preview antes de promover producción.

Referencias oficiales: [FastAPI en Vercel](https://vercel.com/docs/frameworks/backend/fastapi), [configuración de proyecto](https://vercel.com/docs/project-configuration). La guía de FastAPI documenta app.py como entrada admitida, el Build Command y el uso de StaticFiles para servir el frontend.
