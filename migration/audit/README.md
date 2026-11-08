# A9/A7 Resource Library — migration evidence and remaining gates

**Canonical live migration ID:** `A9-RLIB-MIG-000001`  
**As-of:** 8 November 2026 (Asia/Kathmandu)  
**Status:** `HISTORICAL_GIT_GRAPH_IMPORTED_VERIFIED__PROVIDER_PARITY_HOLD`

## Completed and provider-verified
- Original source `main` pinned at `4eb68c004fbe8d19b83bf3b17327c853debef58a`, tree `801df26e061ef20f747f245ce62271e463b7056d`.
- 448 pinned source files copied with original blob SHA, size and mode; staging remains at `018dd5903afcfad0e00a5cc37cefbbe2d399ea10`.
- Original destination initial commit `336a274c2660998041aad506a32b76d03e194e3f` remains recoverable and ancestral to destination native `main`.
- [GitHub Actions run #42467944701](https://github.com/FabinGurung/JP_Field_and_Desk_Resource_Library/actions/runs/42467944701) passed with `IMPORTED_47_BRANCHES_4_TAGS__NO_MAIN_CHANGE`. Artifact #13612640868 digest was independently compared; 1 previously-correct ref and 50 new refs.
- Independent GitHub provider readback found **47/47 exact branch SHAs, 4/4 exact tag object SHAs** including two annotated tags, **zero missing, zero mismatched, zero extra**. Four representative source/destination commit trees and parent lists also matched. The original source working branch remains represented at `imported/cwo/feature/daily-ops-current-work`.
- Source `main` and destination native `main` were not rewritten. Imported original history is isolated in namespaced refs.
- The original destination README remains archived at `99_VERSION_ARCHIVE/migration/000001_PRE_DESTINATION_README.md` in the pinned staging snapshot.

## Authority, linked evidence and archives
- [Live migration manifest](phase1-source-snapshot.v1.json) — same original live audit ID, updated with post-import ref verification.
- [Run #5 provider readback receipt](history-import-provider-readback-42467944701.v1.json) — authenticated status, ZIP and JSON digest, source/destination SHA attestations, exact QA counts.
- Historical frozen manifest and original stage README remain available at branch `migration/phase1_communication_source_20261107`. Do **not** edit or treat historical statements like "NOT_IMPORTED" on that immutable snapshot as current status.
- PRE: `archive/snapshot/000006_PRE_history_import_closeout_20261108`. POST: `archive/snapshot/000006_POST_history_import_closeout_20261108` (to be created only after governed main merge, with provider readback).
- A7 canonical records have not been changed.

## HOLD — separate provider and product migration work
1. GitHub-managed Issues/PRs, reviews, releases and assets, workflow run history, branch/ruleset protections, GitHub Pages deployment/configuration, permissions, secrets/environments, LFS/submodules: separate evidence required.
2. A pattern-based scan checked 1,408 unique source blobs with zero findings. This is **not** comprehensive privacy, license or security certification.
3. Google Drive retains original file authority, revision history and access permissions. Drive/Slack references and client portal link behavior are separate QA.
4. The new Resource Library website is **not** yet approved/published; the old Communication & Web client portal must remain available.
5. Source Communication & Web repository may **not** be deleted, trimmed or redirected until preservation and release criteria are separately met.
6. Owner must revoke the temporary fine-grained PAT and delete repository secret `A9_HISTORY_IMPORT_TOKEN` after confirmed import QA. Never publish or copy secret values.

**NEXT:** close out owner credential cleanup, independently inventory provider metadata, design governed Resource Library website and preserve existing PRJ-000029 client URLs. No more history import runs are needed.
