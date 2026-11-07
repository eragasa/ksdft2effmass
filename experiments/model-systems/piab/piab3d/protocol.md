# PIAB3D orthogonal rectangular-cuboid protocol

## Evidence status

This document specifies proposed work. It records no calculated result and does not
authorize retained-evidence execution.

## Scientific question

For a three-dimensional homogeneous-Dirichlet rectangular cuboid, determine whether a
selected sparse finite representation reproduces a declared analytical mode inventory
for fixed low modes while preserving explicit degeneracy, state-space, flattening, and
resource contracts.

Continuum-model, spatial-discretization, eigensolver, retained-space, and restricted
model-class errors remain separate.

## Initial admitted model

The first version, once frozen, is limited to:

- a finite cuboid `[0, L_x] x [0, L_y] x [0, L_z]`;
- homogeneous Dirichlet boundary conditions;
- positive finite built-in floating-point lengths and mass;
- an explicitly declared unit system;
- orthogonal Cartesian coordinates; and
- a finite declared inventory of positive mode triples `(n_x, n_y, n_z)`.

Cubic and noncubic cases must be declared separately because their degeneracy
structures differ. Full dense eigensystems are outside the intended campaign.

## Owner bindings and blocker

The analytical tranche must consume:

- `projectkoios.physkit.qm.piab3d.base.Piab3D`; and
- `projectkoios.physkit.qm.piab3d.tise.analytical.solution.Piab3DAnalyticalEvaluator`.

The pinned PhysKit revision does not expose a reviewed PIAB3D finite-difference solver.
Reusable three-dimensional sparse-grid construction and solution therefore belong in
PhysKit before KSD can bind a numerical refinement experiment. KSD must not introduce a
duplicate reusable solver inside this experiment.

## Required diagnostics

A frozen numerical version must define and verify at least:

- deterministic energy and mode-triple ordering;
- degeneracy groups and invariant-subspace projectors;
- fixed-mode energy errors over a frozen mesh ladder;
- observed refinement order;
- algebraic residuals, normalization, and orthogonality defects;
- exact three-dimensional shape and row-major flattening convention;
- selected-eigenpair policy; and
- hard memory, state-count, and runtime ceilings.

## Artifact boundary

The experiment directory will own the protocol, request/result/verification schemas,
thin adapters, plotting composition, and evidence policy. A future retained run will
live under:

```text
calculations/model-systems/piab/piab3d/runs/<run-id>/
```

No such run currently exists.
