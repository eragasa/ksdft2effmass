<!-- Generated from SQLite control state; do not edit. -->
# Magnetic iron tutorial simulation

[Task index](index.md) · [Previous](./quantumespresso.simulations.kresolved-dos-silicon.md) · [Next](./quantumespresso.simulations.molecular-dynamics-water.md)

## Status

`blocked`: Planned learning-only candidate; blocked pending FM/AFM inputs, ultrasoft pseudopotential, optional PWTK decision, resources, and execution authorization.

## Objective

Reproduce or explicitly defer the FM/AFM iron, optional cutoff-dual sweeps, DOS, and projected-DOS tutorial as magnetic-workflow learning evidence.

## Parent and prerequisites

- Parent: `quantumespresso.simulations`
- Depends on: `P2`
- Depends on: `quantumespresso.simulations.integration`
- External prerequisite: `local_execution_resource_authorization`
- External prerequisite: `pseudopotential_selection_and_license`
- External prerequisite: `pwtk_tool_selection_and_authorization`
- External prerequisite: `qe_tutorial_execution_authorization`
- External prerequisite: `simulation_input_selection`
- External prerequisite: `tutorial_source_reuse_terms_resolved`

## Authority references

- docs/computational/quantum-espresso-tutorial-simulations.md

## Authorized scope

- Preflight distinct FM/AFM structures, starting magnetizations, ultrasoft cutoff ratios, and sweep cost.
- Run only separately approved pw.x, dos.x, projwfc.x, and optional PWTK stages.
- Capture snapshots, separate streams, exits, runtimes, and magnetic/DOS artifacts.

## Completion criteria

- Every magnetic initial condition and attempted sweep point is explicit.
- Every attempted stage has separate stdout/stderr and before/after snapshots.
- The costly sweep receives an execute or defer disposition before launch.

## Exclusions

- Iron does not become a supported project material.
- PWTK use is separately authorized and may be deferred.
- Ground-state or magnetic-order claims are not scientifically validated.

## Historical source

No archived source.
