"""
fetch_tepc.py — Downloads real ISS radiation data (TEPC dose analyzer, NASA CDAWeb
dataset ISS_DOSANL_TEPC) through the HAPI API and summarizes it per day.
Requires internet access to cdaweb.gsfc.nasa.gov.

Output: data/raw/iss_tepc_radiation/tepc_daily_2017-03-01_2017-08-27.csv
Usage : python scripts/fetch_tepc.py
"""
import statistics
import urllib.request
from collections import defaultdict
from datetime import datetime, timedelta

START, DAYS = datetime(2017, 3, 1), 180
URL = ("https://cdaweb.gsfc.nasa.gov/hapi/data?id=ISS_DOSANL_TEPC&time.min={a}&time.max={b}"
       "&parameters=DOSE,DOSE_EQ60,TIME_INTERVAL")
agg = defaultdict(lambda: dict(raw=0, dup=0, n=0, min=0.0, dose=0.0, eq=0.0, rates=[]))
seen = set()
for c in range(0, DAYS, 30):
    a, b = START + timedelta(days=c), START + timedelta(days=min(c + 30, DAYS))
    text = urllib.request.urlopen(URL.format(a=a.strftime("%Y-%m-%dT%H:%M:%SZ"),
                                             b=b.strftime("%Y-%m-%dT%H:%M:%SZ"))).read().decode()
    for line in text.strip().splitlines():
        ts, d, e, m = line.split(",")
        g = agg[ts[:10]]
        g["raw"] += 1
        if ts[:16] in seen:            # duplicate record for the same minute
            g["dup"] += 1
            continue
        seen.add(ts[:16])
        d, e, m = float(d), float(e), float(m)
        if min(d, e, m) < -1e30 or m <= 0:  # HAPI fill value
            continue
        g["n"] += 1; g["min"] += m; g["dose"] += d * m; g["eq"] += e * m; g["rates"].append(d)

with open("data/raw/iss_tepc_radiation/tepc_daily_2017-03-01_2017-08-27.csv", "w") as f:
    f.write("date,raw_records,duplicate_timestamps,records_used,minutes_covered,absorbed_dose_uGy,"
            "dose_equivalent_uSv,median_rate_uGy_min,max_rate_uGy_min\n")
    for day in sorted(agg):
        g = agg[day]
        f.write(f"{day},{g['raw']},{g['dup']},{g['n']},{g['min']:.1f},{g['dose']:.2f},{g['eq']:.2f},"
                f"{statistics.median(g['rates']):.4f},{max(g['rates']):.3f}\n")
print("days with data:", len(agg))
