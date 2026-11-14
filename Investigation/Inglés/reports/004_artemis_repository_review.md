# ARTEMIS repository and research review

Report 004. English submission edition. Date: 14 November 2026. Version 1.0. Repository: [Jd1278/ARTEMIS](https://github.com/Jd1278/ARTEMIS). Reviewed branch: `main`. Fixed commit: `92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698`.

This report preserves its historical snapshot. Reports 005 onward use the later commit `80be128b17b5046ecd267d5a0604bbc5c74f5444`.

## Main conclusion and method

ARTEMIS contains research material and technical preparation for ARTEMIS HEALTH, the current name of the project previously called ASTROGUARD. Verified progress concerns requirements, modular organization, data preparation, PostgreSQL schema and limited tests. The end-to-end form, API persistence, history and dashboard are not implemented in this snapshot, as the README acknowledges.

The data package investigates daily sleep, fatigue, stress and resting pulse, with laboratory, environmental radiation and bed-rest material. Possession of files and scripts does not establish disease prediction or clinical efficacy.

The GitHub connector supplied metadata, complete tree, files, branches, commits, pull requests and Actions runs. An isolated checkout of the same commit supported document inspection and local read-oriented checks. No remote repository, database or migration was modified. Word paragraphs and tables were read as source material, including differences later introduced in Markdown.

Documentation, the entry point, connection and preparation code, tests and relevant data scripts were inspected. Every scientific transformation and original NASA file was not independently reaudited here. Evidence is in [the verification record](../evidence/004_verificacion_repositorio.json).

## Inventory

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

## History

Three reachable commits were returned, all on 14 November 2026. Times below use Bogotá, UTC−5.

| Time | Commit | Recorded milestone |
| --- | --- | --- |
| 08:59:29 | `5d77f4c` | Initial repository creation |
| 11:44:51 | `a5a8142` | Main structure, with Supabase and Vercel referenced |
| 11:52:16 | `92cf0cf` | Merge of initial histories and README adjustment |

The last commit has two parents and its returned comparison changes the README only. It should not count as another complete implementation. A deployment message alone does not demonstrate production functionality. One branch, zero returned pull requests and zero Actions runs were observed. This does not exclude work outside GitHub or manual tests. [History](https://github.com/Jd1278/ARTEMIS/commits/92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698).

## Research content

The package simulates six fictional crew members over 180 days. It includes self-reported sleep, fatigue, stress, workload, mood, attention and pulse. Events and anomaly labels originate in the generator, not a predictive AI or real clinical event detection. Its cited ISS studies and fatigue instruments motivate simulation parameters, without validating all people or missions.

Laboratory material is attributed to OSDR OSD-569 and OSD-575. It includes blood count and metabolic panels for four participants at seven pre/post timepoints around a three-day flight, plus synthetic panels calibrated from those results. It cannot validate daily alerts over a six-month mission. Derived simulation remains synthetic.

The radiation series is attributed to ISS_DOSANL_TEPC in 2017. Daily aggregation, filling/scaling, reassigned dates and repetition by fictional crew mean these are not contemporary personal exposure measurements. The source package's career-limit percentage is not adopted as an individual medical result.

UTMB Campaign 1 material is attributed to NASA Life Sciences Portal: actigraphy, WinSCAT and tilt tolerance for three subjects in a terrestrial analog. The package documents metadata corrections and exclusion of an alleged heart-rate file duplicating diastolic pressure. This review checked that documentation and absence of the field, without reauditing the original portal.

Sources: [dataset README](https://github.com/Jd1278/ARTEMIS/blob/92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698/artemis-sleep-dataset/README.md), [source register](https://github.com/Jd1278/ARTEMIS/blob/92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698/artemis-sleep-dataset/docs/SOURCES.md), [cleaning report](https://github.com/Jd1278/ARTEMIS/blob/92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698/artemis-sleep-dataset/docs/CLEANING_REPORT.md).

## Verified counts

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

## Implementation versus proposal

Data preparation and packaged artifacts exist. The API only exposes `/api/health`, returning `scaffold` and `database_checked=false`. Database SQL and administrative scripts exist, but remote provisioning, permissions and persistence were not verified. The frontend and product endpoints are pending. Comparison rules and scientific views are specified, not implemented. No trained clinical model or deployed inference pipeline was found.

The declared Vercel URL could not be retrieved by the web tool. This does not prove an outage. SQL rule configuration is not an analysis implementation, and RLS definitions do not establish complete API authorization.

## Local verification

Using Python 3.13.1 in an isolated checkout:

- Two contract/artifact unit tests passed with exit code 0.
- The package validator returned 46 PASS messages and exit code 0.
- Independent counts confirmed profiles, indicators, UUIDs, source labels and nulls.
- The packaged JSON hash matched its manifest and the adapter output matched semantically.
- Twelve audit hashes matched canonical Git blob bytes. Windows line-ending conversions changed working-copy hashes, so blob bytes were used.
- Importing and inspecting the API confirmed the scaffold. This was not an HTTP or database test in this report.

No source-regenerating `run_all.sh`, dependency installation, SQL application or Supabase verification occurred. Calibration checks test consistency and similarity to generator assumptions, not clinical sensitivity, user benefit or full product operation.

## Findings to resolve

1. The Word document retains SQLite and local offline operation. Current Markdown specifies Supabase/PostgreSQL and defers complete offline support. Mark the DOCX historical or reconcile it.
2. The dictionary says 14,612 integrated rows, while the CSV contains 20,080.
3. The review document says the validator does not guarantee nonzero failure exit. The current script does include `sys.exit(1 if errors else 0)`. The old finding is stale.
4. The inherited cleaner uses days 8–21 as a global reference and bidirectional interpolation. That introduces future information for early-day decisions. P0 excludes those derived outputs and flagged imputations.
5. Supabase guidance records pending verification and a user-reported manual migration. Neither proves a correct remote schema, seed or permissions.
6. No LICENSE file or recognized repository license was found. References are not blanket redistribution permission for code or datasets.
7. The AI disclosure describes data work but retains incomplete entries for web, AI functionality and presentation. Declared tools and human reviews were not independently verified.

Evidence links: [requirements](https://github.com/Jd1278/ARTEMIS/blob/92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698/artemis-healt/docs/requirements.md), [review](https://github.com/Jd1278/ARTEMIS/blob/92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698/artemis-healt/docs/review.md), [dictionary](https://github.com/Jd1278/ARTEMIS/blob/92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698/artemis-sleep-dataset/docs/DATA_DICTIONARY.md), [validator](https://github.com/Jd1278/ARTEMIS/blob/92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698/artemis-sleep-dataset/scripts/validate.py), [cleaner](https://github.com/Jd1278/ARTEMIS/blob/92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698/artemis-sleep-dataset/scripts/clean.py), [Supabase](https://github.com/Jd1278/ARTEMIS/blob/92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698/artemis-healt/docs/supabase.md), [AI disclosure](https://github.com/Jd1278/ARTEMIS/blob/92cf0cfe0bcc40f0c59548d104d8ad9ca40ac698/artemis-sleep-dataset/docs/AI_USAGE.md).

## Research integration and conclusion

At this snapshot, the remote repository did not contain our local `investigacion/` folder or reports 001–004. A remote cleanup manifest for earlier ASTROGUARD files does not show deletion of these local reports. Keep scientific background, technical snapshots, source register and chronology distinct. Correct documentation, implement P0 and then update the pitch with demonstrated results.

The supported advance is a reviewed specification, research package and traceable synthetic selection for four indicators, with local data checks passed. A medical application, autonomous offline operation, clinical training or prevention efficacy is not established. Later commits require a separate snapshot.
