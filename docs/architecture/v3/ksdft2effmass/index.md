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
- [`hopping_locality`](hopping_locality/index.md): the nominal locality owner and the
  prospective separation of cell-block, orbital-resolved, and MLWF-resolved peer
  diagnostics on unchanged hopping coefficients.
- [`band_equivalence_hopping_locality`](band_equivalence_hopping_locality/index.md):
  the cross-dimensional aggregate study comparing band equivalence with hopping
  locality while leaving support truncation separate.
- [`subspace_reduction`](scientific-operation-taxonomy.md#subspace-reduction),
  [`representation_equivalence`](scientific-operation-taxonomy.md#representation-equivalence),
  [`real_space_support_truncation`](scientific-operation-taxonomy.md#real-space-support-truncation),
  and [`numerical_consistency`](scientific-operation-taxonomy.md#numerical-consistency):
  nominal cross-dimensional scientific-operation ownership without merged family
  records or evidence identities.
- [`serialization`](serialization/index.md): typed scientific JSON normalization and
  final record boundaries.
- [`visualizations`](visualizations/index.md): domain-neutral authenticated projection,
  figure composition, PNG admission, and closed-inventory mechanics.
- [`models`](models/index.md): the nominal KSD scientific-model root and maintained
  dimension-neutral model families.
- [`periodic`](periodic/index.md): dimension-neutral periodic model vocabulary, the
  domain → dimension → rank nominal hierarchy, and the prospective basis-embedding and
  reciprocal-shift-sewing prerequisites for Wilson analysis.
- [`sewing`](sewing/index.md): dimension-neutral abstract sewing classes, with concrete
  reciprocal, projected-subspace, symmetry, and finite-boundary mechanics retained by
  their applicable domain owners.
- [`study`](study/index.md): reusable one-model study identity and the parallel periodic
  dimension → rank orchestration hierarchy.
- [`geometry/periodic`](geometry/periodic/index.md): prospective typed periodic lattice
  geometry, direct- and reciprocal-lattice displacements, reciprocal coordinates,
  reciprocal-space vectors, and residual-reporting coordinate recovery.
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

- [Cross-dimensional scientific-operation taxonomy](scientific-operation-taxonomy.md)
- [Component-construction and visualization audit](component-construction-and-visualization-audit.md)
- [Schematics](schematics.md)
- [Numerics](numerics.md)
- [Scientific interpretation](scientifics.md)

## Ownership boundary

Model construction remains under `ksdft2effmass.model_systems`. Reusable study
contracts may correlate one exact model without selecting diagnostics. Named diagnostic
composition and multi-model comparison remain with `experiments/` or `calculations/`.
This source mirror does not define a workflow engine, registry, or universal diagnostic
suite.

## Code mapping

- Source root: `python/src/ksdft2effmass/`
- Architecture ownership map: [`../index.md`](../index.md)

## Evidence and limitations

Implemented reduction contracts have focused software evidence. They do not establish
scientific validation, retained-result acceptance, or publication status.
