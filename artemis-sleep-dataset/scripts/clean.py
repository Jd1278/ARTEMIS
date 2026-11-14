"""
clean.py — Cleans the raw crew log, adds personal baselines, derived features
and green/yellow/red status per indicator (rules read from thresholds.csv).

Usage:  python scripts/clean.py
Inputs:  data/raw/crew_daily_log_raw.csv, data/reference/thresholds.csv
Outputs: data/processed/crew_daily_log_clean.csv
         data/processed/crew_daily_log_clean.json   (nested per crew member)
         data/processed/crew_daily_summary.csv      (crew-level per day)
         docs/CLEANING_REPORT.md
"""
import json
import re
import numpy as np
import pandas as pd

RAW = "data/raw/crew_daily_log_raw.csv"
THR = "data/reference/thresholds.csv"
OUT_CSV = "data/processed/crew_daily_log_clean.csv"
OUT_JSON = "data/processed/crew_daily_log_clean.json"
OUT_SUM = "data/processed/crew_daily_summary.csv"
REPORT = "docs/CLEANING_REPORT.md"

log = []  # cleaning report lines


def note(msg):
    log.append(msg)
    print(msg)


df = pd.read_csv(RAW, dtype=str)
note(f"- Raw rows loaded: **{len(df)}**")

# 1. Exact duplicate submissions ---------------------------------------------
before = len(df)
df = df.drop_duplicates()
note(f"- Exact duplicate rows removed: **{before - len(df)}**")

# 2. crew_id normalization ----------------------------------------------------
bad_ids = (~df["crew_id"].str.fullmatch(r"CM-\d{2}")).sum()
df["crew_id"] = df["crew_id"].str.strip().str.upper()
note(f"- crew_id values normalized (whitespace / lowercase): **{bad_ids}**")

# 3. Timestamps in two formats ------------------------------------------------
iso = pd.to_datetime(df["timestamp"], format="%Y-%m-%d %H:%M", errors="coerce")
dmy = pd.to_datetime(df["timestamp"], format="%d/%m/%Y %H:%M", errors="coerce")
note(f"- Timestamps in DD/MM/YYYY format converted to ISO 8601: **{iso.isna().sum()}**")
df["timestamp"] = iso.fillna(dmy)
assert df["timestamp"].notna().all(), "unparsed timestamps"

# 4. sleep_duration: hours / minutes / '6h30' -> hours (float) ----------------
def parse_sleep(v):
    v = str(v).strip()
    m = re.fullmatch(r"(\d+)h(\d{1,2})", v)
    if m:
        return int(m.group(1)) + int(m.group(2)) / 60, "h_m_text"
    x = float(v)
    if x > 24:  # value logged in minutes
        return x / 60, "minutes"
    return x, "hours"

parsed = df["sleep_duration"].apply(parse_sleep)
df["sleep_duration_h"] = parsed.str[0].round(2)
kinds = parsed.str[1].value_counts()
note(f"- sleep_duration converted to hours: **{kinds.get('minutes', 0)}** from minutes, "
     f"**{kinds.get('h_m_text', 0)}** from 'XhYY' text")
df = df.drop(columns="sleep_duration")

# 5. Types -------------------------------------------------------------------
num_cols = ["record_id", "mission_day", "sleep_quality", "samn_perelli", "stress_vas",
            "workload_vas", "mood_vas", "pvt_mean_rt_ms", "pvt_lapses", "resting_hr_bpm"]
for c in num_cols:
    df[c] = pd.to_numeric(df[c], errors="coerce")
df["sleep_medication"] = df["sleep_medication"].str.strip().str.lower().map(
    {"yes": True, "y": True, "no": False, "n": False})

# 6. Same astronaut + same day submitted twice with different record_id --------
before = len(df)
df = df.sort_values(["crew_id", "mission_day", "record_id"]).drop_duplicates(
    ["crew_id", "mission_day"], keep="first")
note(f"- Same crew member/day duplicates removed: **{before - len(df)}**")

# 7. Out-of-range values -> NaN (then flagged) --------------------------------
ranges = {"samn_perelli": (1, 7), "sleep_quality": (1, 5), "resting_hr_bpm": (30, 200),
          "stress_vas": (0, 100), "workload_vas": (0, 100), "mood_vas": (0, 100),
          "sleep_duration_h": (0, 16), "pvt_mean_rt_ms": (100, 2000)}
df["quality_flags"] = ""
for c, (lo, hi) in ranges.items():
    bad = df[c].notna() & ~df[c].between(lo, hi)
    if bad.any():
        note(f"- `{c}`: **{bad.sum()}** out-of-range values set to missing (valid {lo}-{hi})")
        df.loc[bad, "quality_flags"] += f"{c}_out_of_range;"
        df.loc[bad, c] = np.nan

# 8. Missing values: flag, then short-gap interpolation per astronaut --------
interp_cols = ["stress_vas", "mood_vas", "pvt_mean_rt_ms", "resting_hr_bpm",
               "sleep_quality", "pvt_lapses", "samn_perelli"]
miss_tbl = []
df = df.sort_values(["crew_id", "mission_day"]).reset_index(drop=True)
for c in interp_cols:
    miss = df[c].isna()
    miss_tbl.append((c, int(miss.sum())))
    df.loc[miss, "quality_flags"] += f"{c}_imputed;"
    df[c] = df.groupby("crew_id")[c].transform(
        lambda s: s.interpolate(limit=2, limit_direction="both"))
    if c in ("sleep_quality", "pvt_lapses", "samn_perelli"):
        df[c] = df[c].round()
still = df[interp_cols].isna().sum().sum()
note("- Missing values imputed by linear interpolation within each crew member "
     "(max gap 2 days), flagged in `quality_flags`: " +
     ", ".join(f"`{c}` {n}" for c, n in miss_tbl if n))
note(f"- Values still missing after interpolation (gaps > 2 days): **{still}**")
df["quality_flags"] = df["quality_flags"].str.rstrip(";").replace("", "ok")

# 9. Personal baselines (days 8-21, after microgravity adaptation) -----------
base = df[df["mission_day"].between(8, 21)].groupby("crew_id").agg(
    baseline_rt_ms=("pvt_mean_rt_ms", "median"),
    baseline_hr_bpm=("resting_hr_bpm", "median"))
df = df.merge(base, on="crew_id", how="left")

# 10. Derived features ---------------------------------------------------------
g = df.groupby("crew_id")
df["pvt_speed_change_pct"] = ((df["baseline_rt_ms"] / df["pvt_mean_rt_ms"] - 1) * 100).round(1)
df["resting_hr_delta_bpm"] = (df["resting_hr_bpm"] - df["baseline_hr_bpm"]).round(1)
df["sleep_7d_avg_h"] = g["sleep_duration_h"].transform(lambda s: s.rolling(7, 1).mean()).round(2)
df["sleep_debt_3d_h"] = g["sleep_duration_h"].transform(
    lambda s: (7 - s).clip(lower=0).rolling(3, 1).sum()).round(2)
short = df["sleep_duration_h"] < 6
df["short_sleep_streak_d"] = short.groupby(
    [df["crew_id"], (~short).groupby(df["crew_id"]).cumsum()]).cumsum().astype(int)
df["mission_phase"] = pd.cut(df["mission_day"], [0, 7, 60, 120, 180],
                             labels=["adaptation", "early", "mid", "late"]).astype(str)

# 11. Status per indicator from thresholds.csv -------------------------------
thr = pd.read_csv(THR)
RANK = {"green": 0, "yellow": 1, "red": 2}
status_cols = []
for _, t in thr.iterrows():
    col = t["indicator"]
    v = df[col]
    if t["direction"] == "higher_is_worse":
        st = np.where(v >= t["red_at"], "red", np.where(v >= t["yellow_at"], "yellow", "green"))
    else:
        st = np.where(v < t["red_at"], "red", np.where(v < t["yellow_at"], "yellow", "green"))
    st = np.where(v.isna(), "unknown", st)
    df[f"status_{col}"] = st
    status_cols.append(f"status_{col}")
# absolute HR rule
abs_hr = df["resting_hr_bpm"].notna() & ~df["resting_hr_bpm"].between(40, 100)
df.loc[abs_hr, "status_resting_hr_delta_bpm"] = "red"

ranks = df[status_cols].replace({**RANK, "unknown": -1}).astype(int)
df["overall_status"] = ranks.max(axis=1).map({-1: "unknown", 0: "green", 1: "yellow", 2: "red"})
df["n_red"] = (ranks == 2).sum(axis=1)
df["n_yellow"] = (ranks == 1).sum(axis=1)
df["risk_score"] = (df["n_red"] * 2 + df["n_yellow"]).astype(int)  # 0..18

# 12. Ground-truth labels for the AI -----------------------------------------
ANOM = {"sleep_debt_episode", "mood_decline"}
STRESSOR = {"slam_shift", "high_workload"}
df["event_type"] = np.select(
    [df["event_label"].isin(ANOM), df["event_label"].isin(STRESSOR),
     df["event_label"].eq("adaptation")],
    ["anomaly", "scheduled_stressor", "adaptation"], "nominal")
df["is_anomaly"] = df["event_label"].isin(ANOM).astype(int)

# 13. Column order + types ----------------------------------------------------
df["date"] = df["timestamp"].dt.date.astype(str)
df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:00Z")
for c in ["sleep_quality", "samn_perelli", "pvt_lapses", "resting_hr_bpm"]:
    df[c] = df[c].round().astype("Int64")
order = ["record_id", "crew_id", "date", "timestamp", "mission_day", "mission_phase",
         "sleep_duration_h", "sleep_quality", "sleep_medication", "samn_perelli",
         "pvt_mean_rt_ms", "pvt_lapses", "stress_vas", "workload_vas", "mood_vas",
         "resting_hr_bpm", "baseline_rt_ms", "baseline_hr_bpm", "pvt_speed_change_pct",
         "resting_hr_delta_bpm", "sleep_7d_avg_h", "sleep_debt_3d_h", "short_sleep_streak_d",
         *status_cols, "overall_status", "n_red", "n_yellow", "risk_score",
         "event_label", "event_type", "is_anomaly", "quality_flags"]
df = df[order].sort_values(["crew_id", "mission_day"]).reset_index(drop=True)
df.to_csv(OUT_CSV, index=False)

# JSON nested per crew member (for the web app)
roster = pd.read_csv("data/reference/crew_roster.csv").set_index("crew_id")
out = {"mission": "SIM-ISS-180", "generated_by": "scripts/clean.py",
       "thresholds": thr.to_dict(orient="records"), "crew": []}
for cid, sub in df.groupby("crew_id"):
    recs = json.loads(sub.drop(columns=["crew_id"]).to_json(orient="records"))
    out["crew"].append({"crew_id": cid, "role": roster.loc[cid, "role"],
                        "baseline_rt_ms": float(sub["baseline_rt_ms"].iloc[0]),
                        "baseline_hr_bpm": float(sub["baseline_hr_bpm"].iloc[0]),
                        "days": recs})
with open(OUT_JSON, "w") as f:
    json.dump(out, f, indent=1)

# Crew-level daily summary (for dashboard / teamwork view)
summ = df.groupby(["mission_day", "date"]).agg(
    crew_reporting=("crew_id", "nunique"),
    mean_sleep_h=("sleep_duration_h", "mean"),
    mean_samn_perelli=("samn_perelli", "mean"),
    mean_stress_vas=("stress_vas", "mean"),
    mean_mood_vas=("mood_vas", "mean"),
    crew_red=("overall_status", lambda s: (s == "red").sum()),
    crew_yellow=("overall_status", lambda s: (s == "yellow").sum()),
).round(2).reset_index()
summ.to_csv(OUT_SUM, index=False)

note(f"- Clean rows written: **{len(df)}** ({df['crew_id'].nunique()} crew x "
     f"{df['mission_day'].nunique()} days)")
dist = df["overall_status"].value_counts().to_dict()
note(f"- overall_status distribution: {dist}")
note(f"- is_anomaly = 1 rows: **{df['is_anomaly'].sum()}**")

with open(REPORT, "w") as f:
    f.write("# Cleaning Report\n\nAuto-generated by `scripts/clean.py`.\n\n")
    f.write("\n".join(log) + "\n")
