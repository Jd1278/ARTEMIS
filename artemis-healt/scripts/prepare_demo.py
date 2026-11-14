from pathlib import Path
import csv, json, hashlib, uuid
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent / "artemis-sleep-dataset/data/processed/crew_daily_log_clean.csv"
FIELDS = {"sleep_duration_h": ("h", "sleep_report"), "samn_perelli": ("points_1_7", "fatigue_report"), "stress_vas": ("points_0_100", "stress_report"), "resting_hr_bpm": ("bpm", "rest")}
def build(source=SOURCE):
    result=[]
    with source.open(encoding="utf-8-sig", newline="") as f:
        for line,row in enumerate(csv.DictReader(f),2):
            flags=row["quality_flags"].split(";")
            for key,(unit,context) in FIELDS.items():
                relevant=[x for x in flags if x.startswith(key+"_")]
                original=float(row[key]) if row[key] else None
                excluded=any(x.endswith(("_imputed","_out_of_range")) for x in relevant)
                result.append(dict(id=str(uuid.uuid5(uuid.NAMESPACE_URL, "artemis:v1:"+row["crew_id"]+":"+row["date"]+":"+key)), profile_id=row["crew_id"], indicator=key, value=None if excluded else original, source_value=original, unit=unit, timestamp=row["timestamp"], mission_day=int(row["mission_day"]), context=context, namespace="demo", origin_type="synthetic", capture_method="import", quality_flags=relevant or ["ok"], source_file=source.name, source_row=line))
    return result
def main():
    rows=build(); out=ROOT/"data/demo";out.mkdir(parents=True,exist_ok=True)
    payload=json.dumps(rows,ensure_ascii=False,indent=2)+"\n"
    (out/"observations.json").write_bytes(payload.encode("utf-8"))
    manifest=dict(source=str(SOURCE.relative_to(ROOT.parent)),sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),transform="prepare_demo_v1",rows=len(rows),null_values=sum(r["value"] is None for r in rows),output_sha256=hashlib.sha256(payload.encode()).hexdigest(),notice="SIMULADO; imputados excluidos; original conservado")
    (out/"manifest.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
    print(json.dumps(manifest,indent=2))
if __name__ == "__main__": main()
