# Field & Desk Resource Library

This repository owns Field Resources, Desk Resources and the A/B/C client document portal. Use the [Project Resources owner workbook](https://docs.google.com/spreadsheets/d/1e019Jac4lDveZ2glXMph4RLHivqPFEachbcNi-R1DZk/edit) to edit catalogue entries. The Operations website consumes its own source Sheets.

- `project_resources` carries reviewed Field and Desk entries.
- `client_document_packets` carries the project registers and each English, Nepali or original PDF pointer.
- `resource_source_readback` records the matching Drive file identity, last observed modification date, access status and admission basis. Confirm a changed Drive ID with a corresponding readback before marking its row Publish. Links for legacy records retain their existing Drive permissions.
- GitHub Actions reads the three tabs twice, projects public-safe fields into a temporary Pages artifact and deploys only the explicit website files and projections. Drive originals stay in Drive. The private source workbook is never served as a web asset.
- PR QA runs offline with synthetic input. Real publication requires the main workflow's keyless Sheets connection. The earlier v0.1 preview is recoverable at `archive/snapshot/000009_PRE_library_sheets_publication_20261109`.

## First deployment

1. In [Settings → Pages](https://github.com/FabinGurung/JP_Field_and_Desk_Resource_Library/settings/pages), select **GitHub Actions** as the publishing source.
2. Configure the repository Actions variables `JP_GOOGLE_WORKLOAD_IDENTITY_PROVIDER` and `JP_GOOGLE_SERVICE_ACCOUNT` for a main-only Google federation. Give the service account Viewer access to the Project Resources workbook. The job requests the Sheets read-only OAuth scope.
3. Run [Resource Library from Google Sheets](https://github.com/FabinGurung/JP_Field_and_Desk_Resource_Library/actions/workflows/resource-library-pages.yml) on main with **publish** selected. Check the catalogue and the `PRJ-000029` portal on the returned Pages URL. Check both languages and access as a permitted client. Scheduled refreshes run hourly once enabled.

The original Basanti public landing page listed six PDFs for review. Its corresponding six links are re-used; Drive enforces the same named-user access. The worksheet authorization publishes the listing and has no effect on contract execution, material acceptance or drawing approval.
