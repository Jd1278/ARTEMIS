"""
clean_osdr.py — OPTION D (REAL DATA): cleans the SpaceX Inspiration4 blood panels
from NASA OSDR (OSD-575 metabolic panel, OSD-569 complete blood count).

Inputs : data/raw/osdr_inspiration4/{cmp_OSD-575_wide.csv, cbc_OSD-569_wide.csv}
Outputs: data/processed/inspiration4_blood_long.csv   (tidy: 1 row = subject x timepoint x analyte)
         data/processed/inspiration4_blood_wide.csv   (1 row = subject x timepoint)
         data/processed/inspiration4_change_R1_vs_preflight.csv
         appends a section to docs/CLEANING_REPORT.md
"""
import numpy as np
import pandas as pd

RAW = "data/raw/osdr_inspiration4/"
rep = []

cmp_ = pd.read_csv(RAW + "cmp_OSD-575_wide.csv", na_values=["NA", ""])
cbc = pd.read_csv(RAW + "cbc_OSD-569_wide.csv", na_values=["NA", ""])

# ---- 1. CBC: C003 L-92 row is shifted one column to the right from MCH onward
row = (cbc.subject == "C003") & (cbc.timepoint == "L-92")
shift_cols = ["MCH", "MCHC", "RDW", "PLATELET COUNT", "MPV", "ABSOLUTE NEUTROPHILS",
              "ABSOLUTE LYMPHOCYTES", "ABSOLUTE MONOCYTES", "ABSOLUTE EOSINOPHILS", "ABSOLUTE BASOPHILS"]
vals = cbc.loc[row, shift_cols[1:]].values[0]
cbc.loc[row, shift_cols] = list(vals) + [np.nan]
rep.append("CBC C003 L-92: values from MCH to absolute basophils were shifted one column "
           "(e.g., platelets reported as 12.9 and MPV as 330); realigned. Verified: "
           "absolute neutrophils 6826 = WBC 9.6 x 71.1%.")

# ---- 2. CBC: analyte names with '(FEMALE)' suffix -> merge into standard names
for a in ["RED BLOOD CELL COUNT", "HEMOGLOBIN", "HEMATOCRIT"]:
    fem = f"{a} (FEMALE)"
    n = cbc[a].isna() & cbc[fem].notna()
    cbc.loc[n, a] = cbc.loc[n, fem]
    rep.append(f"CBC: {n.sum()} value(s) of '{fem}' merged into '{a}'")
cbc = cbc.drop(columns=[c for c in cbc.columns if c.endswith("(FEMALE)")])

# ---- 3. CBC: derive missing red-cell indices / absolute counts with standard formulas
def fill(col, expr, label):
    m = cbc[col].isna()
    cbc.loc[m, col] = expr[m].round(1)
    if m.any():
        rep.append(f"CBC: {m.sum()} missing `{col}` derived as {label}")
fill("MCHC", cbc["HEMOGLOBIN"] / cbc["HEMATOCRIT"] * 100, "HGB / HCT x 100")
fill("MCH", cbc["HEMOGLOBIN"] / cbc["RED BLOOD CELL COUNT"] * 10, "HGB / RBC x 10")
fill("MCV", cbc["HEMATOCRIT"] / cbc["RED BLOOD CELL COUNT"] * 10, "HCT / RBC x 10")
m = cbc["ABSOLUTE BASOPHILS"].isna()
cbc.loc[m, "ABSOLUTE BASOPHILS"] = (cbc["WHITE BLOOD CELL COUNT"] * cbc["BASOPHILS"] * 10)[m].round()
rep.append(f"CBC: {m.sum()} missing absolute basophils derived as WBC x basophil% x 10")

# ---- 4. CMP: BUN/creatinine ratio only reported by the lab when abnormal -> compute
m = cmp_["BUN/CREATININE RATIO"].isna()
cmp_["BUN/CREATININE RATIO"] = (cmp_["UREA NITROGEN (BUN)"] / cmp_["CREATININE"]).round(1)
rep.append(f"CMP: BUN/creatinine ratio computed for all rows ({m.sum()} were blank/'NA')")
cmp_ = cmp_.drop(columns=["eGFR AFRICAN AMERICAN"])
rep.append("CMP: race-based eGFR column dropped (race coefficient no longer recommended, "
           "NKF-ASN 2021); `eGFR NON-AFR. AMERICAN` kept as `EGFR`")
cmp_ = cmp_.rename(columns={"eGFR NON-AFR. AMERICAN": "EGFR"})
m = cmp_["BILIRUBIN; TOTAL"].isna().sum()
rep.append(f"CMP: {m} missing total bilirubin left as missing (no way to derive it)")

# ---- 5. Long format + reference ranges (sex-specific, from the source lab files)
RANGES = {  # analyte: (unit, male_min, male_max, female_min, female_max)
    "GLUCOSE": ("mg/dL", 65, 99, 65, 99), "UREA NITROGEN (BUN)": ("mg/dL", 7, 25, 7, 25),
    "CREATININE": ("mg/dL", 0.6, 1.35, 0.5, 1.05), "EGFR": ("mL/min/1.73m2", 60, np.nan, 60, np.nan),
    "BUN/CREATININE RATIO": ("ratio", 6, 22, 6, 22), "SODIUM": ("mmol/L", 135, 146, 135, 146),
    "POTASSIUM": ("mmol/L", 3.5, 5.3, 3.5, 5.3), "CHLORIDE": ("mmol/L", 98, 110, 98, 110),
    "CARBON DIOXIDE": ("mmol/L", 20, 32, 20, 32), "CALCIUM": ("mg/dL", 8.6, 10.3, 8.6, 10.4),
    "PROTEIN; TOTAL": ("g/dL", 6.1, 8.1, 6.1, 8.1), "ALBUMIN": ("g/dL", 3.6, 5.1, 3.6, 5.1),
    "GLOBULIN": ("g/dL", 1.9, 3.7, 1.9, 3.7), "ALBUMIN/GLOBULIN RATIO": ("ratio", 1, 2.5, 1, 2.5),
    "BILIRUBIN; TOTAL": ("mg/dL", 0.2, 1.2, 0.2, 1.2), "ALKALINE PHOSPHATASE": ("U/L", 36, 130, 37, 153),
    "AST": ("U/L", 10, 40, 10, 35), "ALT": ("U/L", 9, 46, 6, 29),
    "WHITE BLOOD CELL COUNT": ("10^3/uL", 3.8, 10.8, 3.8, 10.8),
    "RED BLOOD CELL COUNT": ("10^6/uL", 4.2, 5.8, 3.8, 5.1), "HEMOGLOBIN": ("g/dL", 13.2, 17.1, 11.7, 15.5),
    "HEMATOCRIT": ("%", 38.5, 50, 35, 45), "MCV": ("fL", 80, 100, 80, 100), "MCH": ("pg", 27, 33, 27, 33),
    "MCHC": ("g/dL", 32, 36, 32, 36), "RDW": ("%", 11, 15, 11, 15),
    "PLATELET COUNT": ("10^3/uL", 140, 400, 140, 400), "MPV": ("fL", 7.5, 12.5, 7.5, 12.5),
    "ABSOLUTE NEUTROPHILS": ("cells/uL", 1500, 7800, 1500, 7800),
    "ABSOLUTE LYMPHOCYTES": ("cells/uL", 850, 3900, 850, 3900),
    "ABSOLUTE MONOCYTES": ("cells/uL", 200, 950, 200, 950),
    "ABSOLUTE EOSINOPHILS": ("cells/uL", 15, 500, 15, 500), "ABSOLUTE BASOPHILS": ("cells/uL", 0, 200, 0, 200),
    "NEUTROPHILS": ("%", 38, 80, 38, 80), "LYMPHOCYTES": ("%", 15, 49, 15, 49),
    "MONOCYTES": ("%", 0, 13, 0, 13), "EOSINOPHILS": ("%", 0, 8, 0, 8), "BASOPHILS": ("%", 0, 2, 0, 2),
}
rep.append("Reference ranges: the source applied MALE ranges to female crew member C003 at 3 "
           "preflight timepoints (e.g., hemoglobin 13.2-17.1) and the female lab ranges changed "
           "between draws; one sex-specific range per analyte is applied consistently here.")

frames = []
for panel, df in [("CMP", cmp_), ("CBC", cbc)]:
    lg = df.melt(id_vars=["subject", "sex", "timepoint"], var_name="analyte", value_name="value")
    lg["panel"] = panel
    frames.append(lg)
long = pd.concat(frames, ignore_index=True)
r = long["analyte"].map(RANGES)
long["unit"] = r.str[0]
male = long["sex"].eq("M")
long["ref_min"] = np.where(male, r.str[1], r.str[3])
long["ref_max"] = np.where(male, r.str[2], r.str[4])
long["flag"] = np.select(
    [long["value"].isna(), long["value"] < long["ref_min"],
     long["ref_max"].notna() & (long["value"] > long["ref_max"])],
    ["missing", "low", "high"], "normal")

# ---- 6. Timepoints -> numeric
tp = long["timepoint"].str.extract(r"([LR])([+-]\d+)")
long["phase"] = np.where(tp[0] == "L", "preflight", "postflight")
long["days_from_launch"] = np.where(tp[0] == "L", tp[1].astype(int), tp[1].astype(int) + 3)
long["days_rel_event"] = tp[1].astype(int)  # vs launch (L) or vs return (R)

# ---- 7. Review flags (possible pre-analytical artifacts; hypotheses, not diagnoses)
long["review_note"] = ""
g45 = (long.analyte == "GLUCOSE") & (long.timepoint == "R+45") & (long.value < 54)
long.loc[g45, "review_note"] = ("glucose < 54 mg/dL at R+45 in 3 of 4 crew on the same draw date; "
                                "pattern suggests possible delayed sample processing (glycolysis) - verify")
k = (long.analyte == "POTASSIUM") & (long.value > 5.3)
long.loc[k, "review_note"] = "isolated high potassium; possible hemolysis - verify"
rep.append(f"Review flags added: {(long.review_note != '').sum()} values "
           "(R+45 glucose cluster < 54 mg/dL, isolated high potassium) - possible pre-analytical artifacts")

tp_order = {"L-92": 0, "L-44": 1, "L-3": 2, "R+1": 3, "R+45": 4, "R+82": 5, "R+194": 6}
long["tp_order"] = long["timepoint"].map(tp_order)
long = long.sort_values(["subject", "tp_order", "panel", "analyte"]).drop(columns="tp_order")
cols = ["subject", "sex", "timepoint", "phase", "days_from_launch", "days_rel_event", "panel",
        "analyte", "value", "unit", "ref_min", "ref_max", "flag", "review_note"]
long[cols].to_csv("data/processed/inspiration4_blood_long.csv", index=False)
rep.append("Rows re-ordered chronologically (C003 R+1 was stored at the end of the source file)")

wide = long.pivot_table(index=["subject", "sex", "timepoint", "phase", "days_from_launch"],
                        columns="analyte", values="value").reset_index()
wide["_o"] = wide["timepoint"].map(tp_order)
wide = wide.sort_values(["subject", "_o"]).drop(columns="_o")
wide.columns.name = None
wide.to_csv("data/processed/inspiration4_blood_wide.csv", index=False)

# ---- 8. Change right after flight (R+1) vs preflight mean (L-92, L-44, L-3)
pre = long[long.phase == "preflight"].groupby(["subject", "analyte"])["value"].mean()
r1 = long[long.timepoint == "R+1"].set_index(["subject", "analyte"])["value"]
ch = pd.DataFrame({"preflight_mean": pre.round(2), "R+1": r1}).dropna()
ch["pct_change"] = ((ch["R+1"] / ch["preflight_mean"] - 1) * 100).round(1)
summ = ch.groupby("analyte")["pct_change"].agg(["mean", "min", "max", "count"]).round(1)
summ = summ.rename(columns={"mean": "mean_pct_change", "min": "min_pct_change",
                            "max": "max_pct_change", "count": "n_crew"})
summ.sort_values("mean_pct_change", key=abs, ascending=False).to_csv(
    "data/processed/inspiration4_change_R1_vs_preflight.csv")

n_abn = long.flag.isin(["low", "high"]).sum()
rep.append(f"Clean tidy rows: {len(long)} ({long.subject.nunique()} crew x 7 timepoints x "
           f"{long.analyte.nunique()} analytes); out-of-range values: {n_abn}")
with open("docs/CLEANING_REPORT.md", "a") as f:
    f.write("\n## Option D — REAL data: Inspiration4 blood panels (NASA OSDR OSD-575 / OSD-569)\n\n")
    f.write("\n".join(f"- {x}" for x in rep) + "\n")
print("\n".join(rep))
