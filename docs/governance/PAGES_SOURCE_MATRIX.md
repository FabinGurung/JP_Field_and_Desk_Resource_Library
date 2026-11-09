# A9 Field & Desk — Pages, Sheets and original-Drive source map

**Observed source state:** 9 November 2026. **Owning Git repository:** `FabinGurung/JP_Field_and_Desk_Resource_Library`, provider repository ID `1448289662`. **PRE-main:** `9aa0969cfcc6d341962129f6789eab5b76ec0b7e`.

## Public information architecture

```text
A9 Field & Desk Operations Library
├── Organization (company sourced from the LIVE resource register)
│   └── Project (stable PRJ ID, source Project Name)
│       └── Resource category (derived from Document Slot, then Category fallback)
│           ├── Drawings → Architectural / Structural
│           ├── Models & Analysis → 3D / analysis / source models
│           ├── Reports & References
│           ├── Estimates & Calculations
│           ├── Source Folders (open original, not cloned)
│           └── Agreements & Materials → A/B/C document register
├── Source Custody (dated, reviewed GitHub-only public-safe snapshot)
└── How to Edit (source owners, source tabs, operational boundaries)
```

Search is within the current tier and does not replace company/project selection. Public presentation `company_key` is an ephemeral slug, **not** an A7 ORG-ID or authority claim. Project IDs and source document record IDs are never rewritten.

## Exact live source Sheets

The *only* workbook fetched by the GitHub Pages publisher is the existing **Project Resources — LIVE — V000002**, permanent ID `1e019Jac4lDveZ2glXMph4RLHivqPFEachbcNi-R1DZk` (same preexisting live ID).

| Display / output | Native source tab (gid) | Edit scope | Notes |
|---|---|---|---|
| Company directory | `project_resources` (8000011) | `Company`, `Project ID`, `Project Name` | Blank project-packet company stays in a review-only group |
| Projects per company | `project_resources` (8000011), `client_document_packets` (8230001) | Names, existing IDs, `Company Project Code`, `Publish` | Packet-only projects must receive independently confirmed `Company` in their own source, never a code-derived guess |
| Resource categories and detail | `project_resources` (8000011) | `Document Slot`, `Category`, `Format`, `Display Name`, `Approval Status`, `Sort Priority` | Group algorithm versioned in `scripts/publish_library.py` |
| Original Drive links and access labels | `project_resources` (8000011) + `resource_source_readback` (8230002) | `Source Drive File ID`, `Source URL`, review columns | Source file ID, link route and owner receipt must match |
| A/B/C project-document viewer | `client_document_packets` (8230001) + `resource_source_readback` (8230002) | `Document ID`, `Project ID`, `Role`, `Language`, `Version`, `Approval`, original PDF ID, `Publish` | Six currently published packet entries |
| Source custody portal | No Google Sheet | `site/source-custody.json` via reviewed Git change | **Never live private payroll**, dated audit classification only |
| Editing guide | No Google Sheet | `site/editing.html` in Git | Human instructions and permanent owner workbook links |
| Release / history links | GitHub only | Owning repository commits, PRs, Actions, releases | Deployment evidence is not original-document approval |

The source workbook also has `00_START_HERE`, `00_MANIFEST`, `02_HOW_TO`, `01_VERSION_HISTORY`. These control tabs are **not fetched by the website workflow**, though humans must preserve their provenance role. One `00_START_HERE` historical note still describes an older *publishing copy*; the current code explicitly reads the original live workbook directly. Correct that note through the owner's controlled Sheet edit when its native PRE/POST requirements are satisfied, rather than switching source IDs silently.

### Original files

Each published resource row contains a `Source Drive File ID` and Drive `Source URL` to the document/folder original. The *source readback tab* records observed metadata, not fresh file API inspection in each Pages run. Thus original files live in varied project Drive folders, not one uniform repo-owned Drive folder. The A/B/C viewer similarly links source PDF IDs from its packet rows; it never embeds document bytes in Git.

The separate Fishtail payroll/attendance root, Worker Money & Goods collection, and Wage List 11 conversion collection are **not** read by this Actions job; their original private live authority and native IDs remain in Drive. Locked M01–M03 analytical baselines are not live payroll. Worker rollout M04 is not verified final. No private worker IDs or payment rows are copied into the public catalogue.

## Company mismatch requiring source-owner decision

The resource register currently has **46 Publish=TRUE** resources: Fishtail Builders Pvt Ltd (42), Rohini Engineering and Builders Pvt Ltd (4), over eight projects. The packet tab has six A/B/C files under `PRJ-000029`, but no explicit Company column, so it is shown as **Company confirmation required** (a ninth project). The project code `REB-002` is not sufficient to infer or silently assign its ownership. To resolve, source owner should confirm the company against the operational project master, add an explicit `Company` column to `client_document_packets` without replacing its ID, and apply the same confirmed name to all relevant rows. The publisher already reads an optional Company column.

## GitHub Actions pipeline

```text
GitHub PR / push / hourly schedule / manual
  ├─ test: offline unit tests, JS syntax, synthetic projection validator
  ├─ browser-qa: real Chromium desktop + mobile against synthetic fixture
  │    └─ runs for PR, push and manual; skipped on hourly schedules
  ├─ project: wait for tests and browser gate (or scheduled skip)
  │    ├─ existing keyless Workload Identity Federation (Sheets readonly)
  │    ├─ read project_resources, client_document_packets, resource_source_readback twice
  │    ├─ validate ID ↔ link ↔ MIME ↔ review receipt ↔ 30-day age
  │    ├─ build source grouping, output counts and public-safe metadata
  │    └─ validate output artifact and upload to Pages
  ├─ deploy: GitHub Pages, main branch only
  └─ release-cutover: exact served-body check, schema/count check, v1.2.0 release
```

An owner-edited Sheet updates the next successful scheduled/manually initiated published projection; it does **not** require a Git commit for each row. Conversely, frontend, schemas, validation and workflow changes require a reviewed Git commit. Do not edit `catalog.json` or `document-packets.json` by hand: they are derived.

## A7 Memory Palace / version discipline

A7 canonical operating rule: **Organization → Project → Category → Resource**, and **AI operates · Drive preserves · GitHub versions · Actions verifies · Pages presents**. A7 holds identity/policy/routing and *does not* absorb Field & Desk domain edits. See `JP_A7_System_Registry_and_Knowledge_Graph/A7_READ_FIRST.md`, `docs/MEMORY_WALL_READ_FIRST.md`, and `docs/A9_GIT_DRIVE_OPERATING_RULE.md`.

- PRE: unchanged original `main` at `9aa0969cfcc6d341962129f6789eab5b76ec0b7e`; existing v1.1.0 release provides rollback marker.
- POST: feature PR and merge commit with CI/Pages provider readback; version `v1.2.0` only after successful Pages verification.
- Native Google Sheets use their **existing** version history and PRE/POST archives. No new workbook IDs.
- Public repository stores only safely admitted metadata; private A9 Main/Local consumed cursor/ACK is **not** implicitly updated.
- A7 itself is read-only during this site work: registering a new canonical A7 organization or peer-module identity requires a separate governed A7 change.
