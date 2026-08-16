<!-- Generated from SQLite control state; do not edit. -->
# Silicon dielectric-function tutorial simulation

[Task index](index.md) · [Previous](./quantumespresso.simulations.dftu-feo.md) · [Next](./quantumespresso.simulations.dos-silicon.md)

## Status

`blocked`: Planned candidate; blocked pending norm-conserving pseudopotential, exact full-grid inputs, epsilon.x availability, resources, and execution authorization.

## Objective

Reproduce or explicitly defer the silicon full-k-grid SCF and epsilon.x dielectric-function tutorial workflow.

## Parent and prerequisites

- Parent: `quantumespresso.simulations`
- Depends on: `P2`
- Depends on: `quantumespresso.simulations.integration`
- Depends on: `quantumespresso.simulations.scf-silicon`
- External prerequisite: `local_execution_resource_authorization`
- External prerequisite: `pseudopotential_selection_and_license`
- External prerequisite: `qe_tutorial_execution_authorization`
- External prerequisite: `simulation_input_selection`
- External prerequisite: `tutorial_source_reuse_terms_resolved`

## Authority references

- docs/computational/quantum-espresso-tutorial-simulations.md

## Authorized scope

- Preflight norm-conserving pseudopotential compatibility, no-symmetry grid, band count, broadening, and energy grid.
- Run only authorized pw.x SCF/optional NSCF and epsilon.x dielectric stages.
- Capture snapshots, separate streams, exits, runtime, and epsilon data artifacts.

## Completion criteria

- The exact grid, symmetry, band, broadening, and pseudopotential conditions are recorded.
- Every attempted stage has separate stdout/stderr and before/after snapshots.
- The disposition labels results unconverged tutorial behavior.

## Exclusions

- No ultrasoft pseudopotential is substituted into epsilon.x.
- No dielectric spectrum is scientifically validated or treated as converged.
- No source-code recompilation to raise k-point limits is authorized.

## Historical source

No archived source.
