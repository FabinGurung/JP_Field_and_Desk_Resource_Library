# A9 — Workforce / Contractor Billing Sources and A7 Custody
**Verified:** 11 November 2026 · Asia/Kathmandu

## Which system owns which resource?

| Subject | Original authority | Field & Desk Library | Executable financial owner | Verified state |
|---|---|---|---|---|
| Drawings and ETABS/SKP models | Project source Drive originals and live Project Resources register | Named original links + normalized PDF/DWG/E2K/EDB/SKP slots | Engineering, CAD / owner | Published links; issue approval not established |
| Worker Money & Goods | Existing W01–W21 original Sheets | Public custody and safe routing only | Restricted Finance / Manpower | Rollout NOT_VERIFIED_FINAL; no authenticated private payroll read |
| Wage List 11 and M01/M02/M03 | Original immutable source + historical analytic baselines | Reference classification only | Restricted Payroll | Historical evidence, not a live database |
| Contractor bills | Project measurements, Finance source bills | Public navigation only | Cost Estimation / BOQ `MOD-COST-001` | Original sources exist; operational billing live status unverified |
| Vendor bills | Supplier invoices/challans and Finance originals | Public navigation only | Finance / Purchasing | Original or review candidate, approval required |

## Drive move: PRE → POST metadata

**PRE:** `01_JP / 03 Fishtail Builders / Manpower / Money_and_Goods`.
**POST:** `01_JP / 02 Website Sheets and Registers / 06 Finance and Purchasing / 09 Restricted Workforce Source Registers — Not for Public Pages / FBL — Worker Money & Goods — ORIGINAL Sheets (rollout unverified)`.

Drive connector performed one metadata-only move and folder rename; the **same folder ID** and **24 child IDs** remain (21 original worker Sheets, one separate W01 prototype, two W01 backups). Readback verified both parent and collection children, an original W01 child, and the same four permitted Drive users and their roles at original and destination. The PUBLIC Git repository does not include worker names, per-worker file IDs, payroll rows, advances or amounts. The move was not a copy and does not establish new operational authority or additional published data.

The current `Project Resources — LIVE — V000002` Sheet is already under `01_JP / 02 Website Sheets and Registers / 01 Website Source Sheets — Edit Here`. It stays there at its permanent ID. The private worker collection was deliberately *not* put into the public Pages publisher's source workbook folder.

## Readiness for LIVE private worker finance

1. Confirm which W01–W21 originals are final and approved; the separate W01 hardened prototype and backups cannot silently replace operational originals.
2. Normalize per-worker Sheets by named columns and tabs, not positional offsets. A metadata sample showed ordinary W01/W02 have `S00` general and 28 sites, whereas W21 and W01 prototype use different tab grids and admin/transaction layouts. Avoid summing inconsistent records.
3. Verify the **new dedicated restricted identity** can access only approved source IDs. The public Pages publisher currently has access only to its reviewed catalogue workbook; do not broaden that public publisher to all worker financial records.
4. Implement private, read-only reconciliation of rows/IDs, dates, money and goods units, advances, payments and duplication; store sensitive source receipts privately.
5. Serve worker-level views only behind **authenticated staff authorization** (private API + role grants). Static public GitHub Pages, browser JavaScript and source Git cannot protect worker wages or advances.
6. Optionally publish a *non-identifying* source-health timestamp/count once approved; never treat such a timestamp as a verified balance.

A secure workforce feed has **not** been deployed by this change; only original custody and the public-safe navigation are done.

## Contractor and vendor sources

The existing `01_JP / 02 Website Sheets and Registers / 06 Finance and Purchasing / 02 Original Bills and Records` retains source contractor/vendor Excel workbooks, invoice images and candidate bill evidence. A legacy native contractor-bills Sheet exists; it is a historical reference, not automatically a live contractor balance. A separate Amrit Rawat measurements/BOQ/AOC/bills Sheet contains candidate work-package records. Cost Estimation / BOQ owns validated calculation, rate and running-bill derivations; Finance retains signed invoice/payment authority. The public Library does not copy these sources.

## UI normalization and source fidelity

- L1 `workspaces.html`: select Engineering Resources, Worker Money, Contractor Bills, Custody, Land Feasibility or Editing.
- L2 root `/`: Company → Project and fixed category list.
- L3 project: **every** project has Architecture PDF/DWG, Structural PDF/DWG, ETABS E2K/EDB, SketchUp SKP, reports, calculations, original folders and client packet sections.
- Empty states explicitly say **not registered**, not unavailable/missing. Source-only `Original Filename` distinguishes different ETABS files with identical display labels.
- Finance `money.html`: public-safe source-family guidance; its dynamic timestamp references only public `catalog.json` and cannot be mistaken for private payroll sync.

## A7 PRE/POST and version contract

A7 `A9_GIT_DRIVE_BOOTSTRAP.json` and `docs/A9_GIT_DRIVE_OPERATING_RULE.md` were consulted. Domain authority remains with its original Drive and module; GitHub versions the UI logic and this public-safe governance record. Original Google Sheets' native revision histories remain and no new worker workbook copies were created.

PRE Git main: `df14bcc68135ed32e496b68725ac0666b5ef3de7`. POST branch, PR, Actions run and tag `v1.5.0` must be provider-confirmed before release status is claimed. Independent source-file readback and private payroll reconciliation are not part of the public site deployment.
