<!-- Generated from SQLite control state; do not edit. -->
# Periodic electronic-structure record extraction

[Task index](index.md) · [Previous](./bulk-silicon.artifacts.qe.inventory.md) · [Next](./bulk-silicon.simulation.qe.reference.md)

## Status

`blocked`: Blocked by the QE tutorial artifact inventory.

## Objective

Determine and implement the minimal periodic electronic-structure records supported by observed QE tutorial artifacts and accepted scientific conventions.

## Parent and prerequisites

- Depends on: `bulk-silicon.artifacts.qe.inventory`

## Authority references

- docs/computational/ksdft2effmass.computational.bootstrap.md
- harness/reports/simulation-first-task-migration.md

## Authorized scope

- Define immutable compact records for observed structure, sampling, spectra, occupations, energy reference, convergence observations, and artifact references.
- Keep mechanical parsing separate from semantic adaptation.
- Make units, indexing, source conventions, and provenance explicit.
- Retain large native data as external artifact references.

## Completion criteria

- Every extracted field has an identified source, unit, convention, and provenance.
- Parsing and semantic adaptation have focused software-verification evidence.
- Unsupported and unavailable information remains explicit.
- Any public record contract has synchronized schema, fixture, runtime, and documentation surfaces.

## Exclusions

- No universal DFT API or unsupported backend-neutral field is introduced.
- Kohn–Sham eigenvalues are not treated as a unique represented operator or complete many-body spectrum.
- No hidden unit, basis, gauge, geometry, or energy-zero transformation is permitted.
- Software verification does not establish scientific validation.

## Historical source

No archived source.
