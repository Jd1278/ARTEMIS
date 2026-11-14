# AI Usage Disclosure

As required by the event, this file lists which AI tools were used and in which part of the project.

| AI tool | Part of the project | What it did | Human review |
|---|---|---|---|
| Claude (Anthropic, model Claude Opus 5.5) | Data — research | Searched and summarized published evidence (NASA HRP pages, ISS sleep studies, PVT-B and fatigue scale papers) used to set thresholds and calibrate the simulation. | Data lead verified sources and cutoffs. |
| Claude (Anthropic, model Claude Opus 5.5) | Data — dataset generation and cleaning | Wrote the simulation (`generate_raw.py`), cleaning pipeline (`clean.py`), validation checks (`validate.py`) and this documentation. | Data lead ran and reviewed the pipeline and outputs. |
| Claude (Anthropic, model Claude Opus 5.5) | Data — real data retrieval | Located the Inspiration4 blood panels in NASA OSDR (OSD-575, OSD-569), retrieved them through the team's browser and wrote the cleaning script (`clean_osdr.py`). | Data lead reviewed flags and corrections. |
| Claude (Anthropic, model Claude Opus 5.5) | Data — integration | Designed and wrote `integrate.py`: generated the simulated crew's lab panels from the real OSDR data and merged everything into one dataset; added validation checks. | Data lead reviewed the method and checks. |
| Claude (Anthropic, model Claude Opus 5.5) | Data — real radiation | Found the ISS TEPC dataset on data.nasa.gov, downloaded it through the team's browser (HAPI API), and wrote `fetch_tepc.py` and `clean_radiation.py`. | Data lead reviewed the cleaning rules and flags. |
| Claude (Anthropic, model Claude Opus 5.5) | Data — real bed rest analog | Found the open-access UTMB bed rest datasets in the NASA Life Sciences Portal, downloaded them through the team's browser with the data lead's approval, detected source errors (mislabeled subjects, HR file duplicating DBP) and wrote `clean_bedrest.py`. | Data lead approved the download and reviewed the cleaning. |
| Claude (Anthropic, model Claude Opus 5.5) | Web development — frontend | Wrote the React frontend (`artemis-healt/frontend`): screens, charts, orbital map, SVG illustrations and crew avatars, the client-side `baseline_v1` rule used by the offline demo mode, the adapter that connects the interface to the team's FastAPI backend, and the English interface text. Also wrote the frontend specification prompt (`artemis-healt/docs/frontend-prompt.md`). | Frontend lead chose the design, reviewed the code, ran the automated tests and tested the app in the browser against the backend. |
| _(add)_ | Integrated AI feature | | |
| _(add)_ | Slides / video | | |

Per the Space Apps Project Submission Guide, AI-generated data is acknowledged in descriptive text and metadata: see the notice at the top of `README.md` and `docs/DATA_DICTIONARY.md`.

Each team member should add a row for any AI tool they used.
