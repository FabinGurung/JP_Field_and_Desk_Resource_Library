"""Google Sheets staff directory: complete, source-accurate and easy to use."""
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "site/memory-wall/index.html"
GROUPS = {
    "used-here": 2,
    "site": 6,
    "people": 7,
    "projects": 9,
    "materials": 2,
    "office": 3,
    "schedule": 2,
    "previous": 4,
}
SOURCE_DIRECTORY_ID = "1e019Jac4lDveZ2glXMph4RLHivqPFEachbcNi-R1DZk"
SOURCE_PAYMENT_ID = "1ShS8wI6OAZA6Is-DLJK3sVkJzl3i5mn5zK-on38fE9I"


class Cards(HTMLParser):
    def __init__(self):
        super().__init__()
        self.group = None
        self.group_counts = {group: 0 for group in GROUPS}
        self.urls = []
        self.bad_card_links = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "section" and a.get("id") in GROUPS:
            self.group = a["id"]
        if tag == "article" and "sheet-card" in a.get("class", "").split():
            if self.group is not None:
                self.group_counts[self.group] += 1
        if tag == "a" and a.get("class") == "sheet-open":
            if self.group is None:
                self.bad_card_links += 1
            self.urls.append(a.get("href", ""))

    def handle_endtag(self, tag):
        if tag == "section":
            self.group = None


class GoogleSheetsStaffDirectoryTests(unittest.TestCase):
    def test_all_original_links_present_once_and_grouped(self):
        html = PAGE.read_text(encoding="utf-8")
        cards = Cards()
        cards.feed(html)
        self.assertEqual(cards.group_counts, GROUPS)
        self.assertEqual(cards.bad_card_links, 0)
        self.assertEqual(len(cards.urls), 35)
        self.assertEqual(len(set(cards.urls)), 35)
        for url in cards.urls:
            self.assertRegex(url, r"^https://docs\.google\.com/spreadsheets/d/[A-Za-z0-9_-]+/edit$")
        self.assertEqual(cards.urls.count(
            f"https://docs.google.com/spreadsheets/d/{SOURCE_DIRECTORY_ID}/edit"), 1)
        self.assertEqual(cards.urls.count(
            f"https://docs.google.com/spreadsheets/d/{SOURCE_PAYMENT_ID}/edit"), 1)

    def test_published_sources_match_actual_publisher(self):
        content = (ROOT / "scripts/publish_library.py").read_text()
        money = (ROOT / "scripts/publish_field_payments.py").read_text()
        self.assertIn(SOURCE_DIRECTORY_ID, content)
        self.assertIn(SOURCE_PAYMENT_ID, money)
        self.assertIn("project_resources", content)
        self.assertIn("client_document_packets", content)
        self.assertIn("resource_source_readback", content)
        self.assertIn("Payment", money)

    def test_employee_page_avoids_internal_language(self):
        html = PAGE.read_text()
        self.assertRegex(html, r"only.*two Sheets|two Sheets")
        self.assertIn("use the working tab", html)
        self.assertIn("not because this website reads them", html)
        for term in ("machine-readable", "artificial intelligence", "database", "audit",
                     "version history", "snapshot"):
            self.assertNotIn(term.casefold(), html.casefold())
        self.assertNotIn("1MsHpWUj5NU7eEWhAgyJTusn19c1VeppY", html)

    def test_navigation_and_publication_files(self):
        from publish_library import SITE_FILES
        for name in ("memory-wall/index.html", "memory-wall/sheets.css", "memory-wall/sheets.js"):
            self.assertIn(name, SITE_FILES)
            self.assertTrue((ROOT / "site" / name).exists())
        for name in ("index.html", "field.html", "workspaces.html", "operations.html",
                     "editing.html", "money.html"):
            self.assertIn('href="./memory-wall/"', (ROOT / "site" / name).read_text())
        self.assertIn('href="../memory-wall/"',
                      (ROOT / "site/resources/project-documents.html").read_text())


if __name__ == "__main__":
    unittest.main()
