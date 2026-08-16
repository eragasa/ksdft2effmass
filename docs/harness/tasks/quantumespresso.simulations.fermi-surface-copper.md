<!-- Generated from SQLite control state; do not edit. -->
# Copper Fermi-surface tutorial simulation

[Task index](index.md) · [Previous](./quantumespresso.simulations.dos-silicon.md) · [Next](./quantumespresso.simulations.graphene.md)

## Status

`blocked`: Planned learning-only candidate; blocked pending ONCV pseudopotential, dense-grid resource estimate, fs.x availability, and execution authorization.

## Objective

Reproduce or explicitly defer the copper SCF, 30-cubed uniform bands, and fs.x Fermi-surface tutorial as learning-only behavior.

## Parent and prerequisites

- Parent: `quantumespresso.simulations`
- Depends on: `P2`
- Depends on: `quantumespresso.simulations.integration`
- External prerequisite: `local_execution_resource_authorization`
- External prerequisite: `pseudopotential_selection_and_license`
- External prerequisite: `qe_tutorial_execution_authorization`
- External prerequisite: `simulation_input_selection`
- External prerequisite: `tutorial_source_reuse_terms_resolved`

## Authority references

- docs/computational/quantum-espresso-tutorial-simulations.md

## Authorized scope

- Preflight the copper ONCV pseudopotential, smearing, dense mesh, storage, and fs.x output.
- Run only authorized pw.x SCF/bands and fs.x stages.
- Capture snapshots, separate streams, exits, runtime, and BXSF artifacts.

## Completion criteria

- Dense-grid runtime, memory, and disk estimates precede activation.
- Every attempted stage has separate stdout/stderr and before/after snapshots.
- The disposition records transferable artifact behavior or deliberate deferral.

## Exclusions

- Copper does not become a supported project material.
- XCrySDen GUI execution is excluded.
- No Fermi-surface topology is scientifically validated.

## Historical source

No archived source.
