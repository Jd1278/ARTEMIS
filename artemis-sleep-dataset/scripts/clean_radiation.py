"""
clean_radiation.py — Cleans the real ISS daily radiation summary (NASA CDAWeb
ISS_DOSANL_TEPC) and maps it onto the 180 simulated mission days.

Mapping: mission day d  <->  real ISS date 2017-03-01 + (d - 1)  (same month/day as the
simulated mission, which starts 2026-03-01). The radiation values are real; only the
calendar year is re-assigned.

Rules
  - Days missing from the source            -> imputed (7-day centered median of valid days)
  - Coverage < 50% of the day (720 min)      -> invalid, imputed
  - Median dose rate < 50% of mission median -> instrument anomaly, imputed
  - Coverage 50-100%                         -> scaled to 24 h (dose x 1440 / minutes)
  - Duplicate minute records                 -> already removed in the raw summary (counted)
  - Daily dose equivalent > 1.5x / 3x mission median -> yellow / red, kept and flagged
  - Cumulative dose equivalent vs NASA career limit 600 mSv -> % of limit
Output: data/processed/iss_radiation_daily_clean.csv
"""
from datetime import date, timedelta
import numpy as np
import pandas as pd

RAW = "data/raw/iss_tepc_radiation/tepc_daily_2017-03-01_2017-08-27.csv"
OUT = "data/processed/iss_radiation_daily_clean.csv"
CAREER_LIMIT_MSV = 600.0
r = pd.read_csv(RAW, parse_dates=["date"])
rep = [f"Raw daily summary: {len(r)} days with data out of 180; "
       f"{int(r.duplicate_timestamps.sum())} duplicate minute records removed "
       f"(concentrated on 2017-04-06 to 04-12 and 07-06 to 07-12)"]

days = pd.DataFrame({"mission_day": range(1, 181)})
days["source_date"] = [pd.Timestamp(date(2017, 3, 1) + timedelta(days=d - 1)) for d in days.mission_day]
df = days.merge(r, left_on="source_date", right_on="date", how="left").drop(columns="date")

med_rate = df.median_rate_uGy_min.median()
df["radiation_flag"] = ""
missing = df.records_used.isna()
df.loc[missing, "radiation_flag"] = "missing_day_imputed"
low_cov = ~missing & (df.minutes_covered < 720)
df.loc[low_cov, "radiation_flag"] = "low_coverage_imputed"
anom = ~missing & ~low_cov & (df.median_rate_uGy_min < 0.5 * med_rate)
df.loc[anom, "radiation_flag"] = "instrument_anomaly_imputed"
scaled = ~missing & ~low_cov & ~anom & (df.minutes_covered < 1430)
df.loc[scaled, "radiation_flag"] = "partial_day_scaled_to_24h"
rep += [f"Missing days imputed: {missing.sum()}",
        f"Days with < 50% coverage set invalid and imputed: {low_cov.sum()}",
        f"Days with abnormally low dose rate (instrument anomaly) imputed: {anom.sum()}",
        f"Partial days (50-99% coverage) scaled to 24 h: {scaled.sum()}"]

f = (1440 / df.minutes_covered).clip(upper=1.0).where(df.minutes_covered >= 1430, 1440 / df.minutes_covered)
df["absorbed_dose_uGy_day"] = (df.absorbed_dose_uGy * f).round(1)
df["dose_equivalent_uSv_day"] = (df.dose_equivalent_uSv * f).round(1)
bad = missing | low_cov | anom
for c in ["absorbed_dose_uGy_day", "dose_equivalent_uSv_day"]:
    df.loc[bad, c] = np.nan
    roll = df[c].rolling(7, center=True, min_periods=2).median()
    df[c] = df[c].fillna(roll).fillna(df[c].median()).round(1)

med_eq = df.loc[~bad, "dose_equivalent_uSv_day"].median()
ratio = df.dose_equivalent_uSv_day / med_eq
df["status_radiation_daily"] = np.select([ratio > 3, ratio > 1.5], ["red", "yellow"], "green")
spike = df.status_radiation_daily != "green"
df.loc[spike, "radiation_flag"] = (df.loc[spike, "radiation_flag"] + ";dose_spike_verify").str.strip(";")
rep.append(f"Dose spikes kept and flagged (> 1.5x mission median of {med_eq:.0f} uSv/day): "
           f"{spike.sum()} day(s): " + ", ".join(
               f"{d.date()} ({v:.0f} uSv)" for d, v in df.loc[spike, ["source_date", "dose_equivalent_uSv_day"]].values))

df["cumulative_dose_equivalent_mSv"] = (df.dose_equivalent_uSv_day.cumsum() / 1000).round(2)
df["pct_of_career_limit"] = (df.cumulative_dose_equivalent_mSv / CAREER_LIMIT_MSV * 100).round(1)
df["radiation_flag"] = df.radiation_flag.replace("", "ok")
out = df[["mission_day", "source_date", "absorbed_dose_uGy_day", "dose_equivalent_uSv_day",
          "cumulative_dose_equivalent_mSv", "pct_of_career_limit", "status_radiation_daily",
          "radiation_flag", "minutes_covered", "records_used", "duplicate_timestamps"]]
out["source_date"] = out.source_date.dt.strftime("%Y-%m-%d")
out.to_csv(OUT, index=False)
rep.append(f"Mission total: {out.cumulative_dose_equivalent_mSv.iloc[-1]:.1f} mSv dose equivalent "
           f"= {out.pct_of_career_limit.iloc[-1]:.1f}% of NASA's 600 mSv career limit")
with open("docs/CLEANING_REPORT.md", "a") as fh:
    fh.write("\n## Real ISS radiation (NASA CDAWeb ISS_DOSANL_TEPC, `scripts/clean_radiation.py`)\n\n")
    fh.write("\n".join(f"- {x}" for x in rep) + "\n")
print("\n".join(rep))
