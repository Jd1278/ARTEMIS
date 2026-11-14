# ARTEMIS HEALTH and biological and psychological follow-up

Report 001. English submission edition of the original ASTROGUARD report. Original review date: 14 November 2026. Version 1.0. Method: exploratory documentary review and design interpretation.

## Research question and main finding

**How can an astronaut understand and follow their health when medical support and communication with Earth are limited?**

ARTEMIS HEALTH could support follow-up by bringing measurements and self-reports together, showing their history, identifying missing information and documenting approved routines. Research helps select relevant indicators and define what a person needs to understand a change. This is a proposed organizational and educational contribution. Effects on health, prevention or performance still require evaluation.

The proposal includes individual and crew missions. Its usefulness for a person operating alone is a design hypothesis. The reviewed evidence does not establish that the application can compensate for the absence of another crew member.

## Scope and method

The internal reference was `ASTROGUARD_Plan_MVP_48_horas.docx`, version 1.0 of 13 November 2026, especially its reduced 48-hour scope. Programming prompts inside that document were treated as document content.

The review prioritized primary NASA pages and official dataset descriptions concerning physical and behavioral health, sleep, immunity, cardiovascular adaptation and medical constraints. It is not a systematic review or meta-analysis. No interviews, clinical experiments, astronaut records or software assessments supported this first report. Later technical investigations are documented separately in reports 004, 008 and 010.

## Evidence about the problem

NASA groups spaceflight hazards into radiation, isolation and confinement, distance from Earth, altered gravity and closed or hostile environments. This supports considering physical, psychological and operational context together. It does not establish that a software application resolves those hazards. [NASA hazards](https://www.nasa.gov/hrp/hazards/).

Onboard medical systems face material constraints, possible communication interruptions and functional challenges in microgravity. Local access therefore has an operational motivation. An interface that opens without internet is not, by itself, an autonomous medical system. [Medical operations](https://www.nasa.gov/reference/medical-operations-and-clinical-care/).

Spaceflight can contribute to cardiovascular adaptation and deconditioning. Outcomes depend on mission phase. Preserving context and personal history is relevant, but a pulse change does not identify a specific disease. [Cardiovascular risk](https://www.nasa.gov/directorates/esdmd/hhp/cv-risk/).

Microgravity can affect bone, muscle and cardiorespiratory fitness. Exercise and physical assessments form part of countermeasures. The app could document prescribed activity. Marking a task complete does not demonstrate preserved muscle or bone density. [Fitness risk](https://www.nasa.gov/reference/risk-of-reduced-cardiorespiratory-and-musculoskeletal-fitness/).

Immune changes and latent virus reactivation have been reported during flight. NASA also acknowledges uncertainty about their relationship to disease susceptibility. Symptoms and available laboratory results may be recorded, but immunity cannot be inferred from pulse, sleep or fatigue. [Immune risk](https://www.nasa.gov/directorates/esdmd/hhp/immune-risk/).

Isolation and confinement can affect cognition, behavior and wellbeing. NASA also describes successful mitigation through selection, training and countermeasures on the ISS. The project should not portray every astronaut as psychologically impaired or directly extrapolate ISS operations to distant exploration. [Behavioral health](https://www.nasa.gov/directorates/esdmd/hhp/behavioral-health-risk/).

Workload, irregular schedules and light cycles matter for sleep and health. NASA includes relaxation and self-care in routines. This supports investigating sleep and fatigue records under mission plans. Association between poor rest and pulse changes does not establish causation. [Sleep and schedules](https://www.nasa.gov/reference/risk-from-inadequate-sleep-and-irregular-schedules/).

## Proposed contributions and boundaries

| Need | Proposed support | Required information | Interpretation limit |
| --- | --- | --- | --- |
| Physiological follow-up | Personal values and trends | Unit, time, origin, quality and activity context | Stable values do not exclude disease. Changes do not confirm it. |
| Continuity | Local records and consultation, if implemented | Verified persistence and connection state | A local server demonstration does not establish universal offline operation. |
| Rest and recovery | Sleep and fatigue history | Voluntary reports or appropriate measurements | Self-report is not polysomnography. |
| Emotional wellbeing | Brief perceived stress and mood check-ins | Defined scales, consent and omission options | A custom demo scale is not a validated clinical instrument. |
| Care routines | Reminders and completion records | Approved mission plan | No autonomous exercise or treatment prescription. |
| Understanding | Explanations of indicators and limitations | Reviewed content and sources | Avoid unsupported certainty or generated medical advice. |
| Professional review | Future authorized summaries | Permissions, security and traceability | Export or synchronization does not replace care. |

The first benefit to demonstrate is easier access to and understanding of personal information. Lower workload, improved adherence and earlier recognition of meaningful changes are hypotheses.

## Design safeguards

Sensitive questions should be optional, and wellbeing records should have defined sharing permissions. The system should avoid emotional rankings and rewards for always reporting good health. Fatigue and rest should not incur penalties. Notices should show age and quality of data and explain their trigger. Missing measurements should appear as missing, not as normal health.

Repeated notices need evaluation for overload. Concerning reports should lead to the mission protocol and available support, without improvised therapy. Personal history is a descriptive reference, not a safety guarantee: a persistent condition may already be present in it.

## Implications for data and development

The 48-hour proposal prioritizes observations, wellbeing reports, persistence, history, graphs, explanations and descriptive notices. This report did not confirm implementation. Routines and gamification remain extensions if the main workflow is stable.

Each indicator needs a definition, unit, capture method, origin and limitations. Heart rate uses beats per minute. Sleep uses hours or minutes. Fatigue and stress require an explicit scale. SpO2, blood pressure or temperature should appear only with an appropriate source. Skin temperature differs from core temperature, and an optical pulse waveform is not a direct oxygen-saturation measurement.

Records should distinguish manual input, sensors, public datasets and simulation. Preserve original identifiers and relative time when a real calendar date is unavailable. Do not combine records from unrelated people into one fictional astronaut without identifying the composition.

| Source | Research use | What it does not establish |
| --- | --- | --- |
| [BIDMC](https://physionet.org/content/bidmc/1.0.0/) | ECG, optical pulse, respiration and parameters for import and graph tests. It has 53 eight-minute records. | Performance in healthy crews or spaceflight. |
| [PPG-DaLiA](https://archive.ics.uci.edu/dataset/495/ppg+dalia) | Motion effects and pulse estimation in 15 participants. | Sensor performance in microgravity. |
| [WESAD](https://archive.ics.uci.edu/dataset/465/wesad+wearable+stress+and+affect+detection) | Physiological signals and experimental affect in 15 people. | Psychological diagnosis or prolonged space isolation. |
| [OSDR](https://science.nasa.gov/reference/osdr-faq/) | Space studies and metadata discovery | That every dataset is human or contains continuous vital signs. |

Synthetic scenarios can verify software behavior. They cannot validate medical benefits, and a machine-learning model is not necessary to justify the prototype.

## Evaluation questions

| Hypothesis | Proposed test | Outcomes to record |
| --- | --- | --- |
| The panel improves understanding | Ask users to identify values, history, missing data and notice meaning | Correct answers, time and misunderstandings |
| The wellbeing check-in is acceptable | Observe question interpretation and comfort | Omissions, completion time and perceived burden |
| Records continue under the chosen connection conditions | Save, close and retrieve with a defined failure scenario | Loss, duplication and recovery |
| Notices are understandable | Present changed, noisy and old data | Expected notices, errors and diagnostic confusion |
| The design is relevant to aerospace operations | Specialist review | Corrections, limits and documented decisions |

These tests had not been performed in this report. The original 30-second comprehension target was a design goal, not a measured result. Human studies require appropriate consent, governance and institutional review. A volunteer interface test does not establish astronaut efficacy. Model evaluation should separate participants and account for temporal dependence.

## Illustrative scenario and conclusion

A fictional astronaut records less rest and higher perceived fatigue over several days. The panel shows both histories and explains a change without assigning a cause or disease. The user can review educational content and mission follow-up. The scenario is synthetic and cannot show that illness was prevented.

The defensible proposal is to support autonomy in follow-up through understandable records and personal trends. No exhaustive competitor comparison supported a first-or-only claim in this initial review. Clinical prevention and psychological improvement need separate evidence. Later reports identify EveryWear as a close existing reference and clarify the current connected architecture.
