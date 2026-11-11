# A9 · Field & Desk Operations Library

**Human-facing name:** Field & Desk Operations Library. The live GitHub Pages site uses the `jp-field-desk-library` repository slug.

[Company-first Pages directory](https://fabingurung.github.io/jp-field-desk-library/) · [Source custody](https://fabingurung.github.io/jp-field-desk-library/operations.html) · [How to edit](https://fabingurung.github.io/jp-field-desk-library/editing.html)

## Purpose
A reviewed public-safe directory arranged by **Company → Project → Resource category → Original Drive record**. The existing Project Resources LIVE workbook owns catalogue rows. GitHub owns the grouping generator, source-consistency checks, site UI, tests, release notes, and publication pipeline. The original Google Drive files and their permissions remain authoritative.

**Not live:** Worker-level payroll, attendance, advances and private Money & Goods. They retain their original restricted authorities. The resource custody page is a dated static classification, not a worker dataset.

## Operate and verify
- [Pages source map and version-control contract](docs/governance/PAGES_SOURCE_MATRIX.md)
- [Original owner workbook](https://docs.google.com/spreadsheets/d/1e019Jac4lDveZ2glXMph4RLHivqPFEachbcNi-R1DZk/edit)
- [Google Sheets to Pages publisher workflow](.github/workflows/resource-library-pages.yml)
- [Releases and rollback points](https://github.com/FabinGurung/jp-field-desk-library/releases)
- [Existing project PDF viewer](https://fabingurung.github.io/jp-field-desk-library/resources/project-documents.html)

Preserve original names, archival history and ID lineage. A7 cross-system memory and authority live in the A7 semantic registry, not as a duplicate source copy here.

## Prior release
The former v1.1.0 source and original history remain in Git. Earlier handover text can be found in the prior commit rather than a separate cloned website.

## v1.3.0 — source-backed filters and native source reconciliation

The LIVE owner workbook now includes a source-verified Company column in its six original project packet rows. Its obsolete publishing instructions were corrected with V000004 native PRE/POST archives, while the same permanent workbook ID is retained. The website filters use original Discipline, Format, Revision Note and Approval Status fields. Historical at the time: the mismatch was subsequently resolved; both current project registers now report PRJ-000029 `is_public=TRUE`.

## v1.3.2 — Publication and rename status QA

This repository is now `FabinGurung/jp-field-desk-library` (unchanged GitHub provider ID 1448289662). Live CONTINENT_01 Project Identity and Projects & Locations now both have `PRJ-000029.is_public=TRUE`; all six original Basanti packet rows already have `Publish=TRUE`. No source flags or file permissions were modified. Public project listing is distinct from contract signature, construction issue approval, and private Drive access.

## v1.5.0 — Normalized site resources and financial navigation

Every project now displays the same engineering slots even when no entry is registered; original filenames distinguish duplicate generic labels. The new Workspaces and Money & Bills pages separate field/desk originals, restricted worker money sources and contractor BOQ/bill calculations. The original 24-item Money & Goods folder moved in place under `01_JP / 02 Website Sheets and Registers / 06 Finance and Purchasing` preserving original Drive IDs, worker sheet names, history and observed ACLs. Private financial rows remain outside public GitHub Pages. See [source plan](docs/operations/WORKFORCE_BILLING_SOURCE_PLAN_20261111.md).

## v1.6.0 — Two primary tabs: Desk Resources / Field Resources (12 Nov 2026)

The intended **Desk** surface is the existing company/project engineering-source directory (`/`): architectural and structural PDF/DWG, ETABS E2K/EDB, SketchUp SKP, reports/calculations, original folders and A/B/C client packets, including source-backed empty slots. The distinct **Field** tab (`/field.html`) groups workforce and operational-finance record families by confirmed company first, plus a separate cross-company/unassigned intake for original contractor bills, vendor bills and measurements. A status-only Fishtail worker Money & Goods and attendance reference is present; Rohini has matching visible but unregistered slots. No financial amounts, individual worker names or protected Drive links appear in the public Field page.

`/workspaces.html` now promotes only the two major areas, retaining secondary governance, Money & Bills and Astam links. The original `/money.html` is a deeper Field resource guide with its URL preserved. Original workbook and Drive IDs, source status and A7 authority boundaries remain unchanged. See `docs/releases/v1.6.0.md` for release QA.

## v1.7.0 — Explicitly approved, source-derived historical CLEAN Payment publication

The owner explicitly authorized publishing original-derived worker transaction fields on public GitHub Pages on **12 November 2026**. The historical `Wage_List_11__PAYMENT__CLEAN_v1.1` workbook, tab `Payment`, is read directly on every successful Pages build using a specific read-only share with the existing WIF Pages service account. The public output `field-payments.json` includes worker, date, site, category, signed amount in NPR, and original source row/cell; excludes paid-by information, remarks, bank/contact data and original editable files. **The generated GitHub Pages data is public: source Google Sheet ACLs do not transfer to it.**

The checked baseline is **958 source transaction rows** (21 worker identifiers) and an original TOTAL footer. Negative contract adjustments are retained; manifest record-count, source hash, source row uniqueness, date conversion and unrounded totals are strictly validated. Historical CLEAN Payment is **not** the operational W01–W21 Money & Goods ledger nor a certified payroll settlement. The W01–W10 originals currently report zero used money entries; W11–W21 are attendance-only originals and were renamed accordingly. The W01 hardened prototype is retained under a Prototype folder and its two backups are archived, with all source IDs/history preserved. No unrelated worker originals were replaced.
