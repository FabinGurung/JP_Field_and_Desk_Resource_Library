"""Regressions for intentional hourly browser-QA skip and Pages deployment.

GitHub Actions handles the live dependency graph; these tests assert the
source condition and an explicit scheduled deployment audit are preserved.
"""
import re
import unittest
from pathlib import Path


WORKFLOW = Path(__file__).resolve().parents[1] / ".github/workflows/resource-library-pages.yml"


def job(name, text):
    m = re.search(r"(?ms)^  " + re.escape(name) + r":\n(.*?)(?=^  [A-Za-z][\w-]*:\n|\Z)", text)
    if not m:
        raise AssertionError("Missing GitHub Actions job: " + name)
    return m.group(1)


class ScheduledDeploymentRegressionTest(unittest.TestCase):
    def test_hourly_build_accepts_intentionally_skipped_browser_qa(self):
        yml = WORKFLOW.read_text()
        self.assertIn("- cron: '37 * * * *'", yml)
        qa = job("browser-qa", yml)
        self.assertIn("github.event_name != 'schedule'", qa)
        src = job("project", yml)
        self.assertIn("always()", src)
        self.assertIn("needs.test.result == 'success'", src)
        self.assertIn("needs['browser-qa'].result == 'skipped'", src)

    def test_deploy_overrides_implicit_success_but_requires_actual_build(self):
        yml = WORKFLOW.read_text()
        deploy = job("deploy", yml)
        self.assertIn("!cancelled()", deploy)
        self.assertIn("needs.project.result == 'success'", deploy)
        self.assertIn("github.event_name != 'workflow_dispatch' || inputs.publish", deploy)
        self.assertIn("needs: project", deploy)
        self.assertNotIn("always()", deploy)

    def test_scheduled_run_cannot_report_green_when_deployment_skips(self):
        yml = WORKFLOW.read_text()
        assertion = job("scheduled-refresh-assert", yml)
        self.assertIn("github.event_name == 'schedule'", assertion)
        self.assertIn("!cancelled()", assertion)
        self.assertIn("needs: [project, deploy]", assertion)
        self.assertIn("BUILD_RESULT:", assertion)
        self.assertIn("DEPLOY_RESULT:", assertion)
        self.assertIn("test \"$BUILD_RESULT\" = 'success'", assertion)
        self.assertIn("test \"$DEPLOY_RESULT\" = 'success'", assertion)


if __name__ == "__main__":
    unittest.main()
