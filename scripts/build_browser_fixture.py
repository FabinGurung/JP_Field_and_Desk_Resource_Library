"""Build synthetic, offline preview only. Never load confidential Sheets in PR browser QA."""
import json
import sys
from pathlib import Path
from publish_library import build
from test_company_directory import sample

target = Path(sys.argv[1] if len(sys.argv) > 1 else "_preview")
target.mkdir(parents=True, exist_ok=True)
build(sample(), target, "2026-11-09T13:00:00+05:45")
print("Synthetic browser preview:", target, "files:", len(list(target.rglob("*"))))
