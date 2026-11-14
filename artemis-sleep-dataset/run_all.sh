#!/usr/bin/env bash
# Rebuilds every dataset option from scratch and validates it.
set -e
cd "$(dirname "$0")"
python3 scripts/generate_raw.py      # Option A raw log
python3 scripts/clean.py             # Option A clean + statuses + labels
python3 scripts/clean_osdr.py        # Option D (REAL NASA OSDR data)
python3 scripts/clean_radiation.py   # REAL ISS radiation (NASA CDAWeb)
python3 scripts/clean_bedrest.py     # REAL bed rest analog (NASA NLSP)
python3 scripts/integrate.py         # ONE integrated dataset (A + labs simulated from D + D)
python3 scripts/validate.py
