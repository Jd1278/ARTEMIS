"""
generate_raw.py — Simulates a 180-day ISS mission daily self-assessment log
(sleep, fatigue, behavioral health, vigilance) for a 6-person crew.

The simulation parameters are anchored to published spaceflight evidence
(see docs/SOURCES.md). The output is intentionally "dirty" (mixed formats,
missing values, duplicates, sensor glitches) to mimic a real crew log, so the
cleaning pipeline (clean.py) can be demonstrated end to end.

Usage:  python scripts/generate_raw.py [output_csv]
"""
import sys
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

SEED = 2026
rng = np.random.default_rng(SEED)

MISSION_DAYS = 180
LAUNCH = datetime(2026, 3, 1)
OUT = sys.argv[1] if len(sys.argv) > 1 else "data/raw/crew_daily_log_raw.csv"

# Fictional crew. Baselines differ per person (individual vulnerability to
# sleep loss is documented in the HRP sleep evidence report).
CREW = [
    # id,     base_sleep, base_rt_ms, base_hr, sensitivity
    ("CM-01", 6.6, 248, 58, 0.8),
    ("CM-02", 6.2, 262, 64, 1.2),
    ("CM-03", 6.5, 255, 61, 1.0),
    ("CM-04", 6.0, 270, 66, 1.3),
    ("CM-05", 6.8, 243, 55, 0.7),
    ("CM-06", 6.3, 258, 62, 1.0),
]

# Mission-wide schedule events (shared by the whole crew)
# slam shifts before vehicle traffic / EVAs; high-workload weeks.
SLAM_SHIFT_DAYS = {23, 24, 61, 62, 98, 99, 141, 142}
HIGH_WORKLOAD = set(range(40, 47)) | set(range(118, 126))
EVA_DAYS = {62, 99, 142}


def personal_events(cid):
    """Per-astronaut injected episodes (ground truth labels)."""
    ev = {}
    # chronic sleep-debt episode: 4-6 consecutive nights < 6 h
    start = int(rng.integers(30, 150))
    for d in range(start, start + int(rng.integers(4, 7))):
        ev[d] = "sleep_debt_episode"
    # isolation-related mood dip (mid/late mission), ~8-12 days
    if cid in ("CM-02", "CM-04", "CM-06"):
        s = int(rng.integers(95, 140))
        for d in range(s, s + int(rng.integers(8, 13))):
            ev.setdefault(d, "mood_decline")
    return ev


rows = []
rec = 0
for cid, base_sleep, base_rt, base_hr, sens in CREW:
    pev = personal_events(cid)
    debt = 0.0  # rolling sleep debt vs. 7 h need
    mood_level = 72 + rng.normal(0, 5)
    for day in range(1, MISSION_DAYS + 1):
        event = "none"
        sleep = rng.normal(base_sleep + 0.15, 0.7)
        workload = rng.normal(40, 10)
        stress = rng.normal(30, 8)
        mood = mood_level + rng.normal(0, 6)

        if day <= 7:  # adaptation to microgravity
            sleep -= 0.4
            event = "adaptation"
        if day in SLAM_SHIFT_DAYS:
            sleep = rng.uniform(4.0, 5.4)
            event = "slam_shift"
        if day in HIGH_WORKLOAD:
            sleep -= 0.5
            workload += 25
            stress += 12
            event = "high_workload" if event == "none" else event
        if day in EVA_DAYS:
            workload += 20
            stress += 10
        pe = pev.get(day)
        if pe == "sleep_debt_episode":
            sleep = rng.uniform(4.3, 5.8)
            event = pe
        elif pe == "mood_decline":
            mood -= 36 * sens
            stress += 26
            sleep -= 0.4
            event = pe

        sleep = float(np.clip(sleep, 3.0, 9.0))
        debt = 0.6 * debt + max(0.0, 7.0 - sleep)  # decaying cumulative debt

        # Subjective fatigue (Samn-Perelli 1-7) rises with debt + workload
        sp = 2.0 + 0.55 * debt * sens + 0.02 * (workload - 40) + rng.normal(0, 0.5)
        sp = int(np.clip(round(sp), 1, 7))

        # PVT-B: response speed degrades with sleep debt
        rt = base_rt * (1 + 0.07 * debt * sens) + rng.normal(0, 8)
        lam = 0.8 + 1.6 * debt * sens
        lapses = int(rng.poisson(lam))

        hr = base_hr + 0.12 * (stress - 30) + 1.2 * debt + rng.normal(0, 2.5)
        quality = int(np.clip(round(1 + (sleep - 3.5) * 0.8 + rng.normal(0, 0.6)), 1, 5))
        med = rng.random() < (0.35 if sleep < 6 else 0.08)

        ts = LAUNCH + timedelta(days=day - 1, hours=6, minutes=int(rng.integers(30, 75)))
        rec += 1
        rows.append(dict(
            record_id=rec, crew_id=cid, timestamp=ts, mission_day=day,
            sleep_duration=round(sleep, 2), sleep_quality=quality,
            samn_perelli=sp, stress_vas=round(float(np.clip(stress, 0, 100)), 1),
            workload_vas=round(float(np.clip(workload, 0, 100)), 1),
            mood_vas=round(float(np.clip(mood, 0, 100)), 1),
            pvt_mean_rt_ms=round(rt, 1), pvt_lapses=lapses,
            resting_hr_bpm=round(hr), sleep_medication=med,
            event_label=event,
        ))

df = pd.DataFrame(rows)

# ---------------------------------------------------------------- make it dirty
n = len(df)
df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%d %H:%M")
alt = rng.random(n) < 0.15  # some entries saved with another device format
df.loc[alt, "timestamp"] = pd.to_datetime(df.loc[alt, "timestamp"]).dt.strftime("%d/%m/%Y %H:%M")

df["crew_id"] = df["crew_id"].astype(object)
low = rng.random(n) < 0.05
df.loc[low, "crew_id"] = df.loc[low, "crew_id"].str.lower()
sp_ = rng.random(n) < 0.04
df.loc[sp_, "crew_id"] = " " + df.loc[sp_, "crew_id"] + " "

df["sleep_duration"] = df["sleep_duration"].astype(object)
mins = rng.random(n) < 0.02  # logged in minutes
df.loc[mins, "sleep_duration"] = (df.loc[mins, "sleep_duration"].astype(float) * 60).round().astype(int).astype(str)
hm = (rng.random(n) < 0.02) & ~mins  # logged as "6h30"
df.loc[hm, "sleep_duration"] = df.loc[hm, "sleep_duration"].astype(float).apply(
    lambda h: f"{int(h)}h{int(round((h - int(h)) * 60)):02d}")

df["sleep_medication"] = df["sleep_medication"].map({True: "yes", False: "no"}).astype(object)
alt_b = rng.random(n) < 0.1
df.loc[alt_b, "sleep_medication"] = df.loc[alt_b, "sleep_medication"].map({"yes": "Y", "no": "N"})

glitch = rng.random(n) < 0.008  # wearable glitches
df.loc[glitch, "resting_hr_bpm"] = rng.choice([0, 255], glitch.sum())
bad_sp = rng.random(n) < 0.004  # out-of-scale entry
df.loc[bad_sp, "samn_perelli"] = 9

for col, p in [("mood_vas", .03), ("stress_vas", .03), ("pvt_mean_rt_ms", .04),
               ("pvt_lapses", .04), ("resting_hr_bpm", .03), ("sleep_quality", .02)]:
    m = rng.random(n) < p
    df[col] = df[col].astype(object)
    df.loc[m, col] = np.nan

dups = df.sample(frac=0.012, random_state=SEED)  # double submissions
df = pd.concat([df, dups]).sort_values(["record_id"]).reset_index(drop=True)
df.to_csv(OUT, index=False)
print(f"raw rows: {len(df)} -> {OUT}")
