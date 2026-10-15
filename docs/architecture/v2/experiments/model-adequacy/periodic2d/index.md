# Periodic 2-D model-adequacy experiments

## Purpose

This subpackage groups the two-dimensional stages of the selected dimensionality and
anisotropy sequence.

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
- [Anisotropic hopping-support hierarchy](anisotropic-hopping-support-hierarchy/index.md).
- Isotropic 2-D is the first active development stage.
- Anisotropic 2-D is the third selected stage and has no frozen protocol.

## Generalization

General full-rank two-dimensional lattice-vector support is deferred until the concrete
sequence establishes stable ownership.

- Intrinsic `2 x 2` and embedded-plane `3 x 2` geometry remain distinct representations.
- PhysKit owns reusable lattice, dual, metric, and embedding primitives.
- KSD experiments retain symmetry acceptance, support meaning, channels, thresholds, evidence, and interpretation.
- No arbitrary-lattice experiment or API is selected here.
