import unittest, importlib.util
from pathlib import Path
p=Path(__file__).resolve().parents[1]/"scripts/prepare_demo.py"
s=importlib.util.spec_from_file_location("prepare",p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class Contract(unittest.TestCase):
    def test_contract(self):
        rows=m.build()
        self.assertEqual(len(rows),4320)
        self.assertEqual(len({r["id"] for r in rows}),len(rows))
        self.assertEqual(rows,m.build())
        self.assertEqual(len({r["profile_id"] for r in rows}),6)
        for r in rows:
            if any(f.endswith(("_imputed","_out_of_range")) for f in r["quality_flags"]): self.assertIsNone(r["value"])
            self.assertNotIn("risk_score",r)
            self.assertEqual(r["origin_type"],"synthetic")
            if r["value"] is not None and r["indicator"]=="samn_perelli": self.assertTrue(1<=r["value"]<=7)
if __name__=="__main__": unittest.main()
