"""Publish source-derived, historical Wage List 11 clean Payment records.

Publication is explicitly approved by the resource-library owner, 12 Nov 2026.
Never treat this historical clean register as live W01–W21 Money & Goods.
Only project/worker/date/category/amount and source-row provenance are admitted.
"""
import hashlib
import json
import re
from datetime import date, datetime, timedelta
from decimal import Decimal, InvalidOperation
from pathlib import Path

from sheets_read import load_tables

PAYMENT_ID = "1ShS8wI6OAZA6Is-DLJK3sVkJzl3i5mn5zK-on38fE9I"
PAYMENT_SOURCES = {
    "payments": (PAYMENT_ID, "Payment"),
    "manifest": (PAYMENT_ID, "00_Manifest_History"),
}
PAYMENT_HEADERS = [
    "Worker ID", "Worker", "Date", "Calendar", "Site(s)", "Payment category",
    "Paid by", "Amount NPR", "Source type", "Remarks", "Source row", "Source cell",
]
GOOGLE_EPOCH = date(1899, 12, 30)
CATEGORIES = {"Salary", "Advance", "Contract", "Ration", "Kirana"}


def date_string(value):
    if isinstance(value, (int, float)):
        # Sheets UNFORMATTED_VALUE represents native date cells as serial days.
        if value != int(value):
            raise ValueError("Payment date has non-zero time fraction")
        result = GOOGLE_EPOCH + timedelta(days=int(value))
        return result.isoformat()
    value = str(value).strip()
    return date.fromisoformat(value).isoformat()


def build_payments(tables, output_dir: Path, published_at: str):
    values = tables.get("payments", [])
    if not values or values[0] != PAYMENT_HEADERS:
        raise ValueError("Clean Payment source headers differ from approved source")
    meta = {
        str(r[0]).strip(): str(r[1]).strip()
        for r in tables.get("manifest", [])[1:]
        if len(r) > 1 and str(r[0]).strip()
    }
    if meta.get("Clean record count", "").replace(",", "") == "":
        raise ValueError("Clean Payment manifest record count missing")
    expected = int(meta["Clean record count"].replace(",", ""))
    if not meta.get("Source SHA-256") or not re.fullmatch(r"[a-fA-F0-9]{64}", meta["Source SHA-256"]):
        raise ValueError("Clean Payment manifest source hash missing/invalid")
    published, seen, footer, total = [], set(), None, Decimal(0)
    for source_number, source_row in enumerate(values[1:], start=2):
        row = list(source_row) + [""] * (len(PAYMENT_HEADERS) - len(source_row))
        if not any(str(v).strip() for v in row):
            continue
        if str(row[0]).strip().upper() == "TOTAL":
            if footer is not None:
                raise ValueError("Clean Payment has duplicate TOTAL footer")
            footer = Decimal(str(row[7]))
            continue
        if footer is not None:
            raise ValueError("Nonempty transaction after TOTAL footer")
        worker_id, worker_name = str(row[0]).strip(), str(row[1]).strip()
        site, kind = str(row[4]).strip(), str(row[5]).strip()
        source_ref, source_cell = str(row[10]).strip(), str(row[11]).strip()
        if (not worker_id or not worker_name or kind not in CATEGORIES
                or not source_ref or not re.fullmatch(r"[A-Z]+[0-9]+", source_cell)):
            raise ValueError(f"Missing/invalid payment source at Payment!A{source_number}:L{source_number}")
        day = date_string(row[2])
        try:
            money = Decimal(str(row[7]))
        except InvalidOperation:
            raise ValueError(f"Invalid payment value at source row {source_number}") from None
        if not money.is_finite():
            raise ValueError("Non-finite source payment value")
        # Source row and cell form a stable identity. Negative adjustments are valid
        # and must be retained with original sign; do not infer debit/credit.
        identity = (worker_id, source_ref, source_cell)
        if identity in seen:
            raise ValueError("Duplicate provenance identity in clean Payment")
        seen.add(identity)
        record_id = hashlib.sha256("|".join(identity).encode("utf-8")).hexdigest()[:16]
        published.append({
            "id": "PAY-" + record_id,
            "worker_id": worker_id,
            "worker": worker_name,
            "date": day,
            "site": site,
            "category": kind,
            "amount_npr": float(money),
            "source_row": source_ref,
            "source_cell": source_cell,
            "source_tab": "Payment",
        })
        total += money
    if len(published) != expected:
        raise ValueError(f"Clean Payment count mismatch: {len(published)} vs manifest {expected}")
    if footer is None or abs(total - footer) > Decimal("0.01"):
        raise ValueError("Clean Payment amounts do not reconcile to the source TOTAL footer")
    published.sort(key=lambda p: (p["date"], p["id"]), reverse=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    output = {
        "schema_version": "1.0.0",
        "source": {
            "title": "Wage_List_11__PAYMENT__CLEAN_v1.1",
            "spreadsheet_id": PAYMENT_ID,
            "tab": "Payment",
            "manifest_tab": "00_Manifest_History",
            "source_sha256": meta["Source SHA-256"],
            "origin": "24 October 2026 cleaned historical conversion",
            "source_status": "HISTORICAL_CLEANED_PAYMENT_NOT_CERTIFIED_PAYROLL",
            "public_export_approved_on": "2026-11-12",
            "worker_money_goods_transaction_feed": False,
        },
        "fetched_on_npt": published_at,
        "count": len(published),
        "worker_count": len({x["worker_id"] for x in published}),
        "total_npr": float(total),
        "records": published,
    }
    (output_dir / "field-payments.json").write_text(
        json.dumps(output, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    return len(published)


def publish_payments(out_dir: Path):
    tables, timestamp = load_tables(PAYMENT_SOURCES, None)
    return build_payments(tables, out_dir, timestamp)
