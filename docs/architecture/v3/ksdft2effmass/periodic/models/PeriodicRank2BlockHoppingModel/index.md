# `PeriodicRank2BlockHoppingModel`

## Status and responsibility

Implemented shared scientific-model parent in
`python/src/ksdft2effmass/periodic/models/block_hopping.py`.

The owner fixes the public model family to ordinary periodic block hopping with retained
primitive-cell rank two. It inherits KSD scientific-model identity and composes, rather
than subclasses, a PhysKit dense or sparse block-hopping representation.

## Mandatory child contract

A concrete dimensional child supplies:

- a nonempty `model_id`;
- one exact `PeriodicModelRole`;
- spatial dimension one, two, or three;
- the matching exact PhysKit direct-lattice type, supplied through immutable
  dimensional geometry; and
- one immutable PhysKit representation whose coefficient blocks are exactly `2 x 2`.

The shared parent rejects child attempts to override `band_subspace_rank`. Its final
property returns the built-in integer two.

## Admission boundary

Admission requires complete integer-lattice support under negation and exact
coefficient Hermiticity. For the provider integer displacement
\(\mathbf n\in\mathbb Z^d\),

\[
T(-\mathbf n)=T(\mathbf n)^\dagger.
\]

The coefficient is indexed by `IntegerLatticeDisplacement` terminology, represented by
PhysKit `LatticeDisplacement`. The physical direct-lattice displacement
\(\mathbf R_{\mathbf n}=A\mathbf n\) belongs to geometry and is derived only when a
physical distance or phase requires it.

No tolerance is introduced at model construction. Floating-point Fourier output that is
Hermitian only within a tolerance remains a numerical representation until a separately
specified construction policy resolves that discrepancy.

## Ownership exclusions

The model parent owns no mesh, transform, gauge operation, locality-resolution choice,
support decision, campaign, serializer, execution identity, or scientific-acceptance
threshold. It binds ordered internal-basis identity but does not infer intracell centers,
MLWF identities, localization provenance, or a state-by-state embedding. Those values
are explicit inputs to orbital- or MLWF-resolved locality analyzers.

## Detailed documents

- [Numerics](numerics.md)
- [Schematic](schematics.md)
- [Scientific interpretation](scientifics.md)
