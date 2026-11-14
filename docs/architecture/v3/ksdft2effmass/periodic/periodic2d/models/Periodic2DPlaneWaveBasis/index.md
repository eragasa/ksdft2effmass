# `Periodic2DPlaneWaveBasis`

## Contract and identity

Frozen square finite reciprocal basis for the 2D cosine control model. It owns cutoff,
exact reciprocal-index order, represented dimension, and a structured scalar
plane-wave `basis_identity`.

## Invariants

The cutoff is a nonnegative built-in integer. Coordinates are every pair in
`[-M,M]^2`, ordered with `p` outer and `q` inner. The structured identity uses the same
order and explicit scalar `component_label = None`.

## Dependencies and flow

```text
cutoff
  -> reciprocal_indices
  -> PlaneWaveBasisCoordinate tuple
  -> PeriodicBasisIdentity
  -> plane-wave Hamiltonian request/result
```

## Serialization

The class has no standalone wire. `basis_identity` uses periodic basis schema version 1.

## Scientific boundary

It identifies finite matrix coordinates only. It does not own reciprocal geometry,
basis convergence, energy reference, gauge, embedding, or scientific acceptance.

## Mappings

Source: `python/src/ksdft2effmass/periodic/periodic2d/models/cosine.py`.
Direct tests:
`python/tests/ksdft2effmass/periodic/periodic2d/models/test__Periodic2DPlaneWaveBasis.py`.
Sphinx coverage is under the periodic control-model API.

## Provenance and evidence

Tests establish deterministic synthetic basis behavior only.

## Limitations

The fixed display identifier is descriptive and does not distinguish cutoff; coordinates
do.

## Navigation

- [`Periodic2DPlaneWaveHamiltonian`](../Periodic2DPlaneWaveHamiltonian/index.md)
- [Plane-wave coordinate contract](../../../operators/basis/PlaneWaveBasisCoordinate/index.md)
