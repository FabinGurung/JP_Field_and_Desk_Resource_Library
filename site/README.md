# A9 Field & Desk Resource Library — gated presentation prototype v0.1

**Status:** SOURCE-CODE PREVIEW ONLY — NOT deployed to GitHub Pages, not approved for client distribution.  
**As-of:** 2026-11-08 NPT  
**Governing migration:** `A9-RLIB-MIG-000001` (original source Git history and 448-file snapshot retained).

## Human-facing design

- `site/index.html` — standalone responsive Field / Desk / Projects / Source & QA navigation, search and category controls, usable at mobile and desktop widths.
- `site/styles.css` — responsive layout, focus-visible keyboard styles, reduced-motion support.
- `site/app.js` — filtered search. Uses `textContent` for dynamic labels and validated HTTPS links; never inserts untrusted HTML.
- `site/catalog/public-index.v0.1.json` — derived public presentation contract, **not** another canonical document store, with **0 admitted client/project resources** while current publication authority is unresolved.
- `migration/scripts/test_gated_resource_preview.py` and `.github/workflows/a9-gated-preview-qa.yml` — fail-closed automated source, privacy, navigation and syntax QA.

## Where original information lives

- Original Communication & Web repository: [GitHub](https://github.com/FabinGurung/JP_Communication-Command-Centre-and-Resource-Hub).
- Frozen source `main` (legacy resource and project-document routes) was imported under `imported/cwo/main`.
- More recent working-source branch: `feature/daily-ops-current-work` contains the **reviewed 46-resource historical catalogue**, verified source metadata and public admission controls. These are **source references**, not automatic approval for the new library.
- Google Drive remains the original-file authority. Project IDs and public/private state derive from current subject owners and A7.
- Existing public client Pages routes and original source's Actions remain unchanged.

## Publication admission gate

Do **not** add any project/resource card until **all** of the following have been verified against current authorities: stable A7 project/document ID, file ID and revision, source-owner current publication flag, current Drive permissions, explicit reviewed public admission, permission scope and engineer approval as a separate question.

The existing [source Issue #8](https://github.com/FabinGurung/JP_Communication-Command-Centre-and-Resource-Hub/issues/8) holds Basanti `PRJ-000029 / REB-002` public-catalog admission; the referenced private source register flags `is_public=FALSE`. The retired `PRJ-000030` alias is **not** a second project. Do not copy or expose source agreement text, drawing PDFs, original Drive IDs or private links.

`site/app.js` refuses entries unless the catalogue is `PUBLIC_APPROVED_PUBLISHED`, the deployment flag is true, and each individual entry is explicitly public, permission-verified, reviewed and free of the privacy holds. Merely committing a JSON record cannot publish a file.

## Explicit release HOLDs

1. No Resource Library GitHub Pages configuration has been enabled. Static source does not equal a published website.
2. No live Google Drive user authorization or private permission verification has been conducted in this feature branch.
3. No project-specific private files or client document catalogue imported.
4. Interactive real-browser QA and mobile-device acceptance not yet performed. CI checks source and logic syntax, not screenshots or usability on real devices.
5. Navigation has no client document details by design. Initial categorization draws on the older public source schema, subject to A7 review.
6. The existing Communications website is still authoritative for original public routes until cross-links and public admission are verified.
7. This PR may be reviewed or merged as non-deployed preview source only. **Do not enable Pages or claim client release** without a separate governed deployment/QA milestone.

## No credential changes

The owner elected to retain existing PAT/Actions secrets for other work. No access token is used by this preview or its read-only CI, and no credential cleanup action is requested.

**NEXT:** Reconcile each intended public record with current Drive and Sheets identity/permission state, add explicit admission receipts to the same live catalogue ID, run desktop/mobile link/interaction QA, create PRE/POST publishing checkpoints, and only then activate public GitHub Pages and migration redirects.
