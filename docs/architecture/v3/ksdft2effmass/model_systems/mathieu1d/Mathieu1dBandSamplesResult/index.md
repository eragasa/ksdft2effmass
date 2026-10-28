# `Mathieu1dBandSamplesResult`

## Status and responsibility

Implemented immutable result section in
`python/src/ksdft2effmass/model_systems/mathieu1d/result.py`.

It stores selected and adjacent upper-band values on separate construction and withheld
evaluation coordinate inventories, together with the minimum sampled gap on each.

## Invariants

- All coordinate, energy, and gap quantities are explicitly `Unitless()`.
- Selected and upper-band vectors share their role's coordinate length.
- Each stored gap exactly equals the minimum upper-minus-selected sample difference.
- Sampled gaps are nonnegative.
- Training and evaluation coordinates are disjoint.

## Public import

```python
from ksdft2effmass.model_systems.mathieu1d import Mathieu1dBandSamplesResult
```

## Claim boundary

A positive sampled gap is a finite diagnostic. It is not a proof of continuum band
isolation or a certificate between sampled coordinates.
