> **12 November 2026 source-publication addendum:** The 11 November note below is the prior baseline. The owner explicitly approved a limited public projection of the historical CLEAN Payment register. The separate original W01–W21 Money & Goods operational ledger remains disconnected. See the addendum at the end.

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

## Clarified Desk versus Field intent, 12 November 2026

User definition of **Desk Resources** is the existing published engineering-file hierarchy. User definition of **Field Resources** is the discoverability of worker Money & Goods, attendance/wages/advances, vendor bills, contractor bills, measurement of works, and associated site registers. Separate **UI tabs** are appropriate, but source-of-truth is still per-owner, not merged or rehosted: private payroll in Drive, commercial measurements/BOQ in Cost Estimation, supplier invoices in original Finance, and Library only the safe navigation/custody.

The cross-chat wage audit is supplementary and flags the claimed 2,931 extracted attendance rows versus 2,932 accepted M03 payable worker-dates, which count **different admissibility criteria**. Do not treat either number as a consolidated live attendance total without source-row and worker/date reconciliation. M01–M03 stay historical locked results; cleaned October Sheets are staged intake, not promoted payroll; person-wise attendance and worker Money & Goods are separate original collections. No source values were edited under this UI change.

## 12 Nov 2026 — Actual worker-source normalization, archive and publication

A live structural scan of all 21 original worker-site workbooks found two source types, despite their former common Money & Goods title:
- **W01–W10 (10):** 31 tabs, `S00` plus project-site tabs with 8-column `Money Entry ID | Date | Type | Amount / Value (NPR) | Details | Worker ID | Site ID | Slot`. Home summaries for all ten have **zero recorded money entries**.
- **W11–W21 (11):** 30 tabs with attendance-only `Attendance Entry ID | Date | Attendance`; no `S00` and no money ledger columns. Renamed in place to accurately say `Attendance by Project Site — ORIGINAL`, preserving permanent IDs and native formulas/history.
- **W01 v2 hardened (1):** independent 35-tab prototype with `99 Transactions`, explicit statuses/voids and five active records. The Home setup warning says its row-local Apps Script staging is not ready for broad rollout. It remains under `80_Prototype — W01 Hardened v2 — Not Final`.
- **Two older W01 backups:** preserved by a metadata-only move into `90_Archive — W01 Historical Backups — Preserve`. They are not published or deleted. The original 21 workbooks stay at the root of the original stable 24-item collection. Original folder/file IDs and Drive-native history remain; PR/release records the before/after roles.

**Clean original identified:** `Wage_List_11__PAYMENT__CLEAN_v1.1`, one of four October 2026 historical cleaning outputs. It is not a normalized Money & Goods ledger. Its tab `Payment` has exactly 958 transaction rows and a TOTAL footer. The workbook manifest says 958, 21 distinct worker identifiers. Unformatted values reconcile to NPR 3,162,016.38476, or NPR 3,162,016.38 for display. Two signed negative Contract adjustments are preserved. Source dates are interpreted from the native Google Sheets date values, including serials.

The user approved publishing selected rows from this clean historical Payment tab on 12 November 2026. An explicit read-only grant was made to **only this workbook** for the existing Google keyless Library source reader. GitHub source code never includes the transaction corpus: the source is read and validated at build time and the generated `field-payments.json` resides in the Pages artifact. It is **public**; source Google Sheet permissions do **not** carry over to that generated file. The export includes worker ID/name, date, site, category, signed NPR amount and source provenance, but excludes paid-by, narrative remarks, contact and bank information.

**Critical distinction:** Historical CLEAN Payment is now a source-backed public register, but the 21-worker Money & Goods original operational rollout, reconciled wage balances and certified payable totals remain unverified. Do not replace or merge worker-site templates solely by filename; normalize distinct grains and reconcile any overlaps explicitly.

**Production permission correction:** The source read identity for the Library's existing GitHub Actions is `jp-resource-library-reader@just-a-project-5007.iam.gserviceaccount.com`. Initial publication returned 403 because only the different `jp-pages-publisher` identity had been granted read access. Drive metadata now verifies a reader grant to the correct Library identity on just the one CLEAN Payment workbook. No other worker folders or Sheets were granted to that Library identity.
