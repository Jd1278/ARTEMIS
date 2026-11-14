# Aerospace medicine and applications in microgravity

Report 003. English submission edition. Date: 14 November 2026. Version 1.0. Exploratory documentary review with examples of research.

## Main finding and method

Aerospace medicine applies medicine to atmospheric and space flight. It shares clinical foundations with terrestrial care while addressing exposures, operational fitness and mission constraints. It includes prevention, diagnosis, treatment, psychological care and rehabilitation. [National Library of Medicine definition](https://www.ncbi.nlm.nih.gov/mesh/68000337).

This report asks how the specialty works, how delivery differs from terrestrial care and which studies support protection and care in microgravity or partial gravity. The review uses NASA operations sources, exercise and centrifugation studies and the institutional Twins Study results. It is illustrative, not systematic. No individual measurements, software or clinical product efficacy were evaluated.

SPRINT findings were read through indexed original article sections. AGBRESA was reviewed through the DLR abstract and metadata. Twins Study findings here rely on NASA's official summary, not a fresh raw-data analysis.

## Specialty and mission lifecycle

Aviation medicine addresses exposures such as pressure changes, hypoxia and acceleration. Space medicine adds microgravity, longer stays and extravehicular operations. Radiation, cabin conditions, workload and distance also matter. [NASA hazards](https://www.nasa.gov/hrp/hazards/).

At NASA, a flight surgeon is a physician with aerospace medicine training who supports health before, during and after flight. The title does not mean routine surgery aboard the vehicle. Care includes clinical staff, behavioral support, physical conditioning and engineering. [Flight surgeons](https://www.nasa.gov/directorates/esdmd/hhp/flight-surgeons/), [astronaut healthcare](https://www.nasa.gov/missions/station/faq-the-real-story-about-astronaut-health-care-in-space/).

The lifecycle includes preparation and baselines, training and resource planning, inflight monitoring and available treatment, transition and landing assistance, and individualized rehabilitation. Mission destination and constraints change access to communication, specialists and evacuation. [Medical operations](https://www.nasa.gov/reference/medical-operations-and-clinical-care/).

## Comparison with terrestrial care

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

## Research examples

### ADUM and remotely guided ultrasound

Advanced Diagnostic Ultrasound in Microgravity developed procedures for crew imaging with training and remote specialist guidance. NASA describes subsequent terrestrial transfer to remote settings. This combines equipment, adequate acquisition, training and professional interpretation. It does not make every image diagnostically reliable. [NASA ADUM transfer](https://www.nasa.gov/missions/station/ultrasound-scans-in-space-transform-medicine-on-earth/).

The institutional summary provides no universal sensitivity or specificity across all conditions. ARTEMIS can learn from structured information and instructions, but storing vital signs is different from performing ultrasound. Synchronous remote guidance also does not by itself solve exploration delays.

### SPRINT exercise study

English and colleagues compared 26 astronauts in 2020: nine followed higher-intensity/lower-volume SPRINT and 17 an individualized standard program. Subjects selected their groups, so allocation was not randomized. The study described broadly similar bone, muscle and cardiorespiratory outcomes. [Original article, DOI 10.1038/s41526-020-00111-x](https://www.nature.com/articles/s41526-020-00111-x).

Small groups, selection and changing standard care limit causal attribution. Observed similarity does not prove complete protection or suitability for everyone. The application is better supervised exercise programming. ARTEMIS could record approved sessions and assessments, not prescribe automatically.

### AGBRESA and artificial gravity

An experiment randomized 24 participants among continuous centrifugation, intermittent centrifugation and control during 60 days of six-degree head-down bed rest. Intervention groups received 30 minutes daily. The protocol did not preserve aerobic exercise capacity, although it mitigated some muscular losses. [Kramer et al., 2021, DOI 10.1007/s00421-021-04673-w, DLR record](https://elib.dlr.de/143574/).

This was a terrestrial analog, not a spacecraft with artificial gravity or a lunar/Martian stay. Acceleration distribution and exposure duration matter. The result supports studying protocols and combined countermeasures, not declaring every artificial-gravity approach sufficient or useless. ARTEMIS should distinguish completion from measured outcome.

### NASA Twins Study

The study compared Scott Kelly during 340 days in space with Mark Kelly on Earth. Ten investigations examined molecular, physiological and cognitive changes. Some returned toward baseline while others required further follow-up. [NASA official results, 2019](https://www.nasa.gov/news-release/nasas-landmark-twins-study-reveals-resilience-of-human-body-in-space/).

One exposed twin and one terrestrial comparator cannot represent all astronauts or isolate gravity from other flight factors. Gene-expression changes do not mean an equivalent fraction of DNA was replaced. The work motivates longitudinal, integrated and personalized questions, not a universal clinical algorithm inferred from pulse.

### Bone recovery

Gabel and colleagues followed 17 astronauts with specialized imaging. Nine had not fully recovered total tibial mineral density a year after return. That does not establish irreversible damage or whole-skeleton outcomes. [Scientific Reports, 2022, DOI 10.1038/s41598-022-13461-1](https://pmc.ncbi.nlm.nih.gov/articles/PMC9247070/).

The implication is continued outcome assessment after exposure. A pulse graph cannot replace imaging. A tool should store professional results when available and otherwise show missing data.

## Applications to partial gravity and wellbeing

Orbit involves joint free fall under gravity. Lunar and Martian surfaces provide partial loading. Protocols developed in orbit or bed rest need evaluation before transfer. The reviewed technical paper does not establish a universal sufficient gravity threshold. [Microgravity](https://www.nasa.gov/centers-and-facilities/glenn/what-is-microgravity/), [partial-gravity analysis](https://ntrs.nasa.gov/citations/20210019591).

Relevant applications include vehicle-compatible exercise, transition follow-up, imaging under limited assistance and local longitudinal records. Each requires appropriate device validation, training and protocols. Psychological care remains integral. ISS professional support and family contact should not be assumed transferable unchanged to Mars. [NASA healthcare](https://www.nasa.gov/missions/station/faq-the-real-story-about-astronaut-health-care-in-space/).

## Implications for ARTEMIS HEALTH

| Lesson | Proposed functionality | Product evidence needed |
| --- | --- | --- |
| Responses vary by person and phase | Context and personal history | Correct association and understandable comparison |
| Quality and training matter | Explanations and quality flags | Comprehension and error-handling tests |
| Continuity may be interrupted | Defined local or connected architecture | Persistence and recovery under failure |
| Countermeasures need outcomes | Routine and available assessment records | Traceability, without treating adherence as efficacy |
| Specialized tests remain necessary | Indicator method and limitations | Professional content review |
| Wellbeing needs confidentiality | Voluntary reporting and permissions | Governance, access and acceptance evaluation |

These lessons do not automatically expand the 48-hour scope. The defensible first workflow is to record, preserve, consult and understand information. Clinical integration and autonomous interpretation require further work. Studies in flight, randomized analog trials and guided acquisition answer different questions and do not validate the software. Its own operation and usability must be demonstrated before claiming a clinical benefit.
