<!-- Generated from SQLite control state; do not edit. -->
# QE–Wannier90 tutorial bridge

[Task index](index.md) · [Previous](./bulk-silicon.tight-binding.direct-spectral.fitting.md) · [Next](./bulk-silicon.tight-binding.wannier.extraction.md)

## Status

`superseded`: Never-launched tutorial-only QE–Wannier90 bridge identity, superseded by the inactive production Stage 03 Task bulk-silicon.wannier-reference.interface. Supersession does not activate the replacement or authorize execution.

## Objective

Define the tutorial QE–Wannier90 input and artifact bridge from observed QE artifacts.

## Parent and prerequisites

- Depends on: `bulk-silicon.artifacts.qe.inventory`
- Depends on: `bulk-silicon.records.periodic.extraction`
- External prerequisite: `wannier_tutorial_interface_selection`
- Superseded by: `bulk-silicon.wannier-reference.interface`

## Authority references

- docs/computational/ksdft2effmass.computational.bootstrap.md
- harness/reports/simulation-first-task-migration.md

## Authorized scope

- Identify the parent calculation and required child sampling.
- Represent `.nnkp`, `.amn`, `.mmn`, `.eig`, and accepted optional artifacts as typed external references.
- Retain bands, windows, projections, grid, and parent-child lineage as explicit inputs.

## Completion criteria

- Required and optional bridge artifacts are distinguished.
- The exact parent and child lineage is retained.
- Bands, projections, windows, and grids have explicit dispositions.
- The bridge contract is reproducible without executing Wannier90.

## Exclusions

- This Task does not execute Wannier90 or implement localization.
- It does not treat `projwfc.x` output as `.amn`.
- It does not silently select projections, windows, bands, or grids.
- Backend filenames do not become neutral periodic-record fields.

## Historical source

No archived source.
