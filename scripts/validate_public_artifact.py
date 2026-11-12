"""Check the generated GitHub Pages artifact, not just its Python source."""
import argparse
import json
import re
from collections import Counter
from pathlib import Path

URL = re.compile(r"^https://drive\.google\.com/(?:file/d/[A-Za-z0-9_-]+/view|drive/folders/[A-Za-z0-9_-]+)$")


def validate(directory):
    directory = Path(directory)
    catalog = json.loads((directory / "catalog.json").read_text(encoding="utf-8"))
    packets = json.loads((directory / "document-packets.json").read_text(encoding="utf-8"))
    custody = json.loads((directory / "source-custody.json").read_text(encoding="utf-8"))
    payment = json.loads((directory / "field-payments.json").read_text(encoding="utf-8"))
    if payment.get("schema_version") != "1.0.0":
        raise ValueError("Unexpected historical Payment publication schema")
    src = payment.get("source", {})
    if (src.get("source_status") != "HISTORICAL_CLEANED_PAYMENT_NOT_CERTIFIED_PAYROLL"
            or src.get("public_export_approved_on") != "2026-11-12"
            or src.get("worker_money_goods_transaction_feed") is not False):
        raise ValueError("Unapproved/misclassified historical Payment publication")
    entries = payment.get("records", [])
    if (len(entries) != payment.get("count")
            or len({r.get("id") for r in entries}) != len(entries)
            or len({r.get("worker_id") for r in entries}) != payment.get("worker_count")):
        raise ValueError("Historical Payment row/grain count mismatch")
    if round(sum(float(r["amount_npr"]) for r in entries), 2) != round(float(payment["total_npr"]), 2):
        raise ValueError("Historical Payment amount sum mismatch")
    for r in entries:
        # A blank source site is legitimate (184 of the 958 real records).
        # It must remain "", never guessed as a project/site or discarded.
        if (not all(r.get(k) for k in ("id", "worker_id", "worker", "date",
                                     "category", "source_row", "source_cell"))
                or "site" not in r or not isinstance(r["site"], str)
                or not re.fullmatch(r"20[0-9]{2}-[0-9]{2}-[0-9]{2}", r["date"])
                or any(k in r for k in ("paid_by", "bank_details", "phone", "remarks"))):
            raise ValueError("Historical Payment source identity or allowed fields invalid")

    if catalog.get("schema_version") != "2.0.0" or packets.get("schema_version") != "1.0.0":
        raise ValueError("Unexpected public artifact schema")
    source = catalog["source_manifest"]
    if source.get("private_payroll_connected") is not False:
        raise ValueError("Private payroll cannot be exposed by the Pages publisher")
    if source.get("original_drive_files_rechecked") is not False or source.get("source_revision_proven") is not False:
        raise ValueError("False independent Drive revision/readback claim")
    if custody.get("historical_clean_payment_publication") is not True or custody.get("authenticated_private_payroll_reads") is not True:
        raise ValueError("Authenticated historical clean Payment publication not recorded")
    if custody.get("live_worker_sync") is not False:
        raise ValueError("Source custody claims unavailable private sync")
    groups = {c["key"] for c in catalog["groups"]}
    companies = {c["key"]: c for c in catalog["companies"]}
    projects = {p["project_id"]: p for p in catalog["projects"]}
    if len(companies) != len(catalog["companies"]) or len(projects) != len(catalog["projects"]):
        raise ValueError("Duplicate company/project display identities")
    resource_counts = Counter()
    packet_counts = Counter()
    ids = set()
    for r in catalog["resources"]:
        if r["id"] in ids or not URL.fullmatch(r["url"]):
            raise ValueError("Duplicate or invalid public resource")
        ids.add(r["id"])
        if r["group"] not in groups or r["project_id"] not in projects:
            raise ValueError("Unrecognized category/project")
        p = projects[r["project_id"]]
        if p["company_key"] != r["company_key"] or p["company"] != r["company"]:
            raise ValueError("Resource company/project inconsistency")
        if not r.get("readback_checked_on") or r["origin_tab"] != "project_resources" or not r.get("discipline") or not r.get("revision_note"):
            raise ValueError("Unproven published row")
        resource_counts[r["project_id"]] += 1
    for d in packets["documents"]:
        if d["project_id"] not in projects or d["document_id"] in ids or not URL.fullmatch(d["drive_url"]):
            raise ValueError("Broken packet identity")
        ids.add(d["document_id"])
        packet_counts[d["project_id"]] += 1
    for pid, p in projects.items():
        if p["company_key"] not in companies:
            raise ValueError("Project has no company directory")
        if resource_counts[pid] != p["resource_count"] or packet_counts[pid] != p["document_count"]:
            raise ValueError("Incorrect project display counts")
        if p["company"] == "Company confirmation required" and p["company_assignment"] != "NEEDS_OWNER_CONFIRMATION":
            raise ValueError("Unknown company was silently approved")
    for key, c in companies.items():
        related = [p for p in projects.values() if p["company_key"] == key]
        if (len(related), sum(p["resource_count"] for p in related),
            sum(p["document_count"] for p in related)) != (
                c["project_count"], c["resource_count"], c["document_count"]):
            raise ValueError("Company summary counts differ from underlying rows")
    for path in ("index.html", "app.js", "styles.css", "editing.html",
                 "editing.css", "workspaces.html", "field.html", "field-payments.js", "money.html", "money.js", "portal.css",
                 "operations.html", "operations.js", "operations.css",
                 "resources/project-documents.html"):
        if not (directory / path).is_file():
            raise ValueError("Missing public route/asset: " + path)
    # Astam's previously public-safe client resources live with the Library.
    astam_routes = (
        "feasibility/index.html", "feasibility/buyer-guide/index.html",
        "feasibility/buyer-guide/guide.json",
        "ops/data/land-feasibility/astam-village-public.v1.0.json",
        "ops/data/land-feasibility/astam-buyer-guide-public.v1.0.json",
        "assets/css/jp-theme-tokens.css", "assets/css/site-shell.css",
        "assets/css/jp-botanical.css", "assets/botanical/garden-left.svg",
        "assets/botanical/garden-right.svg", "assets/botanical/corner-sprig.svg",
        "assets/botanical/empty-garden.svg", "assets/botanical/tree-silhouette.svg",
    )
    for path in astam_routes:
        if not (directory / path).is_file():
            raise ValueError("Missing migrated Astam route/asset: " + path)
    overview = json.loads((directory / "ops/data/land-feasibility/astam-village-public.v1.0.json").read_text())
    guide = json.loads((directory / "feasibility/buyer-guide/guide.json").read_text())
    if overview["project"].get("legal_status") != "UNVERIFIED" or not guide.get("public_scope") == "EDUCATIONAL_PUBLIC_SAFE":
        raise ValueError("Astam feasibility and buyer guide qualification drift")
    return {"companies": len(companies), "projects": len(projects),
            "resources": len(catalog["resources"]), "packet_files": len(packets["documents"])}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", default="_site")
    args = parser.parse_args()
    print("Public artifact QA PASSED:", validate(args.site))
