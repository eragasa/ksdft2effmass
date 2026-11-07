# `Periodic2DPlaneWaveHamiltonian`

## Status and responsibility

Implemented request-bound operation in
`python/src/ksdft2effmass/periodic/periodic2d/models/control_models/cosine.py`.

```python
request = Periodic2DPlaneWaveHamiltonianRequest(
    model=model,
    reduced_momentum_x=kappa_x,
    reduced_momentum_y=kappa_y,
    cutoff=cutoff,
)
result = Periodic2DPlaneWaveHamiltonian(request).result()
```

The operation constructs one finite reciprocal-basis representation of the exact
request. It owns KSD correlation between the control model, reduced momentum, basis
cutoff, energy reference, provider duality evidence, and immutable result. Reusable
plane-wave matrix assembly remains delegated to Project Koios.

## Request boundary

The constructor admits exactly `Periodic2DPlaneWaveHamiltonianRequest`. The request
already validates:

- exact `Periodic2DCosinePotentialControlModel` ownership;
- built-in finite reduced-momentum components;
- a nonnegative built-in integer cutoff;
- the deterministic `p`-outer, `q`-inner square basis; and
- a finite nonnegative direct--reciprocal duality tolerance.

The operation is frozen and slotted. It retains the exact request object by identity and
has no zero-state construction path.

## Result boundary

`result()` returns `Periodic2DPlaneWaveHamiltonianResult`, which retains:

- the exact request;
- the operationally immutable Hermitian matrix;
- matrix-to-basis dimension compatibility; and
- the provider-computed maximum duality residual.

The result rejects a duality residual above the request tolerance. This is a numerical
representation invariant, not a scientific acceptance threshold.

## Ownership exclusions

`Periodic2DPlaneWaveHamiltonian` does not:

- inherit `Periodic2DModel` or define scientific-model identity;
- own the provider's generic plane-wave model or constructor;
- choose a campaign mesh or basis-convergence criterion;
- compare the representation with another discretization;
- perform filesystem or external-process effects; or
- establish continuum or material validity.

## Detailed documents

- [Numerics](numerics.md)
- [Schematic](schematics.md)
- [Scientific interpretation](scientifics.md)
