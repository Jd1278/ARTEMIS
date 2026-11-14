"""validate.py — Sanity checks on the processed dataset. Exit code 1 on failure."""
import json, sys
import pandas as pd

d = pd.read_csv("data/processed/crew_daily_log_clean.csv")
thr = pd.read_csv("data/reference/thresholds.csv")
errors = []
def check(cond, msg):
    print(("PASS " if cond else "FAIL ") + msg)
    if not cond: errors.append(msg)

check(len(d) == 6 * 180, "1080 rows (6 crew x 180 days)")
check(not d.duplicated(["crew_id", "mission_day"]).any(), "one record per crew member per day")
check(d["crew_id"].str.fullmatch(r"CM-0[1-6]").all(), "crew_id format CM-0X")
check(d["sleep_duration_h"].dropna().between(0, 16).all(), "sleep hours within 0-16")
check(d["samn_perelli"].dropna().between(1, 7).all(), "Samn-Perelli within 1-7")
check(d["resting_hr_bpm"].dropna().between(30, 200).all(), "resting HR within 30-200")
for c in ["stress_vas", "workload_vas", "mood_vas"]:
    check(d[c].dropna().between(0, 100).all(), f"{c} within 0-100")
st = {"green", "yellow", "red", "unknown"}
for i in thr["indicator"]:
    check(set(d[f"status_{i}"].unique()) <= st, f"status_{i} uses valid labels")
check(set(d["event_type"]) <= {"nominal", "adaptation", "scheduled_stressor", "anomaly"}, "event_type labels valid")
check(((d["event_type"] == "anomaly") == (d["is_anomaly"] == 1)).all(), "is_anomaly consistent with event_type")
sl = d["sleep_duration_h"].dropna()
check(5.9 <= sl.mean() <= 6.6, f"mean in-flight sleep {sl.mean():.2f} h within published ISS range (~6.0-6.5 h)")
check(0.15 <= (sl >= 7).mean() <= 0.35, f"share of nights >= 7 h = {(sl >= 7).mean():.0%} (published ISS: 24%)")
j = json.load(open("data/processed/crew_daily_log_clean.json"))
check(len(j["crew"]) == 6 and all(len(c["days"]) == 180 for c in j["crew"]), "JSON has 6 crew x 180 days")
# ---- Option D (real data)
dl = pd.read_csv("data/processed/inspiration4_blood_long.csv")
check(dl["subject"].nunique() == 4 and dl["timepoint"].nunique() == 7, "D: 4 real crew x 7 timepoints")
w = pd.read_csv("data/processed/inspiration4_blood_wide.csv")
plt_ok = w["PLATELET COUNT"].between(100, 500).all() and w["MPV"].between(5, 15).all()
check(plt_ok, "D: column-shift error fixed (platelets 100-500, MPV 5-15 in every row)")
calc = (w["WHITE BLOOD CELL COUNT"] * w["NEUTROPHILS"] * 10 - w["ABSOLUTE NEUTROPHILS"]).abs()
check((calc < 60).all(), "D: absolute neutrophils = WBC x neutrophil% in every row")
# ---- Integrated dataset
o = pd.read_csv("data/processed/astronaut_health_observations.csv", low_memory=False)
check(set(o.source) == {"simulated", "simulated_from_real", "real_nasa_osdr", "real_nasa_cdaweb", "real_nasa_lsda"}, "INT: every observation labeled with its source")
check(o[o.mission == "SIM-ISS-180"].crew_id.str.startswith("CM-").all()
      and o[o.mission == "Inspiration4"].crew_id.str.startswith("C00").all(),
      "INT: real crew and simulated crew never mixed in the same mission")
check(o[o.source == "real_nasa_lsda"].crew_id.str.startswith("C1G").all() and
      (o[o.source == "real_nasa_lsda"].mission == "UTMB Bed Rest Campaign 1 (analog)").all(),
      "INT: bed rest subjects kept in their own analog mission")
check(o.observation_id.is_unique, "INT: observation_id is unique")
cal = pd.read_csv("data/reference/lab_calibration_from_real.csv")
sl = o[(o.source == "simulated_from_real")].copy()
sl["value"] = sl["value"].astype(float)
prem = sl[sl.timepoint.isin(["L-60", "L-10"])].groupby(["indicator", "sex"])["value"].mean()
ok = all(abs(prem[(r.indicator, r.sex)] - r.real_preflight_mean) <= 1.5 * r.real_preflight_sd for r in cal.itertuples())
check(ok, "INT: simulated preflight labs within 1.5 SD of REAL Inspiration4 preflight means (every analyte, by sex)")
big = cal[cal["real_median_pct_change_R+1"].abs() >= 10].drop_duplicates("indicator")
ok = True
for r in big.itertuples():
    pre_ = sl[(sl.indicator == r.indicator) & sl.timepoint.isin(["L-60", "L-10"])]["value"].mean()
    r1 = sl[(sl.indicator == r.indicator) & (sl.timepoint == "R+1")]["value"].mean()
    ok &= (r1 - pre_) * r[cal.columns.get_loc("real_median_pct_change_R+1") + 1] > 0
check(ok, f"INT: post-flight (R+1) change has the same direction as the real crew for {', '.join(big.indicator)}")
oor_sim = (sl.status != "green").mean(); rl = o[o.source == "real_nasa_osdr"]
oor_real = (~rl.status.isin(["green", "unknown"])).mean()
check(abs(oor_sim - oor_real) <= 0.05, f"INT: share of out-of-range lab values similar (simulated {oor_sim:.1%} vs real {oor_real:.1%})")
w = pd.read_csv("data/processed/crew_daily_integrated_wide.csv")
check(len(w) == 1080 and w.filter(like="lab_").notna().all().all(), "INT: wide table 1080 crew-days, latest lab known every day")
# ---- Real ISS radiation
rad = pd.read_csv("data/processed/iss_radiation_daily_clean.csv")
check(len(rad) == 180 and rad.dose_equivalent_uSv_day.notna().all(), "RAD: 180 mission days, no missing dose after cleaning")
check((rad.minutes_covered.fillna(0) <= 1445).all(), "RAD: no day counts more than 24 h of data (duplicates removed)")
check(rad.cumulative_dose_equivalent_mSv.is_monotonic_increasing, "RAD: cumulative dose only increases")
med = rad.dose_equivalent_uSv_day.median() / 1000
check(0.4 <= med <= 1.2, f"RAD: median {med:.2f} mSv/day, consistent with ~300 mSv/year reported for the ISS")
check((rad.status_radiation_daily != "green").sum() >= 1 and rad.loc[rad.source_date == "2017-03-26", "status_radiation_daily"].iloc[0] == "red",
      "RAD: 2017-03-26 spike kept and flagged red")
check(pd.to_datetime(rad.source_date).dt.strftime("%m-%d").tolist() ==
      pd.to_datetime(w.date[w.crew_id == "CM-01"]).dt.strftime("%m-%d").tolist(),
      "RAD: real ISS dates map to the same month/day of the simulated mission")
# ---- Real bed rest analog (NLSP)
ba = pd.read_csv("data/processed/bedrest_actigraphy_clean.csv")
check(len(ba) == 207 and ba.subject.nunique() == 3, "BR: 207 actigraphy nights, 3 subjects (consolidated file, not the mislabeled query file)")
check(ba.sleep_duration_h.dropna().between(0, 12).all() and ba.sleep_efficiency_pct.dropna().between(0, 100).all(),
      "BR: sleep hours 0-12 and efficiency 0-100% after converting H:MM / H:MM:SS text")
check(ba.sleep_duration_h.isna().sum() == 17, "BR: the 17 'No Data' nights stay missing (not invented)")
bw = pd.read_csv("data/processed/bedrest_winscat_clean.csv")
check(len(bw) == 30 and bw.memory_accuracy_pct.between(0, 100).all(), "BR: 30 WinSCAT sessions with valid accuracies")
bt = pd.read_csv("data/processed/bedrest_tilt_clean.csv")
check("heart_rate" not in " ".join(bt.columns), "BR: tilt heart rate excluded (source HR file is a copy of DBP)")
check(bt[bt.timepoint == "R+0"].tilt_tolerance_min.mean() < bt[bt.phase == "pre_bedrest"].tilt_tolerance_min.mean(),
      "BR: tilt tolerance lower after bed rest than before (orthostatic deconditioning)")
print("\nALL CHECKS PASSED" if not errors else f"\n{len(errors)} CHECK(S) FAILED")
sys.exit(1 if errors else 0)
