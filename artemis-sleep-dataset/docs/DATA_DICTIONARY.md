# Data Dictionary

## INTEGRATED DATASET — `data/processed/astronaut_health_observations.csv` (main file)

Long format: 1 row = 1 measurement (14,612 rows).

| Column | Description |
|---|---|
| observation_id | Unique row id. |
| crew_id | CM-01..CM-06 (simulated crew) or C001..C004 (real Inspiration4 crew). |
| sex | M / F (used for lab reference ranges). |
| source | `simulated` (daily check-in), `simulated_from_real` (simulated crew labs generated from real data), `real_nasa_cdaweb` (real ISS radiation), `real_nasa_osdr` (real blood panels), `real_nasa_lsda` (real bed rest analog). |
| mission | SIM-ISS-180 (simulated, 180 days) or Inspiration4 (real, 3 days). |
| data_type | `daily_checkin`, `lab_panel`, `environment` (radiation), `sleep_actigraphy`, `cognition_test`, `tilt_test` (bed rest analog). |
| phase | preflight / inflight / postflight. |
| days_from_launch | Day relative to launch. Simulated: 1-180 in flight, negative before launch, 181 = R+1, 225 = R+45. Real: negative before launch, R+1 = 4. |
| timepoint | FD<n> (flight day), L-<n> (days before launch), R+<n> (days after return). |
| date | Calendar date (simulated mission only; launch 2026-03-01). |
| indicator | What was measured (e.g., `sleep_duration_h`, `mood_vas`, `lymphocytes_abs_cells_ul`). |
| value, unit | Measurement and its unit. |
| ref_low, ref_high | Lab reference range (lab panels only; daily thresholds are in `thresholds.csv`). |
| status | green / yellow / red (`info` = shown without a color; `unknown` = missing). Labs: outside the range by <= 10% of the range width = yellow, more = red (team-defined). |
| status_detail | Labs: low / normal / high. |
| event_label, is_anomaly | Ground truth of the simulated day (labels for the AI); always none/0 for real data. |
| quality_flags | Cleaning flags; for real data, review notes on possible pre-analytical artifacts. |

Radiation indicators (`source = real_nasa_cdaweb`, one row per crew member and day): `radiation_dose_equivalent_uSv_day` (status green / yellow > 1.5x mission median / red > 3x, team-defined spike rule), `radiation_absorbed_dose_uGy_day`, `radiation_cumulative_mSv`, `radiation_pct_career_limit` (% of NASA's 600 mSv career limit). `quality_flags` carries the cleaning flag and the real ISS date.

Bed rest indicators (`source = real_nasa_lsda`, mission `UTMB Bed Rest Campaign 1 (analog)`, subjects C1G0001-C1G0003): `days_from_launch` = day relative to the start of bed rest (negative before, 1-60 during, 61 = R+0 after); `timepoint` = BR-n / BDn / R+n. Actigraphy indicators get the same sleep status rules as the check-in; cognition and tilt indicators are `info`.

### Bed rest component files (real, NASA NLSP)
| File | Columns |
|---|---|
| `bedrest_actigraphy_clean.csv` | subject, date, phase (pre_bedrest / bedrest / post_bedrest), bedrest_day, timepoint, sleep_duration_h, sleep_latency_h, sleep_efficiency_pct, sleep_medication (bool), medication (text) |
| `bedrest_winscat_clean.csv` | subject, date, phase, bedrest_day, timepoint, run, with_instructions, practice_session (runs 1-3), memory_rt_ms, memory_accuracy_pct, memory_lapses_gt700ms, math_rt_ms, math_accuracy_pct, matching_rt_ms, matching_accuracy_pct, coding_rt_ms, coding_accuracy_pct |
| `bedrest_tilt_clean.csv` | subject, date, phase, bedrest_day, timepoint, tilt_tolerance_min, supine_sbp_mean, supine_dbp_mean, last_tilt_sbp, last_tilt_dbp, min_tilt_sbp, quality_flag |
| `bedrest_summary_by_phase.csv` | Means per phase: sleep duration/latency/efficiency, % nights < 7 h, % nights with a sleep aid; WinSCAT memory speed/accuracy/lapses (non-practice runs); tilt tolerance before vs R+0 |

### `iss_radiation_daily_clean.csv` (component: real ISS radiation)
| Column | Description |
|---|---|
| mission_day | 1-180 of the simulated mission. |
| source_date | Real ISS date of the measurement (2017-03-01 + mission_day - 1). |
| absorbed_dose_uGy_day | Absorbed dose for the day (micro-gray), scaled to 24 h when coverage was partial. |
| dose_equivalent_uSv_day | Dose equivalent (ICRP-60, micro-sievert) for the day. |
| cumulative_dose_equivalent_mSv | Running total over the mission (milli-sievert). |
| pct_of_career_limit | Cumulative dose as % of NASA's 600 mSv career limit. |
| status_radiation_daily | green / yellow / red (spike rule above). |
| radiation_flag | ok, partial_day_scaled_to_24h, missing_day_imputed, low_coverage_imputed, instrument_anomaly_imputed, dose_spike_verify. |
| minutes_covered, records_used, duplicate_timestamps | Data coverage of the real day. |

### `crew_daily_integrated_wide.csv` (for the AI model)
All columns of `crew_daily_log_clean.csv` (below) plus the radiation columns above (`radiation_source_date`, `dose_equivalent_uSv_day`, ...) and, for each of the 14 lab analytes, `lab_<indicator>_last` = latest available value (preflight L-10 until the first in-flight draw on day 30), `days_since_last_lab` and `lab_drawn_today` (1 on days 30, 90, 150).

### `crew_integrated.json` (for the web app)
`{mission, launch_date, notice, thresholds_daily[], crew[{crew_id, role, sex, daily[], labs[]}], reference_real_crew[{crew_id, sex, mission, labs[]}]}`.

### `data/reference/lab_calibration_from_real.csv`
Per analyte and sex: real preflight mean and SD (n values), reference range, and the real median % change at R+1 and R+45 (computed only when >= 2 real crew had a valid value; review-flagged values excluded).

---

# Component datasets

> **AI-generated data notice:** `simulated` and `simulated_from_real` observations are synthetic (AI-assisted scripts, calibrated to NASA research and real NASA OSDR data). `real_nasa_osdr` observations are real.

## `data/processed/crew_daily_log_clean.csv` (main table, 1 row = 1 astronaut x 1 mission day)

Each record represents one morning self-assessment (sleep log + 1-minute questionnaire + 3-minute vigilance test), modeled on the NASA ISS Reaction Self Test (see SOURCES S5, S6).

| Column | Type | Unit / values | Description |
|---|---|---|---|
| record_id | int | — | Original log entry id. |
| crew_id | str | CM-01..CM-06 | Fictional crew member (see `crew_roster.csv`). |
| date | date | YYYY-MM-DD | Mission calendar date. |
| timestamp | datetime | ISO 8601 UTC | Time the self-assessment was logged. |
| mission_day | int | 1-180 | Day since launch. |
| mission_phase | str | adaptation (1-7), early (8-60), mid (61-120), late (121-180) | Mission phase. |
| sleep_duration_h | float | hours | Sleep obtained the previous night. |
| sleep_quality | int | 1 (very poor) - 5 (very good) | Self-rated sleep quality. |
| sleep_medication | bool | true/false | Sleep aid taken the previous night. |
| samn_perelli | int | 1-7 | Subjective fatigue (1 fully alert, 7 completely exhausted). |
| pvt_mean_rt_ms | float | ms | Mean reaction time on the 3-min PVT-B. |
| pvt_lapses | int | count | PVT-B responses >= 355 ms. |
| stress_vas | float | 0-100 | Self-rated stress (visual analog scale). |
| workload_vas | float | 0-100 | Self-rated workload. |
| mood_vas | float | 0-100 (higher = better) | Self-rated mood. |
| resting_hr_bpm | int | bpm | Morning resting heart rate. |
| baseline_rt_ms | float | ms | Personal baseline RT (median, days 8-21). |
| baseline_hr_bpm | float | bpm | Personal baseline resting HR (median, days 8-21). |
| pvt_speed_change_pct | float | % | Change in response speed vs. baseline (negative = slower). |
| resting_hr_delta_bpm | float | bpm | Resting HR minus personal baseline. |
| sleep_7d_avg_h | float | hours | 7-day rolling mean sleep. |
| sleep_debt_3d_h | float | hours | Sum of shortfall below 7 h over the last 3 nights. |
| short_sleep_streak_d | int | nights | Consecutive nights < 6 h up to this day. |
| status_<indicator> | str | green / yellow / red / unknown | Color status per indicator (rules in `thresholds.csv`). |
| overall_status | str | green / yellow / red | Worst status among indicators. |
| n_red, n_yellow | int | count | Number of indicators in red / yellow. |
| risk_score | int | 0-18 | 2 x n_red + n_yellow (simple aggregate for ranking). |
| event_label | str | none, adaptation, slam_shift, high_workload, sleep_debt_episode, mood_decline | **Ground truth** of what was simulated that day. |
| event_type | str | nominal, adaptation, scheduled_stressor, anomaly | Grouped label. |
| is_anomaly | int | 0/1 | 1 = unexpected personal episode (sleep_debt_episode or mood_decline). Target for anomaly detection. |
| quality_flags | str | `ok` or `;`-separated flags | Which fields were imputed or out of range in the raw log. |

**For the AI model:** use the measurement + derived columns as features; use `is_anomaly` (or `event_label`) as the label. Do **not** use `status_*`, `overall_status` or `risk_score` as features if you want to show the model learns beyond the fixed rules. Split by `crew_id` (e.g., train on 4, test on 2) to avoid leakage.

## `data/processed/crew_daily_log_clean.json`
Same data nested for the web app: `{mission, thresholds[], crew[{crew_id, role, baseline_rt_ms, baseline_hr_bpm, days[]}]}`.

## `data/processed/crew_daily_summary.csv`
Crew-level per day: mean sleep, fatigue, stress, mood, and how many crew members are red / yellow.

## `data/raw/crew_daily_log_raw.csv`
Uncleaned log (as "received"), kept to demonstrate the cleaning process. See `docs/CLEANING_REPORT.md`.

## Reference tables (`data/reference/`)
- `thresholds.csv` — green/yellow/red cutoffs, direction, evidence level, sources.
- `risk_indicator_map.csv` — NASA HRP risks/hazards -> indicators in this dataset.
- `countermeasures.csv` — suggested action per indicator/level and whether to escalate to a flight surgeon.
- `crew_roster.csv` — fictional crew.

## OPTION D (REAL DATA) — Inspiration4 blood panels, NASA OSDR

`data/processed/inspiration4_blood_long.csv` — 1 row = crew member x timepoint x analyte (1,064 rows).

| Column | Description |
|---|---|
| subject / sex | Real (anonymized) crew ID C001-C004 and sex as published. |
| timepoint | L-92, L-44, L-3 (days before launch), R+1, R+45, R+82, R+194 (days after return). |
| phase | preflight / postflight. |
| days_from_launch | Numeric day relative to launch (flight lasted 3 days, so R+1 = day 4). |
| panel | CMP (metabolic panel) or CBC (complete blood count). |
| analyte, value, unit | Lab measurement. |
| ref_min / ref_max | Lab reference range (sex-specific, applied consistently). |
| flag | normal / low / high / missing. |
| review_note | Possible pre-analytical artifact to verify (not a diagnosis). |

`inspiration4_blood_wide.csv` — same data, one row per crew member x timepoint (38 analyte columns).
`inspiration4_change_R1_vs_preflight.csv` — % change one day after landing vs preflight mean, per analyte (n = 4 crew).
