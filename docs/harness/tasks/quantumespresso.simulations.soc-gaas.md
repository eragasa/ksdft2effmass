<!-- Generated from SQLite control state; do not edit. -->
# GaAs spin-orbit-coupling tutorial simulation

[Task index](index.md) · [Previous](./quantumespresso.simulations.smearing-convergence-aluminum.md) · [Next](./quantumespresso.simulations.soc-iron.md)

## Status

`blocked`: Planned learning-only candidate; blocked pending complete SOC inputs, fully relativistic pseudopotentials, resources, and execution authorization.

## Objective

Reproduce or explicitly defer the GaAs fully relativistic SCF/bands/bands.x tutorial branch.

## Parent and prerequisites

- Parent: `quantumespresso.simulations`
- Depends on: `P2`
- Depends on: `quantumespresso.simulations.bands-gaas`
- Depends on: `quantumespresso.simulations.integration`
- External prerequisite: `local_execution_resource_authorization`
- External prerequisite: `pseudopotential_selection_and_license`
- External prerequisite: `qe_tutorial_execution_authorization`
- External prerequisite: `simulation_input_selection`
- External prerequisite: `tutorial_source_reuse_terms_resolved`

## Authority references

- docs/computational/quantum-espresso-tutorial-simulations.md

## Authorized scope

- Recover and pin all GaAs SOC inputs and both relativistic pseudopotentials.
- Run only authorized pw.x SCF/bands and bands.x stages.
- Capture snapshots, separate streams, exits, runtime, and represented SOC band artifacts.

## Completion criteria

- The relationship to the non-SOC GaAs workflow is explicit and compatible comparisons are guarded.
- Every attempted stage has separate stdout/stderr and before/after snapshots.
- The disposition records workflow lessons without supporting a GaAs scientific claim.

## Exclusions

- GaAs SOC does not enter supported project scope.
- No comparison is made across unmatched pseudopotential or basis conventions.
- No tutorial band splitting is a validation oracle.

## Historical source

No archived source.
