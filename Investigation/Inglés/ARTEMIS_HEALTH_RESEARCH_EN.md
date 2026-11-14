# ARTEMIS HEALTH: Research dossier

English submission edition | ARTEMISA | 14 November 2026

This dossier brings together eleven completed documentary investigations. It explains the scientific motivation, public data, application scope, repository findings and remaining validation work. Completion of these investigations does not mean that the product or its validation is complete.

The project is a research prototype for following sleep duration, fatigue, perceived stress and resting pulse. It does not provide a clinically validated diagnosis, prevention guarantee or autonomous space medical capability. Application screens and workflows in the accompanying slides describe intended behavior. The chart is an illustrative calculation using synthetic data.

The Spanish originals remain unchanged. These English editions preserve the substantive conclusions, numerical results, references and uncertainties, with editorial restructuring. Technical evidence is supplied separately with its original identifiers and outputs. The associated repository snapshot is pinned where relevant; later changes are outside the evidence boundary.

## Contents

- Report 001: ARTEMIS HEALTH and biological and psychological follow-up
- Report 002: Health risks in microgravity and partial gravity
- Report 003: Aerospace medicine and applications in microgravity
- Report 004: ARTEMIS repository and research review
- Report 005: User needs and health follow-up scenarios
- Report 006: Existing solutions and proposed differentiation
- Report 007: Rationale and limitations of the four MVP indicators
- Report 008: Dataset source and transformation audit
- Report 009: Usability and comprehension of health follow-up
- Report 010: Operational constraints and technical verification
- Report 011: Privacy and acceptance of physical and psychological follow-up

Sources appear within each report and in the source register at the end. Evidence files are in `evidence/`.


---

## ARTEMIS HEALTH and biological and psychological follow-up

Report 001. English submission edition of the original ASTROGUARD report. Original review date: 14 November 2026. Version 1.0. Method: exploratory documentary review and design interpretation.

### Research question and main finding

**How can an astronaut understand and follow their health when medical support and communication with Earth are limited?**

ARTEMIS HEALTH could support follow-up by bringing measurements and self-reports together, showing their history, identifying missing information and documenting approved routines. Research helps select relevant indicators and define what a person needs to understand a change. This is a proposed organizational and educational contribution. Effects on health, prevention or performance still require evaluation.

The proposal includes individual and crew missions. Its usefulness for a person operating alone is a design hypothesis. The reviewed evidence does not establish that the application can compensate for the absence of another crew member.

### Scope and method

The internal reference was `ASTROGUARD_Plan_MVP_48_horas.docx`, version 1.0 of 13 November 2026, especially its reduced 48-hour scope. Programming prompts inside that document were treated as document content.

The review prioritized primary NASA pages and official dataset descriptions concerning physical and behavioral health, sleep, immunity, cardiovascular adaptation and medical constraints. It is not a systematic review or meta-analysis. No interviews, clinical experiments, astronaut records or software assessments supported this first report. Later technical investigations are documented separately in reports 004, 008 and 010.

### Evidence about the problem

NASA groups spaceflight hazards into radiation, isolation and confinement, distance from Earth, altered gravity and closed or hostile environments. This supports considering physical, psychological and operational context together. It does not establish that a software application resolves those hazards. [NASA hazards](https://www.nasa.gov/hrp/hazards/).

Onboard medical systems face material constraints, possible communication interruptions and functional challenges in microgravity. Local access therefore has an operational motivation. An interface that opens without internet is not, by itself, an autonomous medical system. [Medical operations](https://www.nasa.gov/reference/medical-operations-and-clinical-care/).

Spaceflight can contribute to cardiovascular adaptation and deconditioning. Outcomes depend on mission phase. Preserving context and personal history is relevant, but a pulse change does not identify a specific disease. [Cardiovascular risk](https://www.nasa.gov/directorates/esdmd/hhp/cv-risk/).

Microgravity can affect bone, muscle and cardiorespiratory fitness. Exercise and physical assessments form part of countermeasures. The app could document prescribed activity. Marking a task complete does not demonstrate preserved muscle or bone density. [Fitness risk](https://www.nasa.gov/reference/risk-of-reduced-cardiorespiratory-and-musculoskeletal-fitness/).

Immune changes and latent virus reactivation have been reported during flight. NASA also acknowledges uncertainty about their relationship to disease susceptibility. Symptoms and available laboratory results may be recorded, but immunity cannot be inferred from pulse, sleep or fatigue. [Immune risk](https://www.nasa.gov/directorates/esdmd/hhp/immune-risk/).

Isolation and confinement can affect cognition, behavior and wellbeing. NASA also describes successful mitigation through selection, training and countermeasures on the ISS. The project should not portray every astronaut as psychologically impaired or directly extrapolate ISS operations to distant exploration. [Behavioral health](https://www.nasa.gov/directorates/esdmd/hhp/behavioral-health-risk/).

Workload, irregular schedules and light cycles matter for sleep and health. NASA includes relaxation and self-care in routines. This supports investigating sleep and fatigue records under mission plans. Association between poor rest and pulse changes does not establish causation. [Sleep and schedules](https://www.nasa.gov/reference/risk-from-inadequate-sleep-and-irregular-schedules/).

### Proposed contributions and boundaries

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

### Design safeguards

Sensitive questions should be optional, and wellbeing records should have defined sharing permissions. The system should avoid emotional rankings and rewards for always reporting good health. Fatigue and rest should not incur penalties. Notices should show age and quality of data and explain their trigger. Missing measurements should appear as missing, not as normal health.

Repeated notices need evaluation for overload. Concerning reports should lead to the mission protocol and available support, without improvised therapy. Personal history is a descriptive reference, not a safety guarantee: a persistent condition may already be present in it.

### Implications for data and development

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

### Evaluation questions

| Hypothesis | Proposed test | Outcomes to record |
| --- | --- | --- |
| The panel improves understanding | Ask users to identify values, history, missing data and notice meaning | Correct answers, time and misunderstandings |
| The wellbeing check-in is acceptable | Observe question interpretation and comfort | Omissions, completion time and perceived burden |
| Records continue under the chosen connection conditions | Save, close and retrieve with a defined failure scenario | Loss, duplication and recovery |
| Notices are understandable | Present changed, noisy and old data | Expected notices, errors and diagnostic confusion |
| The design is relevant to aerospace operations | Specialist review | Corrections, limits and documented decisions |

These tests had not been performed in this report. The original 30-second comprehension target was a design goal, not a measured result. Human studies require appropriate consent, governance and institutional review. A volunteer interface test does not establish astronaut efficacy. Model evaluation should separate participants and account for temporal dependence.

### Illustrative scenario and conclusion

A fictional astronaut records less rest and higher perceived fatigue over several days. The panel shows both histories and explains a change without assigning a cause or disease. The user can review educational content and mission follow-up. The scenario is synthetic and cannot show that illness was prevented.

The defensible proposal is to support autonomy in follow-up through understandable records and personal trends. No exhaustive competitor comparison supported a first-or-only claim in this initial review. Clinical prevention and psychological improvement need separate evidence. Later reports identify EveryWear as a close existing reference and clarify the current connected architecture.


---

## Health risks in microgravity and partial gravity

Report 002. English submission edition. Date: 14 November 2026. Version 1.0. Method: exploratory documentary review for project rationale and development.

### Question and main finding

What biological, psychological and operational risks arise during microgravity or reduced gravity, and which parts of follow-up could ARTEMIS HEALTH support?

Reduced mechanical loading, fluid redistribution and changing sensory references affect several body systems. Documented spaceflight risks include bone and muscle loss, cardiovascular deconditioning, visual changes and difficulties with orientation and balance. Magnitude and recovery vary by person, phase and exposure duration. Routine vital signs cannot identify every alteration. Partial gravity on the Moon and Mars should neither be assumed protective nor treated as identical to orbital microgravity.

### Method and limits

Sources include NASA explanations and risk summaries, a technical conference analysis of partial gravity and an original longitudinal bone study. No dataset measurements or individual astronaut records were analyzed for this report. Numerical findings below come from identified publications. No software or clinical efficacy was evaluated.

Flight evidence, terrestrial analogs and destination extrapolation need separate labels. Bed rest, parabolic flight and weight-unloading systems reproduce aspects of exposure, not the complete space environment or chronic response.

### What reduced or zero gravity means

Gravity still acts on an orbiting station. The vehicle and crew fall together, producing apparent weightlessness. Microgravity describes this environment more accurately than disappearance of gravity. Mass and inertia remain. [NASA explanation](https://www.nasa.gov/centers-and-facilities/glenn/what-is-microgravity/).

| Environment | Condition | Research interpretation |
| --- | --- | --- |
| Earth | About 1 g | Everyday posture and activity provide familiar loading. |
| Orbit or a free-fall transit | Microgravity and apparent weightlessness | Human orbital evidence exists with countermeasures and medical support. |
| Lunar surface | About 0.17 g, roughly one-sixth of Earth | Partial loading. Prolonged human residence is insufficiently characterized. |
| Martian surface | About 0.38 g | Long-duration physiological extrapolation remains uncertain. |

These are gravitational proportions, not percentages of risk. [NASA educator reference](https://www.nasa.gov/wp-content/uploads/2018/05/explorediscover_-_teacher.pdf).

### Biological and functional risks

#### Bone and later recovery

Reduced skeletal loading can change remodeling, density and strength, particularly at weight-bearing sites. Pulse and oxygen saturation do not quantify bone loss. [NASA bone risk](https://www.nasa.gov/reference/risk-of-spaceflight-induced-bone-changes/).

Gabel and colleagues followed 17 astronauts after missions of about four to seven months using high-resolution peripheral imaging. Nine had not fully recovered total tibial bone mineral density 12 months after return. This is a cohort-, site- and time-specific result, not a universal rate of irreversible injury. A year of follow-up does not establish that recovery will never occur. [Original study, Scientific Reports 2022, DOI 10.1038/s41598-022-13461-1](https://pmc.ncbi.nlm.nih.gov/articles/PMC9247070/).

The app could document prescribed exercise and available clinical results. It should not estimate bone density from activity or vital signs.

#### Muscle and task capacity

Unloading can reduce muscular and cardiorespiratory fitness, affecting movement and demanding tasks, especially when gravitational loading returns. Resistance and aerobic exercise are countermeasures, but completion alone does not demonstrate preserved function. [NASA fitness risk](https://www.nasa.gov/reference/risk-of-reduced-cardiorespiratory-and-musculoskeletal-fitness/).

The app could record approved routines, perceived effort and assessments. It should not automatically increase training or reward ignoring symptoms.

#### Circulation and transitions

Fluids shift toward the upper body and cardiovascular adaptation occurs. Risk varies by phase, including tolerance to posture or acceleration and performance after return. NASA also investigates venous flow changes and thrombosis within cardiovascular risk. These events do not occur in every astronaut. [Cardiovascular risk](https://www.nasa.gov/directorates/esdmd/hhp/cv-risk/), [medical operations](https://www.nasa.gov/reference/medical-operations-and-clinical-care/).

Available pulse or blood-pressure measurements should retain symptoms, activity and phase. A normal pulse or SpO2 does not exclude cardiovascular abnormalities, clots or orthostatic problems.

#### Eyes and vision

Spaceflight Associated Neuro-ocular Syndrome, SANS, includes findings such as optic-disc edema, retinal folds and posterior globe flattening. Fluid redistribution is an important research hypothesis, not a complete settled explanation. Manifestations and long-term consequences remain under investigation. [NASA SANS](https://www.nasa.gov/reference/risk-of-spaceflight-associated-neuro-ocular-syndrome-sans/).

The app could retain symptoms and professional assessments. A report of normal vision does not rule out SANS, which needs specialist examination.

#### Balance and movement

Altered gravity changes vestibular and sensorimotor function. Motion sickness, nausea, spatial disorientation and difficulties with posture, locomotion or fine motor control may occur. Transitions matter for landing, egress and early extravehicular activity. [NASA sensorimotor risk](https://www.nasa.gov/directorates/esdmd/hhp/sensorimotor-risk/).

A brief symptom record could provide context. The prototype cannot certify fitness for walking, piloting or spacewalks. A simple interface still requires user evaluation.

#### Urinary health

Bone changes can increase urinary calcium. Hydration and urine chemistry also contribute to stone risk. Clinical and urinary assessment cannot be replaced by a wearable. [NASA urinary health](https://www.nasa.gov/ochmo-mtb-003-urinary-health-2/).

The app could record symptoms and provided results or support approved reminders. It should not diagnose stones or determine hydration from pulse.

#### Immunity and interacting factors

Flight studies describe immune changes while radiation, stress, sleep and altered gravity coexist. Attributing every immune change solely to microgravity or predicting infection from indirect signals is unsupported. [NASA immune risk](https://www.nasa.gov/directorates/esdmd/hhp/immune-risk/).

### Psychological context

Physical adaptation and discomfort may coexist with tiredness and wellbeing difficulties. Isolation, confinement, distance and workload are distinct exposures. The reviewed evidence does not establish that microgravity alone causes depression or anxiety. [Behavioral health](https://www.nasa.gov/directorates/esdmd/hhp/behavioral-health-risk/).

Sleep also depends on schedules, lighting, workload and cabin conditions. Sleep, fatigue and perceived stress records provide context without proving a gravity-related cause. [Sleep and irregular schedules](https://www.nasa.gov/reference/risk-from-inadequate-sleep-and-irregular-schedules/).

Mechanical unloading, fluid redistribution and sensorimotor adaptation should be distinguished from radiation, isolation and other interacting hazards. In particular, weightlessness does not generate radiation.

### Partial gravity and open questions

Harry W. Jones's ICES 2021 technical paper argues from indirect evidence that lunar and Martian gravity may be insufficient to maintain conditioning over time. It is not a trial of years of residence on either surface. Its discussion of exposure below 0.4 g is not a validated clinical threshold or a suitable app alert rule. [NASA NTRS 20210019591](https://ntrs.nasa.gov/citations/20210019591).

Open questions include sufficient loading and exercise for each system, combined transit and surface exposure, individual response, and feasible monitoring with limited resources. Orbital rates cannot simply be transferred to another destination.

### Follow-up across phases

| Phase | Relevant issues under mission protocols | Context to preserve |
| --- | --- | --- |
| Entry into microgravity | Sensorimotor adaptation, symptoms and fluid shifts | Exposure start and recent transition |
| Longer stay | Physical fitness, specialist bone/vision/cardiovascular follow-up, rest | Duration, activity, assessments and quality |
| Landing or gravity change | Balance, locomotion and cardiovascular tolerance | Specific transition and critical tasks |
| Postflight | Functional recovery and potentially persistent changes | Time since return and longitudinal results |

This is a design synthesis, not a clinical schedule or symptom prediction.

### Development priorities and pitch

The MVP could identify mission phase and source, show available measurements and history, collect voluntary rest/fatigue reports, and explain limitations. Approved routine tracking and imported clinical assessments are extensions. Specialized instrumentation and operational performance evaluation need further research.

The 48-hour plan does not require a separate detector for every risk. A defensible message is that the body changes how it supports itself, distributes fluids and orients in space, and some effects require follow-up during and after a mission. ARTEMIS proposes to organize relevant information rather than infer all risks from pulse.

Before proceeding, obtain aerospace medicine review, select indicators with clear definitions, document actual sources and assess whether users distinguish descriptive change from a medical conclusion. No prevention, disease detection or gravity-transition safety claim follows from this report.


---

## Aerospace medicine and applications in microgravity

Report 003. English submission edition. Date: 14 November 2026. Version 1.0. Exploratory documentary review with examples of research.

### Main finding and method

Aerospace medicine applies medicine to atmospheric and space flight. It shares clinical foundations with terrestrial care while addressing exposures, operational fitness and mission constraints. It includes prevention, diagnosis, treatment, psychological care and rehabilitation. [National Library of Medicine definition](https://www.ncbi.nlm.nih.gov/mesh/68000337).

This report asks how the specialty works, how delivery differs from terrestrial care and which studies support protection and care in microgravity or partial gravity. The review uses NASA operations sources, exercise and centrifugation studies and the institutional Twins Study results. It is illustrative, not systematic. No individual measurements, software or clinical product efficacy were evaluated.

SPRINT findings were read through indexed original article sections. AGBRESA was reviewed through the DLR abstract and metadata. Twins Study findings here rely on NASA's official summary, not a fresh raw-data analysis.

### Specialty and mission lifecycle

Aviation medicine addresses exposures such as pressure changes, hypoxia and acceleration. Space medicine adds microgravity, longer stays and extravehicular operations. Radiation, cabin conditions, workload and distance also matter. [NASA hazards](https://www.nasa.gov/hrp/hazards/).

At NASA, a flight surgeon is a physician with aerospace medicine training who supports health before, during and after flight. The title does not mean routine surgery aboard the vehicle. Care includes clinical staff, behavioral support, physical conditioning and engineering. [Flight surgeons](https://www.nasa.gov/directorates/esdmd/hhp/flight-surgeons/), [astronaut healthcare](https://www.nasa.gov/missions/station/faq-the-real-story-about-astronaut-health-care-in-space/).

The lifecycle includes preparation and baselines, training and resource planning, inflight monitoring and available treatment, transition and landing assistance, and individualized rehabilitation. Mission destination and constraints change access to communication, specialists and evacuation. [Medical operations](https://www.nasa.gov/reference/medical-operations-and-clinical-care/).

### Comparison with terrestrial care

The reference below is terrestrial care with infrastructure available. Remote communities, expeditions and emergencies share several constraints.

| Aspect | Terrestrial reference | Aerospace adaptation |
| --- | --- | --- |
| Clinical foundations | History, examination, tests and evidence | Retained and interpreted with exposure and task context |
| Environment | Earth gravity and equipment designed for it | Verification for altered gravity, acceleration and cabin conditions |
| Specialists | Possible onsite assessment or referral | Ground support with delays or interruption |
| Diagnostics | Laboratory and imaging according to facility | Selection constrained by mass, volume, power and operation |
| Prevention | Vaccination, occupational care and follow-up | Mission-specific preparation and countermeasures |
| Operational decisions | Daily and occupational capacity | Also piloting, egress, spacewalks and crew protection |
| Continuity | Individual longitudinal records | Comparison before, during and after exposure |
| Psychological care | Assessment and support when needed | Additional confinement, isolation, teamwork and communication context |

The comparison does not imply that terrestrial medicine lacks prevention, telemedicine or personalization.

### Research examples

#### ADUM and remotely guided ultrasound

Advanced Diagnostic Ultrasound in Microgravity developed procedures for crew imaging with training and remote specialist guidance. NASA describes subsequent terrestrial transfer to remote settings. This combines equipment, adequate acquisition, training and professional interpretation. It does not make every image diagnostically reliable. [NASA ADUM transfer](https://www.nasa.gov/missions/station/ultrasound-scans-in-space-transform-medicine-on-earth/).

The institutional summary provides no universal sensitivity or specificity across all conditions. ARTEMIS can learn from structured information and instructions, but storing vital signs is different from performing ultrasound. Synchronous remote guidance also does not by itself solve exploration delays.

#### SPRINT exercise study

English and colleagues compared 26 astronauts in 2020: nine followed higher-intensity/lower-volume SPRINT and 17 an individualized standard program. Subjects selected their groups, so allocation was not randomized. The study described broadly similar bone, muscle and cardiorespiratory outcomes. [Original article, DOI 10.1038/s41526-020-00111-x](https://www.nature.com/articles/s41526-020-00111-x).

Small groups, selection and changing standard care limit causal attribution. Observed similarity does not prove complete protection or suitability for everyone. The application is better supervised exercise programming. ARTEMIS could record approved sessions and assessments, not prescribe automatically.

#### AGBRESA and artificial gravity

An experiment randomized 24 participants among continuous centrifugation, intermittent centrifugation and control during 60 days of six-degree head-down bed rest. Intervention groups received 30 minutes daily. The protocol did not preserve aerobic exercise capacity, although it mitigated some muscular losses. [Kramer et al., 2021, DOI 10.1007/s00421-021-04673-w, DLR record](https://elib.dlr.de/143574/).

This was a terrestrial analog, not a spacecraft with artificial gravity or a lunar/Martian stay. Acceleration distribution and exposure duration matter. The result supports studying protocols and combined countermeasures, not declaring every artificial-gravity approach sufficient or useless. ARTEMIS should distinguish completion from measured outcome.

#### NASA Twins Study

The study compared Scott Kelly during 340 days in space with Mark Kelly on Earth. Ten investigations examined molecular, physiological and cognitive changes. Some returned toward baseline while others required further follow-up. [NASA official results, 2019](https://www.nasa.gov/news-release/nasas-landmark-twins-study-reveals-resilience-of-human-body-in-space/).

One exposed twin and one terrestrial comparator cannot represent all astronauts or isolate gravity from other flight factors. Gene-expression changes do not mean an equivalent fraction of DNA was replaced. The work motivates longitudinal, integrated and personalized questions, not a universal clinical algorithm inferred from pulse.

#### Bone recovery

Gabel and colleagues followed 17 astronauts with specialized imaging. Nine had not fully recovered total tibial mineral density a year after return. That does not establish irreversible damage or whole-skeleton outcomes. [Scientific Reports, 2022, DOI 10.1038/s41598-022-13461-1](https://pmc.ncbi.nlm.nih.gov/articles/PMC9247070/).

The implication is continued outcome assessment after exposure. A pulse graph cannot replace imaging. A tool should store professional results when available and otherwise show missing data.

### Applications to partial gravity and wellbeing

Orbit involves joint free fall under gravity. Lunar and Martian surfaces provide partial loading. Protocols developed in orbit or bed rest need evaluation before transfer. The reviewed technical paper does not establish a universal sufficient gravity threshold. [Microgravity](https://www.nasa.gov/centers-and-facilities/glenn/what-is-microgravity/), [partial-gravity analysis](https://ntrs.nasa.gov/citations/20210019591).

Relevant applications include vehicle-compatible exercise, transition follow-up, imaging under limited assistance and local longitudinal records. Each requires appropriate device validation, training and protocols. Psychological care remains integral. ISS professional support and family contact should not be assumed transferable unchanged to Mars. [NASA healthcare](https://www.nasa.gov/missions/station/faq-the-real-story-about-astronaut-health-care-in-space/).

### Implications for ARTEMIS HEALTH

| Lesson | Proposed functionality | Product evidence needed |
| --- | --- | --- |
| Responses vary by person and phase | Context and personal history | Correct association and understandable comparison |
| Quality and training matter | Explanations and quality flags | Comprehension and error-handling tests |
| Continuity may be interrupted | Defined local or connected architecture | Persistence and recovery under failure |
| Countermeasures need outcomes | Routine and available assessment records | Traceability, without treating adherence as efficacy |
| Specialized tests remain necessary | Indicator method and limitations | Professional content review |
| Wellbeing needs confidentiality | Voluntary reporting and permissions | Governance, access and acceptance evaluation |

These lessons do not automatically expand the 48-hour scope. The defensible first workflow is to record, preserve, consult and understand information. Clinical integration and autonomous interpretation require further work. Studies in flight, randomized analog trials and guided acquisition answer different questions and do not validate the software. Its own operation and usability must be demonstrated before claiming a clinical benefit.


---

## ARTEMIS repository and research review

Report 004. English submission edition. Date: 14 November 2026. Version 1.0. Repository: [Jd1278/ARTEMIS](https://github.com/Jd1278/ARTEMIS). Reviewed branch: `main`. Fixed commit: `92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698`.

This report preserves its historical snapshot. Reports 005 onward use the later commit `80be128b17b5046ecd267d5a0604bbc5c74f5444`.

### Main conclusion and method

ARTEMIS contains research material and technical preparation for ARTEMIS HEALTH, the current name of the project previously called ASTROGUARD. Verified progress concerns requirements, modular organization, data preparation, PostgreSQL schema and limited tests. The end-to-end form, API persistence, history and dashboard are not implemented in this snapshot, as the README acknowledges.

The data package investigates daily sleep, fatigue, stress and resting pulse, with laboratory, environmental radiation and bed-rest material. Possession of files and scripts does not establish disease prediction or clinical efficacy.

The GitHub connector supplied metadata, complete tree, files, branches, commits, pull requests and Actions runs. An isolated checkout of the same commit supported document inspection and local read-oriented checks. No remote repository, database or migration was modified. Word paragraphs and tables were read as source material, including differences later introduced in Markdown.

Documentation, the entry point, connection and preparation code, tests and relevant data scripts were inspected. Every scientific transformation and original NASA file was not independently reaudited here. Evidence is in [the verification record](evidence/004_verificacion_repositorio.json).

### Inventory

The snapshot has 112 tracked files, including 14 `.gitkeep` placeholders. The GitHub tree was not truncated.

| Location | Observed content | Interpretation |
| --- | --- | --- |
| Root README | Identity, links and status | Main entry and acknowledgement of incomplete functionality |
| Requirements DOCX | Scope, requirements, dataset review and acceptance criteria | Historical source with decisions later changed |
| `artemis-healt/docs/` | Current requirements, architecture, design, audit, review and Supabase guidance | Main technical specification |
| `src/artemis_health/` | FastAPI entry, PostgreSQL connection and reserved modules | Application scaffold |
| `frontend/` | Reserved directories and CSS tokens | No compilable React app or frontend dependency manifest |
| `migrations/` | SQL schema, constraints, indexes, roles and RLS | Prepared database code, without remote verification |
| `scripts/` | P0 adapter, migration, seed, verification and SQL export | Implemented preparation tools |
| `data/demo/` | JSON observations and hash manifest | Packaged synthetic data |
| `tests/` | Two automated tests and reserved folders | Contract and artifact coverage, not end-to-end functionality |
| `artemis-sleep-dataset/` | Source copies, processed tables, references and scripts | Research package extending beyond sleep |

[Fixed repository tree](https://github.com/Jd1278/ARTEMIS/tree/92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698).

### History

Three reachable commits were returned, all on 14 November 2026. Times below use Bogotá, UTC−5.

| Time | Commit | Recorded milestone |
| --- | --- | --- |
| 08:59:29 | `5d77f4c` | Initial repository creation |
| 11:44:51 | `a5a8142` | Main structure, with Supabase and Vercel referenced |
| 11:52:16 | `92cf0cf` | Merge of initial histories and README adjustment |

The last commit has two parents and its returned comparison changes the README only. It should not count as another complete implementation. A deployment message alone does not demonstrate production functionality. One branch, zero returned pull requests and zero Actions runs were observed. This does not exclude work outside GitHub or manual tests. [History](https://github.com/Jd1278/ARTEMIS/commits/92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698).

### Research content

The package simulates six fictional crew members over 180 days. It includes self-reported sleep, fatigue, stress, workload, mood, attention and pulse. Events and anomaly labels originate in the generator, not a predictive AI or real clinical event detection. Its cited ISS studies and fatigue instruments motivate simulation parameters, without validating all people or missions.

Laboratory material is attributed to OSDR OSD-569 and OSD-575. It includes blood count and metabolic panels for four participants at seven pre/post timepoints around a three-day flight, plus synthetic panels calibrated from those results. It cannot validate daily alerts over a six-month mission. Derived simulation remains synthetic.

The radiation series is attributed to ISS_DOSANL_TEPC in 2017. Daily aggregation, filling/scaling, reassigned dates and repetition by fictional crew mean these are not contemporary personal exposure measurements. The source package's career-limit percentage is not adopted as an individual medical result.

UTMB Campaign 1 material is attributed to NASA Life Sciences Portal: actigraphy, WinSCAT and tilt tolerance for three subjects in a terrestrial analog. The package documents metadata corrections and exclusion of an alleged heart-rate file duplicating diastolic pressure. This review checked that documentation and absence of the field, without reauditing the original portal.

Sources: [dataset README](https://github.com/Jd1278/ARTEMIS/blob/92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698/artemis-sleep-dataset/README.md), [source register](https://github.com/Jd1278/ARTEMIS/blob/92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698/artemis-sleep-dataset/docs/SOURCES.md), [cleaning report](https://github.com/Jd1278/ARTEMIS/blob/92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698/artemis-sleep-dataset/docs/CLEANING_REPORT.md).

### Verified counts

| Declared source in integrated CSV | Rows | Meaning |
| --- | ---: | --- |
| `simulated` | 12,960 | Synthetic daily variables, including derived measures |
| `simulated_from_real` | 588 | Synthetic calibrated laboratory values |
| `real_nasa_cdaweb` | 4,320 | Historical environmental variables repeated across profiles |
| `real_nasa_osdr` | 1,064 | Processed Inspiration4 laboratory results |
| `real_nasa_lsda` | 1,148 | Terrestrial analog variables |
| Total | 20,080 | Rows, not independent participants or exposures |

Labels alone do not certify external provenance. The product P0 is narrower: 1,080 daily source records become 4,320 observations, all synthetic, across six profiles and four indicators.

| Indicator | Observations | Excluded/null analysis values |
| --- | ---: | ---: |
| Sleep duration | 1,080 | 0 |
| Samn–Perelli fatigue | 1,080 | 7 |
| Perceived stress | 1,080 | 32 |
| Resting pulse | 1,080 | 53 |
| Total | 4,320 | 92 |

The adapter assigns deterministic UUIDs and preserves source file, row and previous value. Flagged imputations or domain errors become `value=null`, with `source_value` preserved. Risk scores, traffic lights and generator anomaly labels do not become product conclusions. [Adapter](https://github.com/Jd1278/ARTEMIS/blob/92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698/artemis-healt/scripts/prepare_demo.py), [manifest](https://github.com/Jd1278/ARTEMIS/blob/92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698/artemis-healt/data/demo/manifest.json).

### Implementation versus proposal

Data preparation and packaged artifacts exist. The API only exposes `/api/health`, returning `scaffold` and `database_checked=false`. Database SQL and administrative scripts exist, but remote provisioning, permissions and persistence were not verified. The frontend and product endpoints are pending. Comparison rules and scientific views are specified, not implemented. No trained clinical model or deployed inference pipeline was found.

The declared Vercel URL could not be retrieved by the web tool. This does not prove an outage. SQL rule configuration is not an analysis implementation, and RLS definitions do not establish complete API authorization.

### Local verification

Using Python 3.13.1 in an isolated checkout:

- Two contract/artifact unit tests passed with exit code 0.
- The package validator returned 46 PASS messages and exit code 0.
- Independent counts confirmed profiles, indicators, UUIDs, source labels and nulls.
- The packaged JSON hash matched its manifest and the adapter output matched semantically.
- Twelve audit hashes matched canonical Git blob bytes. Windows line-ending conversions changed working-copy hashes, so blob bytes were used.
- Importing and inspecting the API confirmed the scaffold. This was not an HTTP or database test in this report.

No source-regenerating `run_all.sh`, dependency installation, SQL application or Supabase verification occurred. Calibration checks test consistency and similarity to generator assumptions, not clinical sensitivity, user benefit or full product operation.

### Findings to resolve

1. The Word document retains SQLite and local offline operation. Current Markdown specifies Supabase/PostgreSQL and defers complete offline support. Mark the DOCX historical or reconcile it.
2. The dictionary says 14,612 integrated rows, while the CSV contains 20,080.
3. The review document says the validator does not guarantee nonzero failure exit. The current script does include `sys.exit(1 if errors else 0)`. The old finding is stale.
4. The inherited cleaner uses days 8–21 as a global reference and bidirectional interpolation. That introduces future information for early-day decisions. P0 excludes those derived outputs and flagged imputations.
5. Supabase guidance records pending verification and a user-reported manual migration. Neither proves a correct remote schema, seed or permissions.
6. No LICENSE file or recognized repository license was found. References are not blanket redistribution permission for code or datasets.
7. The AI disclosure describes data work but retains incomplete entries for web, AI functionality and presentation. Declared tools and human reviews were not independently verified.

Evidence links: [requirements](https://github.com/Jd1278/ARTEMIS/blob/92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698/artemis-healt/docs/requirements.md), [review](https://github.com/Jd1278/ARTEMIS/blob/92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698/artemis-healt/docs/review.md), [dictionary](https://github.com/Jd1278/ARTEMIS/blob/92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698/artemis-sleep-dataset/docs/DATA_DICTIONARY.md), [validator](https://github.com/Jd1278/ARTEMIS/blob/92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698/artemis-sleep-dataset/scripts/validate.py), [cleaner](https://github.com/Jd1278/ARTEMIS/blob/92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698/artemis-sleep-dataset/scripts/clean.py), [Supabase](https://github.com/Jd1278/ARTEMIS/blob/92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698/artemis-healt/docs/supabase.md), [AI disclosure](https://github.com/Jd1278/ARTEMIS/blob/92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698/artemis-sleep-dataset/docs/AI_USAGE.md).

### Research integration and conclusion

At this snapshot, the remote repository did not contain our local `investigacion/` folder or reports 001–004. A remote cleanup manifest for earlier ASTROGUARD files does not show deletion of these local reports. Keep scientific background, technical snapshots, source register and chronology distinct. Correct documentation, implement P0 and then update the pitch with demonstrated results.

The supported advance is a reviewed specification, research package and traceable synthetic selection for four indicators, with local data checks passed. A medical application, autonomous offline operation, clinical training or prevention efficacy is not established. Later commits require a separate snapshot.


---

## User needs and health follow-up scenarios

Report 005. English submission edition. Date: 14 November 2026. Version 1.0. Sequential investigation 1 of 7. Documentary review complete. Human needs validation pending.

### Question, method and conclusion

Which astronaut and medical-team needs justify ARTEMIS HEALTH? Evidence supports investigating information continuity, understanding recorded status and follow-up under mission constraints. It does not establish that this interface meets those needs. Prioritize clear records, source, age, context and interpretation over a global health score.

Primary NASA care, decision-support and human-integration sources were compared with requirements at commit `80be128b17b5046ecd267d5a0604bbc5c74f5444`. README and requirements still identify functional implementation as pending. No astronauts, clinicians or team members were interviewed or contacted. The personas below are hypotheses, not testimonies.

Sources: [NASA CDS concept](https://ntrs.nasa.gov/citations/20205008731), [Health and Medical Care](https://www.nasa.gov/reference/3-0-health-and-medical-care/), [Human Integration Design Handbook](https://www.nasa.gov/organizations/ochmo/human-integration-design-handbook/), [fixed requirements](https://github.com/Jd1278/ARTEMIS/blob/80be128b17b5046ecd267d5a0604bbc5c74f5444/artemis-healt/docs/requirements.md).

The CDS source discusses autonomy, workload and information under resource constraints in a much broader medical system. Handbook use does not establish certification. Product requirements are scope evidence, not proof of demand or clinical benefit.

### Proposed users

| Hypothetical user | Task | Need to test | Design implication |
| --- | --- | --- | --- |
| Crew member | Record and review daily follow-up | Know what exists, its date and meaning | Brief input, history and units |
| Crew medical officer | Organize information for protocols | Distinguish measurements, reports, missing and synthetic data | Visible source and context |
| Ground professional | Review authorized information | Understand sequence, quality and capture conditions | Future traceable summaries |
| Researcher or demo evaluator | Explore information and limits | Separate real studies and fictional profiles | Distinct demo and research spaces |

Existing operations do not show that astronauts lack tools or medical care. The proposed problem is a comprehensible follow-up experience.

### Priority scenarios

Daily check-in: select a fictional profile and mission day, report sleep, fatigue and stress, and consult pulse if an appropriate source exists. Explain scales and distinguish reports from sensors.

Change review: show reference, days used and quality. A difference is not disease. Insufficient compatible history should produce that explicit state.

Save failure: when Supabase is unavailable, preserve the draft during the session and show NOT SAVED. A local page does not eliminate remote persistence dependence. Complete offline storage remains deferred.

Scientific review: keep real studies separate from personal demo history. The P1 scientific view is proposed, not verified.

Individual and crew use: minimize burden, define permissions and avoid public emotional rankings. The product has not been evaluated in solo missions.

### Proposed design decisions

Prioritize four indicators and one small recording/review workflow. Show phase, time, origin, units and quality. Confirm saving only after actual persistence. Separate synthetic, public and reported data in comparisons. Provide reviewed educational explanations and reference mission protocols rather than autonomous clinical recommendations.

These are proposed requirements. Reduced effort, adoption and medical-team usefulness remain unmeasured.

### Prepared interview guide

Propose a consented 20–30-minute session without medical records or personal health questions. Ask about actual work before showing the solution:

1. How do you currently record and review information during an operation or simulation?
2. What context is needed to interpret a change, and what is often missing?
3. Which recording task requires effort or creates confusion?
4. What changes when communication fails or operations transition?
5. Which wellbeing information should remain private, and who could receive it?
6. In a fictional example, what do old, imputed and changed-from-history mean?
7. What must a tool demonstrate to be useful, and what would prevent adoption?

Record general role, context, consented observation and resulting decision. Separate opinion from observed task behavior. Students or analog operators do not automatically represent astronauts.

### Closure

The documentary needs map and interview plan are complete. Human prioritization, acceptable frequency, burden and professional review format remain pending. No evidence of adoption, time savings or willingness to pay exists. Investigation 2 started only after this documentary closure.


---

## Existing solutions and proposed differentiation

Report 006. English submission edition. Date: 14 November 2026. Version 1.0. Sequential investigation 2 of 7. Documentary comparison complete.

### Question and conclusion

What already exists, and what could ARTEMIS contribute? Astronaut health recording and support systems already exist. ARTEMIS should not claim to be the first system unifying space health information. Its proposed position is an academic prototype for comprehensible follow-up, traceability and reproducible demonstration across four indicators. This is a hypothesis, not a demonstrated competitive advantage.

Research began after report 005 closed. Agency/developer sources and a scientific publication were reviewed. No products were tested, no quotations or interviews were requested, and no price comparison occurred. A feature absent from a public description is unverified, not necessarily absent from the product.

### References compared

| Reference | Documented function | Relationship to ARTEMIS | Maturity and limitation |
| --- | --- | --- | --- |
| EveryWear, CNES/MEDES/ESA | Medical and scientific tablet records, questionnaires, private communication and device integration | Closest functional reference. Unified recording is already established as an idea. | Mission use described by responsible organizations, without an independent product audit here |
| SpaceWear, described by ESA | Body-worn physiological acquisition | Instrumentation reference. Software follow-up differs from measurement hardware. | Orbital research/use described, without verifying current commercial specifications |
| Buras and Hilmers exploration medical agents, 2025 | Proposed assistance to medical officers without immediate terrestrial consultation | Clinical scope much broader than descriptive records | Conceptual publication, not clinical autonomy efficacy evidence |

EveryWear documentation describes an app, onboard server and ground services supporting recording, preprocessing and synchronization. ARTEMIS therefore cannot claim novelty merely by combining mobility, data and follow-up. [Marnat et al., IAC 2022 abstract in DLR](https://elib.dlr.de/191550/). MEDES describes operational use and mission-by-mission development. That is a developer account rather than an independent usability comparison. [MEDES](https://www.medes.fr/en/project/everywear-app/).

ESA's SpaceWear description demonstrates existing physiological acquisition research. ARTEMIS's present scope does not automatically measure variables or replace devices. [ESA Health science in orbit](https://www.esa.int/Science_Exploration/Human_and_Robotic_Exploration/Health_science_in_orbit).

Buras and Hilmers describe desirable characteristics and a concept of operations. That does not justify adding diagnosis to P0 or announcing proven autonomy. [npj Microgravity 2025, DOI 10.1038/s41526-025-00503-x](https://www.nature.com/articles/s41526-025-00503-x).

### Differentiation worth testing

Understanding: can explanations reduce confusion about personal change and missing information? Demonstrate this with interpretation tasks rather than screen counts.

Visible traceability: can people recognize simulation, self-report and public sources? Verify both data preservation and interface communication.

Educational reproducibility: can public scenarios support teaching and evaluation? Data preparation exists, but packaging and integration remain pending.

Limited scope: focusing on four indicators is a design choice, not superiority. These attributes may already exist elsewhere. No exclusivity, patentability, lower cost, higher accuracy or time saving was established.

### Application and market hypotheses

University laboratories, training programs and analog missions could be evaluation contexts. They are potential interlocutors, not confirmed customers. Future commercial research needs demand, alternatives, buying authority, integration, maintenance and willingness-to-pay evidence. Market size and revenue were not estimated.

### Pitch recommendation and closure

Describe a developing, explainable and traceable follow-up experience for investigating physical and wellbeing information in space contexts. Avoid unique, first, better than NASA systems, proven cheaper or autonomous medical assistant.

The documentary comparison closed with a direct reference and testable differentiation. User comparison and specialist review remain pending. No advantage was invented to fill that gap.


---

## Rationale and limitations of the four MVP indicators

Report 007. English submission edition. Date: 14 November 2026. Version 1.0. Sequential investigation 3 of 7. Documentary review complete. Protocol, permissions and translations need specialist review.

### Conclusion and method

Sleep, fatigue, perceived stress and resting pulse support a limited investigation of everyday follow-up. They do not provide a complete assessment of space health or infer immunity, bone density or disease. Selection is suitable for a demonstration, without proving operational sufficiency.

The investigation began after report 006. Original studies, instrument custodians, institutional fatigue documentation and cardiovascular guidance were reviewed. No clinical thresholds or custom-scale validity were invented. [Fixed product requirements](https://github.com/Jd1278/ARTEMIS/blob/80be128b17b5046ecd267d5a0604bbc5c74f5444/artemis-healt/docs/requirements.md).

Jones et al. followed 24 astronauts across approximately six-month ISS missions using reports and vigilance tests. Shorter sleep was associated with slower response and greater perceived stress/workload. An observational association does not establish an individual diagnosis or product efficacy. [Sleep 2022, DOI 10.1093/sleep/zsac006](https://pmc.ncbi.nlm.nih.gov/articles/PMC8919197/).

### Interpretation sheets

| Field | Meaning | Capture requirements | Unsupported inference |
| --- | --- | --- | --- |
| `sleep_duration_h` | Estimated sleep during a defined episode | Hours, recall period, record time and method. Distinguish time in bed and naps. | Sleep stages, insomnia diagnosis or polysomnographic accuracy |
| `samn_perelli` | Subjective fatigue in seven ordinal categories | Preserve 1–7 and consistent category descriptions | Automatic operational fitness, diagnosis or ratio interpretation |
| `stress_vas` | Perceived stress under a defined question and anchors | Period, endpoints, entry method and 0–100 scale | Psychological disorder, hormone level or medical risk |
| `resting_hr_bpm` | Beat frequency in a specified resting context | Beats/minute, device/method, activity and quality | Blood pressure, full ECG, oxygenation or exclusion of disease |

#### Sleep

The Consensus Sleep Diary provides a reference for standardized prospective self-monitoring and distinguishes sleep components. A single hours field is not implementation or validation of that instrument. [Carney et al., 2012, DOI 10.5665/sleep.1642](https://pmc.ncbi.nlm.nih.gov/articles/PMC3250369/).

The university custodian specifies conditions for unaltered nonprofit use with citation. Full reproduction, adaptation or commercial use needs permission clarification. The form is not reproduced here. [University of Pittsburgh](https://www.sleep.pitt.edu/research/measures-and-study-instruments).

#### Fatigue

ICAO-hosted documentation describes Samn–Perelli as a seven-point subjective scale. Aviation evidence does not automatically validate a Spanish translation or clinical space decision. [ICAO Biomathematical Fatigue Models, 2014](https://www.icao.int/safety/fatiguemanagement/ArticlesPublications/biomathematical_fatigue_models.pdf).

Preserve ordinal meaning: a six is above a three, not twice the fatigue. Show category or point changes without percentage improvement. Review translation and instructions before claiming a validated version.

#### Perceived stress

Lesage et al. examined discriminative sensitivity and relationships with related constructs for a visual analogue stress measure in a terrestrial setting. Evidence is specific to that instrument and population. A digital slider or changed wording/period needs further evaluation. [Occupational Medicine 2012, DOI 10.1093/occmed/kqs140](https://pubmed.ncbi.nlm.nih.gov/22965867/).

State perceived stress and the reporting period. Zero is a response to a question, not proof of no psychological problem.

#### Resting pulse

The AHA distinguishes pulse and blood pressure and describes effects of posture, activity, emotion, temperature and medicines. Comparisons require consistent context. Educational terrestrial ranges are not universal astronaut traffic-light rules. [AHA](https://www.heart.org/en/health-topics/high-blood-pressure/the-facts-about-high-blood-pressure/all-about-heart-rate-pulse).

Before device integration, specify method, placement, resting period, accuracy and operating conditions. No medical measurement protocol is prescribed here, and no connected sensor is assumed.

### Product rules and quality

Sleep 0–24 h, integer fatigue 1–7, stress 0–100 and positive pulse are technical input domains. They do not separate healthy and ill. The reference of up to 14 prior days within 30, requiring seven valid days, is an engineering choice without clinical validation established by this review.

Compare compatible observations and exclude the current/future day and flagged imputation. Personal history is not a safety guarantee because a persistent condition may already be represented.

### Closure

Four indicator descriptions and interpretation requirements are complete. Professional review, instrument permissions, translation, stress entry format and comprehension tests remain pending. No sensor accuracy or clinical benefit was measured. Investigation 4 followed this documentary closure.


---

## Dataset source and transformation audit

Report 008. English submission edition. Date: 14 November 2026. Version 1.0. Sequential investigation 4 of 7. Limited audit complete, with coverage boundaries.

### Method and conclusion

After report 007 closed, commit `80be128b17b5046ecd267d5a0604bbc5c74f5444` was examined. Two public OSDR CSVs were downloaded into memory and their pivots compared with repository copies. No project data were modified and no source-overwriting pipeline was executed. [Evidence](evidence/008_auditoria_fuentes.json) records aggregates, exact URLs, hashes and methods. No new individual-data CSVs were saved in the research folder.

The two OSDR sources could be traced to the preserved pivots. HAPI radiation units were confirmed. This does not validate all downstream clinical corrections, the complete radiation series or NLSP provenance. Product P0 remains synthetic.

### Provenance chain

| Group | Chain | Check performed | Boundary |
| --- | --- | --- | --- |
| Daily simulation | Generator, cleaner, P0 adapter | Code, labels and exclusions | Distribution similarity is not real patient data or predictive validity. |
| OSD-569 blood count | Public long CSV, wide pivot, cleaning | HTTP 200, 553 input rows, 28 pivot rows matching the repository in columns and values | Later correction and clinical ranges need review. |
| OSD-575 metabolic panel | Public long CSV, wide pivot, cleaning | HTTP 200, 531 input rows, 28 matching pivot rows | Not every derived result is validated. |
| TEPC | HAPI rates and intervals, daily aggregation, scaling/imputation, fictional calendar | Metadata and two source days sampled | No full 180-day recomputation or personal dose evaluation. |
| NLSP | Attributed UTMB Campaign 1 files, cleaning and summary | Repository and documentation inspection | Portal could not be retrieved for independent comparison. |

OSDR pivots used subject, sex, timepoint and analyte as in `fetch_osdr.py`. No duplicate analyte keys occurred in the current two sources. Matching a pivot establishes neither clinical meaning nor representativeness.

### Primary sources checked

[OSD-569](https://osdr.nasa.gov/bio/repo/data/studies/OSD-569), file `LSDS-7_Complete_Blood_Count_CBC.upload_SUBMITTED.csv`, and [OSD-575](https://osdr.nasa.gov/bio/repo/data/studies/OSD-575), file `LSDS-8_Comprehensive_Metabolic_Panel_CMP.upload_SUBMITTED.csv`, were retrieved using the script's download service. Exact responses and SHA-256 appear in the evidence record.

[HAPI ISS_DOSANL_TEPC metadata](https://cdaweb.gsfc.nasa.gov/hapi/info?id=ISS_DOSANL_TEPC) specifies `DOSE` in µGy/min, `DOSE_EQ60` in µSv/min and `TIME_INTERVAL` in minutes. These are rates requiring interval integration, not daily doses.

[The declared NLSP campaign](https://nlsp.nasa.gov/explore/data/details/6eaf1654-72d4-5d71-a9dd-a02e674c6473?dataType=MISSIONS) was not independently retrieved. [OSDR terms](https://science.nasa.gov/reference/osdr-help-terms-and-conditions/) reference information policy and request study-specific citation. Public download does not replace permissions and attribution records.

### Transformation findings

P0 selects four indicators, preserves source and excludes flagged imputation from analysis. The earlier artifact had 4,320 observations and 92 nulls; later operational checks repeat that count.

The inherited cleaner interpolates bidirectionally and uses days 8–21 for a mission-wide reference. These retrospective operations require disclosure and cannot demonstrate early detection without future information. A per-direction interpolation limit also does not prove a maximum total original gap of two days. P0 avoids these derived outputs and flagged values.

Radiation cleaning uses centered and global medians, scales partial coverage and reassigns dates. Not every final value is direct measurement. Preserve measured, scaled and imputed distinctions. Instrument environmental dose equivalent is not automatically individual effective dose or a personal career-limit fraction.

The downloader deduplicates by minute rather than a complete record identity. On 1 March 2017 the sample contained 1,440 unique timestamps and no duplicates. On 6 April it contained 1,351 records and 90 repeated timestamps, matching minute-based duplicates in that sample. Two days cannot establish a universal deduplication policy, especially if timestamps or values differ. Define treatment of conflicting records before full recomputation.

Laboratory column corrections, calculated values and reference intervals require derived-value flags and clinical rationale. A pivoted file labeled raw is already transformed; retain the original downloaded file hash as well.

### Acceptance decisions

Synthetic P0 is appropriate for software scenarios with explicit labels, nulls and origin, not efficacy. OSDR provenance to pivot is supported, but citations, terms and clinical cleaning remain to close. TEPC belongs in a historical environmental view pending full integration and specialist review. NLSP remains attributed material until source, terms and transformations are independently checked. Integrated repeated rows cannot become independent model samples.

### Closure

Evidence hashes apply to downloads on 14 November 2026. Source updates need a new snapshot. Canonical Git bytes were used in the earlier hash audit to avoid Windows line-ending differences.

This limited audit is complete with additional provenance support and an explicit unresolved list. It is not a complete scientific audit of every source or correction. Investigation 5 followed this closure.


---

## Usability and comprehension of health follow-up

Report 009. English submission edition. Date: 14 November 2026. Version 1.0. Sequential investigation 5 of 7. Methodological review complete. No human tests performed.

### Question and method

How can the team establish that users understand a panel without mistaking observations for diagnoses? Observe tasks and explanations, errors and time. Attractive design, automated checks or developer opinion do not establish human comprehension.

After report 008, primary evaluation and accessibility sources were reviewed. No participants or simulated responses were used. This report provides a protocol and [empty recording template](templates/009_usability_record.csv), not user results.

### Evidence

[NIST Usability Testing](https://www.nist.gov/programs-projects/usability-testing) describes task completion, errors, time and qualitative observations to examine effectiveness, efficiency and satisfaction in a defined context.

[NASA Systems Engineering Processes](https://www.nasa.gov/reference/3-0-systems-engineering-processes-vol-2/) describes iterative human-in-the-loop testing for operational and interface issues. This formative adaptation is not aerospace certification.

[W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/) provides keyboard, label, contrast and non-color communication criteria. Passing selected checks does not establish full conformance.

### Questions to test

Can the person distinguish synthetic from manual records, missing from zero, and old from current data? Do they understand descriptive comparison and insufficient history? Can they recognize a failed save and recover a draft? Can they use keyboard navigation and a small screen?

Visible origin and explanations may reduce confusion, while brief forms may reduce burden. These are hypotheses.

### Prepared formative protocol

Invite adults from an available context and separately seek medical/operations experience. A proposed five-to-eight-person pilot can identify issues, not estimate population performance or represent astronauts. Use codes, general roles and no personal medical information.

Obtain consent, allow withdrawal and use fictional scenarios and a fixed interface version. Do not induce sleep deprivation, stress or physical exposure. If a mockup is used, assess that mockup rather than software persistence.

Explain that the tool is being evaluated. Give tasks without pointing to controls, observe, record assistance and then ask for interpretation. Explanation by the moderator during a task changes the measurement and needs recording.

| Task | Expected evidence | Important error |
| --- | --- | --- |
| T1 Latest observation | Correct value, unit, time and origin | Treating fictional data as an actual astronaut record |
| T2 Fictional input | Correct scale and saving state | Assuming sent means stored despite failure |
| T3 Missing values | Recognizing absence | Reading no data as healthy or zero |
| T4 Comparison | Reference, period and descriptive meaning | Inferring diagnosis or guaranteed safety |
| T5 Profile/origin change | Distinct histories | Mixing people or sources |
| T6 Simulated connection failure | NOT SAVED and draft recovery | Believing durable offline storage already exists |

### Metrics and proposed criteria

Record unassisted success, assisted success or failure, time, number/type of helps, errors, explanation and a clearly labeled nonvalidated ease question. Do not call that question SUS or NASA-TLX.

Preserve the engineering goal of finding main information within two screens. Set any timing goal before testing. Record denominators, withdrawals and unexecutable tasks. Missing results are not zero. A medical interpretation or save-confirmation error merits investigation even if other tasks perform well. Small pilots should report case details and counts rather than generalized astronaut satisfaction rates.

### Accessibility review prepared

Check focus and keyboard operation, control names, field errors, text with states, table alternatives to charts, zoom and planned screen sizes. WCAG AA's normal-text contrast reference is 4.5:1, with conditions and exceptions. A compliant color token does not establish application compliance.

### Closure

The rationale, tasks, protocol and template are complete. A testable interface, consent and sessions remain pending. The correct presentation claim is that a comprehension evaluation is prepared, not that astronauts validated the experience. Operational investigation followed without treating human validation as complete.


---

## Operational constraints and technical verification

Report 010. English submission edition. Date: 14 November 2026. Version 1.0. Sequential investigation 6 of 7. Documentary and local verification complete. No remote database or space-environment validation.

### Question and conclusion

What should happen when communication, data or components fail? Distinguish interface availability, API, storage and external link. The architecture depends on Supabase for persistence and does not establish autonomous space operation. It can be investigated as a connected prototype with possible later local storage and synchronization.

After report 009 closed, commit `80be128b17b5046ecd267d5a0604bbc5c74f5444` was fixed. It adds visual identity relative to report 004 but retains the API scaffold. Requirements and connection code were inspected and tests ran in an isolated checkout. Only the research evidence file was written outside that checkout. No remote database was accessed.

[NASA/TM-2019-220335](https://ntrs.nasa.gov/citations/20200001702) describes exploration medical communication and evacuation/resupply constraints. These motivate continuity and autonomy, but slow terrestrial networking does not reproduce the full space context. [Supabase connection documentation](https://supabase.com/docs/guides/database/connecting-to-postgres) describes pool/connection considerations, not elimination of remote dependence.

### Executed checks

[Evidence JSON](evidence/010_operacion.json) preserves commands, output and in-process HTTP responses under Python 3.13.1.

| Check | Result | Meaning |
| --- | --- | --- |
| Contract/artifact unit tests | Two passed, exit 0 | Data coverage, not full product workflow |
| Package validator | 46 PASS, exit 0 | Consistency with rules, not clinical validity |
| P0 artifact | 4,320 synthetic observations, six profiles, 92 nulls | Prepared demonstration selection |
| GET `/api/health` | 200, scaffold, database unchecked | Service entry only |
| GET profiles, indicators, example dashboard | 404 | Product routes absent |
| POST observations, fictional example | 404 | No save or Supabase contact |

The 404 results describe unfinished functionality, not accepted workflows. FastAPI TestClient operated inside the process. There was no public server or space network. The frontend remains reserved with logo and visual tokens, not a functional interaction.

### Failure matrix for later evaluation

| Condition | Proposed behavior | Required evidence | Status |
| --- | --- | --- | --- |
| API unavailable | Clear message and draft under agreed scope | Interrupt API during task | Pending integration |
| Supabase unreachable | No false save confirmation; session draft | Timeout test | Pending |
| Response lost after save | Idempotent retry | One stored row; conflict for altered UUID content | Designed, not remotely verified |
| Old/missing data | Visible age or absence | Fixed cases and table/chart agreement | Pending UI |
| Invalid or incompatible input | Explain rejection without partial write | API/SQL tests in test environment | Constraints written, integration pending |
| Profile/origin changed | Separate histories and references | Multiple-profile/source cases | Contract prepared |
| Close/restart | Explicit durable and nondurable state | Controlled client/server restart | Pending |

### Levels of autonomy

A connected demonstration stores remotely when a link exists and is the present intended scope, still awaiting integration. Durable local operation additionally needs appropriate local storage, bundled resources and recovery tests. Operation across disrupted links adds queues, synchronization, conflict management, audit and operational procedures. That third level is future research.

Finish and measure the selected level before adding unnecessary distributed services. Before claiming offline support, test reload, closure, restart, retries and persistence without an external link.

### Decisions and limits

Separate sent from confirmed saved. Preserve source, quality and time. Version comparisons and expose fictional calendar context. SQL and RLS definitions need authorized remote verification and do not replace API controls.

Performance, energy, radiation tolerance, sensor accuracy, usability and full security were not measured. No dependencies, migrations or publications were performed. These checks do not establish flight readiness.

### Closure and sources

The fixed-snapshot operational investigation is complete. A full save–retrieve–restart workflow and connection failure test are the next useful evidence. Marketing should describe development and intended follow-up rather than proven offline autonomy or implemented real-time monitoring.

Technical sources: [requirements](https://github.com/Jd1278/ARTEMIS/blob/80be128b17b5046ecd267d5a0604bbc5c74f5444/artemis-healt/docs/requirements.md), [API](https://github.com/Jd1278/ARTEMIS/blob/80be128b17b5046ecd267d5a0604bbc5c74f5444/artemis-healt/src/artemis_health/main.py), [Supabase design](https://github.com/Jd1278/ARTEMIS/blob/80be128b17b5046ecd267d5a0604bbc5c74f5444/artemis-healt/docs/supabase.md).


---

## Privacy and acceptance of physical and psychological follow-up

Report 011. English submission edition. Date: 14 November 2026. Version 1.0. Sequential investigation 7 of 7. Documentary research and evaluation design complete. Human acceptance and comprehensive compliance unvalidated.

### Question and method

How can wellbeing follow-up avoid becoming intrusive surveillance? Minimize information, explain purpose and recipients, distinguish sensitive data and evaluate acceptance. Written consent alone does not establish trust, and an access policy does not prove implementation.

The investigation began after report 010 closed. Medical operations, data protection and technical-security sources were compared with a fictional-only demo. No personal health or emotional responses were collected. This report does not certify legal compliance or determine medical-device classification.

### Evidence

[NASA Medical Operations](https://www.nasa.gov/reference/6-0-medical-operations/) includes private medical and psychological communication. This supports separating personal confidentiality and mission coordination rather than exposing every record to the crew.

Colombian Law 1581 classifies health data as sensitive and establishes special treatment rules. If real information is collected, the team and institution must determine purpose, responsible parties, authorization or applicable grounds and rights. A hackathon label or alias is not an assumed exception. [Official law compilation](https://normograma.dian.gov.co/dian/compilacion/docs/ley_1581_2012.htm), [SIC interpretation](https://sedeelectronica.sic.gov.co/publicaciones/boletin-juridico/concepto/tratamiento-de-datos-sensibles-relativos-la-salud). Other jurisdictions, transfers and institutional procedures were not resolved here.

[OWASP authorization guidance](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html) recommends least privilege, default denial and request-level checks. [Supabase RLS](https://supabase.com/docs/guides/database/postgres/row-level-security) describes row policies. Privileged roles can alter protection, so actual identities and permissions need tests. Neither source certifies the project.

### Separate data contexts

| Context | Proposed information | Recommended treatment |
| --- | --- | --- |
| Public demo | Fictional profiles and measurements | Visible simulation and no invitation to upload real medical records |
| Interface evaluation | Participant code, task, time and errors on fictional scenarios | Defined consent and retention, no names or personal medical questions |
| Public research | Source files and appropriately deidentified material | Attribution and source terms, no reidentification attempts |
| Future real use | Potentially sensitive readings and reports | Governance, authorization, access and institutional review before collection |

An alias remains pseudonymous if someone can link it to a person. Small crews, dates and roles can also identify individuals. Deleting a row from a public repository does not undo historical exposure.

### Proposed access matrix

The person should understand their records, purpose and recipients. An authorized professional needs only relevant access with traceability. Crew-wide information should follow operational protocols without emotional rankings. Researchers need study-appropriate access rather than unrestricted convenience. Technical administrators need limited permissions and role separation.

This is a future design. Current backend permissions target demo data without a complete real-user workflow. Demo/research separation is not equivalent to isolation among real patients. Comprehensive authorization and security were not tested.

### Acceptance hypothesis

Explaining purpose, allowing questions to be skipped and defining recipients may improve acceptance. This effect has not been measured. Avoid rewarding low stress, penalizing tiredness or pressuring positive responses because these could distort reports. This is design reasoning, not an experimental result.

Acceptance interviews should ask about scenarios: information a person would share with a professional or colleague, optional questions and required explanations. Record reasons and role differences without asking participants to disclose psychological experiences.

### Consent and management preparation

Before sessions, define institutional contact/responsibility, purpose, records, storage, access, retention and consultation/withdrawal procedures. Recording requires a separate clear decision. A default interface test can use fictional scenarios without recordings or real health collection.

Retention should follow purpose and institutional review rather than an invented universal legal duration. Document disposal or anonymization where appropriate. The institution should determine applicable ethics review for sensitive or clinical research.

### Closure

Documentary research and the privacy proposal are complete. Implementation, permission tests, institutional review and human acceptance remain pending. This closes the seventh sequential investigation. Commercial writing followed afterward using documented findings and actual technical results, without presenting missing validation as complete.


---

## Source register

Consultation date: 14 November 2026. This register links primary sources and the reports using them. Consult the reports for population, methods, transformation and inference limits. Exact URLs and hashes for independent data checks appear in evidence 008.

### Background sources

| ID | Source | Use and limitation |
| --- | --- | --- |
| F01 | [NASA, Five Hazards](https://www.nasa.gov/hrp/hazards/) | Context, without product efficacy |
| F02 | [NASA, Medical Operations and Clinical Care](https://www.nasa.gov/reference/medical-operations-and-clinical-care/) | Care constraints, without endorsement |
| F03 | [NASA, Cardiovascular Risk](https://www.nasa.gov/directorates/esdmd/hhp/cv-risk/) | Phase-dependent risk, not universal app thresholds |
| F04 | [NASA, Fitness Risk](https://www.nasa.gov/reference/risk-of-reduced-cardiorespiratory-and-musculoskeletal-fitness/) | Exercise and assessments, not adherence-based efficacy |
| F05 | [NASA, Immune Risk](https://www.nasa.gov/directorates/esdmd/hhp/immune-risk/) | Changes and clinical uncertainty |
| F06 | [NASA, Behavioral Health Risk](https://www.nasa.gov/directorates/esdmd/hhp/behavioral-health-risk/) | Context and mitigation, not universal impairment |
| F07 | [NASA, Sleep and Irregular Schedules](https://www.nasa.gov/reference/risk-from-inadequate-sleep-and-irregular-schedules/) | Relevance of sleep and workload |
| F08 | [PhysioNet, BIDMC v1.0.0](https://physionet.org/content/bidmc/1.0.0/) | DOI 10.13026/C2208R. ICU data. ODC Attribution 1.0 conditions apply. |
| F09 | [UCI, PPG-DaLiA](https://archive.ics.uci.edu/dataset/495/ppg+dalia) | DOI 10.24432/C53890. Fifteen terrestrial participants. CC BY 4.0 shown by custodian. |
| F10 | [UCI, WESAD](https://archive.ics.uci.edu/dataset/465/wesad+wearable+stress+and+affect+detection) | DOI 10.24432/C57K5T. Fifteen laboratory participants. Consult original terms. |
| F11 | [NASA OSDR FAQ](https://science.nasa.gov/reference/osdr-faq/) | Repository scope and access, study-specific checks needed |
| F12 | [NASA, What Is Microgravity](https://www.nasa.gov/centers-and-facilities/glenn/what-is-microgravity/) | Physical explanation of joint free fall |
| F13 | [NASA, Bone Risk](https://www.nasa.gov/reference/risk-of-spaceflight-induced-bone-changes/) | Loading and bone follow-up |
| F14 | [Gabel et al., Scientific Reports 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9247070/) | DOI 10.1038/s41598-022-13461-1. Seventeen astronauts, tibial recovery after 12 months. Not irreversible universal loss. |
| F15 | [NASA, SANS](https://www.nasa.gov/reference/risk-of-spaceflight-associated-neuro-ocular-syndrome-sans/) | Specialized ocular findings and unresolved mechanism |
| F16 | [NASA, Sensorimotor Risk](https://www.nasa.gov/directorates/esdmd/hhp/sensorimotor-risk/) | Transitions, orientation and motor function |
| F17 | [NASA, Urinary Health](https://www.nasa.gov/ochmo-mtb-003-urinary-health-2/) | Clinical assessment context, not treatment instructions |
| F18 | [Jones, ICES 2021, NTRS 20210019591](https://ntrs.nasa.gov/citations/20210019591) | Indirect partial-gravity analysis, no validated 0.4 g clinical threshold |
| F19 | [NASA educator guide](https://www.nasa.gov/wp-content/uploads/2018/05/explorediscover_-_teacher.pdf) | Physical gravity proportions, not medical risk rates |
| F20 | [NLM MeSH Aerospace Medicine](https://www.ncbi.nlm.nih.gov/mesh/68000337) | Discipline definition |
| F21 | [NASA Flight Surgeons](https://www.nasa.gov/directorates/esdmd/hhp/flight-surgeons/) | NASA operational role, not universal country-specific training requirements |
| F22 | [NASA Astronaut Healthcare](https://www.nasa.gov/missions/station/faq-the-real-story-about-astronaut-health-care-in-space/) | ISS care and rehabilitation context |
| F23 | [NASA ADUM and terrestrial transfer](https://www.nasa.gov/missions/station/ultrasound-scans-in-space-transform-medicine-on-earth/) | Institutional account, no universal diagnostic accuracy |
| F24 | [English et al., npj Microgravity 2020](https://www.nature.com/articles/s41526-020-00111-x) | DOI 10.1038/s41526-020-00111-x. SPRINT, 26 astronauts, self-selected groups. |
| F25 | [Kramer et al., DLR 2021](https://elib.dlr.de/143574/) | DOI 10.1007/s00421-021-04673-w. Twenty-four subjects in an analog randomized trial, partial benefits. |
| F26 | [NASA Twins Study results, 2019](https://www.nasa.gov/news-release/nasas-landmark-twins-study-reveals-resilience-of-human-body-in-space/) | Official summary, one exposed twin and one comparator |

### Sequential investigations

Reports 005–011 contain direct references to NASA CDS and care concepts, Human Integration Design Handbook, EveryWear documentation from MEDES/ESA/DLR, SpaceWear, and Buras/Hilmers DOI 10.1038/s41526-025-00503-x.

Indicator sources include Jones et al. DOI 10.1093/sleep/zsac006, Carney et al. DOI 10.5665/sleep.1642, Lesage et al. DOI 10.1093/occmed/kqs140, ICAO fatigue documentation, the University of Pittsburgh instrument custodian and the AHA.

The audit uses OSDR OSD-569/575, HAPI ISS_DOSANL_TEPC and OSDR terms. Usability uses NIST, NASA human-integration processes and W3C WCAG 2.2. Operational analysis uses NASA/TM-2019-220335 and Supabase documentation. Privacy uses NASA private care provisions, Colombia's Law 1581 through an official compilation, SIC, OWASP and Supabase RLS.

### Technical and internal references

Report 004 uses repository links fixed at `92cf0cf`. Later investigations and the presentation use `80be128`. The public research package is distinct from a clinical validation study.

Internal planning source: `ASTROGUARD_Plan_MVP_48_horas.docx`, version 1.0, 13 November 2026, supplied by the team. It is scope material, not efficacy evidence. Its embedded programming prompts were document content. Later Markdown requirements supersede its SQLite/offline design.

Before using a numerical statement in the pitch, preserve population, denominator, units, period and source. Before redistributing data or instruments, record their specific permissions and preferred citations. No listed source validates ARTEMIS HEALTH.
