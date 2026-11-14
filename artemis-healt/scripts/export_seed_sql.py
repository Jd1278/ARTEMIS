"""Build an atomic SQL Editor import from the verified, packaged demo."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]

def literal(value):
    return "'" + str(value).replace("'", "''") + "'"

def build():
    raw = (ROOT / 'data/demo/observations.json').read_bytes()
    manifest = json.loads((ROOT / 'data/demo/manifest.json').read_text(encoding='utf-8'))
    rows = json.loads(raw)
    batch = hashlib.sha256(raw).hexdigest()
    assert batch == manifest['output_sha256'], 'Dataset hash mismatch'
    assert len(rows) == manifest['rows'] == 4320
    assert len({r['id'] for r in rows}) == len(rows)
    assert sum(r['value'] is None for r in rows) == 92
    payload = json.dumps(rows, ensure_ascii=False, separators=(',', ':'))
    assert '$artemis_data$' not in payload
    sql = f'''-- Run the entire file in Supabase SQL Editor after 001_initial.sql.
-- Only synthetic demo data. No deletion or update of existing observations.
BEGIN;
SELECT pg_advisory_xact_lock(82710421);
CREATE TEMP TABLE artemis_seed_input ON COMMIT DROP AS
SELECT * FROM jsonb_to_recordset($artemis_data${payload}$artemis_data$::jsonb)
AS r(id uuid, profile_id text, namespace text, indicator text, value numeric,
source_value numeric, unit text, context text, timestamp timestamptz, mission_day integer,
origin_type text, capture_method text, quality_flags jsonb, source_file text, source_row integer);

DO $seed$
BEGIN
 IF NOT EXISTS(SELECT 1 FROM artemis.import_batches WHERE id={literal(batch)}) THEN
  INSERT INTO artemis.import_batches
   (id,source_file,source_sha256,output_sha256,transform_version,row_count,manifest)
  VALUES ({literal(batch)},{literal(manifest['source'])},{literal(manifest['sha256'])},
   {literal(batch)},{literal(manifest['transform'])},4320,{literal(json.dumps(manifest))}::jsonb);
  INSERT INTO artemis.profiles(id,display_name,namespace)
   SELECT DISTINCT profile_id,profile_id,'demo' FROM artemis_seed_input
   ON CONFLICT(id) DO NOTHING;
  INSERT INTO artemis.observations
   (id,profile_id,namespace,indicator,value,source_value,unit,context,measured_at,mission_day,
    origin_type,capture_method,quality_flags,source_file,source_row,import_batch_id)
   SELECT id,profile_id,namespace,indicator,value,source_value,unit,context,timestamp,mission_day,
    origin_type,capture_method,quality_flags,source_file,source_row,{literal(batch)}
   FROM artemis_seed_input;
 END IF;
 -- Compare every imported field; an incomplete or changed previous load aborts.
 IF EXISTS (
  SELECT 1 FROM artemis_seed_input s LEFT JOIN artemis.observations o ON o.id=s.id
  WHERE o.id IS NULL OR ROW(o.profile_id,o.namespace,o.indicator,o.value,o.source_value,o.unit,
   o.context,o.measured_at,o.mission_day,o.origin_type,o.capture_method,o.quality_flags,o.source_file,o.source_row,o.import_batch_id)
   IS DISTINCT FROM ROW(s.profile_id,s.namespace,s.indicator,s.value,s.source_value,s.unit,
   s.context,s.timestamp,s.mission_day,s.origin_type,s.capture_method,s.quality_flags,s.source_file,s.source_row,{literal(batch)}::text)
 ) THEN RAISE EXCEPTION 'Existing data differs from the expected demo; no changes committed'; END IF;
 IF (SELECT count(*) FROM artemis.observations WHERE import_batch_id={literal(batch)}) <> 4320
 THEN RAISE EXCEPTION 'Unexpected import count'; END IF;
END $seed$;
COMMIT;

SELECT count(*) AS observations,
 count(DISTINCT profile_id) AS profiles,
 count(DISTINCT indicator) AS indicators,
 count(*) FILTER (WHERE value IS NULL) AS null_values
FROM artemis.observations WHERE import_batch_id={literal(batch)};
'''
    return sql

if __name__ == '__main__':
    target = ROOT / 'scripts/sql/load_demo.sql'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(build().encode('utf-8'))
    print(f'Generated {target.name}: {target.stat().st_size} bytes')
