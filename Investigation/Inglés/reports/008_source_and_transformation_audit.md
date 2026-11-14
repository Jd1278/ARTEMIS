# Dataset source and transformation audit

Report 008. English submission edition. Date: 14 November 2026. Version 1.0. Sequential investigation 4 of 7. Limited audit complete, with coverage boundaries.

## Method and conclusion

After report 007 closed, commit `80be128b17b5046ecd267d5a0604bbc5c74f5444` was examined. Two public OSDR CSVs were downloaded into memory and their pivots compared with repository copies. No project data were modified and no source-overwriting pipeline was executed. [Evidence](../evidence/008_auditoria_fuentes.json) records aggregates, exact URLs, hashes and methods. No new individual-data CSVs were saved in the research folder.

The two OSDR sources could be traced to the preserved pivots. HAPI radiation units were confirmed. This does not validate all downstream clinical corrections, the complete radiation series or NLSP provenance. Product P0 remains synthetic.

## Provenance chain

| Group | Chain | Check performed | Boundary |
| --- | --- | --- | --- |
| Daily simulation | Generator, cleaner, P0 adapter | Code, labels and exclusions | Distribution similarity is not real patient data or predictive validity. |
| OSD-569 blood count | Public long CSV, wide pivot, cleaning | HTTP 200, 553 input rows, 28 pivot rows matching the repository in columns and values | Later correction and clinical ranges need review. |
| OSD-575 metabolic panel | Public long CSV, wide pivot, cleaning | HTTP 200, 531 input rows, 28 matching pivot rows | Not every derived result is validated. |
| TEPC | HAPI rates and intervals, daily aggregation, scaling/imputation, fictional calendar | Metadata and two source days sampled | No full 180-day recomputation or personal dose evaluation. |
| NLSP | Attributed UTMB Campaign 1 files, cleaning and summary | Repository and documentation inspection | Portal could not be retrieved for independent comparison. |

OSDR pivots used subject, sex, timepoint and analyte as in `fetch_osdr.py`. No duplicate analyte keys occurred in the current two sources. Matching a pivot establishes neither clinical meaning nor representativeness.

## Primary sources checked

[OSD-569](https://osdr.nasa.gov/bio/repo/data/studies/OSD-569), file `LSDS-7_Complete_Blood_Count_CBC.upload_SUBMITTED.csv`, and [OSD-575](https://osdr.nasa.gov/bio/repo/data/studies/OSD-575), file `LSDS-8_Comprehensive_Metabolic_Panel_CMP.upload_SUBMITTED.csv`, were retrieved using the script's download service. Exact responses and SHA-256 appear in the evidence record.

[HAPI ISS_DOSANL_TEPC metadata](https://cdaweb.gsfc.nasa.gov/hapi/info?id=ISS_DOSANL_TEPC) specifies `DOSE` in µGy/min, `DOSE_EQ60` in µSv/min and `TIME_INTERVAL` in minutes. These are rates requiring interval integration, not daily doses.

[The declared NLSP campaign](https://nlsp.nasa.gov/explore/data/details/6eaf1654-72d4-5d71-a9dd-a02e674c6473?dataType=MISSIONS) was not independently retrieved. [OSDR terms](https://science.nasa.gov/reference/osdr-help-terms-and-conditions/) reference information policy and request study-specific citation. Public download does not replace permissions and attribution records.

## Transformation findings

P0 selects four indicators, preserves source and excludes flagged imputation from analysis. The earlier artifact had 4,320 observations and 92 nulls; later operational checks repeat that count.

The inherited cleaner interpolates bidirectionally and uses days 8–21 for a mission-wide reference. These retrospective operations require disclosure and cannot demonstrate early detection without future information. A per-direction interpolation limit also does not prove a maximum total original gap of two days. P0 avoids these derived outputs and flagged values.

Radiation cleaning uses centered and global medians, scales partial coverage and reassigns dates. Not every final value is direct measurement. Preserve measured, scaled and imputed distinctions. Instrument environmental dose equivalent is not automatically individual effective dose or a personal career-limit fraction.

The downloader deduplicates by minute rather than a complete record identity. On 1 March 2017 the sample contained 1,440 unique timestamps and no duplicates. On 6 April it contained 1,351 records and 90 repeated timestamps, matching minute-based duplicates in that sample. Two days cannot establish a universal deduplication policy, especially if timestamps or values differ. Define treatment of conflicting records before full recomputation.

Laboratory column corrections, calculated values and reference intervals require derived-value flags and clinical rationale. A pivoted file labeled raw is already transformed; retain the original downloaded file hash as well.

## Acceptance decisions

Synthetic P0 is appropriate for software scenarios with explicit labels, nulls and origin, not efficacy. OSDR provenance to pivot is supported, but citations, terms and clinical cleaning remain to close. TEPC belongs in a historical environmental view pending full integration and specialist review. NLSP remains attributed material until source, terms and transformations are independently checked. Integrated repeated rows cannot become independent model samples.

## Closure

Evidence hashes apply to downloads on 14 November 2026. Source updates need a new snapshot. Canonical Git bytes were used in the earlier hash audit to avoid Windows line-ending differences.

This limited audit is complete with additional provenance support and an explicit unresolved list. It is not a complete scientific audit of every source or correction. Investigation 5 followed this closure.
