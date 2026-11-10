import json
import tempfile
import unittest
from pathlib import Path

from publish_library import build


class LibraryPublicationTest(unittest.TestCase):
    def test_live_sources_keep_project_links_separate_and_gate_drive_targets(self):
        file_id = "synthetic_public_file_id"
        doc_id = "synthetic_document_file_id"
        tables = {
            "resources": [
                ["Resource ID", "Publish", "Source Drive File ID", "Source URL", "Project ID",
                 "Project Name", "Site Reference", "Display Name", "Category", "Format", "Sort Priority", "Approval Status", "Discipline", "Revision Note"],
                ["RES-001", True, file_id, f"https://drive.google.com/file/d/{file_id}/view", "PRJ-000001",
                 "Example", "P001", "Field plan", "issued_reports", "PDF", 1, "Unverified", "Architecture", "Issue/revision not independently certified"],
                ["RES-002", False, "private", "https://example.org/private", "PRJ-000001",
                 "Example", "P001", "Private", "issued_reports", "PDF", 1, "Unverified", "Architecture", "Issue/revision not independently certified"],
            ],
            "packets": [
                ["Document ID", "Publish", "Project ID", "Company Project Code", "Project Name", "Locality",
                 "Drive File ID", "Role", "Language", "Title", "Version", "Pages", "Approval"],
                ["DOC-001", True, "PRJ-000001", "REB-001", "Example", "Ward 1", doc_id,
                 "A", "en", "Agreement", "v1", 2, "Unsigned"],
            ],
            "readback": [
                ["Record ID", "Drive File ID", "MIME Type", "Modified At", "Access Mode", "Checked On", "Admission Basis"],
                ["RES-001", file_id, "application/pdf", "2026-11-09T00:00:00Z", "PUBLIC_LINK", "2026-11-09", "LEGACY_PUBLIC_ROUTE"],
                ["DOC-001", doc_id, "application/pdf", "2026-11-09T00:00:00Z", "DRIVE_PERMISSION_REQUIRED", "2026-11-09", "LEGACY_PUBLIC_ROUTE"],
            ],
        }
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp)
            self.assertEqual(build(tables, out, "test"), (1, 1))
            catalog = json.loads((out / "catalog.json").read_text())
            self.assertEqual([r["id"] for r in catalog["resources"]], ["RES-001"])
            self.assertNotIn("Private", (out / "catalog.json").read_text())
            packet = json.loads((out / "document-packets.json").read_text())
            self.assertEqual(packet["documents"][0]["access"], "DRIVE_PERMISSION_REQUIRED")
            self.assertFalse((out / "catalog/public-index.v0.1.json").exists())
            self.assertTrue((out / "operations.html").exists())
            self.assertTrue((out / "source-custody.json").exists())
            with self.assertRaisesRegex(ValueError, "Stale Drive owner readback"):
                build(tables, out, "2026-12-20T12:00:00+05:45")
            tables["packets"][1][6] = "changed_file_id_123456"
            with self.assertRaisesRegex(ValueError, "matching Drive readback"):
                build(tables, out, "test")


if __name__ == "__main__":
    unittest.main()
