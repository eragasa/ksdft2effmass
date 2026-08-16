<!-- Generated from SQLite control state; do not edit. -->
# Silicon k-resolved DOS tutorial simulation

[Task index](index.md) · [Previous](./quantumespresso.simulations.jdos-silicon.md) · [Next](./quantumespresso.simulations.magnetism-iron.md)

## Status

`blocked`: Planned candidate; blocked pending complete source inputs, pseudopotential, resources, and execution authorization.

## Objective

Reproduce or explicitly defer the silicon bands-to-projwfc.x k-resolved DOS workflow and inventory its projection artifacts.

## Parent and prerequisites

- Parent: `quantumespresso.simulations`
- Depends on: `P2`
- Depends on: `quantumespresso.simulations.bands-silicon`
- Depends on: `quantumespresso.simulations.integration`
- External prerequisite: `local_execution_resource_authorization`
- External prerequisite: `pseudopotential_selection_and_license`
- External prerequisite: `qe_tutorial_execution_authorization`
- External prerequisite: `simulation_input_selection`
- External prerequisite: `tutorial_source_reuse_terms_resolved`

## Authority references

- docs/computational/quantum-espresso-tutorial-simulations.md

## Authorized scope

- Resolve the page's externally referenced SCF and doubled-path inputs before activation.
- Run only authorized pw.x SCF/bands and projwfc.x stages.
- Capture snapshots, separate streams, exits, runtime, and k-resolved projection outputs.

## Completion criteria

- All omitted inputs are recovered and pinned or the Task is explicitly deferred.
- Every attempted stage has separate stdout/stderr and before/after snapshots.
- The disposition records projection and indexing conventions without scientific-validation claims.

## Exclusions

- No input is inferred silently from a different tutorial version.
- No orbital projection is treated as basis independent.
- No plotting output is required.

## Historical source

No archived source.
