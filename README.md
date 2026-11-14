# ARTEMIS HEALTH

An educational web prototype for exploring astronaut wellbeing indicators across a fictional space mission, developed for NASA Space Apps Challenge 2026.

**[Open the public demo](https://artemis-health-five.vercel.app/)** · [Application setup](artemis-healt/README.md) · [API documentation](artemis-healt/docs/api_endpoints.md) · [English research package](Investigation/Inglés/README.md)

ARTEMIS brings sleep, perceived fatigue, perceived stress and resting pulse into a single historical view. Its purpose is to make changes, missing measurements and data provenance understandable. The public demo uses fictional profiles and synthetic observations and is read-only.

> **Non-clinical scope:** this is not a medical device or an operational astronaut monitoring system. It does not diagnose conditions, predict disease, prescribe treatment or calculate a health score. NASA sources provide research context; they do not establish NASA endorsement or validate this application.

## Functionality

| Area | Implemented behavior |
| --- | --- |
| Mission overview | Six fictional profiles, CM-01 through CM-06; four indicator cards; historical mission cursor; day-by-day navigation and playback; mission-themed orbital visualization. The orbital view is illustrative, not live spacecraft telemetry. |
| Historical readings | Values retain their observation date and mission day. Selecting a mission day changes the historical view; the demo is not a live sensor feed. |
| Personal comparison | Previous median, signed difference in the same unit, days used, reference period and rule version. Explicit insufficient-history and excluded-value states. |
| History | Profile-specific indicator, inclusive day-range and origin filters; chart/table views in chronological order. The daily view retains the last observation for each day and origin. Missing or excluded values remain gaps. |
| Observation detail | Provenance and quality information, including original excluded values and source file/row where supplied. |
| Manual observation form | Indicator-specific validation, explicit UTC time, session draft, saving/error feedback and UUID-based retry handling. The public deployment rejects writes; the form cannot create production records. |
| Learning | Four indicator explanations covering meaning, scale, recording context and limitations. References marked pending review remain pending; no clinical advice is generated. |
| Interface | Responsive layouts, local Inter fonts, labelled controls, chart alternatives and route recovery. Browser translation is disabled to reduce DOM mutation conflicts with React. This is not a complete accessibility certification. |
| Developer gallery | `/components` displays reusable visual components. |

### Four indicators

| Indicator | API key | Unit / input domain | Interpretation boundary |
| --- | --- | --- | --- |
| Sleep duration | `sleep_duration_h` | Hours, 0–24 | Reported duration, not a sleep-quality or sleep-disorder diagnosis. |
| Perceived fatigue | `samn_perelli` | Integer points, 1–7 | 1: fully alert; 7: completely exhausted, unable to function effectively. Subjective fatigue is not a direct performance measurement. |
| Perceived stress | `stress_vas` | Points, 0–100 | No perceived stress to maximum perceived stress. Points are not percentages or diagnostic probabilities. |
| Resting pulse | `resting_hr_bpm` | Beats per minute, positive values | Context-dependent resting measurement; no healthy/unhealthy classification. |

These are technical input domains; backend validation remains authoritative. Legacy check-ins use separate 1–5 scales. The frontend requests strict indicator filtering to keep those separate from the four indicators above.

### How comparison works

In connected mode, the backend computes `baseline_v1`. It selects observations from the same profile, indicator, unit, context and origin, strictly before the reference calendar day. It considers the previous 30 days, uses at most the 14 most recent distinct valid days and requires at least 7. For multiple compatible observations on one day, it selects the latest.

Null, imputed and otherwise excluded observations do not enter the median. The difference is the selected value minus that median, in hours, scale points or bpm. Synthetic observations and manual self-reports are never pooled. This deterministic descriptive calculation is not an AI prediction or clinical alert. Offline mock mode has a separate implementation for demonstration and testing.

## Data used by the application

The dashboard uses only the four-indicator synthetic subset, not the complete research dataset:

| Property | Committed demo artifact |
| --- | --- |
| Crew | 6 fictional profiles |
| Mission | 180 days, starting 1 March 2026 |
| Observation slots | 4,320 = 6 profiles × 180 days × 4 indicators |
| Null values | 92 missing or excluded values |
| Namespace / origin / capture | `demo` / `synthetic` / `import` |
| Source | `artemis-sleep-dataset/data/processed/crew_daily_log_clean.csv` |
| Application transformation | `prepare_demo_v1` in `artemis-healt/scripts/prepare_demo.py` |

These counts describe the committed [manifest](artemis-healt/data/demo/manifest.json), not real astronauts or independent clinical samples. Observation metadata includes UUID, profile, indicator, value, unit, timestamp, mission day, context, origin, capture method, quality flags and source file/row. `source_value` preserves the adapter input when a value is excluded; it is not necessarily an untouched raw measurement.

### Generation and cleaning

1. **Simulation:** [`generate_raw.py`](artemis-sleep-dataset/scripts/generate_raw.py) uses NumPy's seeded random generator (`SEED = 2026`) to construct a fictional six-person, 180-day mission. Individual baselines, random variation and scripted adaptation, schedule-shift, workload and personal episodes shape the records. Relationships between sleep, fatigue, stress and vigilance are assumptions encoded by the team, informed by published work.
2. **Deliberate data problems:** the generator introduces missing values, duplicates, inconsistent formats and glitches to exercise cleaning. Injected episode labels are simulation labels, not independently observed outcomes.
3. **Cleaning:** [`clean.py`](artemis-sleep-dataset/scripts/clean.py) standardizes the daily log and produces quality flags and additional research columns. The inherited cleaner includes bidirectional interpolation and a mission-wide reference based on days 8–21. These retrospective operations can use future information and cannot establish prospective detection.
4. **Application adaptation:** [`prepare_demo.py`](artemis-healt/scripts/prepare_demo.py) selects four indicators, interprets flags per indicator, sets flagged imputed/out-of-range values to `null`, retains the adapter input in `source_value`, and assigns deterministic UUIDv5 identifiers. It writes observation JSON and a SHA-256 manifest. Inherited risk scores, countermeasures and episode labels are not adopted as personal health conclusions.
5. **Storage and display:** the fixture can seed SQLite locally or PostgreSQL in a configured environment. The chart retains nulls as gaps (`connectNulls=false`), without converting them to zero or interpolating across them.

Seeded simulation makes software scenarios reproducible; distribution similarity does not validate physiology, clinical safety or predictive accuracy. Exact regeneration also depends on input files and dependency versions.

## Research data and cited sources

The repository includes a broader research package. Its integrated long-format CSV has **20,080 rows** in the committed audit. That includes simulated values, transformed real observations and repeated environmental records; it is not a count of independent participants. Research `source` labels differ from the application's `origin_type` labels.

| Source / citation | Repository use and relevance | Limits |
| --- | --- | --- |
| [NASA: Five Hazards of Human Spaceflight](https://www.nasa.gov/hrp/hazards/) and [sleep and irregular schedules](https://www.nasa.gov/reference/risk-from-inadequate-sleep-and-irregular-schedules/) | Motivation for tracking sleep, fatigue and subjective wellbeing in mission context. | Background evidence, not evidence of ARTEMIS effectiveness. |
| Barger et al. (2014), *Prevalence of sleep deficiency and use of hypnotic drugs in astronauts before, during, and after spaceflight*. [DOI: 10.1016/S1474-4422(14)70122-X](https://doi.org/10.1016/S1474-4422(14)70122-X) | Published sleep observations informed simulation calibration. | Group statistics cannot validate individual synthetic trajectories. |
| Jones et al. (2022), *Sleep deficiency in spaceflight is associated with degraded neurobehavioral functions and elevated stress in astronauts on six-month missions aboard the ISS*. [DOI: 10.1093/sleep/zsac006](https://pmc.ncbi.nlm.nih.gov/articles/PMC8919197/) | Supports observing sleep alongside perceived stress and fatigue; informed the broader check-in simulation. | Associations do not prove causal effects or validate the app's rules. |
| Samn & Perelli (1982), *Estimating Aircrew Fatigue*, SAM-TR-82-21. [Original report](https://apps.dtic.mil/sti/pdfs/ADA125319.pdf) | Basis for the seven-point fatigue scale. | Subjective aviation scale; not a medical diagnosis or standalone fitness-for-duty decision. |
| Lesage, Berjot & Deschamps (2012), *Clinical stress assessment using a visual analogue scale*. [DOI: 10.1093/occmed/kqs140](https://doi.org/10.1093/occmed/kqs140) | Reference for perceived-stress VAS documentation. | Does not establish astronaut-specific thresholds; the in-app citation remains pending review. |
| [NASA OSDR OSD-575](https://osdr.nasa.gov/bio/repo/data/studies/OSD-575), Inspiration4 metabolic panel; [OSD-569](https://osdr.nasa.gov/bio/repo/data/studies/OSD-569), blood count | Preserved real blood-panel references (`real_nasa_osdr`); preflight distributions and postflight changes inform fictional labs (`simulated_from_real`). | Four civilian participants on a short flight; no daily records for the six fictional crew. Simulated labs remain synthetic and are outside the dashboard. |
| [NASA CDAWeb HAPI: ISS_DOSANL_TEPC](https://cdaweb.gsfc.nasa.gov/hapi/info?id=ISS_DOSANL_TEPC) | Historical ISS environmental radiation (`real_nasa_cdaweb`), using 1 March–27 August 2017 and mapping dates to the fictional calendar. | Processing includes scaling/imputation. Repetition per fictional crew adds no independent measurement. Area-monitor dose equivalent is not personal effective dose. Outside the dashboard. |
| [NASA Life Sciences Portal: UTMB Bed Rest Campaign 1](https://nlsp.nasa.gov/explore/data/details/6eaf1654-72d4-5d71-a9dd-a02e674c6473?dataType=MISSIONS) | Attributed actigraphy, WinSCAT cognition and tilt-test records (`real_nasa_lsda`), kept as a separate analog mission. | Three terrestrial participants, not spaceflight. Independent portal retrieval and complete provenance/terms checks remain unresolved in the audit. |

The broader integration generates fictional laboratory baselines around sex-specific real preflight means, adds within-person variation and applies observed postflight median changes. No in-flight laboratory shift is calibrated. Extending short-flight patterns to a fictional 180-day mission is a modelling assumption, not a validated biological forecast.

See the complete [dataset sources](artemis-sleep-dataset/docs/SOURCES.md), [cleaning report](artemis-sleep-dataset/docs/CLEANING_REPORT.md), [source register](Investigation/Inglés/source_register.md) and [limited transformation audit](Investigation/Inglés/reports/008_source_and_transformation_audit.md). The audit traced two OSDR pivots to public source files and sampled radiation metadata/data; it did not validate every correction or the complete radiation/NLSP pipelines. Public accessibility does not replace study-specific citation, permission and redistribution checks.

## How AI was used

AI assisted development and documentation. The deployed application does not call an LLM, train a predictive model, generate diagnoses or use generative AI to calculate its comparison median.

| Tool | Documented contribution | Review and disclosure boundary |
| --- | --- | --- |
| Claude (Anthropic) | The team's disclosure attributes research assistance, Python simulation/cleaning/integration scripts, data retrieval support, documentation, the team's React interface and HTTP adapter to Claude. | The disclosure records review by data/frontend leads. This README reports that attribution rather than independently certifying every review. Its exact model label has not been independently verified here. |
| Codex (OpenAI) | Assisted repository integration, Vercel configuration, database connection diagnosis, the browser-translation crash fix, route recovery, regression testing and this README update. | Changes were inspected and targeted checks were run during development. AI does not replace source verification, scientific review or access controls. |
| Kombai | Visual identity and interface prompts are preserved in the design documentation. | Prompts document design exploration; they do not establish authorship of the final team-selected interface. |

See the team's original [AI usage disclosure](artemis-sleep-dataset/docs/AI_USAGE.md) and [visual-design prompts](artemis-healt/docs/visual/03-prompts-kombai.txt). The disclosure still has placeholders for an integrated AI feature and presentation/video work; placeholders do not establish implemented features. Synthetic records are generated by executable Python rules with a fixed seed, not invented by an LLM during a user's request.

## Architecture and deployment

```text
Browser: React + TypeScript + Vite + Recharts
                 | same-origin /api
                 v
FastAPI: validation, repositories, baseline_v1
                 | server-side PostgreSQL connection
                 v
Supabase PostgreSQL: private artemis schema
```

Vercel builds `artemis-healt/frontend/dist` and serves the frontend and FastAPI in one project. The deployment entrypoint `artemis-healt/app.py` blocks methods other than GET, HEAD and OPTIONS with `403 READ_ONLY_DEMO`. Backend write endpoints exist for controlled development; the public deployment does not authorize personal-data collection. SQLite is available locally; explicit production PostgreSQL mode must not silently fall back to fixtures.

The browser receives no `DATABASE_URL`, administrative database credentials or Supabase service-role key. Keep secrets in backend environment variables. Research data, local backups and raw datasets are excluded from deployment packaging. Repository presence does not mean all data is loaded into the public app.

## Repository guide

| Path | Contents |
| --- | --- |
| [`artemis-healt/`](artemis-healt/README.md) | Runnable frontend/backend, tests, migrations and deployment configuration. Directory spelling follows the existing repository. |
| [`artemis-sleep-dataset/`](artemis-sleep-dataset/README.md) | Simulation and research-data scripts, preserved inputs, processed outputs and methods. |
| [`Investigation/Inglés/`](Investigation/Inglés/README.md) | English research reports, evidence and source register. |
| [`artemis-healt/docs/`](artemis-healt/docs/architecture.md) | Architecture, requirements, API contracts, dataset review and visual design. Some supporting documents remain in Spanish. |

## Reproduction and verification

See the [English application guide](artemis-healt/README.md) for installation, local HTTP/mock modes, API routes and checks. To rebuild only the application fixture, run `python scripts/prepare_demo.py` from `artemis-healt/`. This overwrites its JSON and manifest; inspect the diff.

The research package's `run_all.sh` regenerates and overwrites outputs from supplied raw inputs. Use a separate working copy when intentionally reproducing that pipeline. Its historical validation script checks simulation assumptions and prints results; it is not clinical validation and must not be assumed to fail the process for every reported failure.

## Limitations and next steps

- The public demo is synthetic and read-only. Authenticated write authorization and real-participant consent/privacy workflows are not implemented for public use.
- Educational references and some source permissions/transformations require review. Clinical effectiveness and operational flight suitability have not been established.
- There is no live wearable ingestion, clinical chat, medical record system or deployed AI prediction feature. The orbital visualization is illustrative.
- Mock writes do not establish database persistence. API, browser and scientific validation are separate tasks.
- Future work must preserve origin separation, excluded-value provenance and historical cursor semantics before adding data sources or analysis.
