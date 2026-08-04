# Task G — Direct spectral tight-binding target fan-out

Status: prospectively superseded for workflow sequencing by P7; never launched

The direct spectral-TB content remains preserved. See `.pi/tasks/backend-neutral-cpn-workflow-architecture.md`.

## Objective

Implement neutral target construction for direct spectral DFT-to-TB fitting.

## Prerequisites

- human acceptance of Tasks C and E.

## Owned objects and actions

- immutable target specifications and target ResultObjects;
- `TightBindingTargetBuilder`;
- explicit training and withheld-validation partitions;
- retained parent dataset/manifest identities;
- spectral, band-edge, and separately validated observable targets.

This task does not fit a TB model unless separately authorized, parse QE, reconstruct operators from eigenvalues, call the branch operator fitting, or claim a common operator representation.

## Completion sequence

Implementation, software and applicable numerical verification, documentation, independent read-only review, parent verification, and human acceptance are required. It is independently bounded and not bundled with the Wannier branch.
