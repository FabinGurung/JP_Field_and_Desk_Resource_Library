# A9 Field & Desk — Pages, Sheets and original-Drive source map

**Observed source state:** 9 November 2026. **Owning Git repository:** `FabinGurung/jp-field-desk-library`, provider repository ID `1448289662`. **PRE-main:** `9aa0969cfcc6d341962129f6789eab5b76ec0b7e`.

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

The source workbook also has `00_START_HERE`, `00_MANIFEST`, `02_HOW_TO`, `01_VERSION_HISTORY`. These control tabs are **not fetched by the website workflow**, though humans must preserve their provenance role. The live control tabs were corrected in-place on 10 November 2026; the old publishing-copy URL remains labeled historical. No source IDs were replaced.

### Original files

Each published resource row contains a `Source Drive File ID` and Drive `Source URL` to the document/folder original. The *source readback tab* records observed metadata, not fresh file API inspection in each Pages run. Thus original files live in varied project Drive folders, not one uniform repo-owned Drive folder. The A/B/C viewer similarly links source PDF IDs from its packet rows; it never embeds document bytes in Git.

The separate Fishtail payroll/attendance root, Worker Money & Goods collection, and Wage List 11 conversion collection are **not** read by this Actions job; their original private live authority and native IDs remain in Drive. Locked M01–M03 analytical baselines are not live payroll. Worker rollout M04 is not verified final. No private worker IDs or payment rows are copied into the public catalogue.

## PRJ-000029 — current publication status, checked 10 November 2026

The original project identity is **PRJ-000029 / REB-002 → ORG-000002**, Rohini Engineering and Builders Pvt Ltd. The permanent Resource Library owner workbook contains the verified Company on all six original A/B/C packet rows; those source IDs and approval notes were preserved.

**Current live readbacks (supersede the archived 23 October read-first warning):**
- `CONTINENT_01__PROJECT_IDENTITY__v0.1`, `AI_Project_Identity!O30`: `is_public=TRUE`.
- `Projects and Locations — v1.3`, `projects!AA30`: `is_public=TRUE`.
- `Project Resources — LIVE — V000002`, `client_document_packets!N2:N7`: all six `Publish=TRUE`.

The previous project-level publication HOLD is resolved for **public listing**, not for contract execution, signed drawing approval, private cost details or unrestricted access to Drive originals. These are independently governed. The retired alias `PRJ-000030` stays `FALSE`. The prior user-verified read-first document remains immutable historical evidence.

No Google Sheet edit was required or made to apply the requested TRUE flag. The authoritative values were already TRUE at this live QA pass.

## Filters grounded in the live workbook

Within a selected project the directory filters `Discipline` (L), `Format` (G), `Revision Note` (M) and `Approval Status` (N) from the original `project_resources` rows. Raw source values are retained; the user-facing translation only makes review text easier to read. All 46 resource rows currently have `UNVERIFIED_AS_CURRENT_ISSUE` and no approved revision can be inferred.

## Google Sheet V000004 archive and rollback

The live source ID was preserved; `00_START_HERE` and `02_HOW_TO` now describe the direct authenticated three-tab publisher. The prior publishing-copy link is retained as **historical**. `01_VERSION_HISTORY` gained V000004, and the existing resource archive folder holds matching native `000004_PRE` and `000004_POST` snapshots. Their private provider IDs do not belong in this public GitHub source map. Restorations go into the same live Sheet ID; never repoint Actions to a snapshot.

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
  └─ release-cutover: exact served-body check, schema/count check, release after deployment
```

An owner-edited Sheet updates the next successful scheduled/manually initiated published projection; it does **not** require a Git commit for each row. Conversely, frontend, schemas, validation and workflow changes require a reviewed Git commit. Do not edit `catalog.json` or `document-packets.json` by hand: they are derived.

## A7 Memory Palace / version discipline

A7 canonical operating rule: **Organization → Project → Category → Resource**, and **AI operates · Drive preserves · GitHub versions · Actions verifies · Pages presents**. A7 holds identity/policy/routing and *does not* absorb Field & Desk domain edits. See `JP_A7_System_Registry_and_Knowledge_Graph/A7_READ_FIRST.md`, `docs/MEMORY_WALL_READ_FIRST.md`, and `docs/A9_GIT_DRIVE_OPERATING_RULE.md`.

- PRE: unchanged original `main` at `9aa0969cfcc6d341962129f6789eab5b76ec0b7e`; existing v1.1.0 release provides rollback marker.
- POST: feature PR and merge commit with CI/Pages provider readback; version `v1.2.0` only after successful Pages verification.
- Native Google Sheets use their **existing** version history and PRE/POST archives. No new workbook IDs.
- Public repository stores only safely admitted metadata; private A9 Main/Local consumed cursor/ACK is **not** implicitly updated.
- A7 itself is read-only during this site work: registering a new canonical A7 organization or peer-module identity requires a separate governed A7 change.

## v1.5.0 — Normalized source slots and private financial boundaries (11 November 2026)

The Library now maintains the same display slots for all projects (Architectural PDF/DWG, Structural PDF/DWG, ETABS E2K/EDB, SketchUp SKP, reports, calculations, source folders and client packet). Empty slots mean **not registered in this published workbook**; no false file or link is invented. `Original Filename` is displayed as owner-entered metadata for file differentiation.

New Level 1 `workspaces.html` routes to the existing site-directory root (Level 2 → company → project) or to `money.html` (Level 2 → workforce/contractor/vendor families). Contractor BOQ and bills belong to peer Cost Estimation; payment proofs stay Finance, while public Pages is a navigator only.

The existing 24-item Money & Goods original collection was renamed and moved by Drive metadata (not copied) into `01_JP / 02 Website Sheets and Registers / 06 Finance and Purchasing / 09 Restricted Workforce Source Registers`; all original child IDs and Drive permissions were checked unchanged. The worker-level finance integration remains **NOT_CONNECTED**. See `docs/operations/WORKFORCE_BILLING_SOURCE_PLAN_20261111.md` for A7 PRE/POST and readiness gates.
