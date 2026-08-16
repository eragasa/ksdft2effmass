<!-- Generated from SQLite control state; do not edit. -->
# Quantum ESPRESSO hands-on simulation campaign

[Task index](index.md) · [Previous](./operator-record-validation-correction.md) · [Next](./quantumespresso.simulations.aluminum-metal.md)

## Status

`inactive`: Human-requested campaign planned with no simulation active; every child remains blocked pending explicit activation and protected-execution authorization.

## Objective

Coordinate bounded, isolated reproductions or explicit deferrals of every workflow in the selected Quantum ESPRESSO hands-on tutorial category and synthesize what they reveal about execution, artifacts, extraction, and scope.

## Parent and prerequisites

- Depends on: `P2`

## Authority references

- docs/computational/quantum-espresso-tutorial-simulations.md

## Authorized scope

- Prepare source, input, executable, pseudopotential, resource, and retention preflights for each child simulation.
- Activate at most one child simulation at a time after its exact protected-execution authorization.
- Require isolated ignored workspaces, deterministic before/after snapshots, and separate standard-output and standard-error files.
- Record an executed, failed, or deliberately deferred learning disposition for every child.

## Completion criteria

- Every child simulation has a durable disposition supported by its preflight and, when run, its execution record.
- The campaign review distinguishes reusable silicon/QE/Wannier behavior from learning-only or deferred examples.
- No tutorial observation is presented as production, convergence, scientific-validation, uncertainty-quantification, or human-acceptance evidence.

## Exclusions

- This coordinating Task does not itself authorize any executable invocation.
- Automatic successor activation, concurrent simulation execution, remote execution, and production execution are prohibited.
- Large native outputs, restart data, wavefunctions, charge densities, and dense matrices are not committed to Git.
- Tutorial settings do not override accepted project scientific specifications.

## Historical source

No archived source.
