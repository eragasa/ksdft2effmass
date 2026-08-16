<!-- Generated from SQLite control state; do not edit. -->
# FeO DFT+U tutorial simulation

[Task index](index.md) · [Previous](./quantumespresso.simulations.convergence-silicon.md) · [Next](./quantumespresso.simulations.dielectric-silicon.md)

## Status

`blocked`: Planned high-risk learning candidate; blocked pending QE-version syntax, inputs, pseudopotentials, Hubbard policy, resources, and execution authorization.

## Objective

Reproduce or explicitly defer the FeO DFT, DFT+U, projected-DOS, and optional hp.x self-consistent-Hubbard workflow as learning-only behavior.

## Parent and prerequisites

- Parent: `quantumespresso.simulations`
- Depends on: `P2`
- Depends on: `quantumespresso.simulations.integration`
- External prerequisite: `dftu_hubbard_parameter_policy`
- External prerequisite: `local_execution_resource_authorization`
- External prerequisite: `pseudopotential_selection_and_license`
- External prerequisite: `qe_tutorial_execution_authorization`
- External prerequisite: `simulation_input_selection`
- External prerequisite: `tutorial_source_reuse_terms_resolved`

## Authority references

- docs/computational/quantum-espresso-tutorial-simulations.md

## Authorized scope

- Resolve QE pre-7.1 versus 7.1-plus Hubbard syntax and exact FeO inputs.
- Run only individually approved pw.x, projwfc.x, and optional hp.x stages.
- Capture iteration-level snapshots, separate streams, exits, runtimes, Hubbard artifacts, and local-minimum observations.

## Completion criteria

- The baseline, DFT+U, and hp.x branches each receive an explicit run or defer disposition.
- Every attempted stage has separate stdout/stderr and before/after snapshots.
- Reported Hubbard values remain tutorial outputs tied to exact pseudopotentials and manifolds.

## Exclusions

- The hp.x iteration is deferred by default pending a bounded stopping rule and resource estimate.
- FeO and DFT+U do not enter supported project scope.
- No Hubbard parameter or insulating-state claim is scientifically accepted.

## Historical source

No archived source.
