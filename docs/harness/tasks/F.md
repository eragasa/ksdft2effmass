<!-- Generated from SQLite control state; do not edit. -->
# Task F — Quantum ESPRESSO execution boundary

[Task index](index.md) · [Previous](./EVIDENCE-DOC-1.md) · [Next](./G.md)

## Status

`superseded`: prospectively superseded for workflow sequencing by P2/P5/P6; never launched

## Objective

Implement the explicit QE process boundary and synthetic execution infrastructure while preserving the separate states of process completion, SCF convergence, numerical acceptance, and scientific validation.

## Parent and prerequisites

None.

## Authority references

- harness/archive/task-control-v1/tasks/F.md

## Authorized scope

- execution configuration DataObjects;
- `QuantumEspressoExecutionResult` ResultObject;
- concrete runner/executor composition;
- `SCFConvergenceResult` and convergence analyzer;
- artifact classification and sealed-output handoff;
- synthetic command-executor fixtures.

## Completion criteria

- Implementation, software-verification tests, documentation, independent read-only review, parent verification, and human acceptance are required. Acceptance completes the synthetic execution/parser component of G01a but does not itself pass G01a or authorize G02 production.

## Exclusions

- A generic DFT backend protocol is not approved. Scheduler submission and real QE execution are excluded until a separate production authorization checkpoint records machine/cluster, executable, pseudopotential, resources, roots, runtime, retained outputs, and transfer policy.

## Historical source

`harness/archive/task-control-v1/tasks/F.md` (`sha256:e76394dc83c830fd347177b8663afb68d7ebc9967e03d538c2d8dfc3d5f026a4`)
