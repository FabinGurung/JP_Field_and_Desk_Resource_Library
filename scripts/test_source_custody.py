"""Public source-custody and layout regression tests."""
import json
import re
import unittest
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class OperationsCustodyTest(unittest.TestCase):
    def test_public_snapshot_is_gated(self):
        data=json.loads((ROOT/"site/source-custody.json").read_text())
        self.assertEqual(data["schema_version"],"1.1.0")
        self.assertFalse(data["live_worker_sync"])
        self.assertTrue(data["authenticated_private_payroll_reads"])
        self.assertTrue(data["historical_clean_payment_publication"])
        self.assertLessEqual(date.fromisoformat(data["as_of_npt"]),datetime.now(timezone(timedelta(hours=5, minutes=45))).date())
        self.assertEqual(len({r["id"] for r in data["subjects"]}),len(data["subjects"]))
        for row in data["subjects"]:
            self.assertIn(row["group"],("desk","field","labour"))
            self.assertTrue(all(row[k] for k in ("name","authority","custody","integration","limit")))
            if row["group"]=="labour":self.assertNotEqual(row["status"],"PUBLISHED_CATALOGUE")
        self.assertNotIn("drive.google.com/drive/folders/",json.dumps(data))
        self.assertNotIn("docs.google.com/spreadsheets/d/",json.dumps(data))
    def test_navigation_and_publication(self):
        html=(ROOT/"site/operations.html").read_text()
        for side in ("north","west","east","south","centre"):self.assertIn('id="'+side+'"',html)
        self.assertIn('aria-pressed="true"',html)
        self.assertIn("@media(max-width:680px)",(ROOT/"site/operations.css").read_text())
        self.assertIn('source-custody.json',(ROOT/"site/operations.js").read_text())
        from publish_library import SITE_FILES
        for path in ("operations.html","operations.css","operations.js","source-custody.json"):
            self.assertIn(path,SITE_FILES)
if __name__=="__main__":unittest.main()
