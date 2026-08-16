<!-- Generated from SQLite control state; do not edit. -->
# Bi2Se3 bulk, SOC, slab, and DOS tutorial simulation

[Task index](index.md) · [Previous](./quantumespresso.simulations.bands-silicon.md) · [Next](./quantumespresso.simulations.convergence-silicon.md)

## Status

`blocked`: Planned high-cost learning candidate; blocked pending complete inputs, relativistic pseudopotentials, 24-rank resource review, and execution authorization.

## Objective

Reproduce or explicitly defer the Bi2Se3 bulk, SOC, slab, dense-DOS, and postprocessed-bands tutorial branches as high-cost learning evidence.

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

- Preflight each branch independently, including slab size, vacuum, odd dense DOS mesh, disk, memory, and 24-rank commands.
- Run only separately approved pw.x, bands.x, and dos.x stages.
- Capture branch- and stage-level snapshots, separate streams, exits, runtimes, and artifacts.

## Completion criteria

- Bulk, SOC, slab, and DOS branches each receive an explicit execute or defer disposition.
- Every attempted stage has separate stdout/stderr and before/after snapshots.
- Known tutorial caveats about finite size and Fermi energy remain visible.

## Exclusions

- Bi2Se3 does not enter supported project scope.
- The 24-rank example is not itself resource authorization.
- No topological, surface-state, or finite-size scientific claim is validated.

## Historical source

No archived source.
