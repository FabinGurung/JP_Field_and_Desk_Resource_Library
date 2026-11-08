#!/usr/bin/env python3
"""Fail-closed review gates for the A9 Resource Library preview (no network)."""
import json
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "site"


class TagAudit(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []
        self.meta = []
        self.inputs = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a: self.ids.add(a["id"])
        if tag == "a": self.links.append(a)
        if tag == "meta": self.meta.append(a)
        if tag == "input": self.inputs.append(a)


class SafePreviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = json.loads((SITE / "catalog/public-index.v0.1.json").read_text())
        cls.html = (SITE / "index.html").read_text()
        cls.js = (SITE / "app.js").read_text()
        cls.css = (SITE / "styles.css").read_text()
        cls.tags = TagAudit()
        cls.tags.feed(cls.html)

    def test_source_of_truth_is_not_forked(self):
        c = self.catalog
        self.assertEqual(c["schema_version"], "0.1.0")
        self.assertEqual(c["authority"], "DERIVED_PUBLIC_PRESENTATION_ONLY__NEVER_SOURCE_OF_DOCUMENT_TRUTH")
        self.assertEqual(c["original_files_authority"], "GOOGLE_DRIVE_RESTRICTED_ORIGINALS")
        self.assertIn("A7", c["relationship_authority"])
        self.assertEqual(c["source_lineage"]["pinned_source_main"], "4eb68c004fbe8d19b83bf3b17327c853debef58a")

    def test_not_published_and_zero_admitted_client_records(self):
        c = self.catalog
        self.assertEqual(c["status"], "PREVIEW_NOT_PUBLISHED__PUBLIC_ADMISSION_GATE_UNRESOLVED")
        self.assertEqual(c["projects"], [])
        self.assertEqual(c["resources"], [])
        self.assertFalse(c["deployment"]["github_pages_enabled"])
        self.assertFalse(c["deployment"]["publish_requested"])
        self.assertTrue(c["private_and_unreviewed_excluded"])
        self.assertTrue(all(s["admitted_resources"] == 0 for s in c["requested_sections"]))

    def test_basanti_privacy_hold_cannot_be_omitted(self):
        holds = self.catalog["privacy_holds"]
        self.assertEqual(len(holds), 1)
        self.assertEqual(holds[0]["canonical_project_id"], "PRJ-000029")
        self.assertFalse(holds[0]["copy_private_contracts_drawings_drive_links"])
        self.assertIn("IS_PUBLIC_FALSE", holds[0]["status"])
        self.assertTrue(holds[0]["retired_alias_is_not_new_project"])

    def test_no_private_client_details_in_public_page(self):
        for text in [self.html, self.js, self.css]:
            self.assertNotIn("drive.google.com/file/", text)
            self.assertNotIn("docs.google.com/spreadsheets/", text)
            self.assertNotIn("PRJ-000029", text)
            self.assertNotIn("REB-002", text)
        self.assertNotIn("drive_file_id", self.catalog)
        self.assertNotIn("file_id", self.catalog)

    def test_accessible_navigation_and_preview_noscript(self):
        for name in ["main", "browse", "field", "desk", "projects", "governance", "catalog-search", "catalog-results"]:
            self.assertIn(name, self.tags.ids)
        self.assertTrue(any(a.get("href") == "#main" for a in self.tags.links))
        self.assertTrue(any(a.get("name") == "robots" and "noindex" in a.get("content", "") for a in self.tags.meta))
        self.assertIn("<noscript>", self.html)
        self.assertTrue(any(a.get("type") == "search" for a in self.tags.inputs))

    def test_client_side_filter_requires_all_explicit_gates(self):
        for literal in [
            'item.public_admission !== "APPROVED_PUBLIC"',
            "item.is_public !== true",
            "item.current_source_permission_verified !== true",
            "item.review_id",
            'catalog.status === "PUBLIC_APPROVED_PUBLISHED"',
            "catalog.deployment?.github_pages_enabled === true",
            "blockedProjectIds.has(item.project_id)",
            "noopener noreferrer",
            "textContent"
        ]:
            self.assertIn(literal, self.js)
        self.assertNotIn("innerHTML", self.js)
        self.assertNotIn("eval(", self.js)

    def test_mobile_responsive_and_keyboard_styles(self):
        self.assertIn("@media(max-width:620px)", self.css)
        self.assertIn("focus-visible", self.css)
        self.assertIn("prefers-reduced-motion", self.css)

    def test_exact_source_policy_references(self):
        refs = self.catalog["source_lineage"]
        for key in ["original_source_main_resource_page", "original_source_main_project_documents_page",
                    "existing_source_catalog", "reviewed_dispositions",
                    "public_files_allowlist", "display_and_admission_policy",
                    "original_workflow_contract"]:
            record = refs[key]
            self.assertTrue(record["path"])
            self.assertRegex(record["git_blob_sha"], r"^[a-f0-9]{40}$")

if __name__ == "__main__":
    unittest.main()
