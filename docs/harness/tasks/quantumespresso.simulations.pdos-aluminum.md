<!-- Generated from SQLite control state; do not edit. -->
# Aluminum projected-DOS tutorial simulation

[Task index](index.md) · [Previous](./quantumespresso.simulations.molecular-dynamics-water.md) · [Next](./quantumespresso.simulations.phonons-gaas.md)

## Status

`blocked`: Planned learning candidate after aluminum preflight; blocked pending inputs, resources, and execution authorization.

## Objective

Reproduce or explicitly defer the aluminum SCF/NSCF-to-projwfc.x projected-DOS workflow and its artifact naming behavior.

## Parent and prerequisites

- Parent: `quantumespresso.simulations`
- Depends on: `P2`
- Depends on: `quantumespresso.simulations.aluminum-metal`
- Depends on: `quantumespresso.simulations.integration`
- External prerequisite: `local_execution_resource_authorization`
- External prerequisite: `pseudopotential_selection_and_license`
- External prerequisite: `qe_tutorial_execution_authorization`
- External prerequisite: `simulation_input_selection`
- External prerequisite: `tutorial_source_reuse_terms_resolved`

## Authority references

- docs/computational/quantum-espresso-tutorial-simulations.md

## Authorized scope

- Preflight reused or independently repeated aluminum state and projection inputs.
- Run only authorized pw.x SCF/NSCF, projwfc.x, and optional sumpdos.x stages.
- Capture snapshots, separate streams, exits, runtime, and orbital-projection artifacts.

## Completion criteria

- The pseudopotential-owned projection basis and file naming are recorded.
- Every attempted stage has separate stdout/stderr and before/after snapshots.
- The disposition distinguishes parser behavior from physical interpretation.

## Exclusions

- Projected DOS is not treated as a basis-independent observable.
- Aluminum remains outside supported material scope.
- No plotting step is required for completion.

## Historical source

No archived source.
