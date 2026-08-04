# Task F — Quantum ESPRESSO execution boundary

Status: prospectively superseded for workflow sequencing by P2/P5/P6; never launched

The immutable execution/convergence content remains preserved. See `.pi/tasks/backend-neutral-cpn-workflow-architecture.md`.

## Objective

Implement the explicit QE process boundary and synthetic execution infrastructure while preserving the separate states of process completion, SCF convergence, numerical acceptance, and scientific validation.

## Prerequisites

- human acceptance of Tasks B, D, and E.

## Owned objects and actions

- execution configuration DataObjects;
- `QuantumEspressoExecutionResult` ResultObject;
- concrete runner/executor composition;
- `SCFConvergenceResult` and convergence analyzer;
- artifact classification and sealed-output handoff;
- synthetic command-executor fixtures.

A generic DFT backend protocol is not approved. Scheduler submission and real QE execution are excluded until a separate production authorization checkpoint records machine/cluster, executable, pseudopotential, resources, roots, runtime, retained outputs, and transfer policy.

## Completion sequence

Implementation, software-verification tests, documentation, independent read-only review, parent verification, and human acceptance are required. Acceptance completes the synthetic execution/parser component of G01a but does not itself pass G01a or authorize G02 production.
