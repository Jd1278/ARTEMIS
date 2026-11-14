# ARTEMIS HEALTH — Backend REST (FastAPI + PostgreSQL/Supabase)

Plataforma web informativa y educativa de seguimiento y visualización de indicadores de bienestar para un perfil ficticio de astronauta (`DEMO / SIMULADO`).

> **Alcance No Clínico:** ARTEMIS HEALTH no es un dispositivo médico. No diagnostica, no predice enfermedades, no prescribe tratamientos, no calcula puntuaciones globales de salud ni genera recomendaciones clínicas.

---

## 1. Arquitectura y Organización del Proyecto

El backend sigue una arquitectura modular por capas dentro de `src/artemis_health/`:

```text
artemis-healt/
├── data/demo/                 # Contrato de datos semilla (observations.json y manifest.json)
├── docs/                      # Requisitos, arquitectura, auditoría de datasets y documentación API
│   └── api_endpoints.md       # Documentación completa de endpoints y ejemplos JSON
├── migrations/                # Esquema PostgreSQL y políticas RLS para Supabase
│   ├── 001_initial.sql        # Esquema privado artemis, dominios, triggers y RLS base
│   └── 002_complete_schema.sql# Tablas checkins, educational_content, research_datasets y perfiles
├── scripts/                   # Utilidades de preparación, migración y exportación SQL
│   ├── prepare_demo.py        # Genera data/demo/observations.json desde crew_daily_log_clean.csv
│   ├── database.py            # Comandos migrate, seed y verify contra Supabase PostgreSQL
│   └── export_seed_sql.py     # Genera scripts/sql/load_demo.sql para Supabase SQL Editor
├── src/artemis_health/
│   ├── main.py                # Punto de entrada FastAPI, CORS, OpenAPI y montaje de rutas
│   ├── core/                  # Configuración (.env), constantes de dominio, excepciones y logs seguros
│   ├── database/              # Conexiones TLS PostgreSQL/Supabase, SQLite local y datos semilla
│   ├── models/                # Entidades de dominio tipadas
│   ├── schemas/               # Esquemas y validadores estrictos Pydantic v2
│   ├── repositories/          # Repositorios parametrizados (SupabasePostgresRepository y SQLiteWellnessRepository)
│   ├── services/              # Lógica de negocio y algoritmo causal de mediana (baseline_v1)
│   ├── routers/               # Endpoints REST desacoplados de la lógica de negocio
│   └── modules/               # Re-exportación modular compatible (profiles, observations, analysis, education, research)
├── tests/                     # Suite de pruebas automatizadas (pytest y unittest)
├── .env.example               # Plantilla de variables de entorno sin secretos
├── pyproject.toml             # Metadatos del paquete y configuración de pytest
└── requirements.txt           # Dependencias de producción y pruebas
```

---

## 2. Instalación y Configuración

### Requisitos previos
- Python 3.11+
- Proyecto en Supabase PostgreSQL (para producción/despliegue remoto) o modo persistente local automático (`var/artemis_health.db`) para desarrollo y pruebas sin conexión.

### Instalación
```bash
cd artemis-healt
python -m venv .venv
# En Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# En Linux/macOS:
# source .venv/bin/activate

pip install -r requirements.txt
pip install -e .
```

### Variables de Entorno (`.env`)
Copia `.env.example` a `.env` y completa las variables según el entorno:
```bash
cp .env.example .env
```
- `ARTEMIS_MODE=demo`
- `ARTEMIS_STORAGE=auto` (`auto` selecciona PostgreSQL/Supabase si `DATABASE_URL` está definida; de lo contrario utiliza SQLite persistente local en `var/artemis_health.db` auto-sembrado con las 4.320 observaciones simuladas).
- `DATABASE_URL`: Cadena de conexión PostgreSQL de Supabase (Supavisor en modo transacción con TLS).
- `DATABASE_ADMIN_URL`: Cadena exclusiva para ejecutar migraciones desde el entorno local (no desplegar en producción).
- `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`: Credenciales opcionales de Supabase (**jamás exponer `SUPABASE_SERVICE_ROLE_KEY` al frontend**).
- `CORS_ORIGINS`: Lista separada por comas de dominios permitidos (ej. `http://localhost:5173,https://tu-frontend.vercel.app`).

---

## 3. Base de Datos en Supabase y Semilla de Datos

1. Aplicar las migraciones SQL (`migrations/001_initial.sql` y `migrations/002_complete_schema.sql`) y cargar la semilla verificada:
   ```bash
   python scripts/database.py migrate
   python scripts/database.py seed
   python scripts/database.py verify
   ```
   *(Alternativamente, en el SQL Editor de Supabase puedes ejecutar `migrations/001_initial.sql`, `migrations/002_complete_schema.sql` y `scripts/sql/load_demo.sql`).*

2. Regenerar el contrato local desde el dataset fuente (opcional, determinista):
   ```bash
   python scripts/prepare_demo.py
   ```

---

## 4. Ejecución del Servidor API

```bash
uvicorn artemis_health.main:app --app-dir src --host 0.0.0.0 --port 8000 --reload
```
- Documentación interactiva Swagger UI: `http://localhost:8000/docs`
- Especificación OpenAPI JSON: `http://localhost:8000/openapi.json`

---

## 5. Endpoints Disponibles

Todas las rutas responden tanto en la raíz como bajo el prefijo `/api`:

| Método | Ruta | Descripción |
| :--- | :--- | :--- |
| `GET` | `/health` (`/api/health`) | Estado de la API y conexión a Supabase / base de datos. |
| `GET` | `/indicators` (`/api/indicators`) | Catálogo de los indicadores, unidades permitidas y dominios técnicos. |
| `GET` | `/profiles` (`/api/profiles`) | Lista de perfiles ficticios de demostración (`demo`, `CM-01`..`CM-06`). |
| `GET` | `/profiles/demo/dashboard` (`/profiles/{id}/dashboard`) | Resumen de los 4 indicadores, último valor y comparación con mediana personal. |
| `POST` | `/observations` (`/api/observations`) | Registrar observación validada con idempotencia por UUID (`201`, `200`, `409`). |
| `GET` | `/profiles/demo/observations` (`/profiles/{id}/observations`) | Historial filtrable por `indicator`, `from` y `to` en orden cronológico. |
| `GET` | `/profiles/demo/trends` (`/profiles/{id}/trends`) | Series cronológicas para Recharts sin interpolar huecos (`value: null`). |
| `GET` | `/profiles/demo/comparison` (`/profiles/{id}/comparison`) | Detalle de la línea base personal (`baseline_v1`) para un indicador y fecha. |
| `POST` | `/checkins` (`/api/checkins`) | Registrar seguimiento diario de bienestar (fatiga 1–5, estrés 1–5 y notas). |
| `GET` | `/educational-content` (`/api/education`) | Fichas educativas con unidad, limitaciones y referencia bibliográfica. |
| `GET` | `/research/datasets` (`/api/research/datasets`) | Metadatos de datasets públicos/análogos aislados del espacio `demo`. |

Consulta ejemplos detallados de solicitudes y respuestas en [docs/api_endpoints.md](docs/api_endpoints.md).

---

## 6. Ejecución de Pruebas Automatizadas

```bash
pytest -v
python -m unittest discover -s tests -v
```

---

## 7. Despliegue Independiente e Integración con Frontend en Vercel

- **Backend (Render, Railway, Fly.io, Cloud Run o VPS con contenedor/Uvicorn):**
  - Comando de inicio: `uvicorn artemis_health.main:app --app-dir src --host 0.0.0.0 --port $PORT`
  - Variables de entorno requeridas en el servicio backend: `DATABASE_URL`, `ARTEMIS_MODE=demo`, `CORS_ORIGINS=https://<tu-dominio-en-vercel>.vercel.app`.
- **Frontend (Vercel — React + Vite + TypeScript + Recharts):**
  - Configurar en Vercel únicamente la URL pública del backend: `VITE_API_BASE_URL=https://<tu-backend-url>`.
  - Nunca configurar `DATABASE_URL`, `DATABASE_ADMIN_URL` ni `SUPABASE_SERVICE_ROLE_KEY` en las variables del frontend.
