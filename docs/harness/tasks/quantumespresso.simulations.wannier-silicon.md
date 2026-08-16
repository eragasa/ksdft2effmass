<!-- Generated from SQLite control state; do not edit. -->
# Silicon QE-Wannier90 tutorial simulation

[Task index](index.md) · [Previous](./quantumespresso.simulations.structure-optimization-silicon.md)

## Status

`blocked`: Planned candidate; blocked pending complete inputs, QE/Wannier interface versions, pseudopotential, resource estimate, and separate Wannier execution authorization.

## Objective

Reproduce or explicitly defer the pinned silicon QE-to-Wannier90 SCF, NSCF, interface, localization, and represented-band workflow.

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
- External prerequisite: `wannier_tutorial_execution_authorization`

## Authority references

- docs/computational/quantum-espresso-tutorial-simulations.md

## Authorized scope

- Recover and pin all abbreviated page inputs, kmesh.pl output, QE version, Wannier90 version, and pw2wannier90 ownership.
- Run only authorized pw.x, kmesh.pl, wannier90.x preprocessing/localization, and pw2wannier90.x stages.
- Capture per-stage snapshots, separate streams, exits, runtimes, interface artifacts, and represented Wannier outputs.

## Completion criteria

- Every omitted input and interface convention is explicit or causes deliberate deferral.
- Every attempted stage has separate stdout/stderr and before/after snapshots.
- The disposition distinguishes localization, basis transformation, representation, and truncation.

## Exclusions

- Wannierization alone is not described as low-rank approximation.
- No represented Hamiltonian is compared before basis, gauge, energy, unit, and geometry alignment.
- No execution occurs under QE-only authorization.

## Historical source

No archived source.
