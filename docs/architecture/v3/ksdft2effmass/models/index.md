# `ksdft2effmass.models`

## Status

Implemented nominal model root and maintained model-family namespace.

## Ownership

`Model` is the KSD-owned nominal root for scientific models. It requires only a stable
`model_id`. It does not choose a physical domain, periodic dimension, retained rank,
representation, provider integration, campaign, serializer, tolerance, or acceptance
policy.

The package also owns:

- the dimension-neutral Bloch-hopping contract documented under
  [`blochhopping`](blochhopping/index.md); and
- the complete periodic scientific-model hierarchy documented under
  [`ksdft2effmass.periodic.models`](../periodic/models/index.md).

These narrower model families do not add provider requirements to `Model` itself.

## Source mapping

- `python/src/ksdft2effmass/models/base.py`: `Model`
- `python/src/ksdft2effmass/models/blochhopping/`: dimension-neutral Bloch-hopping
  contract
- `python/src/ksdft2effmass/periodic/models/`: dimension-neutral periodic model
  contracts
- `python/src/ksdft2effmass/periodic/periodic*d/`: dimensional and rank-qualified
  periodic model owners

The retired singular package `ksdft2effmass.model` has no compatibility alias.
