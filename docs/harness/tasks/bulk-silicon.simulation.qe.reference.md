<!-- Generated from SQLite control state; do not edit. -->
# Bulk-silicon QE tutorial reference simulation

[Task index](index.md) · [Previous](./bulk-silicon.records.periodic.extraction.md) · [Next](./bulk-silicon.tight-binding.comparison-reduction.md)

## Status

`closed_human_accepted_pass`: Human-accepted and completed as a successful tutorial smoke-test reproduction. Accepted claim: Quantum ESPRESSO 7.2 reproduced the selected official example01 silicon Davidson SCF result using the identified legacy pseudopotential, with retained compact provenance and externally retained native artifacts. Recorded observations: total energy -15.84452726 Ry; 6 SCF iterations; bundled-reference difference 0.00000000 Ry at printed precision; exit status 0; JOB DONE present; pseudopotential SHA-256 e8d933754cd51c6bb4b2a809151f89e0647e53d878bab88d26e1b5a5d68d5217; executable SHA-256 6e8720e74cbafa7c7f07ee61ec6f5944c15d59bffa8ee8423fae14364f21c8ca. The exact IEEE warning remains observed and unresolved. No production, validation, UQ, Stage 02, suitability, or transferability claim is accepted.

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
