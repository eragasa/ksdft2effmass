# Periodic 2-D model-adequacy experiments

## Purpose

This subpackage groups the orthogonal two-dimensional stages of the selected
dimensionality and anisotropy sequence and dimension-wide deformation controls that
start from those stages. Fixed non-orthogonal 2-D families use the separate
[`periodic2d_nonorthog`](../periodic2d_nonorthog/index.md) subtree.

- It owns no shared experiment result.
- It distinguishes isotropic and anisotropic scientific families.
- It preserves two-dimensional lattice and sample-role conventions at a coarse level.
- Child packages own exact parents, channels, controls, schemas, and evidence.

## Architecture bundle

The subpackage pages summarize two-dimensional method choices and delegate all
experiment-specific detail.

- [Science](science.md).
- [Numerics](numerics.md).
- [Implementation](implementation.md).
- [Schematics](schematics.md).

## Child map

The children are separate experiment families rather than versions or cases of one
experiment.

- [Isotropic hopping-shell hierarchy](hopping-shell-hierarchy/index.md).
- [Band equivalence versus hopping locality](band-equivalence-versus-hopping-locality/index.md).
- [Gauge locality under synthetic strain](gauge-locality-under-synthetic-strain/index.md).
- [Anisotropic hopping-support hierarchy](anisotropic-hopping-support-hierarchy/index.md).
- The square-lattice band-equivalence family has a substantive protocol plus a bounded,
  independently verified development calculation; it has no immutable or retained
  result.
- The area-preserving rhombic strain family has bounded M0 and separately labeled M1/M2
  smoke diagnostics with strict packaged result schemas; typed input/verification
  binding, independent artifact verification, and convergence remain open.
- Isotropic 2-D hopping-shell adequacy is the first active dimensional-ladder stage.
- Anisotropic 2-D is the third selected stage and has no frozen protocol.

## Generalization

General full-rank geometry is outside this orthogonal subtree. The selected graphene-
inspired triangular/honeycomb experiment is documented separately and does not
establish an arbitrary-lattice or graphene-material API.

- Intrinsic `2 x 2` and embedded-plane `3 x 2` geometry remain distinct representations.
- PhysKit owns reusable lattice, dual, metric, and embedding primitives.
- KSD experiments retain symmetry acceptance, support meaning, channels, thresholds, evidence, and interpretation.
