# Sources

IDs (S1, S2, ...) are referenced in `data/reference/*.csv` (`source_ids` column).

## Official NASA Space Apps challenge resources (required data use)

| ID | Source | Used for |
|----|--------|----------|
| S1 | NASA Human Research Program — *Risks of Human Spaceflight*. https://www.nasa.gov/hrp/risks/ | `risk_indicator_map.csv`: the 17 HRP risks; this dataset focuses on *Inadequate Sleep and Irregular Schedules* and *Behavioral Changes and Psychiatric Disorders*. |
| S2 | NASA Human Research Program — *5 Hazards of Human Spaceflight*. https://www.nasa.gov/hrp/hazards/ | Hazard column of `risk_indicator_map.csv` (Isolation & Confinement, Distance from Earth, Hostile/Closed Environment). |

## Other NASA / NASA-funded evidence (external, referenced)

| ID | Source | Used for |
|----|--------|----------|
| S3 | Barger LK et al. (2014). *Prevalence of sleep deficiency and use of hypnotic drugs in astronauts before, during, and after spaceflight.* The Lancet Neurology. doi:10.1016/S1474-4422(14)70122-X. Summary: https://www.sciencedaily.com/releases/2014/08/140807215803.htm | NASA schedules 8.5 h of sleep; in-flight mean ~6.09 h on ISS; only 24% of ISS sleep episodes >= 7 h; ~75% of ISS crew used sleep medication. Used to calibrate the simulation and the 7 h / 6 h cutoffs. |
| S4 | NASA — *Risk from Inadequate Sleep and Irregular Schedules*. https://www.nasa.gov/reference/risk-from-inadequate-sleep-and-irregular-schedules/ and HRP Evidence Report (NTRS 20150016964). https://ntrs.nasa.gov/citations/20150016964 | Stressors modeled: work overload, irregular light-dark cycles, schedule shifts. |
| S5 | Jones CW et al. (2022). *Sleep deficiency in spaceflight is associated with degraded neurobehavioral functions and elevated stress in astronauts on six-month missions aboard the ISS.* SLEEP. https://pmc.ncbi.nlm.nih.gov/articles/PMC8919197 | 24 astronauts on 6-month ISS missions; ~6.5 h sleep in flight; < 6 h linked to slower psychomotor speed, higher stress and workload. Model for the daily self-test design (sleep, VAS stress/workload, PVT-B). |
| S6 | NASA NTRS 20090029851 — *Psychomotor Vigilance Self Test on ISS (Reaction Self Test, Expeditions 21 & 22)*. https://ntrs.nasa.gov/citations/20090029851 | Hypothesis that performance declines when sleep is restricted to < 6 h for 3+ days -> `short_sleep_streak_d` red rule. |
| S12 | NASA NTRS 20230003916 — AsMA poster on ISS crew sleep under NASA Standard Measures (2019-2022). https://ntrs.nasa.gov/citations/20230003916 | Recent ISS sleep (~6.6 h) used as upper bound for calibration. |

## Fatigue / vigilance scales (external)

| ID | Source | Used for |
|----|--------|----------|
| S7 | Samn SW, Perelli LP (1982). *Estimating Aircrew Fatigue.* USAF SAM-TR-82-21. https://apps.dtic.mil/sti/pdfs/ADA125319.pdf | 7-point fatigue scale (1 = fully alert, 7 = completely exhausted). |
| S8 | Tritschler K. (2016). *Fatigue. Risk. Assessment.* ICAO Fatigue Management Approaches Symposium. https://icao.int/Meetings/fmas/Documents/Presentations/Kris%20Tritschler_%20Fatigue.Risk.Assessment.pdf | Severity mapping of Samn-Perelli scores (4 = a little tired; 5-7 = moderately tired to exhausted). |
| S9 | Basner M, Mollicone D, Dinges DF (2011). *Validity and sensitivity of a brief psychomotor vigilance test (PVT-B).* Acta Astronautica 69:949-959. https://pmc.ncbi.nlm.nih.gov/articles/PMC3197786 | PVT-B lapse threshold = 355 ms; response speed most sensitive metric. |
| S10 | Basner M, Rubinstein J (2011). *Fitness for duty: a 3-minute PVT predicts fatigue-related declines.* J Occup Environ Med. https://pmc.ncbi.nlm.nih.gov/articles/PMC3190077 | 11 and 20 lapses as fitness-for-duty cutoffs. |

## Clinical reference

| ID | Source | Used for |
|----|--------|----------|
| S11 | American Heart Association — normal adult resting heart rate 60-100 bpm (athletes may be ~40 bpm). https://www.heart.org/en/health-topics/high-blood-pressure/the-facts-about-high-blood-pressure/all-about-heart-rate-pulse | Absolute HR sanity range (40-100 bpm) in `thresholds.csv`. |

## Option D — REAL NASA data (official NASA Open Science Data Repository)

| ID | Source | Used for |
|----|--------|----------|
| D1 | NASA OSDR **OSD-575** — SpaceX Inspiration4 serum: Comprehensive Metabolic Panel (file `LSDS-8_Comprehensive_Metabolic_Panel_CMP.upload_SUBMITTED.csv`). https://osdr.nasa.gov/bio/repo/data/studies/OSD-575 | Real glucose, electrolytes, kidney and liver markers of 4 astronauts, 7 timepoints. |
| D2 | NASA OSDR **OSD-569** — SpaceX Inspiration4 whole blood: Complete Blood Count (file `LSDS-7_Complete_Blood_Count_CBC.upload_SUBMITTED.csv`). https://osdr.nasa.gov/bio/repo/data/studies/OSD-569 | Real red/white blood cell counts (immune changes after flight). |
| D3 | Overbey EG et al. (2024). *Collection of biospecimens from the Inspiration4 mission establishes the standards for the Space Omics and Medical Atlas (SOMA).* Nature Communications; and OSDR I4 access guide, npj Microgravity 2024, doi:10.1038/s41526-024-00393-5 | Study design and timepoints. |

## Real ISS radiation (official NASA data)

| ID | Source | Used for |
|----|--------|----------|
| R1 | NASA CDAWeb **ISS_DOSANL_TEPC** — ISS Tissue-Equivalent Proportional Counter, dose analyzer (NASA Space Radiation Analysis Group, JSC). Listed on data.nasa.gov: https://data.nasa.gov/dataset/iss-tissue-equivalent-proportional-counter-tepc-dose-analyzer-10-s-data-61b24 ; HAPI: https://cdaweb.gsfc.nasa.gov/hapi/info?id=ISS_DOSANL_TEPC | Real per-minute dose rate inside the ISS, 2017-03-01 to 2017-08-27, summarized per day. |
| R2 | NASA OCHMO-TB-020 *Design for Ionizing Radiation Protection* (NASA-STD-3001 Vol 1 [V1 4030]). https://www.nasa.gov/wp-content/uploads/2023/03/radiation-protection-technical-brief-ochmo.pdf | Career limit of 600 mSv effective dose; 250 mSv per solar particle event. |

## Real bed rest analog (official NASA data, open access)

| ID | Source | Used for |
|----|--------|----------|
| B1 | NASA Life Sciences Portal (NLSP) — UTMB Bed Rest Campaign 1 (Flight Analogs Research Unit, University of Texas Medical Branch). https://nlsp.nasa.gov/explore/data/details/6eaf1654-72d4-5d71-a9dd-a02e674c6473?dataType=MISSIONS ; open-access datasets listed at https://www.nasa.gov/hrp/nlsp/ | Mission context: 3 subjects, 60 days 6-degree head-down-tilt bed rest. |
| B2 | NLSP experiment BRSMAct — Bed Rest Standard Measures: Actilight (dataset BRSMACT_Campaign_1_Actigraphy) | Nightly sleep duration, latency, efficiency, sleep aids. |
| B3 | NLSP experiment MR085G — Neurocognitive Assessment (WinSCAT) (dataset MR085G_Campaign_1_WinSCAT) | Cognitive test battery before, during and after bed rest. |
| B4 | NLSP experiment MR001G — Neuroendocrine and Cardiovascular Response to Tilt (dataset MR001G_Campaign_1_Tilt; PI Platts, DOI 10.83263/g31q-a824) | Tilt tolerance and blood pressure before vs after bed rest. |

## How the real data feeds the integrated dataset

The simulated crew's blood panels (`source = simulated_from_real`) are generated from D1/D2: each crew member's baseline is drawn around the real preflight mean of their sex (spread = 0.6 x real SD), each draw adds within-person noise (0.6 x real SD), and the post-flight draws apply the median % change seen in the real crew at R+1 and R+45. Full table: `data/reference/lab_calibration_from_real.csv`. No in-flight shift is applied because no open in-flight blood data exist for calibration.

## Other open data (not used)

| Source | What it has | Limitation |
|---|---|---|
| NASA OSDR — Inspiration4 / SOMA (https://osdr.nasa.gov, search "Inspiration4") | Real astronaut blood panels (incl. metabolic panel with glucose), omics, pre/in/post-flight timepoints. | 4 civilian crew, 3-day flight, few timepoints — good for validating ranges, not for daily time series. |
| PhysioNet (https://physionet.org) — open sleep and PPG datasets (e.g., Sleep-EDF) | Real sleep staging, heart rate, SpO2 signals. | Earth-based subjects; use only as external reference. |
| NASA LSDA (https://lsda.jsc.nasa.gov) | Historical astronaut biomedical data. | Requires a formal data request (weeks). Not usable in a 48-h hackathon. |

## What is simulated (be transparent in the pitch)

- **Option A is synthetic; Option D is real NASA OSDR data.** No real astronaut data is publicly downloadable at daily resolution (NASA LSDA requires a formal request). Simulation parameters are calibrated so the output matches published ISS statistics (mean sleep, share of nights >= 7 h) — this is checked automatically by `scripts/validate.py`.
- Thresholds marked `team-defined` in `thresholds.csv` are design choices of the team, not clinical standards.
- This dataset is for a hackathon prototype; it is **not** medical guidance.
