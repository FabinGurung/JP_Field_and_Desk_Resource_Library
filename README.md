# A9 · Field & Desk Operations Library

**Human-facing name:** Field & Desk Operations Library. The live GitHub Pages site uses the `jp-field-desk-library` repository slug.

[Google Sheets for staff](https://fabingurung.github.io/jp-field-desk-library/memory-wall/) · [Company-first Pages directory](https://fabingurung.github.io/jp-field-desk-library/) · [Source custody](https://fabingurung.github.io/jp-field-desk-library/operations.html) · [How to edit](https://fabingurung.github.io/jp-field-desk-library/editing.html)

## Purpose
A reviewed public-safe directory arranged by **Company → Project → Resource category → Original Drive record**. The existing Project Resources LIVE workbook owns catalogue rows. GitHub owns the grouping generator, source-consistency checks, site UI, tests, release notes, and publication pipeline. The original Google Drive files and their permissions remain authoritative.

**Currently published:** the reviewed Project Resources LIVE directory and owner-approved **historical CLEAN Payment v1.1** transactions. Operational W01–W21 Money & Goods balances, live payroll certification and contractor bill calculations remain separate; the source-custody page is dated evidence, not itself a current operational ledger.

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

The owner explicitly authorized publishing original-derived worker transaction fields on public GitHub Pages on **12 November 2026**. The historical `Wage_List_11__PAYMENT__CLEAN_v1.1` workbook, tab `Payment`, is read directly on every successful Pages build using a specific read-only share with the existing WIF Library read-only service account. The public output `field-payments.json` includes worker, date, site, category, signed amount in NPR, and original source row/cell; excludes paid-by information, remarks, bank/contact data and original editable files. **The generated GitHub Pages data is public: source Google Sheet ACLs do not transfer to it.**

The checked baseline is **958 source transaction rows** (21 worker identifiers) and an original TOTAL footer. Negative contract adjustments are retained; manifest record-count, source hash, source row uniqueness, date conversion and unrounded totals are strictly validated. Historical CLEAN Payment is **not** the operational W01–W21 Money & Goods ledger nor a certified payroll settlement. The W01–W10 originals currently report zero used money entries; W11–W21 are attendance-only originals and were renamed accordingly. The W01 hardened prototype is retained under a Prototype folder and its two backups are archived, with all source IDs/history preserved. No unrelated worker originals were replaced.

**Read-back correction:** Source publication uses the actual configured WIF `jp-resource-library-reader@just-a-project-5007.iam.gserviceaccount.com`, not `jp-pages-publisher@...`. First attempted deployment correctly failed closed on HTTP 403; the correct reader permission was then granted to the one clean Payment workbook and independently verified in Google Drive metadata. See the revised v1.7.0 release notes.

## Current Drive custody and scheduled publishing (12 November 2026)

The authoritative source locations were verified through Google Drive parent readback:
- **LIVE catalogue** — `01_JP / 02 Website Sheets and Registers / 01 Website Source Sheets — Edit Here / Project Resources — LIVE — V000002` (unchanged original ID).
- **Approved historical Payment publication** — `01_JP / 02 Website Sheets and Registers / 04 Published Historical Source Sheets — Reviewed / Wage_List_11__PAYMENT__CLEAN_v1.1`. This is the original workbook **moved** out of Cost Estimation's `97_STAGED_INTAKE_NOT_ADMITTED` conversion folder, not a replacement workbook. Its original ID and specific read-only Library Actions service-account grant remain.
- **Original worker-site registers** — `01_JP / 03 Fishtail Builders / Manpower / 09 Restricted Workforce Source Registers / FBL — Worker Site Records — ORIGINAL W01–W21`. Includes separate `01 Money & Goods Entries` (10 W01–W10 originals), `02 Attendance` (11 W11–W21 originals), `80_Prototype` and `90_Archive`; original 24 file IDs remain intact across children.
- Original other cleaned Wage List conversions remain in `03_JP_Cost_Estimation / 97_STAGED_INTAKE_NOT_ADMITTED / Wage_List_11__Conversion_and_Cleaning__20261024`. They are not published by this Library.

Earlier v1.5 descriptions of a `01_JP / 02 Website Sheets and Registers / 06 Finance and Purchasing` worker path were **incorrect**. The verified original parent is the Fishtail Builders Manpower branch above, before and after the 12 November subfolder grouping.

GitHub Actions scheduled runs previously passed `project` but skipped `deploy` because intentional schedule-only `browser-qa=skipped` propagated through an implicit `success()` status check on `deploy.if`. v1.7.1 adds `!cancelled()` with an explicit `needs.project.result == 'success'` gate, allowing **scheduled validated builds** to deploy while still blocking on failed/cancelled builds. A separate scheduled assertion marks the run failed rather than green when deployment is skipped or unsuccessful.

## Google Sheets for staff — Memory Wall (13 November 2026)

Open `/memory-wall/` on the Library website for the everyday Google Sheets directory. This page gives employees direct links, names the working tabs and groups the Sheets by their actual work: site visits/daily progress, company and people, projects, materials, website notices, scheduling and earlier cleaned copies. Staff see clean names and simple entry instructions, not internal program terminology.

**Currently read by this Library: exactly two original Google Sheets:**
1. `Project Resources — LIVE — V000002` — three original tabs: `project_resources`, `client_document_packets` and `resource_source_readback`.
2. `Wage_List_11__PAYMENT__CLEAN_v1.1` — `Payment` and `00_Manifest_History` for the owner-approved, earlier payment publication. It is not a current worker money-entry Sheet.

The 27 other native Sheets directly inside `01_JP / 02 Website Sheets and Registers / 01 Website Source Sheets — Edit Here` are **not** read by this Library. The page also links two scheduling reference Sheets under their existing folder and four earlier cleaned conversion workbooks under their existing folder, clearly separated. An employee opening or updating one of those other Sheets does not automatically change the Field & Desk website.

The directory contains **35 distinct direct Google Sheet links: 2 used here, 27 other Website Sheets, 2 scheduling Sheets and 4 earlier cleaned copies**. Original Sheet IDs, Drive parents, permissions, tabs, values and publishing rules remain unchanged. No new Google Sheets were created, moved or renamed for this page.

## v1.8.1 — Desk drawings and models (14 November 2026)

The existing `Project Resources — LIVE — V000002` original Google Sheet now contains **68** project resource entries (previously 46), **74** matching source checks, and the original **six** Basanti A/B/C packet documents. The workbook ID, original 46 existing rows and client packet references are preserved.

**19 full-size original engineering files** were copied from the separate Construction Sites Drive into seven existing A9 project source folders, with destination ownership, matching byte sizes and parent folders verified. Project counts: Bishal Paija 2; Samir Man Ghubaju 5; Hari Baral 4; Yamuna Pun Adai 2; Sabitri/Dipti Giri 2; Sharada Adhikari 3; Kharika Paudel 1. Foreign originals and unrelated financial/personal records were not changed. The A9 copies have their own permanent Drive IDs and normal Drive access permissions.

Basanti's existing 21-page original B drawing PDF includes architectural floor plans, structural details and septic/soak-pit details. Its one unchanged original PDF is now listed under three corresponding Desk categories, not misrepresented as three separate files. Kharika's already-listed structural analysis report was recategorized from Drawings to Reports.

All 22 new entries are `UNVERIFIED_AS_CURRENT_ISSUE` and require ordinary Google Drive permissions. No engineering approval, signed issuance or current design revision is inferred. The same native owner Sheet contains its PRE/POST snapshots under `000005`, history entry `V000007`, and refreshed original-sheet staff guidance. GitHub Actions regenerates public links from the original native sheet; do not edit generated JSON.
