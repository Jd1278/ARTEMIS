# ARTEMIS HEALTH

Monolito modular con base compartida. Una aplicación FastAPI, un proceso de ejecución y una base PostgreSQL en Supabase. React se compila y se sirve desde la misma aplicación; Vite se usa únicamente durante desarrollo. No hay microservicios.

## Estado
La capa PostgreSQL para Supabase está preparada en `migrations/001_initial.sql`. Aprovisionamiento y aplicación remota pendientes. Seguir [configuración Supabase](docs/supabase.md). Se requiere conexión a internet para persistir; offline completo queda diferido.
Estructura inicial y contrato de datos preparados. Las funciones del producto todavía no están implementadas. La fuente normativa es docs/requirements.md; los documentos ASTROGUARD quedan sustituidos.

## Preparar datos
Desde esta carpeta: `python scripts/prepare_demo.py`. Solo necesita la biblioteca estándar. Lee ../artemis-sleep-dataset y genera data/demo/observations.json y manifest.json, sin modificar la fuente. `python -m unittest discover -s tests` verifica la preparación.

## API mínima
Crear un entorno virtual, instalar con `pip install -e .` y ejecutar `uvicorn artemis_health.main:app --app-dir src`. GET /api/health expone el estado del esqueleto. Esta instalación aún requiere resolver dependencias; el MVP no está terminado. El frontend P0 está en `frontend/` (ver sección Frontend).

## Organización
- src/artemis_health/modules: perfiles, observaciones, análisis, educación e investigación.
- src/artemis_health/platform: configuración y conexión PostgreSQL en Supabase compartidas.
- frontend: interfaz React, tokens y componentes.
- data/demo: contrato de demostración generado; var: persistencia local ignorada por Git.
- docs: requisitos finales, arquitectura, auditoría y diseño.
- scripts: preparación reproducible; tests: pruebas.

La carpeta fuente ../artemis-sleep-dataset es necesaria para regenerar datos. La distribución de ejecución empaquetará solo data/demo y frontend/dist. No ejecutar run_all.sh de la fuente como parte del arranque.


## Frontend
React + TypeScript + Vite. Especificación y prompt de generación: [docs/frontend-prompt.md](docs/frontend-prompt.md).

Desde `frontend/`:
- `npm install` (requiere Node 20+; el lockfile fija versiones).
- `npm run dev`: abre http://localhost:5173. Por defecto usa `VITE_API_MODE=mock`, que implementa el contrato API en el navegador sobre `data/demo/observations.json`. No necesita backend; las capturas manuales viven en memoria y se pierden al recargar.
- `VITE_API_MODE=http npm run dev`: llama a `/api`, que Vite redirige a `http://localhost:8000` (uvicorn).
- `npm test`: pruebas de la regla `baseline_v1`. `npm run build`: genera `frontend/dist`, que FastAPI sirve en entrega.

Pantallas: Resumen, Registrar, Historial, Aprender y `/componentes` (galería interna, con interruptor para simular caída del servidor). La regla de comparación del mock (`src/features/analysis/baseline.ts`) sirve de referencia para la implementación del backend. Las referencias de las fichas educativas están marcadas como pendientes de revisión.
