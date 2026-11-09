"""Read the Resource Library owner workbook and build the Pages artifact."""
import argparse
import json
import re
import shutil
from pathlib import Path
from urllib.parse import urlsplit

from sheets_read import ROOT, load_tables, records

SOURCES = {
    "resources": ("1e019Jac4lDveZ2glXMph4RLHivqPFEachbcNi-R1DZk", "project_resources"),
    "packets": ("1e019Jac4lDveZ2glXMph4RLHivqPFEachbcNi-R1DZk", "client_document_packets"),
    "readback": ("1e019Jac4lDveZ2glXMph4RLHivqPFEachbcNi-R1DZk", "resource_source_readback"),
}
ACCESS_MODES = {"PUBLIC_LINK", "DRIVE_PERMISSION_REQUIRED"}
ADMISSION = {"LEGACY_PUBLIC_ROUTE", "OWNER_REVIEWED_PUBLIC_LINK"}
SITE_FILES = ("index.html", "app.js", "styles.css", "resources/project-documents.html")


def checked_source(row, key, receipt):
    file_id = row["drive_file_id"] if key == "document_id" else row["source_drive_file_id"]
    if not re.fullmatch(r"[A-Za-z0-9_-]{15,100}", file_id):
        raise ValueError("Invalid Drive file ID")
    source = receipt.get(row[key])
    if not source or source["drive_file_id"] != file_id:
        raise ValueError("Published link has no matching Drive readback")
    if (source["access_mode"] not in ACCESS_MODES or source["admission_basis"] not in ADMISSION
            or not source["modified_at"] or not source["checked_on"]):
        raise ValueError("Incomplete Drive readback")
    return source


def build(tables, out, received_at):
    receipts = {r["record_id"]: r for r in records(tables["readback"], "record_id",
        "drive_file_id", "mime_type", "modified_at", "access_mode", "checked_on", "admission_basis")}
    resources = []
    projects = {}
    documents = []
    for row in records(tables["resources"], "resource_id", "publish", "source_drive_file_id",
                       "source_url", "project_id", "project_name", "site_reference",
                       "display_name", "category", "format", "sort_priority", "approval_status"):
        if row["publish"].upper() != "TRUE":
            continue
        s = checked_source(row, "resource_id", receipts)
        file_id = s["drive_file_id"]
        parsed = urlsplit(row["source_url"])
        folder = s["mime_type"] == "application/vnd.google-apps.folder"
        path = f"/drive/folders/{file_id}" if folder else f"/file/d/{file_id}/view"
        if parsed.scheme != "https" or parsed.netloc != "drive.google.com" or parsed.path != path:
            raise ValueError("Resource URL does not match the verified Drive file")
        kind = "desk" if row["category"] in {"calculations_and_support", "source_folders"} else "field"
        resources.append({"id": row["resource_id"], "title": row["display_name"], "kind": kind,
                          "project_id": row["project_id"], "project": row["project_name"],
                          "site": row["site_reference"], "format": row["format"],
                          "approval": row["approval_status"], "priority": int(row["sort_priority"]),
                          "access": s["access_mode"], "url": f"https://drive.google.com{path}"})
    for row in records(tables["packets"], "document_id", "publish", "project_id",
                       "company_project_code", "project_name", "locality", "drive_file_id",
                       "role", "language", "title", "version", "pages", "approval"):
        if row["publish"].upper() != "TRUE":
            continue
        s = checked_source(row, "document_id", receipts)
        pid = row["project_id"]
        if (not re.fullmatch(r"PRJ-[0-9]{6}", pid) or row["role"] not in {"A", "B", "C"}
                or row["language"] not in {"en", "ne", "source"} or s["mime_type"] != "application/pdf"
                or int(row["pages"]) < 1):
            raise ValueError("Invalid published document packet")
        project = {"project_id": pid, "company_project_code": row["company_project_code"],
                   "name": row["project_name"], "locality": row["locality"]}
        if projects.setdefault(pid, project) != project:
            raise ValueError("Conflicting project-document identity")
        doc = {k: row[k] for k in ("document_id", "project_id", "role", "language", "title", "version", "pages", "approval", "drive_file_id")}
        doc.update(drive_url=f'https://drive.google.com/file/d/{s["drive_file_id"]}/view', access=s["access_mode"])
        documents.append(doc)
    resources.sort(key=lambda r: (r["priority"], r["project"], r["id"]))
    for name in SITE_FILES:
        target = out / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / "site" / name, target)
    (out / ".nojekyll").touch()
    (out / "catalog.json").write_text(json.dumps({"resources": resources, "projects": list(projects.values()),
        "verified_on_npt": received_at}, ensure_ascii=False), encoding="utf-8")
    (out / "document-packets.json").write_text(json.dumps({"schema_version": "1.0.0",
        "projects": list(projects.values()), "documents": documents, "verified_on_npt": received_at},
        ensure_ascii=False), encoding="utf-8")
    return len(resources), len(documents)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--fixture", type=Path)
    args = parser.parse_args()
    tables, stamp = load_tables(SOURCES, args.fixture)
    print("Catalogue records and client documents:", *build(tables, args.output, stamp))
