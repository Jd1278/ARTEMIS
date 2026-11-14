# Astronaut Health Monitoring — Integrated Dataset

Dataset for the NASA Space Apps Challenge 2026 — *Create Health Monitoring Software for Astronauts on Space Missions*.

**One integrated dataset** combines a simulated 180-day ISS mission (6 fictional crew members) with **real NASA data**: blood panels of the 4 SpaceX Inspiration4 astronauts (NASA OSDR OSD-575 / OSD-569), **real daily radiation measured inside the ISS** (NASA CDAWeb, ISS_DOSANL_TEPC), and **real sleep (actigraphy), cognition and tilt-test data from a 60-day NASA bed rest study** (NASA Life Sciences Portal, open access). Every observation carries a `source` label:

| `source` | What it is | Observations |
|---|---|---|
| `simulated` | Daily morning check-in of the simulated crew: sleep, fatigue, 3-min alertness test (PVT-B), stress, workload, mood, resting heart rate — calibrated to published ISS studies | 12,960 |
| `simulated_from_real` | Periodic blood panels of the simulated crew (2 preflight, 3 in-flight, 2 post-flight; 14 analytes), **generated from the real Inspiration4 values**: baselines by sex and the real post-flight change | 588 |
| `real_nasa_cdaweb` | **Real ISS radiation** (TEPC dose analyzer): daily dose, cumulative dose and % of NASA's 600 mSv career limit for each of the 180 mission days, taken from 180 consecutive real days (2017-03-01 to 2017-08-27) with the same month/day; repeated for each crew member (shared environment) | 4,320 |
| `real_nasa_osdr` | Real Inspiration4 blood panels (4 crew, 7 timepoints, 38 analytes), cleaned | 1,064 |
| `real_nasa_lsda` | **Real bed rest analog** (UTMB Campaign 1, 3 subjects, 60 days of head-down-tilt bed rest): nightly actigraphy (sleep duration, latency, efficiency, sleep aids), WinSCAT cognitive tests and tilt-test tolerance; kept as its own mission, never mixed with the simulated crew | 1,148 |

> **AI-generated data notice:** the `simulated` and `simulated_from_real` observations are synthetic, produced by Python scripts written with the assistance of an AI tool (Claude, Anthropic). They are simulations calibrated against published NASA research and real NASA OSDR data, not records of real astronauts. The `real_nasa_osdr`, `real_nasa_cdaweb` and `real_nasa_lsda` observations are real NASA data, cleaned with AI-assisted scripts (radiation dates are re-assigned to the simulated mission calendar).

## Main files

| File | Use |
|---|---|
| `data/processed/astronaut_health_observations.csv` | **The single dataset** (long format: 1 row = 1 measurement) |
| `data/processed/crew_daily_integrated_wide.csv` | 1 row = 1 crew member x 1 mission day, with the latest lab values — for the AI model |
| `data/processed/crew_integrated.json` | Same data nested per crew member (daily + labs) plus the real crew as reference — for the web app |
| `data/reference/thresholds.csv` | Green/yellow/red rules for the daily check-in, with sources |
| `data/reference/lab_calibration_from_real.csv` | How each simulated lab was calibrated from the real data |
| `data/processed/iss_radiation_daily_clean.csv` | Real ISS radiation per mission day, cleaned (component file) |
| `data/processed/bedrest_actigraphy_clean.csv`, `bedrest_winscat_clean.csv`, `bedrest_tilt_clean.csv`, `bedrest_summary_by_phase.csv` | Real bed rest analog data, cleaned (component files) |
| `data/reference/countermeasures.csv` | Recommended action per alert |

Component datasets kept for transparency: `crew_daily_log_clean.csv` (daily check-in only), `inspiration4_blood_long.csv` / `_wide.csv` (real data only), `inspiration4_change_R1_vs_preflight.csv`.

## Structure

```
data/raw/                 uncleaned data (simulated log as "received"; real OSDR blood panels; real ISS radiation daily summary;
                          real NLSP bed rest files)
data/processed/           integrated dataset + component datasets
data/reference/           thresholds, lab calibration, countermeasures, risk map, crew roster
scripts/                  generate_raw.py, clean.py (daily check-in) · fetch_osdr.py, clean_osdr.py (real data)
                          fetch_tepc.py, clean_radiation.py (real ISS radiation) · clean_bedrest.py (real bed rest) ·
                          integrate.py (single dataset) · validate.py
docs/                     DATA_DICTIONARY.md, CLEANING_REPORT.md, SOURCES.md, AI_USAGE.md
run_all.sh                rebuilds everything and runs the checks
```

## Reproduce

```bash
pip install pandas numpy
./run_all.sh
```

## Key facts for the pitch

- Simulated mean sleep **6.36 h**, **24%** of nights >= 7 h — matches the published ISS figure (24%; Barger 2014).
- Simulated blood panels sit within 1.5 SD of the **real** Inspiration4 preflight means for every analyte, and their post-flight change follows the real crew (e.g., lymphocytes −20% one day after landing).
- Out-of-range lab values: 3.6% simulated vs 3.8% real.
- **Real ISS radiation:** median 0.88 mSv/day; the 180-day mission accumulates 162 mSv = **27% of NASA's 600 mSv career limit** in a single mission. A real dose spike on 2017-03-26 (4.1 mSv in one day) is kept and flagged red.
- **Real bed rest analog (NLSP):** sleep fell from 7.8 h before to 7.2 h during 60 days of bed rest; nights under 7 h went from 0% to 22%; tilt tolerance dropped from 25 to 16 min on the day bed rest ended. Days 53-57 show poor sleep in all three subjects at once (6.0 h, 1.9 h to fall asleep).
- Bed rest cleaning: the actigraphy 'query' file mislabels 185 of 191 rows as one subject (consolidated file used instead); the tilt 'heart rate' file is a copy of diastolic pressure (excluded); H:MM / H:MM:SS text converted to hours; 17 'No Data' nights kept missing; metadata errors flagged.
- Radiation cleaning: 13 missing days, 1,046 duplicate minute records, 6 low-coverage days and 1 instrument anomaly imputed; 35 partial days scaled to 24 h.
- 55 labeled anomaly days (sleep-debt episodes, mood decline) for the AI feature.
- Cleaning of the real data fixed a column-shift error, duplicated analyte names, wrong-sex reference ranges and missing indices, and flagged a suspicious low-glucose cluster (see `docs/CLEANING_REPORT.md`).

## Limitations

- Daily check-in and crew lab panels are **simulated**; the real blood data is small (4 civilians, 3-day flight, no in-flight blood draws).
- Bed rest data come from only 3 healthy volunteers on Earth (pre-bed-rest actigraphy exists for one subject only); it is an analog of microgravity, not spaceflight.
- Radiation is an **area monitor** reading (dose equivalent at the TEPC location), used as a proxy for crew exposure; personal effective dose differs.
- No in-flight lab shift is modelled (no open in-flight data to calibrate it). The post-flight change after a 180-day mission is taken from a 3-day mission, so it is a conservative stand-in.
- Thresholds marked `team-defined` are design choices. Not a medical device.
