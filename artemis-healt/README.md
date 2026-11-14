# ARTEMIS HEALTH — Application guide

React/TypeScript frontend and FastAPI backend for a fictional astronaut wellbeing demo. See the [project overview](../README.md) for functionality, data generation, cited sources and AI disclosure.

**[Public demo](https://artemis-health-five.vercel.app/)** — synthetic, read-only and non-clinical. Screens: Overview, Log, History, Learn and `/components`. A visible form does not authorize public writes.

## Requirements

- Python 3.11 or later.
- Node.js 24 for consistency with deployment; use the committed frontend lockfile.
- Supabase PostgreSQL for production; SQLite is available for local development.

## Backend setup

From the repository root:

```powershell
cd artemis-healt
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -e .
Copy-Item .env.example .env
```

On Linux/macOS, activate with `source .venv/bin/activate` and copy with `cp .env.example .env`.

For local development without PostgreSQL, use `ARTEMIS_STORAGE=sqlite` and leave `DATABASE_URL` empty. The default local database is `var/artemis_health.db`, seeded from the committed fixture. Local development permits writes; do not enter real personal data.

For PostgreSQL, set `ARTEMIS_STORAGE=postgres`, `ARTEMIS_MODE=demo` and backend-only `DATABASE_URL` using the Supabase pooler with TLS. Keep secrets out of Git, logs and browser variables. `DATABASE_ADMIN_URL` is reserved for an authorized migration operator and must not be deployed.

```powershell
uvicorn artemis_health.main:app --app-dir src --host 127.0.0.1 --port 8000 --reload
```

Swagger: `http://127.0.0.1:8000/docs`; OpenAPI: `http://127.0.0.1:8000/openapi.json`. This development entrypoint does not apply the public deployment's read-only middleware.

## Frontend setup

In another terminal, from `artemis-healt/frontend`:

```powershell
npm ci
npm run dev
```

Open `http://localhost:5173`. Development HTTP mode proxies `/api` to the local backend. Production uses same-origin `/api`.

For the isolated browser demonstration without a backend:

```powershell
npm run dev:mock
```

Mock mode is explicit; its writes do not demonstrate database persistence and must not disguise production API failures.

## API capabilities

Routes are available under `/api`. Consult the [endpoint guide](docs/api_endpoints.md) and running OpenAPI for exact parameters and response schemas.

| Method | Path under `/api` | Purpose |
| --- | --- | --- |
| GET | `/health` | API/database health. |
| GET | `/indicators` | Indicator domains, units and contexts. |
| GET | `/profiles` | Fictional demo profiles. |
| GET | `/profiles/{id}/dashboard` | Historical overview and comparisons. |
| GET | `/profiles/{id}/observations` | Filtered observation history. |
| GET | `/profiles/{id}/trends` | Historical series preserving nulls. |
| GET | `/profiles/{id}/comparison` | Backend `baseline_v1` response. |
| POST | `/observations` | Development contract with UUID idempotency: 201/200, conflict 409, validation 422. Blocked publicly. |
| POST | `/checkins` | Separate legacy check-in contract using 1–5 scales. Blocked publicly. |
| GET | `/education` | Educational content; consult OpenAPI for aliases. |
| GET | `/research/datasets` | Research metadata, separate from the demo. Does not imply a released research screen. |

The frontend requests history with `strict_indicator=true` to separate legacy scales from fatigue 1–7 and stress 0–100. Connected comparisons are supplied by the backend.

## Demo data and database operations

`data/demo/observations.json` contains 4,320 slots across six profiles, 180 days and four indicators, including 92 null values in the committed manifest. `scripts/prepare_demo.py` adapts the synthetic daily log, excludes flagged imputation/out-of-range values, retains provenance and generates deterministic UUIDs and hashes.

```powershell
python scripts/prepare_demo.py
```

This overwrites the local fixture and manifest; inspect the diff. It does not update production.

For an explicitly selected, authorized database only:

```powershell
python scripts/database.py migrate
python scripts/database.py seed
python scripts/database.py verify
```

Migration and seed commands modify their target. They are not required to inspect an already provisioned production deployment. Review the [Supabase guide](docs/supabase.md) and migrations first. The application uses the private `artemis` schema.

## Verification

Backend, from `artemis-healt` with the virtual environment active:

```powershell
pytest -v
```

Frontend, from `artemis-healt/frontend`:

```powershell
npm run typecheck
npm test
npm run build
npm run test:e2e
```

The browser regression uses mock mode and tests playback/navigation after a simulated translation mutation. On Windows, Playwright expects Chrome at `C:/Program Files/Google/Chrome/Application/chrome.exe`. Other systems use Playwright Chromium, which may require `npx playwright install chromium`. This test does not verify PostgreSQL persistence or production writes. These commands are instructions, not a claim that every suite ran for each documentation update.

## Current Vercel deployment

Frontend and backend are packaged in one project:

- Root Directory: `artemis-healt`.
- Framework: FastAPI; entrypoint: `app.py`.
- Build: `npm --prefix frontend ci && npm --prefix frontend run build`.
- Frontend output: `frontend/dist`, served by FastAPI with SPA route support.
- Node.js 24 for the frontend build; Python for FastAPI.
- Backend environment: `ARTEMIS_MODE=demo`, `ARTEMIS_STORAGE=postgres`, secret `DATABASE_URL`.
- Browser API base: `/api`. Database credentials must never use a `VITE_` prefix.

`app.py` rejects methods other than GET, HEAD and OPTIONS with `403 READ_ONLY_DEMO`. The public Log form cannot persist submissions. Keep this boundary until an appropriate authenticated write flow is authorized and implemented. The GitHub-connected project deploys updates to `main` automatically.

## Code map

| Directory | Responsibility |
| --- | --- |
| `frontend/src/features/` | Overview, recording, history, comparisons and education. |
| `frontend/src/services/` | Domain types, HTTP adapter and isolated mock implementation. |
| `frontend/src/design-system/` | Tokens, styles, components and illustrations. |
| `src/artemis_health/routers/` | REST endpoints. |
| `src/artemis_health/schemas/` | Pydantic validation. |
| `src/artemis_health/services/` | Domain behavior and `baseline_v1`. |
| `src/artemis_health/repositories/` | PostgreSQL/SQLite adapters. |
| `migrations/` | PostgreSQL schema and policies. |
| `tests/`, `frontend/e2e/` | Backend and browser checks. |

References: [architecture](docs/architecture.md), [requirements](docs/requirements.md), [dataset review](docs/review.md), [audit artifact](docs/dataset-audit.json), [visual system](docs/visual/README.md), [English source audit](../Investigation/Inglés/reports/008_source_and_transformation_audit.md). Some supporting documents describe earlier plans; current code and deployment configuration establish implemented behavior.
