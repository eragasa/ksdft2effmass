# Periodic 3-D model-adequacy experiments

## Purpose

This subpackage groups the orthogonal isotropic and anisotropic three-dimensional stages
of the selected controlled sequence and dimension-wide deformation controls that start
from those stages. Fixed non-orthogonal 3-D families use the separate
[`periodic3d_nonorthog`](../periodic3d_nonorthog/index.md) subtree.

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
- [Band equivalence versus hopping locality](band-equivalence-versus-hopping-locality/index.md).
- [Gauge locality under a synthetic Bain strain](gauge-locality-under-synthetic-strain/index.md).
- [Anisotropic hopping-support hierarchy](anisotropic-hopping-support-hierarchy/index.md).
- The simple-cubic band-equivalence family has a substantive protocol plus a bounded,
  independently verified local development calculation; it has no immutable or retained
  result.
- The volume-preserving Bain family has bounded M0 and separately labeled M1/M2 smoke
  diagnostics plus a software-verified unimodular FCC common-cell map and strict
  packaged result schemas; typed input/verification binding, independent artifact
  verification, and convergence remain open.
- Isotropic 3-D hopping support has an active development task but no frozen protocol.
- Anisotropic 3-D has a preserved pre-version protocol and exploratory design record.

## Material distinction

Neither child is a bulk-silicon admissible-set experiment.

- No diamond-lattice basis is assumed.
- No silicon orbital, valley, spin, or Wannier basis is assumed.
- No Kohn–Sham or Wannier90 output is consumed.
- A future silicon study requires a distinct family identity and exact material provenance.

## Generalization

General full-rank geometry is outside this orthogonal subtree. The selected silicon-
inspired FCC/diamond experiment is documented separately and does not establish an
arbitrary-lattice or silicon-material API.

- PhysKit owns reusable direct, reciprocal, and metric primitives.
- Child experiments own support meaning, symmetry acceptance, channels, thresholds, and evidence.
- Triclinic support cannot be claimed from cubic and orthorhombic fixtures alone.
