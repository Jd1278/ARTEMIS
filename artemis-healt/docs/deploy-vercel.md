# Despliegue del código del equipo en Vercel

Base local actualizada mediante fast-forward a `origin/main`, commit `ba70824` (PR #1, frontend-p0 integrado). No se mezcló el frontend anterior. El respaldo completo del frontend y del Git anidado se guardó en `.local-backups/20261114-before-team-ba70824/` de la raíz del workspace, excluido de Git. No borrar este respaldo hasta revisar la versión nueva.

## Proyecto existente

El proyecto anterior fue eliminado por el usuario. Se creó `artemis-health` en `jd1279w-1611s-projects`. Dominio nuevo: https://artemis-health-five.vercel.app. Settings → Build and Deployment:

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

## Estado del despliegue

El usuario autorizó la cuenta y la creación del proyecto nuevo. Vercel asignó automáticamente el primer despliegue a producción. Estado Ready, deployment `dpl_By2ncQZJgHfdMYJTn9UVGoKxBGoW`. El usuario autorizó explícitamente conectar GitHub y habilitar los despliegues automáticos. Raíz artemis-healt, FastAPI, Node 24 y salida automática aplicados. No se desactivó la protección de despliegues.

Verificación HTTP real del dominio nuevo: `/`, `/history`, `/log` y `/learn` responden 200, así como el JS y CSS del build. POST `/api/observations` responde 403 READ_ONLY_DEMO. `/api/health` responde 503 SUPABASE_UNAVAILABLE porque falta configurar DATABASE_URL; no se afirma que el flujo de datos esté operativo.

El conector Supabase confirmado apunta a `qupghjvxflmkzasaubwb`. La revisión completa encontró los datos en el esquema privado `artemis`: 6 perfiles, 4 indicadores y 4320 observaciones. El esquema public está vacío; no confundirlo con una base sin datos. No se ejecutaron migraciones ni se cambió el esquema expuesto.

Pendiente: el usuario añadirá DATABASE_URL como variable sensible de servidor en Production y Preview. Después se requiere un redeploy y verificar salud, perfiles, dashboard e historial contra Supabase. No pegar credenciales en Git o en chats. El sitio está desplegado, pero su API de datos no está operativa hasta completar ese paso.

### Verificación final · 14 de noviembre de 2026

El usuario corrigió la conexión para usar el pooler compartido y realizó un nuevo redeploy. Producción activa: `dpl_r6RDhjjnxtHhbpjbN8yM5nBfzkfD`, estado Ready, dominio https://artemis-health-five.vercel.app.

La comprobación real desde producción confirmó HTTP 200 en `/api/health` con `database_connected: true`, `/api/profiles` con 6 perfiles, dashboard CM-01 con 4 indicadores, historial de sueño entre 1 y 29 de abril de 2026 con 29 observaciones, y comparación de sueño para el 29 de abril. Esto sustituye el estado de API pendiente registrado arriba. No se leyó ni se imprimió el secreto de conexión, ni se modificaron los datos de Supabase.

La configuración de Preview debe revisarse por separado: la primera variable inspeccionada estaba asignada solo a Production. No se afirma haber probado Preview con base de datos. Tampoco se afirma persistencia de nuevas escrituras: la demo pública mantiene la barrera de solo lectura.

Referencias oficiales: [FastAPI en Vercel](https://vercel.com/docs/frameworks/backend/fastapi), [configuración de proyecto](https://vercel.com/docs/project-configuration). La guía de FastAPI documenta app.py como entrada admitida, el Build Command y el uso de StaticFiles para servir el frontend.
