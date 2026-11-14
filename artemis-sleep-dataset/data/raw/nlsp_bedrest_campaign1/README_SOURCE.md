# Raw real data — UTMB Bed Rest Campaign 1 (NASA Life Sciences Portal, open access)

Downloaded 2026-11-14 from https://nlsp.nasa.gov (bulk-download of open-access datasets), Campaign 1 of the
University of Texas Medical Branch (UTMB) Flight Analogs Research Unit: 3 healthy subjects (C1G0001-C1G0003),
60 days of 6-degree head-down-tilt bed rest (a NASA analog of microgravity), Sept-Nov 2004.

| File | Source experiment | Notes |
|---|---|---|
| `BRSMACT_Campagin_1_Actigraphy.csv` | BRSMAct — Bed Rest Standard Measures: Actilight (actigraphy) | Verbatim. File name typo "Campagin" kept as published. 207 nights (3 subjects x 69). |
| `BRSMACT_Campaign_1_Actigraphy_ReadMe.txt` | BRSMAct | Verbatim. |
| (not stored) `BRSMACT_Campagin_1_Actigraphy_Query_Result` | BRSMAct | 191 rows; analysed but not used — see CLEANING_REPORT (subject labels are wrong). |
| `MR085G_Campaign_1_WinSCAT_All.csv` | MR085G — Neurocognitive Assessment (WinSCAT) | Verbatim. 30 test sessions (3 subjects x 10). |
| `MR085G_Campaign_1_WinSCAT_ReadMe.txt` | MR085G | Verbatim (header says "MR010G" and "Subject C1G0002": metadata errors in the source). |
| `MR001G_Campaign_1_Tilt_session_summary.csv` | MR001G — Neuroendocrine and Cardiovascular Response to Tilt | **Derived** per session from the source minute-by-minute SBP/DBP files (MR001G_Campaign_1_Tilt_SBP, _DBP). The source "_HR" file is a copy of the DBP file and was not used. |
