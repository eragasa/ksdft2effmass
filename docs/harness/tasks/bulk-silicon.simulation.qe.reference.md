<!-- Generated from SQLite control state; do not edit. -->
# Bulk-silicon QE tutorial reference simulation

[Task index](index.md) · [Previous](./bulk-silicon.records.periodic.extraction.md) · [Next](./bulk-silicon.tight-binding.comparison-reduction.md)

## Status

`active`: The one authorized local single-process QE 7.2 example01 silicon SCF Davidson smoke test executed exactly once and exited 0 with JOB DONE. SCF convergence was reported in 6 iterations at -15.84452726 Ry, matching the bundled tutorial reference at printed precision. Compact input, provenance, artifact identities, and result note are retained under calculations/bulk-silicon/qe-example01-si-scf-davidson/. The Task remains active pending human review; this is not production convergence, numerical validation, scientific acceptance, or successor authorization.

## Objective

Reproduce a bounded established bulk-silicon Quantum ESPRESSO tutorial calculation before fixing the project extraction and storage architecture.

## Parent and prerequisites

- Depends on: `P2`
- External prerequisite: `qe_tutorial_execution_authorization`
- External prerequisite: `silicon_tutorial_input_selection`

## Authority references

- calculations/bulk-silicon/qe-example01-si-scf-davidson/execution-provenance.json
- calculations/bulk-silicon/qe-example01-si-scf-davidson/result.md
- docs/computational/ksdft2effmass.computational.bootstrap.md
- harness/reports/simulation-first-task-migration.md

## Authorized scope

- Prepare and validate the explicitly selected tutorial input.
- Execute only the separately authorized tutorial calculation.
- Retain sanitized input, compact provenance, and external artifact identities.
- Record executable identity, resources, runtime, outputs, and execution state.

## Completion criteria

- The selected tutorial calculation has an explicit execution record.
- Sanitized input and compact provenance are retained.
- Produced external artifacts are identified for inventory.
- Failures and convergence observations are reported without scientific acceptance claims.

## Exclusions

- No execution occurs without separate explicit authorization.
- No unapproved pseudopotential, structure, cutoff, mesh, or convergence change is permitted.
- No tutorial result satisfies the production Stage 02 convergence or acceptance gates.
- Large native calculation artifacts are not committed to Git.

## Historical source

No archived source.
