"""Strict source-derived Payment publication tests; synthetic records only."""
import json
import tempfile
import unittest
from pathlib import Path

from publish_field_payments import PAYMENT_HEADERS, build_payments, date_string


def fixture():
    return {
        "payments": [
            PAYMENT_HEADERS,
            ["WKR-SYN-001", "Synthetic Person", 45656, "AD", "Sample Site",
             "Salary", "", 250, "Salary", "", "Synthetic!10", "O10"],
            ["WKR-SYN-001", "Synthetic Person", "2024-12-30", "AD", "Sample Site",
             "Contract", "", -50, "Contract", "", "Synthetic!11", "Q11"],
            ["TOTAL", "", "", "", "", "", "", 200],
        ],
        "manifest": [
            ["Manifest and version history", "Value"],
            ["Clean record count", "2"],
            ["Source SHA-256", "a" * 64],
        ],
    }


class HistoricalPaymentPublicationTest(unittest.TestCase):
    def test_real_source_grain_and_signed_adjustments(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(build_payments(fixture(), root, "2026-11-12T04:00:00+05:45"), 2)
            out = json.loads((root / "field-payments.json").read_text())
            self.assertEqual(out["count"], 2)
            self.assertEqual(out["worker_count"], 1)
            self.assertEqual(out["total_npr"], 200.0)
            self.assertEqual(sorted(x["amount_npr"] for x in out["records"]), [-50.0, 250.0])
            self.assertEqual(out["records"][0]["date"], date_string(45656))
            self.assertEqual(out["source"]["worker_money_goods_transaction_feed"], False)
            self.assertNotIn("Paid by", (root / "field-payments.json").read_text())
            self.assertNotIn("Synthetic Person's phone", (root / "field-payments.json").read_text())

    def test_blank_project_site_is_preserved_not_invented(self):
        tables = fixture()
        tables["payments"][1][4] = ""
        with tempfile.TemporaryDirectory() as tmp:
            build_payments(tables, Path(tmp), "2026-11-12T04:00:00+05:45")
            records = json.loads((Path(tmp) / "field-payments.json").read_text())["records"]
            self.assertEqual(1, sum(1 for x in records if x["site"] == ""))
            self.assertFalse(any(x["site"] == "General" for x in records))

    def test_fails_if_manifest_claims_different_record_count(self):
        tables = fixture()
        tables["manifest"][1][1] = "3"
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "count mismatch"):
                build_payments(tables, Path(tmp), "test")

    def test_duplicate_source_identity_is_not_published_twice(self):
        tables = fixture()
        tables["payments"][2][10] = "Synthetic!10"
        tables["payments"][2][11] = "O10"
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "Duplicate provenance identity"):
                build_payments(tables, Path(tmp), "test")

    def test_source_total_is_authoritative_and_rounded_only_for_display(self):
        tables = fixture()
        tables["payments"][-1][7] = 999
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "do not reconcile"):
                build_payments(tables, Path(tmp), "test")


if __name__ == "__main__":
    unittest.main()
