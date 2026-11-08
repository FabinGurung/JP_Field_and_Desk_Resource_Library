# A9 Phase 2 — GitHub provider-resource preservation inventory

**One canonical migration ID:** `A9-RLIB-MIG-000001`  
**Dated snapshot:** 2026-11-08 · Asia/Kathmandu  
**Role:** Read-only source-provider metadata pointers and QA evidence. **Not** a second operational Issues/PRs/Releases authority.

## Current preservation evidence

| Source GitHub resource | Dated inventory | Copy status |
| --- | ---: | --- |
| Standalone Issues | **4** | Source issue IDs, URLs, titles, status, times, comment counts indexed; discussion bodies and events remain at original GitHub provider |
| Pull requests | **21** (20 merged, 1 closed unmerged) | Original PR IDs/URLs/head and base SHAs indexed; **21/21** head commit objects verified reachable in the imported destination Git graph. Provider discussions, reviews and approvals remain at source |
| Releases | **4** | Tag names, original release URLs and publication metadata indexed. **Zero attached release assets**. Release notes remain at original provider; imported Git tag objects are preserved |
| Actions execution runs | **1,915** | All 1,915 run IDs indexed in four JSONL files, unique and ordered with source browser URLs. **No** historical logs, jobs, artifact bytes or execution state are recreated |
| Branch protection/rulesets | 0 protected among 47 branch-list entries; 0 reported rulesets | Read-only observation, **not** proof of full administrative configuration parity |
| GitHub Pages | Source `has_pages=true`; destination `has_pages=false` | Existing Communication website remains source; no new Resource Library Pages publication claimed |

## Evidence files

- [Source Issues/PRs/Releases and provider status](source-provider-metadata.v1.json)
- [Actions runs 1–500](source-actions-runs-0001-0500.jsonl)
- [Actions runs 501–1,000](source-actions-runs-0501-1000.jsonl)
- [Actions runs 1,001–1,500](source-actions-runs-1001-1500.jsonl)
- [Actions runs 1,501–1,915](source-actions-runs-1501-1915.jsonl)
- [Canonical migration manifest](../../audit/phase1-source-snapshot.v1.json) (same audit ID; do not treat the pinned staging copy as live)
- [Git history import receipt](../../audit/history-import-provider-readback-42467944701.v1.json)

**Provider readback + automation:** `migration/scripts/test_provider_snapshot.py` and `.github/workflows/a9-provider-inventory-qa.yml` check snapshot cardinality, run ID uniqueness, source links, source commit refs, release/tag references and fail-closed privacy controls. The tests need no PAT, provider session, or network.

## Operational holds — not overwritten by this index

1. [Source Issue #8 — PRJ-000029 Basanti](https://github.com/FabinGurung/JP_Communication-Command-Centre-and-Resource-Hub/issues/8) explicitly keeps current public-catalog admission **on HOLD** with the referenced private register `is_public=FALSE`. Do not automatically display restricted agreements, source drawings or private Drive links on new public Pages; preserve the original source URLs and obtain a reviewed publication authorization first.
2. [Source Issue #23](https://github.com/FabinGurung/JP_Communication-Command-Centre-and-Resource-Hub/issues/23) remains open for progress-evidence reconciliation. Do not convert pending historical records into verified construction completion.
3. [Source Issue #24](https://github.com/FabinGurung/JP_Communication-Command-Centre-and-Resource-Hub/issues/24) remains open for default-branch hourly Sheets-to-Pages dispatcher; do not assume it is enabled by this migration.
4. [Source Issue #25](https://github.com/FabinGurung/JP_Communication-Command-Centre-and-Resource-Hub/issues/25) remains open for finance custody; original Google Sheets/Drive authority belongs to the other designated workstream.
5. GitHub issue/PR conversations, reviews/approvals, release notes, Actions logs/artifacts, settings, environment secrets, permission matrices, Pages settings, LFS/submodules and external Drive/Slack links remain in their original providers. This repository records **source references**, not replacement provider objects.
6. A source `main` tree has no root `.gitmodules` or `.gitattributes`, but historical branch/object-wide Git LFS and submodule audit is not claimed complete.
7. Owner instructed retention of the existing fine-grained PAT and repository Actions secret. No secret management or access-policy mutations are performed by this workstream.

## Phase 2 and next engineering actions

- **DONE:** Git history refs, original content snapshots and preservation of original destination commit; see original migration manifest.
- **INDEXED:** Date-scoped source provider metadata for all currently reported Issues/PRs/releases and 1,915 historical Actions runs.
- **NOT MIGRATED:** Provider-managed conversations/release objects/run execution histories; source remains authority. No need to recreate historical comments under new numeric IDs.
- **NEXT:** Plan Resource Library catalogue and safe read-only client navigation against the original Drive source IDs. Gate all public data by explicit current authority. Keep Communication & Web live; no broad merge, trim, force-push, or duplicate canonical ID. Use a separate governed preview/QA before enabling GitHub Pages.

This snapshot is a historical observation. New source events after 2026-11-08 must be captured as new dated snapshots; do not silently edit this dated evidence.
