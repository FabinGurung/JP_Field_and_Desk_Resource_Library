# A9 historical Git import — owner workflow-permission recovery
**Dated incident:** 2026-11-08 · **source:** `FabinGurung/JP_Communication-Command-Centre-and-Resource-Hub` · **destination:** `FabinGurung/JP_Field_and_Desk_Resource_Library`

## Verified failure
[Run #42464563697](https://github.com/FabinGurung/JP_Field_and_Desk_Resource_Library/actions/runs/42464563697) was correctly invoked with `mode=import` and confirmation `IMPORT_47_BRANCHES_4_TAGS` on `main` at `87a5305306faf8a4ecffb0376eba363e86ff6dea`. The historical SHA checks, Git integrity check and 1,408-blob pattern scan passed (zero pattern findings, NOT an independent privacy certification). The first missing ref push was rejected because the ephemeral Actions `GITHUB_TOKEN` could not create or update historical `.github/workflows/daily-ops-branch-preview.yml` without **Workflows** permission. Artifact `13611207006`, ZIP SHA256 `a8ec2c90a0cfecb566f15cdecb8e8255239e7152bbf0ce25089b5821efc3cb62`, status `HOLD`. Exactly one already-correct imported branch `imported/cwo/main` exists; no imported tags or newly created refs.

## Required owner UI actions — only after repair is merged
1. In a **browser**, signed into an account allowed to write the destination repository, create a **fine-grained personal access token** using [GitHub token settings](https://github.com/settings/personal-access-tokens/new). Set resource owner `FabinGurung`, **Only select repositories** = `JP_Field_and_Desk_Resource_Library`, repository **Contents: Read and write** and **Workflows: Read and write**, shortest practical expiration. Do not give the token access to other repositories or public chat.
2. Open [Repository Actions secrets](https://github.com/FabinGurung/JP_Field_and_Desk_Resource_Library/settings/secrets/actions), choose **New repository secret**, name it exactly `A9_HISTORY_IMPORT_TOKEN`, and paste the token **there only**. No token contents go into a repository file, issue, PR, report, screenshot or conversation.
3. Open [manual import workflow](https://github.com/FabinGurung/JP_Field_and_Desk_Resource_Library/actions/workflows/a9-history-transfer.yml). Launch a **new** run (NOT re-run the prior failed job) from destination `main`: `mode=import`, `confirmation=IMPORT_47_BRANCHES_4_TAGS`. The newly patched script FAILS CLOSED if the repository secret is absent, rather than retrying using `GITHUB_TOKEN`.
4. Inspect the new run's artifact and provider refs. Expected result (not yet asserted): `IMPORTED_47_BRANCHES_4_TAGS__NO_MAIN_CHANGE`, 47 exact branch refs, four exact tag object refs (including annotated tags), original source/destination `main` intact. If rejected, stop and inspect the **sanitized** error.
5. **After successful import and verification**, revoke the short-lived PAT and delete the temporary `A9_HISTORY_IMPORT_TOKEN` repository secret. Archive PRE/POST and update the same canonical migration manifest via governed review. Do not trim either repository.

## Workflow activation risk
An owner PAT **may trigger GitHub Actions** for new pushed refs, unlike `GITHUB_TOKEN`. The 24 distinct source branch tips and their top-level `.github/workflows` inventories were inspected during recovery; examined push-trigger definitions used explicit source-branch filters (not `imported/cwo/...`). This is a dated inspection, not a proof against arbitrary workflow code/credential exposure. Avoid changing imported branches after migration; independently review workflow activation and Actions settings before operating them. The runner is constrained to `main` and is manual-only.

## Governance
- PRE: `archive/snapshot/000005_PRE_workflows_credential_gate_20261108` at `87a5305306faf8a4ecffb0376eba363e86ff6dea`.
- The original source pinned `main`, stage, previous PRE/POST branches, and destination initial `336a274c2660998041aad506a32b76d03e194e3f` must remain recoverable.
- This repair changes only the credential gate, runner token scope, unit tests and this runbook. It does **not** itself import refs.
- Independent provider-resource migration (issues, PRs, releases, secrets, environments, Pages, Drive and Slack) remains separate.

Reference: [GitHub Workflows repository permission](https://docs.github.com/en/rest/authentication/permissions-required-for-fine-grained-personal-access-tokens), [GitHub Actions secrets](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions).
