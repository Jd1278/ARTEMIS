"""
fetch_osdr.py — Downloads the original Inspiration4 blood panel files from NASA OSDR
and pivots them into data/raw/osdr_inspiration4/*_wide.csv (same format clean_osdr.py reads).
Requires internet access to osdr.nasa.gov.

Usage: python scripts/fetch_osdr.py
"""
import io
import urllib.request
import pandas as pd

BASE = "https://osdr.nasa.gov/geode-py/ws/studies/{s}/download?source=datamanager&file={f}"
FILES = {
    "cmp_OSD-575_wide.csv": ("OSD-575", "LSDS-8_Comprehensive_Metabolic_Panel_CMP.upload_SUBMITTED.csv", "timepoint"),
    "cbc_OSD-569_wide.csv": ("OSD-569", "LSDS-7_Complete_Blood_Count_CBC.upload_SUBMITTED.csv", "TEST_DATE"),
}
for out, (study, fname, tcol) in FILES.items():
    raw = urllib.request.urlopen(BASE.format(s=study, f=fname)).read().decode()
    df = pd.read_csv(io.StringIO(raw), dtype=str)
    df.to_csv(f"data/raw/osdr_inspiration4/{study}_{fname}", index=False)  # keep original
    wide = df.pivot_table(index=["SUBJECT_ID", "SEX", tcol], columns="ANALYTE", values="VALUE",
                          aggfunc="first", sort=False).reset_index()
    wide.columns = ["subject", "sex", "timepoint"] + list(wide.columns[3:])
    wide.to_csv(f"data/raw/osdr_inspiration4/{out}", index=False)
    print("saved", out, wide.shape)
