"""Explicit migration/seed/verify commands; never run during application startup."""
import argparse
import hashlib
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from artemis_health.platform.database import connection
from psycopg.types.json import Jsonb

def migrate():
    with connection(admin=True) as c:
        c.execute('SELECT pg_advisory_xact_lock(82710421)')
        for path in sorted((ROOT/'migrations').glob('*.sql')):
            sql=path.read_text(encoding='utf-8')
            checksum=hashlib.sha256(path.read_bytes()).hexdigest()
            exists=c.execute("SELECT to_regclass('artemis.schema_migrations') AS name").fetchone()['name']
            prior=c.execute('SELECT checksum FROM artemis.schema_migrations WHERE version=%s',(path.name,)).fetchone() if exists else None
            if prior:
                if prior['checksum']!=checksum: raise ValueError('Applied migration changed: '+path.name)
                continue
            c.execute(sql)
            c.execute('INSERT INTO artemis.schema_migrations(version,checksum) VALUES (%s,%s)',(path.name,checksum))
    print('Migrations committed')

def seed():
    raw=(ROOT/'data/demo/observations.json').read_bytes()
    manifest=json.loads((ROOT/'data/demo/manifest.json').read_text(encoding='utf-8'))
    digest=hashlib.sha256(raw).hexdigest()
    if digest!=manifest['output_sha256']: raise ValueError('Dataset hash mismatch')
    rows=json.loads(raw)
    if len(rows)!=manifest['rows'] or len({r['id'] for r in rows})!=len(rows): raise ValueError('Invalid row count or duplicate ids')
    batch=digest
    with connection(admin=True) as c:
        c.execute('SELECT pg_advisory_xact_lock(82710421)')
        prior=c.execute('SELECT row_count FROM artemis.import_batches WHERE id=%s',(batch,)).fetchone()
        if prior:
            count=c.execute('SELECT count(*) AS n FROM artemis.observations WHERE import_batch_id=%s',(batch,)).fetchone()['n']
            if count!=len(rows): raise ValueError('Existing import is incomplete')
            print('Dataset already imported; no changes')
            return
        c.execute('INSERT INTO artemis.import_batches VALUES (%s,%s,%s,%s,%s,%s,%s,now())',
                  (batch,manifest['source'],manifest['sha256'],digest,manifest['transform'],len(rows),Jsonb(manifest)))
        for profile in sorted({r['profile_id'] for r in rows}):
            c.execute("INSERT INTO artemis.profiles(id,display_name,namespace) VALUES (%s,%s,'demo') ON CONFLICT(id) DO NOTHING",(profile,profile))
        for r in rows:
            c.execute('''INSERT INTO artemis.observations
            (id,profile_id,namespace,indicator,value,source_value,unit,context,measured_at,mission_day,
             origin_type,capture_method,quality_flags,source_file,source_row,import_batch_id)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
            (r['id'],r['profile_id'],r['namespace'],r['indicator'],r['value'],r['source_value'],r['unit'],r['context'],
             r['timestamp'],r['mission_day'],r['origin_type'],r['capture_method'],Jsonb(r['quality_flags']),r['source_file'],r['source_row'],batch))
    print(f'Committed {len(rows)} observations')

def verify():
    manifest=json.loads((ROOT/'data/demo/manifest.json').read_text(encoding='utf-8'))
    with connection(admin=True) as c:
        result=c.execute('''SELECT count(*) AS rows, count(*) FILTER(WHERE value IS NULL) AS null_values,
        count(DISTINCT profile_id) AS profiles FROM artemis.observations WHERE import_batch_id=%s''',
        (manifest['output_sha256'],)).fetchone()
        if result!={'rows':manifest['rows'],'null_values':manifest['null_values'],'profiles':6}: raise ValueError('Stored dataset verification failed')
        print(json.dumps(result))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=['migrate','seed','verify'])
    args=parser.parse_args()
    try: {'migrate':migrate,'seed':seed,'verify':verify}[args.command]()
    except Exception as exc:
        # Connection exceptions can contain host names or credentials. Never print them.
        print(f'Command failed ({type(exc).__name__}); check configuration and database logs.',file=sys.stderr)
        sys.exit(1)
