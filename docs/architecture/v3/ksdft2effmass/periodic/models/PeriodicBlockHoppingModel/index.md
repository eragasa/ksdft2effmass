# `PeriodicBlockHoppingModel`

## Status and responsibility

Implemented dimension-neutral finite-rank block-hopping scientific-model contract in
`python/src/ksdft2effmass/periodic/models/block_hopping.py`.

The owner fixes the represented-operator family without fixing spatial dimension or
retained rank. It composes, rather than subclasses, an immutable PhysKit dense or sparse
block-hopping representation. KSD retains scientific-model identity, role, dimensional
geometry correlation, structured periodic basis identity, retained-rank correlation,
and exact scientific-model admissibility.

## Inheritance refinement

Fixed-rank models refine their dimensional finite-rank owners:

- `Periodic1DRank2Model` refines `Periodic1DRankNModel`;
- `Periodic2DRank2Model` refines `Periodic2DRankNModel`; and
- `Periodic3DRank2Model` refines `Periodic3DRankNModel`.

The complete dimensional block-hopping models use multiple inheritance to combine that
scientific rank refinement with `PeriodicBlockHoppingModel`. There is no separate
shared dimension-neutral fixed-rank block-hopping class. Rank two is a value-level
refinement of the finite-rank contract, while block hopping is an orthogonal
representation capability.

## Mandatory concrete contract

A complete dimensional child supplies:

- a nonempty `model_id`;
- one exact `PeriodicModelRole`;
- a positive built-in `band_subspace_rank`;
- one exact dimensional structured basis identity whose coordinate count equals that
  rank;
- the matching exact PhysKit direct-lattice type, supplied through immutable
  unit-bearing dimensional geometry; and
- one immutable PhysKit representation whose coefficient-block size equals the same
  retained rank.

The three maintained rank-two children require `Periodic1DBasisIdentity`,
`Periodic2DBasisIdentity`, or `Periodic3DBasisIdentity`, respectively, each containing
exactly two ordered coordinates.

## Admission boundary

For provider displacement \(\mathbf n\in\mathbb Z^d\), admission requires complete
support under negation and exact coefficient Hermiticity,

\[
T(-\mathbf n)=T(\mathbf n)^\dagger.
\]

PhysKit `LatticeDisplacement` stores the dimensionless integer support index. The
physical translation \(\mathbf R_{\mathbf n}=A\mathbf n\) belongs to dimensional
geometry and is derived only when a physical phase or distance requires it.

No tolerance is introduced at model construction. Floating-point Fourier output that is
Hermitian only within a tolerance remains a numerical representation until a separately
specified construction policy resolves that discrepancy.

## Basis boundary

The structured basis coordinates identify coefficient-block rows and columns. They are
not inferred from the provider `basis_identifier`, model identity, retained rank,
lattice geometry, or hopping support. The provider string remains descriptive storage
and does not establish compatibility.

Wigner--Seitz representatives and ordinary-lattice displacements identify operator
support, not an intracell Hilbert-space basis. Basis identity also remains distinct from
state-space embedding, gauge, frame, energy reference, sewing, and artifact provenance.

## Ownership exclusions

This owner defines no reciprocal mesh, Fourier transform, gauge operation, locality
resolution, support decision, campaign, serializer, execution identity, validation
claim, or scientific-acceptance threshold.

## Detailed documents

- [Numerics](numerics.md)
- [Schematic](schematics.md)
- [Scientific interpretation](scientifics.md)
