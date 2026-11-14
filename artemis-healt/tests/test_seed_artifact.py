import hashlib
import json
import unittest
from pathlib import Path

class SeedArtifact(unittest.TestCase):
    def test_seed_is_self_contained_and_verified(self):
        root=Path(__file__).resolve().parents[1]/'data/demo'
        raw=(root/'observations.json').read_bytes()
        manifest=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
        rows=json.loads(raw)
        self.assertEqual(hashlib.sha256(raw).hexdigest(),manifest['output_sha256'])
        self.assertEqual(len(rows),manifest['rows'])
        self.assertEqual(sum(r['value'] is None for r in rows),manifest['null_values'])
        self.assertEqual(len({r['id'] for r in rows}),len(rows))
        self.assertEqual(len({r['profile_id'] for r in rows}),6)
        self.assertTrue(all(r['namespace']=='demo' and r['origin_type']=='synthetic' for r in rows))
