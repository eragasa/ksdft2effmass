<!-- Generated from SQLite control state; do not edit. -->
# Silicon structure-optimization tutorial simulation

[Task index](index.md) · [Previous](./quantumespresso.simulations.spin-bands-nickel.md) · [Next](./quantumespresso.simulations.wannier-silicon.md)

## Status

`blocked`: Planned candidate; blocked pending exact VC-relax input, pseudopotential, resources, and execution authorization.

## Objective

Reproduce or explicitly defer the silicon pw.x variable-cell relaxation tutorial and observe its native structural outputs and failure boundaries.

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

- Preflight the fixed-position VC-relax input and cell_dofree convention.
- Run only the authorized pw.x VC-relax stage.
- Capture final-coordinate artifacts, snapshots, streams, exit state, and runtime.

## Completion criteria

- Input and structure conventions are explicit and provenance-complete.
- Any attempted relaxation has distinct stdout/stderr and before/after snapshots.
- Observed final coordinates are labeled tutorial results rather than accepted geometry.

## Exclusions

- No tutorial-relaxed geometry is promoted to a project structure.
- No convergence tolerance is changed without separate authority.
- No production or remote execution occurs.

## Historical source

No archived source.
