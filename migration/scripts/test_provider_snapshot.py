#!/usr/bin/env python3
"""Read-only QA for A9 Source GitHub provider-pointer inventory.

This script never calls GitHub or reads credentials. Original Issues, pull requests,
release notes, Actions logs, and files remain with the originating provider.
"""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SNAPSHOT_DIR = ROOT / "migration/provider-snapshots/20261108"
META_PATH = SNAPSHOT_DIR / "source-provider-metadata.v1.json"
HEX40 = re.compile(r"^[0-9a-f]{40}$")


def load_metadata():
    return json.loads(META_PATH.read_text(encoding="utf-8"))


def load_run_rows(meta):
    rows = []
    sizes = []
    for segment in meta["actions_run_index"]["segments"]:
        source_path = segment["path"]
        path = ROOT / source_path
        if not path.is_file():
            raise AssertionError("Missing indexed Actions segment: " + source_path)
        lines = path.read_text(encoding="utf-8").splitlines()
        if not lines or any(not line.strip() for line in lines):
            raise AssertionError("Empty or blank line in indexed Actions segment")
        parsed = [json.loads(line) for line in lines]
        sizes.append(len(parsed))
        if len(parsed) != segment["rows"]:
            raise AssertionError("Expected segment size mismatch for " + source_path)
        rows.extend(parsed)
    return rows, sizes


class ProviderInventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.meta = load_metadata()
        cls.runs, cls.sizes = load_run_rows(cls.meta)

    def test_one_governed_audit_identity(self):
        self.assertEqual(self.meta["audit_id"], "A9-RLIB-MIG-000001")
        self.assertEqual(self.meta["schema_version"], "1.0.0")
        self.assertTrue(self.meta["source_is_authoritative_for_issues_prs_release_notes_runs"])
        self.assertTrue(self.meta["governance"]["no_mutation_to_source"])
        self.assertTrue(self.meta["governance"]["no_provider_replay"])

    def test_complete_run_count_and_segments(self):
        self.assertEqual(self.sizes, [500, 500, 500, 415])
        self.assertEqual(len(self.runs), 1915)
        self.assertEqual(len(self.runs), self.meta["counts"]["actions_runs_indexed_in_sibling_jsonl"])
        self.assertEqual(len(set(run["id"] for run in self.runs)), 1915)

    def test_run_order_and_url_identity(self):
        source = self.meta["source_repository"]
        ids = [run["id"] for run in self.runs]
        self.assertTrue(all(ids[i] > ids[i+1] for i in range(len(ids)-1)))
        for run in self.runs:
            self.assertEqual(run["html_url"], "https://github.com/" + source + "/actions/runs/" + str(run["id"]))
            self.assertRegex(run["head_sha"], HEX40)
            self.assertGreaterEqual(run["run_attempt"], 1)
            self.assertTrue(run["created_at"].endswith("Z"))

    def test_run_event_and_conclusion_distribution(self):
        from collections import Counter
        summary = self.meta["actions_run_index"]["summary"]
        self.assertEqual(dict(Counter(r["event"] for r in self.runs)), summary["events"])
        self.assertEqual(dict(Counter(r["conclusion"] for r in self.runs)), summary["conclusions"])
        self.assertEqual({r["status"] for r in self.runs}, {"completed"})
        self.assertEqual(summary["range_latest_created_utc"], self.runs[0]["created_at"])
        self.assertEqual(summary["range_earliest_created_utc"], self.runs[-1]["created_at"])

    def test_source_issue_numbers_and_privacy_gate(self):
        issues = self.meta["issues"]
        self.assertEqual(len(issues), self.meta["counts"]["issues"])
        self.assertEqual(sorted(i["source_number"] for i in issues), [8, 23, 24, 25])
        source = self.meta["source_repository"]
        for issue in issues:
            self.assertEqual(issue["source_url"], "https://github.com/" + source + "/issues/" + str(issue["source_number"]))
            self.assertFalse(issue["source_body_copied"])
            self.assertEqual(issue["migration"], "LINK_INDEX_ONLY")
        basanti = next(i for i in issues if i["source_number"] == 8)
        self.assertEqual(basanti["privacy_gate"], "PRJ-000029_PRIVATE_PUBLICATION_ADMISSION_HOLD")

    def test_pull_request_counts_and_imported_commit_links(self):
        prs = self.meta["pull_requests"]
        self.assertEqual(len(prs), 21)
        self.assertEqual(len(set(p["source_number"] for p in prs)), 21)
        self.assertEqual(sum(p["merged_at"] is not None for p in prs), 20)
        source = self.meta["source_repository"]
        for pr in prs:
            self.assertEqual(pr["source_url"], "https://github.com/" + source + "/pull/" + str(pr["source_number"]))
            self.assertRegex(pr["head_sha"], HEX40)
            self.assertTrue(pr["imported_git_commit_object_reachable"])
            self.assertFalse(pr["provider_discussion_copied"])
            self.assertEqual(pr["migration"], "LINK_INDEX_ONLY")

    def test_release_records_preserve_source_authority(self):
        rel = self.meta["releases"]
        self.assertEqual(len(rel), 4)
        self.assertEqual(sum(len(x["assets"]) for x in rel), 0)
        tags = sorted(x["source_tag"] for x in rel)
        self.assertEqual(tags, ["v1.1.0", "v1.2.0-alpha.1", "v2.1.0", "v2.2.0"])
        for release in rel:
            self.assertFalse(release["release_provider_object_migrated"])
            self.assertTrue(release["tag_git_object_imported_and_SHA_verified"])
            self.assertFalse(release["source_body_copied"])

    def test_pages_and_provider_settings_not_overclaimed(self):
        src = self.meta["repository_snapshot"]["source"]
        dst = self.meta["repository_snapshot"]["destination"]
        self.assertTrue(src["has_pages"])
        self.assertFalse(dst["has_pages"])
        gates = self.meta["additional_provider_gates"]
        self.assertEqual(gates["environments"], "UNVERIFIED")
        self.assertEqual(gates["client_publication"], "HOLD__PRJ-000029")
        self.assertEqual(gates["credential_management"], "OWNER_RETAINS_TOKEN_AND_SECRET__NO_CHANGE_REQUESTED")

if __name__ == "__main__":
    unittest.main()
