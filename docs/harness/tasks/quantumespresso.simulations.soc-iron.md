<!-- Generated from SQLite control state; do not edit. -->
# Iron spin-orbit-coupling tutorial simulation

[Task index](index.md) · [Previous](./quantumespresso.simulations.soc-gaas.md) · [Next](./quantumespresso.simulations.spin-bands-nickel.md)

## Status

`blocked`: Planned learning-only candidate; blocked pending fully relativistic pseudopotential, inputs, resource estimate, and execution authorization.

## Objective

Reproduce or explicitly defer the noncollinear fully relativistic Fe SCF/bands/bands.x tutorial workflow.

## Parent and prerequisites

- Parent: `quantumespresso.simulations`
- Depends on: `P2`
- Depends on: `quantumespresso.simulations.integration`
- Depends on: `quantumespresso.simulations.magnetism-iron`
- External prerequisite: `local_execution_resource_authorization`
- External prerequisite: `pseudopotential_selection_and_license`
- External prerequisite: `qe_tutorial_execution_authorization`
- External prerequisite: `simulation_input_selection`
- External prerequisite: `tutorial_source_reuse_terms_resolved`

## Authority references

- docs/computational/quantum-espresso-tutorial-simulations.md

## Authorized scope

- Preflight relativistic representation, noncollinear settings, high cutoffs, dense mesh, and eight-rank resource request.
- Run only authorized pw.x SCF/bands and bands.x stages.
- Capture snapshots, separate streams, exits, runtime, spin-expectation artifacts, and convergence behavior.

## Completion criteria

- Relativistic pseudopotential and spin conventions are provenance-complete.
- Every attempted stage has separate stdout/stderr and before/after snapshots.
- The disposition records transferable behavior or a resource/scientific-scope deferral.

## Exclusions

- Iron SOC does not enter supported project scope.
- No tutorial spin texture or band result is scientifically validated.
- No pseudopotential substitution is made for convenience.

## Historical source

No archived source.
