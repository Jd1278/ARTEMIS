"""
integrate.py — Builds ONE integrated dataset from Option A (simulated daily check-in)
and Option D (real Inspiration4 blood panels, NASA OSDR).

Method ("Option 2"):
  1. Real data are NOT attached to fictional people. Instead, the simulated crew
     (CM-01..CM-06) gets periodic blood panels GENERATED FROM the real data:
       - personal baselines and day-to-day variation come from the real preflight
         values of the Inspiration4 crew, by sex;
       - the post-flight change at R+1 and R+45 copies the median change observed
         in the real crew at the same timepoints.
       - in-flight draws (days 30, 90, 150) get no modelled shift: there are no open
         in-flight blood data to calibrate one (declared assumption).
  2. Everything goes into one long "observations" table with a `source` column:
       simulated | simulated_from_real | real_nasa_osdr
  3. A wide daily table (for the AI model) and a JSON (for the web app) are derived.

Inputs : data/processed/crew_daily_log_clean.csv, data/processed/inspiration4_blood_long.csv,
         data/reference/thresholds.csv, data/reference/crew_roster.csv
Outputs: data/processed/astronaut_health_observations.csv  (THE single dataset, long)
         data/processed/crew_daily_integrated_wide.csv     (AI / analysis, 1 row = crew-day)
         data/processed/crew_integrated.json               (web app)
         data/reference/lab_calibration_from_real.csv      (how each lab was calibrated)
"""
import json
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

rng = np.random.default_rng(575569)
LAUNCH = datetime(2026, 3, 1)          # mission day 1
MISSION_DAYS = 180

A = pd.read_csv("data/processed/crew_daily_log_clean.csv")
D = pd.read_csv("data/processed/inspiration4_blood_long.csv")
roster = pd.read_csv("data/reference/crew_roster.csv")
RAD = pd.read_csv("data/processed/iss_radiation_daily_clean.csv")  # real ISS radiation, by mission day
BR_ACT = pd.read_csv("data/processed/bedrest_actigraphy_clean.csv")  # real bed rest analog (NLSP)
BR_WIN = pd.read_csv("data/processed/bedrest_winscat_clean.csv")
BR_TILT = pd.read_csv("data/processed/bedrest_tilt_clean.csv")
SEX = dict(zip(roster.crew_id, roster.sex))

# Lab analytes carried into the integrated dataset (real name -> indicator name)
LABS = {
    "GLUCOSE": "glucose_mg_dl",
    "WHITE BLOOD CELL COUNT": "wbc_10e3_ul",
    "ABSOLUTE LYMPHOCYTES": "lymphocytes_abs_cells_ul",
    "ABSOLUTE NEUTROPHILS": "neutrophils_abs_cells_ul",
    "HEMOGLOBIN": "hemoglobin_g_dl",
    "HEMATOCRIT": "hematocrit_pct",
    "PLATELET COUNT": "platelets_10e3_ul",
    "SODIUM": "sodium_mmol_l",
    "POTASSIUM": "potassium_mmol_l",
    "CALCIUM": "calcium_mg_dl",
    "CREATININE": "creatinine_mg_dl",
    "UREA NITROGEN (BUN)": "bun_mg_dl",
    "ALBUMIN": "albumin_g_dl",
    "ALT": "alt_u_l",
}
DECIMALS = {"glucose_mg_dl": 0, "lymphocytes_abs_cells_ul": 0, "neutrophils_abs_cells_ul": 0,
            "platelets_10e3_ul": 0, "sodium_mmol_l": 0, "bun_mg_dl": 0, "alt_u_l": 0,
            "creatinine_mg_dl": 2}

# Lab schedule for the simulated crew (days_from_launch; mission day 1 = launch day)
SCHEDULE = [("L-60", -60, "preflight"), ("L-10", -10, "preflight"),
            ("FD30", 30, "inflight"), ("FD90", 90, "inflight"), ("FD150", 150, "inflight"),
            ("R+1", MISSION_DAYS + 1, "postflight"), ("R+45", MISSION_DAYS + 45, "postflight")]

# ---------------------------------------------------------------- 1. calibration
real = D[D.analyte.isin(LABS) & D.value.notna() & D.review_note.isna()].copy()
pre = real[real.phase == "preflight"]
cal_rows = []
for analyte, ind in LABS.items():
    for sex in ("M", "F"):
        v = pre[(pre.analyte == analyte) & (pre.sex == sex)]["value"]
        mu, sd = v.mean(), v.std(ddof=1)
        sd = max(sd, 0.02 * mu)  # floor: 2% of mean
        rr = D[(D.analyte == analyte) & (D.sex == sex)][["ref_min", "ref_max", "unit"]].iloc[0]
        cal_rows.append(dict(analyte=analyte, indicator=ind, sex=sex, real_preflight_mean=round(mu, 3),
                             real_preflight_sd=round(sd, 3), n_real_values=len(v),
                             ref_min=rr.ref_min, ref_max=rr.ref_max, unit=rr.unit))
cal = pd.DataFrame(cal_rows)

# post-flight shifts: median per-subject % change vs own preflight mean (real data)
subj_pre = pre.groupby(["subject", "analyte"])["value"].mean()
for tp in ("R+1", "R+45"):
    post = real[real.timepoint == tp].set_index(["subject", "analyte"])["value"]
    pct = ((post / subj_pre.reindex(post.index)) - 1).dropna() * 100
    med = pct.groupby(level="analyte").median()
    n = pct.groupby(level="analyte").size()
    shift = med.where(n >= 2, 0.0)  # need >= 2 real crew with a valid value, else no shift
    cal[f"real_median_pct_change_{tp}"] = cal.analyte.map(shift).fillna(0).round(1)
    cal[f"n_real_crew_{tp}"] = cal.analyte.map(n).fillna(0).astype(int)
cal.to_csv("data/reference/lab_calibration_from_real.csv", index=False)

# ---------------------------------------------------------------- 2. simulated labs
def lab_status(v, lo, hi):
    if pd.isna(v):
        return "unknown", ""
    width = (hi - lo) if pd.notna(hi) else abs(lo)
    if v < lo:
        return ("yellow" if lo - v <= 0.10 * width else "red"), "low"
    if pd.notna(hi) and v > hi:
        return ("yellow" if v - hi <= 0.10 * width else "red"), "high"
    return "green", "normal"

labs = []
for cid in roster.crew_id:
    sex = SEX[cid]
    for _, c in cal[cal.sex == sex].iterrows():
        base = rng.normal(c.real_preflight_mean, 0.6 * c.real_preflight_sd)
        for tp, day, phase in SCHEDULE:
            shift = {"R+1": c["real_median_pct_change_R+1"], "R+45": c["real_median_pct_change_R+45"]}.get(tp, 0.0)
            val = base * (1 + shift / 100) + rng.normal(0, 0.6 * c.real_preflight_sd)
            val = max(val, 0)
            val = round(val, DECIMALS.get(c.indicator, 1))
            st, det = lab_status(val, c.ref_min, c.ref_max)
            labs.append(dict(crew_id=cid, sex=sex, timepoint=tp, phase=phase, days_from_launch=day,
                             indicator=c.indicator, value=val, unit=c.unit, ref_low=c.ref_min,
                             ref_high=c.ref_max, status=st, status_detail=det))
labs = pd.DataFrame(labs)

def date_of(day):
    return (LAUNCH + timedelta(days=int(day) - 1 if day >= 1 else int(day))).strftime("%Y-%m-%d")

# ---------------------------------------------------------------- 3. long table
DAILY = [  # indicator, status column, unit
    ("sleep_duration_h", "status_sleep_duration_h", "h"),
    ("short_sleep_streak_d", "status_short_sleep_streak_d", "nights"),
    ("sleep_quality", None, "1-5"),
    ("sleep_medication", None, "bool"),
    ("samn_perelli", "status_samn_perelli", "1-7"),
    ("pvt_mean_rt_ms", None, "ms"),
    ("pvt_lapses", "status_pvt_lapses", "count"),
    ("pvt_speed_change_pct", "status_pvt_speed_change_pct", "% vs baseline"),
    ("stress_vas", "status_stress_vas", "0-100"),
    ("workload_vas", "status_workload_vas", "0-100"),
    ("mood_vas", "status_mood_vas", "0-100"),
    ("resting_hr_bpm", "status_resting_hr_delta_bpm", "bpm"),
]
rows = []
for ind, scol, unit in DAILY:
    t = pd.DataFrame({
        "crew_id": A.crew_id, "sex": A.crew_id.map(SEX), "source": "simulated", "mission": "SIM-ISS-180",
        "data_type": "daily_checkin", "phase": "inflight", "days_from_launch": A.mission_day,
        "timepoint": "FD" + A.mission_day.astype(str), "date": A.date, "indicator": ind,
        "value": A[ind].astype(object), "unit": unit, "ref_low": np.nan, "ref_high": np.nan,
        "status": A[scol] if scol else "info", "status_detail": "",
        "event_label": A.event_label, "is_anomaly": A.is_anomaly, "quality_flags": A.quality_flags})
    rows.append(t)
# real ISS radiation: same environment for the whole crew -> one row per crew member and day
for ind, col, unit, scol in [("radiation_dose_equivalent_uSv_day", "dose_equivalent_uSv_day", "uSv/day", "status_radiation_daily"),
                             ("radiation_absorbed_dose_uGy_day", "absorbed_dose_uGy_day", "uGy/day", None),
                             ("radiation_cumulative_mSv", "cumulative_dose_equivalent_mSv", "mSv", None),
                             ("radiation_pct_career_limit", "pct_of_career_limit", "% of 600 mSv", None)]:
    t = A[["crew_id", "mission_day", "date", "event_label", "is_anomaly"]].merge(RAD, on="mission_day")
    rows.append(pd.DataFrame({
        "crew_id": t.crew_id, "sex": t.crew_id.map(SEX), "source": "real_nasa_cdaweb", "mission": "SIM-ISS-180",
        "data_type": "environment", "phase": "inflight", "days_from_launch": t.mission_day,
        "timepoint": "FD" + t.mission_day.astype(str), "date": t.date, "indicator": ind,
        "value": t[col], "unit": unit, "ref_low": np.nan, "ref_high": np.nan,
        "status": t[scol] if scol else "info", "status_detail": "",
        "event_label": t.event_label, "is_anomaly": t.is_anomaly,
        "quality_flags": t.radiation_flag + "; real ISS date " + t.source_date}))
sim_labs = labs.assign(source="simulated_from_real", mission="SIM-ISS-180", data_type="lab_panel",
                       date=labs.days_from_launch.map(date_of), event_label="", is_anomaly=0,
                       quality_flags="ok")
# in-flight lab draws inherit that day's event label / anomaly from the daily check-in
ev = A.set_index(["crew_id", "mission_day"])[["event_label", "is_anomaly"]]
inf = sim_labs.phase == "inflight"
keys = list(zip(sim_labs.loc[inf, "crew_id"], sim_labs.loc[inf, "days_from_launch"]))
sim_labs.loc[inf, "event_label"] = [ev.loc[k, "event_label"] for k in keys]
sim_labs.loc[inf, "is_anomaly"] = [ev.loc[k, "is_anomaly"] for k in keys]
rows.append(sim_labs)

realr = D.copy()
st = [lab_status(v, lo, hi) for v, lo, hi in zip(realr.value, realr.ref_min, realr.ref_max)]
rows.append(pd.DataFrame({
    "crew_id": realr.subject, "sex": realr.sex, "source": "real_nasa_osdr", "mission": "Inspiration4",
    "data_type": "lab_panel", "phase": realr.phase, "days_from_launch": realr.days_from_launch,
    "timepoint": realr.timepoint, "date": "", "indicator": realr.analyte.map(LABS).fillna(
        realr.analyte.str.lower().str.replace(r"[^a-z0-9]+", "_", regex=True).str.strip("_")),
    "value": realr.value, "unit": realr.unit, "ref_low": realr.ref_min, "ref_high": realr.ref_max,
    "status": [s[0] for s in st], "status_detail": [s[1] for s in st], "event_label": "",
    "is_anomaly": 0, "quality_flags": realr.review_note.fillna("ok")}))

# real bed rest analog data (NASA NLSP, UTMB Campaign 1): different people and mission, reference only
thr = pd.read_csv("data/reference/thresholds.csv").set_index("indicator")
def daily_status(v, ind):
    if ind not in thr.index or pd.isna(v):
        return "info" if ind not in thr.index else "unknown"
    t = thr.loc[ind]
    if t.direction == "lower_is_worse":
        return "red" if v < t.red_at else "yellow" if v < t.yellow_at else "green"
    return "red" if v >= t.red_at else "yellow" if v >= t.yellow_at else "green"
BR_SPECS = [(BR_ACT, "sleep_actigraphy", [("sleep_duration_h", "h"), ("sleep_latency_h", "h"),
                                          ("sleep_efficiency_pct", "%"), ("sleep_medication", "bool")]),
            (BR_WIN, "cognition_test", [("memory_rt_ms", "ms"), ("memory_accuracy_pct", "%"),
                                        ("memory_lapses_gt700ms", "count"), ("math_rt_ms", "ms"),
                                        ("math_accuracy_pct", "%"), ("matching_rt_ms", "ms"),
                                        ("matching_accuracy_pct", "%"), ("coding_rt_ms", "ms"),
                                        ("coding_accuracy_pct", "%")]),
            (BR_TILT, "tilt_test", [("tilt_tolerance_min", "min"), ("supine_sbp_mean", "mmHg"),
                                    ("supine_dbp_mean", "mmHg"), ("last_tilt_sbp", "mmHg"),
                                    ("last_tilt_dbp", "mmHg")])]
for tab, dtype, inds in BR_SPECS:
    for ind, unit in inds:
        flags = (tab["quality_flag"] if "quality_flag" in tab else
                 np.where(tab.get("practice_session", pd.Series(False, index=tab.index)), "practice_session", "ok"))
        rows.append(pd.DataFrame({
            "crew_id": tab.subject, "sex": "", "source": "real_nasa_lsda", "mission": "UTMB Bed Rest Campaign 1 (analog)",
            "data_type": dtype, "phase": tab.phase, "days_from_launch": tab.bedrest_day, "timepoint": tab.timepoint,
            "date": tab.date, "indicator": ind, "value": tab[ind].astype(object), "unit": unit,
            "ref_low": np.nan, "ref_high": np.nan,
            "status": [daily_status(v, ind) for v in tab[ind]] if dtype == "sleep_actigraphy" else "info",
            "status_detail": "", "event_label": "", "is_anomaly": 0,
            "quality_flags": (tab.medication.fillna("").replace("", "ok") if dtype == "sleep_actigraphy" else flags)}))
obs = pd.concat(rows, ignore_index=True)
order = {"simulated": 0, "simulated_from_real": 0, "real_nasa_cdaweb": 0, "real_nasa_osdr": 1, "real_nasa_lsda": 2}
obs["_o"] = obs.source.map(order)
obs = obs.sort_values(["_o", "crew_id", "days_from_launch", "data_type", "indicator"]).drop(columns="_o")
obs.insert(0, "observation_id", range(1, len(obs) + 1))
obs.to_csv("data/processed/astronaut_health_observations.csv", index=False)

# ---------------------------------------------------------------- 4. wide daily table (AI)
W = A.merge(RAD.rename(columns={"source_date": "radiation_source_date"})[[
    "mission_day", "radiation_source_date", "dose_equivalent_uSv_day", "absorbed_dose_uGy_day",
    "cumulative_dose_equivalent_mSv", "pct_of_career_limit", "status_radiation_daily", "radiation_flag"]],
    on="mission_day", how="left")
inflight_labs = labs[labs.phase.isin(["preflight", "inflight"])]
piv = inflight_labs.pivot_table(index=["crew_id", "days_from_launch"], columns="indicator",
                                values="value").reset_index()
for ind in LABS.values():
    last = []
    for cid, sub in W.groupby("crew_id", sort=False):
        p = piv[piv.crew_id == cid].sort_values("days_from_launch")
        draws = list(zip(p.days_from_launch, p[ind]))
        for d in sub.mission_day:
            known = [v for dd, v in draws if dd <= d]
            last.append(known[-1] if known else np.nan)
    W[f"lab_{ind}_last"] = last
draw_days = sorted(d for _, d, ph in SCHEDULE if ph in ("preflight", "inflight"))
W["days_since_last_lab"] = W.mission_day.apply(lambda d: d - max(x for x in draw_days if x <= d))
W["lab_drawn_today"] = W.mission_day.isin([d for d in draw_days if d >= 1]).astype(int)
W.to_csv("data/processed/crew_daily_integrated_wide.csv", index=False)

# ---------------------------------------------------------------- 5. JSON (web)
out = {"mission": "SIM-ISS-180", "launch_date": LAUNCH.strftime("%Y-%m-%d"),
       "notice": "Daily check-in is simulated; lab panels are simulated from real NASA OSDR "
                 "Inspiration4 data (see reference_real_crew); radiation fields are REAL ISS measurements "
                 "(NASA CDAWeb ISS_DOSANL_TEPC, 2017-03-01..2017-08-27) mapped to mission days.",
       "radiation_career_limit_mSv": 600,
       "thresholds_daily": pd.read_csv("data/reference/thresholds.csv").to_dict(orient="records"),
       "crew": [], "reference_real_crew": []}
for cid, sub in A.groupby("crew_id"):
    r = roster.set_index("crew_id").loc[cid]
    out["crew"].append({
        "crew_id": cid, "role": r.role, "sex": r.sex,
        "daily": json.loads(sub.drop(columns=["crew_id"]).merge(
            RAD.rename(columns={"source_date": "radiation_source_date"}), on="mission_day", how="left").to_json(orient="records")),
        "labs": json.loads(labs[labs.crew_id == cid].drop(columns=["crew_id", "sex"]).to_json(orient="records"))})
for sid, sub in D[D.analyte.isin(LABS)].groupby("subject"):
    out["reference_real_crew"].append({
        "crew_id": sid, "sex": sub.sex.iloc[0], "mission": "Inspiration4 (real, NASA OSDR OSD-575/OSD-569)",
        "labs": json.loads(sub[["timepoint", "phase", "days_from_launch", "analyte", "value", "unit",
                                "ref_min", "ref_max", "flag", "review_note"]].to_json(orient="records"))})
out["reference_bedrest_analog"] = {
    "source": "NASA Life Sciences Portal (NLSP), UTMB Bed Rest Campaign 1, open access (real data, 3 subjects, 60 days head-down tilt)",
    "actigraphy": json.loads(BR_ACT.to_json(orient="records")),
    "winscat": json.loads(BR_WIN.to_json(orient="records")),
    "tilt": json.loads(BR_TILT.to_json(orient="records")),
    "summary_by_phase": json.loads(pd.read_csv("data/processed/bedrest_summary_by_phase.csv").to_json(orient="records"))}
with open("data/processed/crew_integrated.json", "w") as f:
    json.dump(out, f, indent=1)

summary = obs.groupby(["source", "data_type"]).size()
with open("docs/CLEANING_REPORT.md", "a") as f:
    f.write("\n## Integration (`scripts/integrate.py`)\n\n")
    f.write(f"- Single long dataset `astronaut_health_observations.csv`: **{len(obs)}** observations\n")
    for (s, t), n in summary.items():
        f.write(f"  - {s} / {t}: {n}\n")
    f.write(f"- Simulated crew lab panels: {len(labs)} values ({labs.crew_id.nunique()} crew x "
            f"{len(SCHEDULE)} draws x {len(LABS)} analytes), calibrated from {len(pre)} real preflight values "
            "(review-flagged values excluded)\n")
print(summary)
print(cal[["analyte", "sex", "real_preflight_mean", "real_median_pct_change_R+1", "real_median_pct_change_R+45"]].to_string())
