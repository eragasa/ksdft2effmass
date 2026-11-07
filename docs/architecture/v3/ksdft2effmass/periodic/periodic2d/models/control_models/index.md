# `ksdft2effmass.periodic.periodic2d.models.control_models`

## Status and responsibility

Implemented periodic-2D control-model and represented-Hamiltonian boundary.

The package owns the dimensionless cosine control model, its exact plane-wave and
finite-difference requests, the request-bound represented-Hamiltonian operations, and
immutable correlated results. It does not own reusable plane-wave assembly, generic
lattice primitives, scientific-model acceptance, campaign policy, or continuum
convergence.

## Represented-Hamiltonian operations

- [`Periodic2DPlaneWaveHamiltonian`](Periodic2DPlaneWaveHamiltonian/index.md) binds one
  exact reciprocal-basis request and returns its finite represented matrix.
- [`Periodic2DFiniteDifferenceHamiltonian`](Periodic2DFiniteDifferenceHamiltonian/index.md)
  binds one exact coordinate-grid request and returns its finite represented matrix.

Both use the request-bound form:

```python
result = Periodic2DPlaneWaveHamiltonian(request).result()
```

The retired zero-state `...Constructor().execute(request)` owners have no compatibility
aliases. Neither operation is a `Periodic2DModel`; each constructs one finite
representation of the identified `Periodic2DCosinePotentialControlModel`.

## Source mapping

- `python/src/ksdft2effmass/periodic/periodic2d/models/control_models/cosine.py`
- `python/tests/ksdft2effmass/periodic2d/models/control_models/`
