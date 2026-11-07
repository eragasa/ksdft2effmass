# `ksdft2effmass.periodic.periodic2d.models`

Implemented periodic-2D nominal model ownership. `Periodic2DModel` fixes
`spatial_dimension == 2`; `Periodic2DDefectModel` additionally requires a stable pristine
parent identity. Rank specializations are owned by the corresponding
`ksdft2effmass.periodic.periodic2d.rank*.models` packages.

The existing [`control_models`](control_models/index.md) and `retained` namespaces were
moved from singular `model` ownership without compatibility aliases. Their concrete
scientific classification remains separate follow-up work.

The represented control-Hamiltonian boundary binds each exact request at construction:

```python
plane_wave = Periodic2DPlaneWaveHamiltonian(plane_wave_request).result()
finite_difference = Periodic2DFiniteDifferenceHamiltonian(
    finite_difference_request
).result()
```

These represented-Hamiltonian operations do not inherit `Periodic2DModel`; they build
finite matrix representations of an identified scientific model. Their immutable result
objects retain the exact request and represented matrix. The retired zero-state
`...Constructor().execute(request)` owners have no compatibility aliases.
