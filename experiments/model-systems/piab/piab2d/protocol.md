# PIAB2D orthogonal rectangular-box protocol

## Evidence status

This document specifies proposed work. It records no calculated result and does not
authorize retained-evidence execution.

## Scientific question

For a two-dimensional homogeneous-Dirichlet rectangular box, determine whether the
selected finite-difference representation reproduces the declared analytical mode
inventory with the expected fixed-mode refinement behavior while keeping the following
errors distinct:

1. continuum-model versus finite-difference discretization error;
2. eigensolver residual error;
3. finite retained-state compression error, when compression is applied; and
4. model-class approximation error, when a restricted operator family is fitted.

Degenerate energy levels are identified by their complete integer mode pairs and by the
associated invariant subspaces. Individual eigenvectors inside a degenerate subspace
are not compared without an explicit alignment convention.

## Initial admitted model

The first version, once frozen, is limited to:

- a finite rectangle `[0, L_x] x [0, L_y]`;
- homogeneous Dirichlet boundary conditions;
- positive finite built-in floating-point lengths and mass;
- an explicitly declared unit system;
- orthogonal Cartesian coordinates; and
- a finite declared inventory of positive mode pairs `(n_x, n_y)`.

Square and nonsquare rectangles must be separate declared cases because their
degeneracy structures differ. Numerical settings, mode inventories, and tolerances
remain to be frozen before execution.

## Owner bindings

The experiment must consume the pinned PhysKit owners:

- `projectkoios.physkit.qm.piab2d.base.Piab2D`;
- `projectkoios.physkit.qm.piab2d.tise.analytical.solution.Piab2DAnalyticalEvaluator`;
  and
- the reviewed PhysKit finite-difference owner admitted by the frozen version.

The currently pinned PhysKit oblique-grid solver can represent a diagonal direct basis,
but using it as the orthogonal finite-difference owner requires an explicit binding and
verification decision. KSD must not copy its stencil or eigensolver implementation.

## Required diagnostics

A frozen version must define and verify at least:

- deterministic energy and mode-pair ordering;
- degeneracy groups and invariant-subspace projectors;
- finite-difference energy errors for fixed mode pairs;
- observed refinement order over a frozen mesh ladder;
- algebraic eigensolver residuals;
- discrete normalization and orthogonality defects;
- exact grid shape and row-major flattening convention; and
- resource ceilings preventing accidental dense scaling.

## Artifact boundary

The experiment directory will own the protocol, request/result/verification schemas,
thin run and verification adapters, plotting composition, and evidence policy. A future
retained run will live under:

```text
calculations/model-systems/piab/piab2d/runs/<run-id>/
```

No such run currently exists.
