# Periodic 3-D model-adequacy experiments

## Purpose

This subpackage groups the isotropic and anisotropic three-dimensional stages of the
selected controlled sequence.

- Isotropic 3-D introduces a third periodic coordinate while preserving cubic axis-permutation symmetry.
- Anisotropic 3-D later combines three dimensions with removed axis-permutation equivalence.
- Both are synthetic scalar families rather than silicon models.
- Each child owns an independent experiment identity and protocol.

## Architecture bundle

The subpackage pages summarize three-dimensional method choices and delegate exact
controls to the children.

- [Science](science.md).
- [Numerics](numerics.md).
- [Implementation](implementation.md).
- [Schematics](schematics.md).
- [Sequence ladder](../dimensional-anisotropy-ladder.md).

## Child map

The children remain separate families rather than versions or threshold cases.

- [Isotropic hopping-support hierarchy](isotropic-hopping-support-hierarchy/index.md).
- [Anisotropic hopping-support hierarchy](anisotropic-hopping-support-hierarchy/index.md).
- Isotropic 3-D has an active development task but no frozen protocol.
- Anisotropic 3-D has a preserved pre-version protocol and exploratory design record.

## Material distinction

Neither child is a bulk-silicon admissible-set experiment.

- No diamond-lattice basis is assumed.
- No silicon orbital, valley, spin, or Wannier basis is assumed.
- No Kohn–Sham or Wannier90 output is consumed.
- A future silicon study requires a distinct family identity and exact material provenance.

## Generalization

General full-rank three-dimensional lattice-vector support is deferred until the
concrete sequence establishes stable ownership.

- PhysKit owns reusable direct, reciprocal, and metric primitives.
- Child experiments own support meaning, symmetry acceptance, channels, thresholds, and evidence.
- Triclinic support cannot be claimed from cubic and orthorhombic fixtures alone.
- No arbitrary-lattice API is selected here.
