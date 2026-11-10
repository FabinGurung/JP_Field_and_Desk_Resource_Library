"""Read the Resource Library owner workbook and build the Pages artifact."""
import argparse
import json
import re
import shutil
from pathlib import Path
from datetime import date, datetime
from urllib.parse import urlsplit

from sheets_read import ROOT, load_tables, records

SOURCES = {
    "resources": ("1e019Jac4lDveZ2glXMph4RLHivqPFEachbcNi-R1DZk", "project_resources"),
    "packets": ("1e019Jac4lDveZ2glXMph4RLHivqPFEachbcNi-R1DZk", "client_document_packets"),
    "readback": ("1e019Jac4lDveZ2glXMph4RLHivqPFEachbcNi-R1DZk", "resource_source_readback"),
}
ACCESS_MODES = {"PUBLIC_LINK", "DRIVE_PERMISSION_REQUIRED"}
ADMISSION = {"LEGACY_PUBLIC_ROUTE", "OWNER_REVIEWED_PUBLIC_LINK"}
SITE_FILES = ("index.html", "app.js", "styles.css", "resources/project-documents.html",
              "operations.html", "operations.css", "operations.js", "source-custody.json",
              "editing.html", "editing.css",
              "feasibility/index.html", "feasibility/buyer-guide/index.html",
              "feasibility/buyer-guide/guide.json",
              "ops/data/land-feasibility/astam-village-public.v1.0.json",
              "ops/data/land-feasibility/astam-buyer-guide-public.v1.0.json",
              "assets/css/jp-theme-tokens.css", "assets/css/site-shell.css",
              "assets/css/jp-botanical.css",
              "assets/botanical/garden-left.svg", "assets/botanical/garden-right.svg",
              "assets/botanical/corner-sprig.svg", "assets/botanical/empty-garden.svg",
              "assets/botanical/tree-silhouette.svg")


def checked_source(row, key, receipt, publication_day=None):
    file_id = row["drive_file_id"] if key == "document_id" else row["source_drive_file_id"]
    if not re.fullmatch(r"[A-Za-z0-9_-]{15,100}", file_id):
        raise ValueError("Invalid Drive file ID")
    source = receipt.get(row[key])
    if not source or source["drive_file_id"] != file_id:
        raise ValueError("Published link has no matching Drive readback")
    if (source["access_mode"] not in ACCESS_MODES or source["admission_basis"] not in ADMISSION
            or not source["modified_at"] or not source["checked_on"]):
        raise ValueError("Incomplete Drive readback")
    # The owner-entered receipt is not a fresh authenticated Drive file read.
    try:
        observed = date.fromisoformat(str(source["checked_on"])[:10])
        datetime.fromisoformat(str(source["modified_at"]).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        raise ValueError("Malformed Drive source readback timestamp") from None
    if publication_day is not None and not (0 <= (publication_day - observed).days <= 30):
        raise ValueError("Stale Drive owner readback; review required")
    return source


# These are presentation categories, not a new operational classification authority.
GROUPS = [
    ("drawings", "Drawings"),
    ("models", "Models & Analysis"),
    ("reports", "Reports & References"),
    ("calculations", "Estimates & Calculations"),
    ("source-folders", "Source Folders"),
    ("project-packets", "Agreements & Materials"),
    ("other", "Other References"),
]
UNASSIGNED_COMPANY = "Company confirmation required"


def company_key(company):
    value = re.sub(r"[^a-z0-9]+", "-", company.casefold()).strip("-")
    return "display-" + (value or "unassigned")


def resource_group(row):
    slot = row.get("document_slot", "").casefold()
    category = row.get("category", "").casefold()
    if "folder" in slot or category == "source_folders":
        return "source-folders"
    if "drawing" in slot:
        return "drawings"
    if "model" in slot:
        return "models"
    if "estimate" in slot or "calculation" in slot or category == "calculations_and_support":
        return "calculations"
    if "report" in slot or category == "issued_reports":
        return "reports"
    return "other"


def build(tables, out, received_at):
    try:
        publication_day = datetime.fromisoformat(received_at).date()
    except (TypeError, ValueError):
        publication_day = None  # Synthetic PR fixtures can use 'test'; production has an ISO timestamp.
    receipts = {r["record_id"]: r for r in records(tables["readback"], "record_id",
        "drive_file_id", "mime_type", "modified_at", "access_mode", "checked_on", "admission_basis")}
    resources, documents, project_map = [], [], {}

    def ensure_project(pid, name, company, code=""):
        if not re.fullmatch(r"PRJ-[0-9]{6}", pid) or not name.strip():
            raise ValueError("Invalid project identity in owner register")
        company = company.strip() or UNASSIGNED_COMPANY
        existing = project_map.get(pid)
        if existing is not None:
            if existing["name"] != name:
                raise ValueError("Conflicting project names in owner register")
            if company != UNASSIGNED_COMPANY and existing["company"] not in (company, UNASSIGNED_COMPANY):
                raise ValueError("Conflicting company assignments")
            if existing["company"] == UNASSIGNED_COMPANY and company != UNASSIGNED_COMPANY:
                existing["company"], existing["company_key"] = company, company_key(company)
                existing["company_assignment"] = "SOURCE_REGISTER"
            if code and existing.get("company_project_code") not in ("", code):
                raise ValueError("Conflicting company project code")
            if code:
                existing["company_project_code"] = code
            return existing
        entry = {
            "project_id": pid, "name": name, "company": company,
            "company_key": company_key(company), "company_project_code": code,
            "resource_count": 0, "document_count": 0, "categories": {},
            "company_assignment": "NEEDS_OWNER_CONFIRMATION" if company == UNASSIGNED_COMPANY else "SOURCE_REGISTER",
        }
        project_map[pid] = entry
        return entry

    for row in records(tables["resources"], "resource_id", "publish", "source_drive_file_id",
                       "source_url", "project_id", "project_name", "site_reference",
                       "display_name", "category", "format", "sort_priority", "approval_status",
                       "discipline", "revision_note"):
        if row["publish"].upper() != "TRUE":
            continue
        source = checked_source(row, "resource_id", receipts, publication_day)
        file_id = source["drive_file_id"]
        parsed = urlsplit(row["source_url"])
        folder = source["mime_type"] == "application/vnd.google-apps.folder"
        path = f"/drive/folders/{file_id}" if folder else f"/file/d/{file_id}/view"
        if parsed.scheme != "https" or parsed.netloc != "drive.google.com" or parsed.path != path:
            raise ValueError("Resource URL does not match the verified Drive file")
        company = row.get("company", "").strip()
        project = ensure_project(row["project_id"], row["project_name"], company,
                                 row.get("company_project_code", ""))
        group = resource_group(row)
        kind = "desk" if row["category"] in {"calculations_and_support", "source_folders"} else "field"
        resources.append({
            "id": row["resource_id"], "title": row["display_name"],
            "kind": kind, "group": group, "category": row["category"],
            "discipline": row["discipline"], "revision_note": row["revision_note"],
            "document_slot": row.get("document_slot", ""), "project_id": row["project_id"],
            "project": row["project_name"], "company": project["company"],
            "company_key": project["company_key"], "site": row["site_reference"],
            "format": row["format"], "approval": row["approval_status"],
            "priority": int(row["sort_priority"]), "access": source["access_mode"],
            "url": f"https://drive.google.com{path}", "readback_checked_on": source["checked_on"],
            "origin_tab": "project_resources", "readback_tab": "resource_source_readback",
        })
        project["resource_count"] += 1
        project["categories"][group] = project["categories"].get(group, 0) + 1

    for row in records(tables["packets"], "document_id", "publish", "project_id",
                       "company_project_code", "project_name", "locality", "drive_file_id",
                       "role", "language", "title", "version", "pages", "approval"):
        if row["publish"].upper() != "TRUE":
            continue
        source = checked_source(row, "document_id", receipts, publication_day)
        pid = row["project_id"]
        if (row["role"] not in {"A", "B", "C"} or row["language"] not in {"en", "ne", "source"}
                or source["mime_type"] != "application/pdf" or int(row["pages"]) < 1):
            raise ValueError("Invalid published document packet")
        project = ensure_project(pid, row["project_name"], row.get("company", ""),
                                 row["company_project_code"])
        doc = {k: row[k] for k in ("document_id", "project_id", "role", "language",
                                   "title", "version", "pages", "approval", "drive_file_id")}
        doc.update(
            drive_url=f'https://drive.google.com/file/d/{source["drive_file_id"]}/view',
            access=source["access_mode"], source_checked_on=source["checked_on"],
            origin_tab="client_document_packets"
        )
        documents.append(doc)
        project["document_count"] += 1
        project["categories"]["project-packets"] = project["categories"].get("project-packets", 0) + 1

    resources.sort(key=lambda r: (r["priority"], r["project"], r["id"]))
    projects = sorted(project_map.values(), key=lambda p: (p["company"] == UNASSIGNED_COMPANY,
                      p["company"].casefold(), p["name"].casefold(), p["project_id"]))
    companies = []
    for key in sorted({p["company_key"] for p in projects}):
        related = [p for p in projects if p["company_key"] == key]
        companies.append({
            "key": key, "name": related[0]["company"],
            "status": related[0]["company_assignment"],
            "project_count": len(related),
            "resource_count": sum(p["resource_count"] for p in related),
            "document_count": sum(p["document_count"] for p in related),
        })
    companies.sort(key=lambda c: (c["status"] == "NEEDS_OWNER_CONFIRMATION", c["name"].casefold()))
    # A presentation key is not an A7 canonical organization identifier.
    public_source = {
        "name": "Project Resources — LIVE — V000002",
        "tabs_fetched": ["project_resources", "client_document_packets", "resource_source_readback"],
        "method": "Sheets read-only double readback via authenticated GitHub Actions",
        "last_publication_npt": received_at,
        "source_revision_proven": False,
        "original_drive_files_rechecked": False,
        "private_payroll_connected": False,
    }
    for name in SITE_FILES:
        target = out / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / "site" / name, target)
    (out / ".nojekyll").touch()
    (out / "catalog.json").write_text(json.dumps({
        "schema_version": "2.0.0", "companies": companies, "projects": projects,
        "groups": [{"key": key, "label": label} for key, label in GROUPS],
        "resources": resources, "source_manifest": public_source,
        "verified_on_npt": received_at
    }, ensure_ascii=False), encoding="utf-8")
    (out / "document-packets.json").write_text(json.dumps({
        "schema_version": "1.0.0", "projects": [
            {"project_id": p["project_id"], "company_project_code": p["company_project_code"],
             "name": p["name"], "company": p["company"]}
            for p in projects if p["document_count"] > 0
        ], "documents": documents, "verified_on_npt": received_at
    }, ensure_ascii=False), encoding="utf-8")
    return len(resources), len(documents)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--fixture", type=Path)
    args = parser.parse_args()
    tables, stamp = load_tables(SOURCES, args.fixture)
    print("Catalogue records and client documents:", *build(tables, args.output, stamp))
