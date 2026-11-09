# A9 Field & Desk — public interface

The homepage is a company-first reviewed directory. The static [editing guide](editing.html) explains source tabs, provider authority and permitted edits. The independent [source custody portal](operations.html) is **dated static governance**, not a live payroll view.

All values for `catalog.json` and `document-packets.json` are **derived by GitHub Actions** from the one existing owner workbook. They are never manually edited. The generator reads `project_resources`, `client_document_packets` and `resource_source_readback` (double readback of values) using the existing keyless Sheets read-only Workload Identity Federation configuration.

Project packet-only records without an explicit Company field are shown in **Company confirmation required**. They are not reassigned by `REB` code heuristics; the source owner must approve and add the Company value.

See [source matrix](../docs/governance/PAGES_SOURCE_MATRIX.md), [original publication/policy history](https://github.com/FabinGurung/JP_Field_and_Desk_Resource_Library/releases/tag/v1.1.0), and [current Pages Actions](../.github/workflows/resource-library-pages.yml). The Basanti A/B/C project-document portal retains its preexisting path and Google Drive original links.

The publisher includes only explicit site assets; `site/catalog/public-index.v0.1.json` is a historical **unpublished** preview and must not be used as current source data. Source-file and payroll contents remain outside the public Pages artifact.
