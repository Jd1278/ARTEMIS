"""
clean_bedrest.py — Cleans REAL open-access data from NASA's Life Sciences Portal (NLSP):
UTMB Bed Rest Campaign 1 (3 subjects, 60 days of 6-degree head-down-tilt bed rest, a NASA
ground analog of microgravity, 2004).

  - Actigraphy (BRSMAct): nightly sleep duration, sleep latency, sleep efficiency, sleep aids
  - WinSCAT (MR085G): cognitive test battery (memory, math, matching, coding; lapses > 700 ms)
  - Tilt test (MR001G): orthostatic tolerance before vs after bed rest (session summary)

Inputs : data/raw/nlsp_bedrest_campaign1/*
Outputs: data/processed/bedrest_actigraphy_clean.csv
         data/processed/bedrest_winscat_clean.csv
         data/processed/bedrest_tilt_clean.csv
         data/processed/bedrest_summary_by_phase.csv
         appends a section to docs/CLEANING_REPORT.md
"""
import re
import numpy as np
import pandas as pd

RAW = "data/raw/nlsp_bedrest_campaign1/"
BED_REST_DAYS = 60
rep = []


def to_hours(v):
    """'7:44', '7:44:00', '0' -> hours (float). Missing -> NaN."""
    if pd.isna(v) or str(v).strip() in ("", "NA"):
        return np.nan
    s = str(v).strip()
    if s == "0":
        return 0.0
    m = re.fullmatch(r"(\d+):(\d{2})(?::(\d{2}))?", s)
    if not m:
        return np.nan
    return int(m.group(1)) + int(m.group(2)) / 60 + (int(m.group(3) or 0)) / 3600


def day_index(phase, br_day):
    """Day relative to the start of bed rest: PRE -> negative, IN -> 1..60, POST -> 61.. (R+0 = 61)."""
    br_day = int(br_day)
    return {"PRE_TEST": -br_day, "IN_TEST": br_day, "POST_TEST": BED_REST_DAYS + 1 + br_day}[phase]


def label(phase, br_day):
    return {"PRE_TEST": f"BR-{br_day}", "IN_TEST": f"BD{br_day}", "POST_TEST": f"R+{br_day}"}[phase]


PHASE = {"PRE_TEST": "pre_bedrest", "IN_TEST": "bedrest", "POST_TEST": "post_bedrest"}

# ------------------------------------------------------------------ actigraphy
a = pd.read_csv(RAW + "BRSMACT_Campagin_1_Actigraphy.csv", dtype=str)
rep.append("Actigraphy: the source folder has two files. The 'Query_Result' file (191 rows) labels 185 rows as "
           "subject C1G0003, but matching dates and values against the consolidated file shows they belong to all "
           "three subjects (68 to C1G0001, 56 to C1G0002, 59 to C1G0003); it also has one malformed duration "
           "('6.56' instead of 6:56). The consolidated file (`BRSMACT_Campagin_1_Actigraphy`, 207 nights) is used.")
rep.append("Actigraphy: file name typo 'Campagin' kept as published by NASA.")
no_data = a["Notes"].eq("No Data")
a["sleep_duration_h"] = a["Sleep Duration (hours)"].map(to_hours).round(2)
a["sleep_latency_h"] = a["Sleep Latency (hours)"].map(to_hours).round(2)
a["sleep_efficiency_pct"] = pd.to_numeric(a["Sleep Efficiency (%)"], errors="coerce")
fmt = a["Sleep Duration (hours)"].str.count(":").eq(2).sum()
rep.append(f"Actigraphy: durations stored as 'H:MM:SS' text ({fmt} rows) and latencies as 'H:MM' or '0' converted "
           "to decimal hours")
rep.append(f"Actigraphy: {no_data.sum()} nights marked 'No Data' kept as missing (not imputed: real gaps in the "
           "recording, e.g., C1G0003 bed rest days 1-8 and C1G0002 days 26-29)")
notes = a["Notes"].fillna("NA")
med = notes.where(~notes.isin(["NA", "No Data"]), "")
a["sleep_medication"] = med.ne("")
a["medication"] = med
rep.append(f"Actigraphy: free-text notes split into `sleep_medication` (bool) and `medication` "
           f"({a.sleep_medication.sum()} nights with a sleep aid: zolpidem/Ambien or diphenhydramine)")
a["date"] = pd.to_datetime(a["Date"], format="%m/%d/%Y").dt.strftime("%Y-%m-%d")
a["phase"] = a["Test_Phase"].map(PHASE)
a["bedrest_day"] = [day_index(p, d) for p, d in zip(a.Test_Phase, a.BR_Day)]
a["timepoint"] = [label(p, d) for p, d in zip(a.Test_Phase, a.BR_Day)]
a = a.rename(columns={"Subject": "subject"})
act = a[["subject", "date", "phase", "bedrest_day", "timepoint", "sleep_duration_h", "sleep_latency_h",
         "sleep_efficiency_pct", "sleep_medication", "medication"]].sort_values(["subject", "bedrest_day"])
act.to_csv("data/processed/bedrest_actigraphy_clean.csv", index=False)

# a cluster of very poor sleep in all three subjects at the same time
low = act[(act.phase == "bedrest") & act.bedrest_day.between(53, 57)]
rep.append(f"Actigraphy finding: bed rest days 53-57 show poor sleep in all 3 subjects at once (mean "
           f"{low.sleep_duration_h.mean():.1f} h, latency {low.sleep_latency_h.mean():.1f} h, efficiency "
           f"{low.sleep_efficiency_pct.mean():.0f}%) vs {act[act.phase == 'bedrest'].sleep_duration_h.mean():.1f} h "
           "over the whole bed rest; kept as real data (shared cause unknown)")

# ------------------------------------------------------------------ WinSCAT
w = pd.read_csv(RAW + "MR085G_Campaign_1_WinSCAT_All.csv")
rep.append("WinSCAT: the ReadMe header says 'MR010G' and 'Subject C1G0002' although the files belong to experiment "
           "MR085G and contain all three subjects (metadata error in the source; data unaffected)")
w = w.rename(columns={"Subject": "subject", "CPTRT": "memory_rt_ms", "CPTA": "memory_accuracy_pct",
                      "CPTL": "memory_lapses_gt700ms", "MTHRT": "math_rt_ms", "MTHA": "math_accuracy_pct",
                      "MTSRT": "matching_rt_ms", "MTSA": "matching_accuracy_pct", "CDDRT": "coding_rt_ms",
                      "CDDA": "coding_accuracy_pct"})
w["with_instructions"] = w["Test"].eq("Nasa1p")
w["date"] = pd.to_datetime(w["Date"], format="%m/%d/%Y").dt.strftime("%Y-%m-%d")
w["phase"] = w["Test_Phase"].map(PHASE)
w["bedrest_day"] = [day_index(p, d) for p, d in zip(w.Test_Phase, w.BR_Day)]
w["timepoint"] = [label(p, d) for p, d in zip(w.Test_Phase, w.BR_Day)]
w["practice_session"] = w["Run"] <= 3  # first runs show a learning effect
rep.append(f"WinSCAT: {w.with_instructions.sum()} sessions run with on-screen instructions (Nasa1p) flagged; runs 1-3 "
           "flagged as practice sessions (learning effect: accuracy rises and lapses fall regardless of bed rest)")
win = w[["subject", "date", "phase", "bedrest_day", "timepoint", "Run", "with_instructions", "practice_session",
         "memory_rt_ms", "memory_accuracy_pct", "memory_lapses_gt700ms", "math_rt_ms", "math_accuracy_pct",
         "matching_rt_ms", "matching_accuracy_pct", "coding_rt_ms", "coding_accuracy_pct"]].rename(
    columns={"Run": "run"}).sort_values(["subject", "run"])
win.to_csv("data/processed/bedrest_winscat_clean.csv", index=False)

# ------------------------------------------------------------------ Tilt
t = pd.read_csv(RAW + "MR001G_Campaign_1_Tilt_session_summary.csv")
rep.append("Tilt: the source file 'MR001G_Campaign_1_Tilt_HR' is an exact copy of the diastolic pressure file "
           "(173 of 173 rows identical, header says DBP) — heart rate is NOT available; the file was excluded")
bad = (t.subject == "C1G0002") & (t.br_day == 5)
rep.append("Tilt: one session (C1G0002, post bed rest day 5) contains a single tilt minute and no supine baseline; "
           "it duplicates the day-4 session's last minute and is flagged `incomplete_session`")
t["quality_flag"] = np.where(bad, "incomplete_session", "ok")
t["phase"] = t.test_phase.map(PHASE)
t["bedrest_day"] = [day_index(p, d) for p, d in zip(t.test_phase, t.br_day)]
t["timepoint"] = [label(p, d) for p, d in zip(t.test_phase, t.br_day)]
t["date"] = pd.to_datetime(t["date"], format="%m/%d/%Y").dt.strftime("%Y-%m-%d")
tilt = t[["subject", "date", "phase", "bedrest_day", "timepoint", "time_standing_min", "supine_sbp_mean",
          "supine_dbp_mean", "last_tilt_sbp", "last_tilt_dbp", "min_tilt_sbp", "quality_flag"]].rename(
    columns={"time_standing_min": "tilt_tolerance_min"}).sort_values(["subject", "bedrest_day"])
tilt.to_csv("data/processed/bedrest_tilt_clean.csv", index=False)

# ------------------------------------------------------------------ summary by phase
rows = []
for ph in ["pre_bedrest", "bedrest", "post_bedrest"]:
    s = act[act.phase == ph]
    rows.append(dict(source="actigraphy", phase=ph, n=int(s.sleep_duration_h.notna().sum()),
                     sleep_duration_h=round(s.sleep_duration_h.mean(), 2),
                     sleep_latency_h=round(s.sleep_latency_h.mean(), 2),
                     sleep_efficiency_pct=round(s.sleep_efficiency_pct.mean(), 1),
                     nights_lt_7h_pct=round((s.sleep_duration_h < 7).mean() * 100, 1),
                     sleep_aid_nights_pct=round(s.sleep_medication.mean() * 100, 1)))
for ph in ["pre_bedrest", "bedrest", "post_bedrest"]:
    s = win[(win.phase == ph) & ~win.practice_session]
    if len(s):
        rows.append(dict(source="winscat (non-practice runs)", phase=ph, n=len(s),
                         memory_rt_ms=round(s.memory_rt_ms.mean(), 1),
                         memory_accuracy_pct=round(s.memory_accuracy_pct.mean(), 1),
                         memory_lapses_gt700ms=round(s.memory_lapses_gt700ms.mean(), 1)))
for ph, sel in [("pre_bedrest", tilt.phase.eq("pre_bedrest")),
                ("post_bedrest_R+0", tilt.timepoint.eq("R+0"))]:
    s = tilt[sel]
    rows.append(dict(source="tilt", phase=ph, n=len(s), tilt_tolerance_min=round(s.tilt_tolerance_min.mean(), 1)))
summ = pd.DataFrame(rows)
summ.to_csv("data/processed/bedrest_summary_by_phase.csv", index=False)
pre, br = summ.iloc[0], summ.iloc[1]
rep.append(f"Summary: sleep {pre.sleep_duration_h} h before vs {br.sleep_duration_h} h during bed rest; "
           f"nights < 7 h: {pre.nights_lt_7h_pct}% vs {br.nights_lt_7h_pct}%; sleep aid on "
           f"{br.sleep_aid_nights_pct}% of bed rest nights. Tilt tolerance: "
           f"{summ[summ.phase == 'pre_bedrest'].tilt_tolerance_min.dropna().iloc[0]} min before vs "
           f"{summ[summ.phase == 'post_bedrest_R+0'].tilt_tolerance_min.iloc[0]} min on the day bed rest ended")

with open("docs/CLEANING_REPORT.md", "a") as fh:
    fh.write("\n## Real bed rest analog data (NASA NLSP, UTMB Campaign 1, `scripts/clean_bedrest.py`)\n\n")
    fh.write("\n".join(f"- {x}" for x in rep) + "\n")
print("\n".join(rep))
print(summ.to_string())
