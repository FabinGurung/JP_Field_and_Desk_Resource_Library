#!/usr/bin/env python3
"""Offline unit checks for the fail-closed historical import continuation."""
import importlib.util
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import unittest

SCRIPT = Path(__file__).with_name("history_transfer.py")
SPEC = importlib.util.spec_from_file_location("history_transfer", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def fixture():
    branches = {}
    tags = {}
    manifest = {"branches": [], "tags": []}
    for i in range(47):
        src = "refs/heads/main" if i == 0 else f"refs/heads/audit/ref-{i:03}"
        dst = "refs/heads/imported/cwo/" + src[len("refs/heads/"):]
        sha = f"{i+1:040x}"
        branches[src] = sha
        manifest["branches"].append(
            {"source_ref": src, "target_ref": dst, "source_sha": sha}
        )
    for i in range(4):
        src = f"refs/tags/v-{i}"
        dst = f"refs/tags/imported-cwo/v-{i}"
        sha = f"{100+i:040x}"
        tags[src] = sha
        manifest["tags"].append(
            {"source_ref": src, "target_ref": dst, "source_object_sha": sha}
        )
    return manifest, branches, tags


class ImportPlanTests(unittest.TestCase):
    def test_empty_destination_plans_all_refs(self):
        manifest, branches, tags = fixture()
        expected, refspecs, missing = MODULE.build_import_plan(
            manifest, branches, tags, {}
        )
        self.assertEqual(len(expected), 51)
        self.assertEqual(len(missing), 51)
        self.assertEqual(
            refspecs["refs/heads/imported/cwo/main"],
            "refs/heads/main:refs/heads/imported/cwo/main"
        )

    def test_exact_existing_ref_skipped_not_overwritten(self):
        manifest, branches, tags = fixture()
        existing = {"refs/heads/imported/cwo/main": branches["refs/heads/main"]}
        expected, refspecs, missing = MODULE.build_import_plan(
            manifest, branches, tags, existing
        )
        self.assertEqual(len(expected), 51)
        self.assertEqual(len(missing), 50)
        self.assertNotIn("refs/heads/imported/cwo/main", missing)

    def test_complete_state_is_noop(self):
        manifest, branches, tags = fixture()
        expected, _, _ = MODULE.build_import_plan(manifest, branches, tags, {})
        _, _, missing = MODULE.build_import_plan(manifest, branches, tags, expected)
        self.assertEqual(missing, [])

    def test_unexpected_ref_blocks(self):
        manifest, branches, tags = fixture()
        with self.assertRaisesRegex(RuntimeError, "unrecognized imported ref"):
            MODULE.build_import_plan(manifest, branches, tags, {
                "refs/heads/imported/cwo/unknown": "f"*40
            })

    def test_sha_mismatch_blocks(self):
        manifest, branches, tags = fixture()
        with self.assertRaisesRegex(RuntimeError, "SHA mismatch"):
            MODULE.build_import_plan(manifest, branches, tags, {
                "refs/heads/imported/cwo/main": "f"*40
            })

    def test_redirect_to_real_main_blocks(self):
        manifest, branches, tags = fixture()
        manifest["branches"][0]["target_ref"] = "refs/heads/main"
        with self.assertRaisesRegex(RuntimeError, "unsafe branch mapping"):
            MODULE.build_import_plan(manifest, branches, tags, {})

    def test_duplicate_target_blocks(self):
        manifest, branches, tags = fixture()
        manifest["branches"][1]["target_ref"] = manifest["branches"][0]["target_ref"]
        with self.assertRaises(RuntimeError):
            MODULE.build_import_plan(manifest, branches, tags, {})

    def test_audit_does_not_need_import_credential(self):
        with patch.dict("os.environ", {"HISTORY_WRITE_TOKEN": "", "GITHUB_TOKEN": "actions-token"}):
            self.assertEqual(MODULE.import_credential("audit"), "")

    def test_import_requires_owner_secret(self):
        with patch.dict("os.environ", {"HISTORY_WRITE_TOKEN": "", "GITHUB_TOKEN": "actions-token"}):
            with self.assertRaisesRegex(RuntimeError, "A9_HISTORY_IMPORT_TOKEN"):
                MODULE.import_credential("import")

    def test_import_refuses_same_github_token(self):
        with patch.dict("os.environ", {"HISTORY_WRITE_TOKEN": "actions-token", "GITHUB_TOKEN": "actions-token"}):
            with self.assertRaisesRegex(RuntimeError, "GITHUB_TOKEN cannot replace"):
                MODULE.import_credential("import")

    def test_import_accepts_distinct_workflow_secret(self):
        with patch.dict("os.environ", {"HISTORY_WRITE_TOKEN": "separately-authorized-token", "GITHUB_TOKEN": "actions-token"}):
            self.assertEqual(MODULE.import_credential("import"), "separately-authorized-token")

    def test_redact_credentials_keep_push_error(self):
        message = b"remote: authorization: basic abcdef \nremote: refused test ref ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ123456\n"
        proc = SimpleNamespace(stderr=message)
        result = MODULE.sanitized_push_error(proc, "abcdef")
        self.assertIn("refused test ref", result)
        self.assertNotIn("abcdef", result)
        self.assertNotIn("ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ123456", result)


if __name__ == "__main__":
    unittest.main()
