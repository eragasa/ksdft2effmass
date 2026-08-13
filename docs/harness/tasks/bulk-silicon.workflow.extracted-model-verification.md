<!-- Generated from SQLite control state; do not edit. -->
# Extracted-model workflow verification

[Task index](index.md) · [Previous](./bulk-silicon.wannier-reference.uniform-nscf.md) · [Next](./cpn-skill-capability-audit.md)

## Status

`blocked`: Blocked by tight-binding comparison and reduction.

## Objective

Verify the composed tutorial artifact-to-record-to-model workflow and its explicit failure boundaries.

## Parent and prerequisites

- Depends on: `bulk-silicon.tight-binding.comparison-reduction`

## Authority references

- docs/computational/ksdft2effmass.computational.bootstrap.md
- harness/reports/simulation-first-task-migration.md

## Authorized scope

- Verify artifact lineage, deterministic extraction, public record round trips, fit reproducibility, Hamiltonian extraction, and comparison prerequisites.
- Verify represented failure, retry, partial-result, and restart behavior where implemented.
- Classify each retained claim as software verification, numerical verification, scientific validation, or uncertainty quantification.

## Completion criteria

- The declared software contract has focused verification.
- Applicable numerical checks pass or have an explicit disposition.
- Provenance and lineage are complete for the represented tutorial workflow.
- Limitations and missing evidence are explicit.

## Exclusions

- This Task performs no new external calculation.
- Passing software tests does not establish scientific correctness.
- Scientific validation and uncertainty quantification require separate authorization and evidence.
- Completion does not activate another Task, release, or publication.

## Historical source

No archived source.
