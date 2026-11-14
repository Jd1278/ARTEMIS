# Raw real data — SpaceX Inspiration4 (NASA OSDR)

Pivoted to one row per subject x timepoint from the original long-format files, values unchanged (row order kept as in source):

- `cmp_OSD-575_wide.csv` <- OSD-575, `LSDS-8_Comprehensive_Metabolic_Panel_CMP.upload_SUBMITTED.csv`
  https://osdr.nasa.gov/bio/repo/data/studies/OSD-575
- `cbc_OSD-569_wide.csv` <- OSD-569, `LSDS-7_Complete_Blood_Count_CBC.upload_SUBMITTED.csv`
  https://osdr.nasa.gov/bio/repo/data/studies/OSD-569

Crew: 4 civilian astronauts (C001-C004), 3-day orbital flight, Sept 16-18 2021.
Timepoints: L-92, L-44, L-3 (days before launch); R+1, R+45, R+82, R+194 (days after return). No in-flight blood draws in these panels.
Lab reference ranges per analyte/sex are in the original files (see `scripts/clean_osdr.py` for the ranges used).
To re-download the originals: `python scripts/fetch_osdr.py` (needs internet access to osdr.nasa.gov).
