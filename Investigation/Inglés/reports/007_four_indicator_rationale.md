# Rationale and limitations of the four MVP indicators

Report 007. English submission edition. Date: 14 November 2026. Version 1.0. Sequential investigation 3 of 7. Documentary review complete. Protocol, permissions and translations need specialist review.

## Conclusion and method

Sleep, fatigue, perceived stress and resting pulse support a limited investigation of everyday follow-up. They do not provide a complete assessment of space health or infer immunity, bone density or disease. Selection is suitable for a demonstration, without proving operational sufficiency.

The investigation began after report 006. Original studies, instrument custodians, institutional fatigue documentation and cardiovascular guidance were reviewed. No clinical thresholds or custom-scale validity were invented. [Fixed product requirements](https://github.com/Jd1278/ARTEMIS/blob/80be128b17b5046ecd267d5a0604bbc5c74f5444/artemis-healt/docs/requirements.md).

Jones et al. followed 24 astronauts across approximately six-month ISS missions using reports and vigilance tests. Shorter sleep was associated with slower response and greater perceived stress/workload. An observational association does not establish an individual diagnosis or product efficacy. [Sleep 2022, DOI 10.1093/sleep/zsac006](https://pmc.ncbi.nlm.nih.gov/articles/PMC8919197/).

## Interpretation sheets

| Field | Meaning | Capture requirements | Unsupported inference |
| --- | --- | --- | --- |
| `sleep_duration_h` | Estimated sleep during a defined episode | Hours, recall period, record time and method. Distinguish time in bed and naps. | Sleep stages, insomnia diagnosis or polysomnographic accuracy |
| `samn_perelli` | Subjective fatigue in seven ordinal categories | Preserve 1–7 and consistent category descriptions | Automatic operational fitness, diagnosis or ratio interpretation |
| `stress_vas` | Perceived stress under a defined question and anchors | Period, endpoints, entry method and 0–100 scale | Psychological disorder, hormone level or medical risk |
| `resting_hr_bpm` | Beat frequency in a specified resting context | Beats/minute, device/method, activity and quality | Blood pressure, full ECG, oxygenation or exclusion of disease |

### Sleep

The Consensus Sleep Diary provides a reference for standardized prospective self-monitoring and distinguishes sleep components. A single hours field is not implementation or validation of that instrument. [Carney et al., 2012, DOI 10.5665/sleep.1642](https://pmc.ncbi.nlm.nih.gov/articles/PMC3250369/).

The university custodian specifies conditions for unaltered nonprofit use with citation. Full reproduction, adaptation or commercial use needs permission clarification. The form is not reproduced here. [University of Pittsburgh](https://www.sleep.pitt.edu/research/measures-and-study-instruments).

### Fatigue

ICAO-hosted documentation describes Samn–Perelli as a seven-point subjective scale. Aviation evidence does not automatically validate a Spanish translation or clinical space decision. [ICAO Biomathematical Fatigue Models, 2014](https://www.icao.int/safety/fatiguemanagement/ArticlesPublications/biomathematical_fatigue_models.pdf).

Preserve ordinal meaning: a six is above a three, not twice the fatigue. Show category or point changes without percentage improvement. Review translation and instructions before claiming a validated version.

### Perceived stress

Lesage et al. examined discriminative sensitivity and relationships with related constructs for a visual analogue stress measure in a terrestrial setting. Evidence is specific to that instrument and population. A digital slider or changed wording/period needs further evaluation. [Occupational Medicine 2012, DOI 10.1093/occmed/kqs140](https://pubmed.ncbi.nlm.nih.gov/22965867/).

State perceived stress and the reporting period. Zero is a response to a question, not proof of no psychological problem.

### Resting pulse

The AHA distinguishes pulse and blood pressure and describes effects of posture, activity, emotion, temperature and medicines. Comparisons require consistent context. Educational terrestrial ranges are not universal astronaut traffic-light rules. [AHA](https://www.heart.org/en/health-topics/high-blood-pressure/the-facts-about-high-blood-pressure/all-about-heart-rate-pulse).

Before device integration, specify method, placement, resting period, accuracy and operating conditions. No medical measurement protocol is prescribed here, and no connected sensor is assumed.

## Product rules and quality

Sleep 0–24 h, integer fatigue 1–7, stress 0–100 and positive pulse are technical input domains. They do not separate healthy and ill. The reference of up to 14 prior days within 30, requiring seven valid days, is an engineering choice without clinical validation established by this review.

Compare compatible observations and exclude the current/future day and flagged imputation. Personal history is not a safety guarantee because a persistent condition may already be represented.

## Closure

Four indicator descriptions and interpretation requirements are complete. Professional review, instrument permissions, translation, stress entry format and comprehension tests remain pending. No sensor accuracy or clinical benefit was measured. Investigation 4 followed this documentary closure.
