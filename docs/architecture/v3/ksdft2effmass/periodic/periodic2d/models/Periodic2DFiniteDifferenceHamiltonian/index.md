# `Periodic2DFiniteDifferenceHamiltonian`

## Status and responsibility

Implemented request-bound operation in
`python/src/ksdft2effmass/periodic/periodic2d/models/cosine.py`.

```python
request = Periodic2DFiniteDifferenceHamiltonianRequest(
    model=model,
    reduced_momentum_x=kappa_x,
    reduced_momentum_y=kappa_y,
    points_per_direction=points,
)
result = Periodic2DFiniteDifferenceHamiltonian(request).result()
```

The operation constructs one centered finite-difference coordinate representation of
the exact request. It owns the KSD correlation between the control model, reduced
momentum, odd periodic grid, Bloch seam phases, flattened ordering, and immutable result.

## Request boundary

The constructor admits exactly `Periodic2DFiniteDifferenceHamiltonianRequest`. The
request validates:

- exact `Periodic2DCosinePotentialModel` ownership;
- built-in finite reduced-momentum components;
- an odd built-in integer grid size of at least five;
- the dimensionless period `2*pi`; and
- `x`-outer, `y`-inner site ordering.

The operation is frozen and slotted, retains the exact request by identity, and has no
zero-state construction path.

## Result boundary

`result()` returns `Periodic2DFiniteDifferenceHamiltonianResult`, which retains the exact
request and an operationally immutable exactly Hermitian matrix whose shape agrees with
the declared grid dimension.

## Ownership exclusions

`Periodic2DFiniteDifferenceHamiltonian` does not:

- inherit `Periodic2DModel` or define scientific-model identity;
- choose grid-convergence or finite-size acceptance criteria;
- compare against the plane-wave representation;
- own common-space transport or subtraction;
- perform filesystem or external-process effects; or
- establish continuum or material validity.

## Detailed documents

- [Numerics](numerics.md)
- [Schematic](schematics.md)
- [Scientific interpretation](scientifics.md)
