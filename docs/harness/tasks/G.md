<!-- Generated from SQLite control state; do not edit. -->
# Task G — Direct spectral tight-binding target fan-out

[Task index](index.md) · [Previous](./F.md) · [Next](./H.md)

## Status

`superseded`: prospectively superseded for workflow sequencing by P7; never launched

## Objective

Implement neutral target construction for direct spectral DFT-to-TB fitting.

## Parent and prerequisites

None.

## Authority references

- harness/archive/task-control-v1/tasks/G.md

## Authorized scope

- immutable target specifications and target ResultObjects;
- `TightBindingTargetBuilder`;
- explicit training and withheld-validation partitions;
- retained parent dataset/manifest identities;
- spectral, band-edge, and separately validated observable targets.

## Completion criteria

- Implementation, software and applicable numerical verification, documentation, independent read-only review, parent verification, and human acceptance are required. It is independently bounded and not bundled with the Wannier branch.

## Exclusions

- This task does not fit a TB model unless separately authorized, parse QE, reconstruct operators from eigenvalues, call the branch operator fitting, or claim a common operator representation.

## Historical source

`harness/archive/task-control-v1/tasks/G.md` (`sha256:8944817cb30b8caa9025cdebe2e54ff860b12fd9dc769a65aee44dffcf761f98`)
