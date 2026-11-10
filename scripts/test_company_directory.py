"""Company-first site projection, source mapping and privacy regression tests."""
import json
import tempfile
import unittest
from pathlib import Path

from publish_library import build, company_key, GROUPS, UNASSIGNED_COMPANY

ROOT = Path(__file__).resolve().parents[1]


def sample():
    resources = [[
        "Resource ID", "Publish", "Source Drive File ID", "Source URL", "Project ID", "Project Name",
        "Site Reference", "Display Name", "Category", "Format", "Sort Priority", "Approval Status",
        "Company", "Document Slot", "Discipline", "Revision Note",
    ]]
    receipts = [[
        "Record ID", "Drive File ID", "MIME Type", "Modified At", "Access Mode", "Checked On", "Admission Basis"
    ]]
    for rid, pid, owner, slot, fmt in [
        ("RES-SYN-A", "PRJ-000001", "Example Construction A", "Architectural drawings", "DWG"),
        ("RES-SYN-B", "PRJ-000002", "Example Construction B", "Source folder", "FOLDER"),
    ]:
        fid = "SyntheticDriveFile" + rid[-1]
        link = (f"https://drive.google.com/drive/folders/{fid}" if fmt == "FOLDER" else
                f"https://drive.google.com/file/d/{fid}/view")
        resources.append([rid, True, fid, link, pid, "Site " + rid[-1], "S-01", "Source " + rid[-1],
                          "source_folders" if fmt == "FOLDER" else "source_models", fmt, 1,
                          "Review pending", owner, slot,
                          "Architecture" if fmt == "DWG" else "Source file folder",
                          "Issue/revision not independently certified"])
        receipts.append([rid, fid, "application/vnd.google-apps.folder" if fmt == "FOLDER" else
                         "application/dwg", "2026-11-09T06:00:00Z", "DRIVE_PERMISSION_REQUIRED",
                         "2026-11-09", "LEGACY_PUBLIC_ROUTE"])
    # A restricted/unreviewed entry must never become publicly searchable.
    resources.append(["RES-PRIVATE", False, "SensitiveOriginal12345",
                      "https://drive.google.com/file/d/SensitiveOriginal12345/view",
                      "PRJ-000001", "Site A", "S-01", "DO-NOT-PUBLISH", "source_models", "PDF", 1,
                      "Private", "Example Construction A", "Technical reports and supporting files",
                      "Structure", "Issue/revision not independently certified"])
    packets = [[
        "Document ID", "Publish", "Project ID", "Company Project Code", "Project Name", "Locality",
        "Drive File ID", "Role", "Language", "Title", "Version", "Pages", "Approval",
    ], ["DOC-SYN-A", True, "PRJ-000029", "REB-002", "Site C", "Site C", "SyntheticPacketFileABC",
         "A", "en", "Agreement", "draft", "2", "Not signed"]]
    receipts.append(["DOC-SYN-A", "SyntheticPacketFileABC", "application/pdf",
                     "2026-11-09T06:00:00Z", "DRIVE_PERMISSION_REQUIRED",
                     "2026-11-09", "LEGACY_PUBLIC_ROUTE"])
    return {"resources": resources, "packets": packets, "readback": receipts}


class CompanyDirectoryTest(unittest.TestCase):
    def test_company_first_grouping_without_inference(self):
        with tempfile.TemporaryDirectory() as folder:
            out = Path(folder)
            self.assertEqual(build(sample(), out, "2026-11-09T13:00:00+05:45"), (2, 1))
            catalog = json.loads((out / "catalog.json").read_text())
            self.assertEqual(catalog["schema_version"], "2.0.0")
            self.assertEqual(len(catalog["companies"]), 3)
            self.assertEqual(len(catalog["projects"]), 3)
            self.assertEqual(sum(c["project_count"] for c in catalog["companies"]), 3)
            self.assertEqual(sum(c["resource_count"] for c in catalog["companies"]), 2)
            self.assertEqual(sum(c["document_count"] for c in catalog["companies"]), 1)
            self.assertIn(UNASSIGNED_COMPANY, [c["name"] for c in catalog["companies"]])
            self.assertEqual(catalog["resources"][0]["group"], "drawings")
            self.assertEqual(catalog["resources"][1]["group"], "source-folders")
            self.assertEqual(catalog["resources"][0]["discipline"], "Architecture")
            self.assertEqual(catalog["resources"][0]["revision_note"], "Issue/revision not independently certified")
            self.assertEqual(catalog["source_manifest"]["tabs_fetched"], [
                "project_resources", "client_document_packets", "resource_source_readback"])
            self.assertFalse(catalog["source_manifest"]["private_payroll_connected"])
            self.assertFalse(catalog["source_manifest"]["original_drive_files_rechecked"])
            self.assertNotIn("DO-NOT-PUBLISH", (out / "catalog.json").read_text())
            packet = json.loads((out / "document-packets.json").read_text())
            self.assertEqual(packet["projects"][0]["company"], UNASSIGNED_COMPANY)
            self.assertEqual(packet["documents"][0]["document_id"], "DOC-SYN-A")

    def test_explicit_company_on_packet_overrides_unassigned_group_without_code_guess(self):
        tables = sample()
        tables["packets"][0].append("Company")
        tables["packets"][1].append("Example Construction C")
        with tempfile.TemporaryDirectory() as folder:
            build(tables, Path(folder), "2026-11-09T13:00:00+05:45")
            catalog = json.loads((Path(folder) / "catalog.json").read_text())
            pid = next(p for p in catalog["projects"] if p["project_id"] == "PRJ-000029")
            self.assertEqual(pid["company"], "Example Construction C")
            self.assertEqual(pid["company_assignment"], "SOURCE_REGISTER")
            self.assertNotIn(UNASSIGNED_COMPANY, [c["name"] for c in catalog["companies"]])
            packet = json.loads((Path(folder) / "document-packets.json").read_text())
            self.assertEqual(packet["projects"][0]["company"], "Example Construction C")

    def test_public_files_and_editor_guide(self):
        from publish_library import SITE_FILES
        for name in ("editing.html", "editing.css", "operations.html", "operations.js",
                     "source-custody.json", "index.html", "app.js", "styles.css"):
            self.assertIn(name, SITE_FILES)
            self.assertTrue((ROOT / "site" / name).exists())
        html = (ROOT / "site/index.html").read_text()
        for cardinal in ("north", "west", "east", "south"):
            self.assertIn('id="' + cardinal + '"', html)
        self.assertIn("Company", html)
        self.assertIn("editing.html", html)
        editing = (ROOT / "site/editing.html").read_text()
        self.assertIn("is_public=TRUE", editing)
        for name in ("index.html", "editing.html", "operations.html", "resources/project-documents.html"):
            page = (ROOT / "site" / name).read_text()
            self.assertNotIn("github.com/FabinGurung/JP_Field_and_Desk_Resource_Library", page)
            self.assertNotIn("fabingurung.github.io/JP_Field_and_Desk_Resource_Library/", page)
        self.assertIn("fabingurung.github.io/jp-field-desk-library/", html)
        self.assertIn('id="facet-discipline"', html)
        self.assertIn('id="facet-revision"', html)
        self.assertIn('id="facet-approval"', html)
        self.assertIn("@media(max-width:700px)", (ROOT / "site/styles.css").read_text())
        self.assertIn('resource_source_readback', (ROOT / "site/editing.html").read_text())
        self.assertIn("Project Resources", (ROOT / "site/editing.html").read_text())
        self.assertTrue(company_key("Company A").startswith("display-"))
        self.assertIn(("project-packets", "Agreements & Materials"), GROUPS)


if __name__ == "__main__":
    unittest.main()
