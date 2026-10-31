# `ksdft2effmass` source mirror

## Purpose and status

This directory mirrors selected maintained and prospective source contracts below
`python/src/ksdft2effmass/`. Architecture v3 records current ownership and proposed
contract changes separately; a prospective page does not claim that its source symbol
or supported import already exists.

## Child map

- [`hamiltonian`](hamiltonian/index.md): Hamiltonian records, spectral spaces,
  reduction, diagnostics, and decomposition.
- [`operators`](operators/index.md): representation-independent finite-operator values
  and operations.
- [`spaces`](spaces/index.md): finite state-space and subspace contracts.
- [`analysis`](analysis/index.md): reusable analyses over already typed numerical
  objects.
- [`serialization`](serialization/index.md): typed scientific JSON normalization and
  final record boundaries.
- [`visualizations`](visualizations/index.md): domain-neutral authenticated projection,
  figure composition, PNG admission, and closed-inventory mechanics.
- [`model_systems`](model_systems/index.md): controlled physical and mathematical
  systems plus shared model-analysis verification sequencing.
- [`model_systems/piab1d`](model_systems/piab1d/index.md): the complete typed PIAB1D
  calculate, verify, and render vertical slice.
- [`model_systems/qho1d`](model_systems/qho1d/index.md): the typed QHO1D spatial-
  truncation calculate, verify, and render vertical slice.
- [`model_systems/mathieu1d`](model_systems/mathieu1d/index.md): the direct typed
  Mathieu1D finite-parent, Fourier-reduction, verification, and rendering vertical slice.
- [`model_systems/slater_koster`](model_systems/slater_koster/index.md): the reusable
  spinless homopolar diamond $sp^3s^*$ Level 1 foundation without fitting or adequacy
  claims.
- [`periodic1d`](periodic1d/index.md): the active family-by-family rewrite of
  one-dimensional periodic calculation, byte-owning verification, and authenticated
  rendering; Mathieu1D, compatible rank-one Fourier locality, and rank-two composite
  alignment are implemented, while five studies remain prospective.

Only touched source areas are mirrored in this tranche. Absence from this directory is
not an ownership reassignment.

## Package pages

- [Component-construction and visualization audit](component-construction-and-visualization-audit.md)
- [Schematics](schematics.md)
- [Numerics](numerics.md)
- [Scientific interpretation](scientifics.md)

## Ownership boundary

Model construction remains under `ksdft2effmass.model_systems`. Selection and
composition of multiple diagnostics remain with `experiments/` or `calculations/`.
This source mirror does not define a workflow engine, registry, or universal diagnostic
suite.

## Code mapping

- Source root: `python/src/ksdft2effmass/`
- Architecture ownership map: [`../index.md`](../index.md)

## Evidence and limitations

Implemented reduction contracts have focused software evidence. They do not establish
scientific validation, retained-result acceptance, or publication status.
