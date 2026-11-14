# `Periodic2DPlaneWaveBlochHamiltonianModel`

## Contract and identity

Frozen finite spinless scalar plane-wave Fourier model. The existing
`basis_identifier` remains its descriptive display identifier; `basis_identity` exposes
the exact `p`-outer, `q`-inner reciprocal-index coordinate inventory.

## Invariants

The cutoff is a nonnegative built-in integer. Reciprocal indices cover the complete
square `[-M,M]^2` in deterministic order. Fourier coefficients are unique, sorted, and
conjugate paired. Identity strings and energy metadata are nonempty.

## Dependencies and flow

PhysKit provides direct/reciprocal lattices and quantities. The model constructs
`PlaneWaveBasisCoordinate` values and one `PeriodicBasisIdentity`; fiber construction
then consumes the same reciprocal-index order.

## Serialization

The model has no standalone retained wire. Its structured basis uses periodic basis
schema version 1 when a consumer serializes it.

## Scientific boundary

The model is finite numerical infrastructure. Basis identity does not establish cutoff
convergence, continuum equivalence, material validity, or provider provenance.

## Mappings

Source: `python/src/ksdft2effmass/periodic/periodic2d/models/plane_waves.py`. Direct tests:
`python/tests/ksdft2effmass/periodic/periodic2d/models/test__Periodic2DPlaneWaveBlochHamiltonianModel.py`.
Sphinx: `doc/sphinx/api/ksdft2effmass/periodic/periodic2d/models/plane_waves.rst`.

## Provenance and evidence

Tests use synthetic exact square lattices and Fourier coefficients. Evidence is software
and numerical verification only.

## Limitations

The legacy descriptive `basis_identifier` remains for current callers but does not
control structured compatibility.

## Navigation

- [Module](../index.md)
- [Plane-wave coordinate contract](../../../operators/basis/PlaneWaveBasisCoordinate/index.md)
