"""Build synthetic, offline preview only. Never load confidential Sheets in PR browser QA."""
import json
import sys
from pathlib import Path
from publish_library import build
from test_company_directory import sample
from publish_field_payments import build_payments, PAYMENT_HEADERS

target = Path(sys.argv[1] if len(sys.argv) > 1 else "_preview")
target.mkdir(parents=True, exist_ok=True)
build(sample(), target, "2026-11-09T13:00:00+05:45")
print("Synthetic browser preview:", target, "files:", len(list(target.rglob("*"))))

# Synthetic-only clean Payment data for Chromium QA: no original worker records.
synthetic = {
    "payments": [
        PAYMENT_HEADERS,
        ["synthetic_001", "Synthetic Worker", "2025-01-01", "AD", "Sample Site",
         "Salary", "", 100, "", "", "SyntheticWorker!10", "P10"],
        ["synthetic_001", "Synthetic Worker", "2025-01-02", "AD", "Sample Site",
         "Contract", "", -20, "", "", "SyntheticWorker!11", "Q11"],
        ["TOTAL", "", "", "", "", "", "", 80],
    ],
    "manifest": [
        ["Manifest and version history", "Value"],
        ["Clean record count", "2"],
        ["Source SHA-256", "f" * 64],
    ]
}
build_payments(synthetic, target, "2026-11-12T04:00:00+05:45")
