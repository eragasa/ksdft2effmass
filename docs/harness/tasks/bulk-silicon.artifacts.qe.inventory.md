<!-- Generated from SQLite control state; do not edit. -->
# QE tutorial artifact inventory

[Task index](index.md) · [Previous](./backend-neutral-kohn-sham-qe-architecture.md) · [Next](./bulk-silicon.records.periodic.extraction.md)

## Status

`active`: Inventory implementation complete and awaiting human review. Twenty-nine observed or explicitly missing/optional artifact records classify the actual QE tutorial input, stdout/stderr, selected pseudopotential, QEXSD metadata, native charge density, all ten k-point wavefunction files, save-directory pseudopotential copy, compact records, execution sidecars, and relevant absent optional outputs. Exact paths, sizes, SHA-256 identities, formats, structural facts, roles, completeness, retention classes, and extraction candidacy are retained under calculations/bulk-silicon/qe-example01-si-scf-davidson/. QE was not rerun; native artifacts remain external and unchanged; no successor is activated.

## Objective

Inventory and classify the actual artifacts produced by the selected QE tutorial before fixing extraction records.

## Parent and prerequisites

- Depends on: `bulk-silicon.simulation.qe.reference`

## Authority references

- calculations/bulk-silicon/qe-example01-si-scf-davidson/artifact-inventory.json
- calculations/bulk-silicon/qe-example01-si-scf-davidson/artifact-inventory.md
- docs/computational/ksdft2effmass.computational.bootstrap.md
- harness/reports/simulation-first-task-migration.md

## Authorized scope

- Inventory retained native inputs, outputs, restart data, and interface artifacts.
- Record explicit paths, sizes, checksums, formats, roles, producer identities, and retention classes.
- Identify compact, large, optional, partial, scratch, and disposable artifacts.

## Completion criteria

- Every retained tutorial artifact has an explicit disposition.
- Missing, partial, and optional outputs remain visible.
- Candidate inputs to periodic record extraction are identified with provenance.

## Exclusions

- Calculation data are not deleted, relocated, or committed to Git by this Task.
- Absence in one tutorial is not treated as universal backend absence.
- Artifact inventory does not establish scientific validity or a final public schema.

## Historical source

No archived source.
