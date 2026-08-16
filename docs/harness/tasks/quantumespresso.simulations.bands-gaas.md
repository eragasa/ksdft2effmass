<!-- Generated from SQLite control state; do not edit. -->
# GaAs bandstructure tutorial simulation

[Task index](index.md) · [Previous](./quantumespresso.simulations.aluminum-metal.md) · [Next](./quantumespresso.simulations.bands-silicon.md)

## Status

`blocked`: Planned learning-only candidate outside project material scope; blocked pending complete inputs, two pseudopotentials, resources, and execution authorization.

## Objective

Reproduce or explicitly defer the GaAs relaxation, SCF, optional NSCF, bands, and bands.x tutorial workflow as compound-semiconductor learning evidence.

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

- Recover and pin every GaAs input and both pseudopotential identities.
- Run only authorized pw.x relaxation/SCF/NSCF/bands and bands.x stages.
- Capture per-stage snapshots, separate streams, exits, runtime, and artifacts.

## Completion criteria

- Version-sensitive convergence behavior and all exact inputs are recorded.
- Every attempted stage has separate stdout/stderr and before/after snapshots.
- The disposition records software lessons without adding GaAs to project scope.

## Exclusions

- GaAs does not become a supported project material.
- No tutorial bandstructure is a scientific oracle.
- The separate SOC and phonon branches are owned by their own Tasks.

## Historical source

No archived source.
