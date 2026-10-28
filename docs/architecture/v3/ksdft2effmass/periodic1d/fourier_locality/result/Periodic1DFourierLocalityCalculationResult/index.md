# `Periodic1DFourierLocalityCalculationResult`

## Responsibility

Implemented immutable root for one complete compatible rank-one Fourier-locality
calculation. It owns the single calculation-family identity and composes the authored
configuration, common evaluation section, ordered mesh sections, adjacent-mesh
refinement values, and sampled-gap minimum.

## Root invariants

- The calculation family is `periodic1d-rank1-fourier-locality`.
- The exact controlled-parent identity and coefficients remain bound through the embedded
  configuration.
- Mesh sizes, exact-rational-derived evaluation coordinates, support ranges, and
  production mesh agree with the configuration.
- Refinement-channel names equal the one ordered semantic inventory defined by the
  configuration.
- Complete and finite-support coefficients reproduce their declared construction and
  evaluation candidates.
- Stored decisive total-error summaries agree with their represented candidates.
- Application, sampled-gap, and refinement dispositions fail closed at their configured
  boundaries.

```python
from ksdft2effmass.periodic1d.fourier_locality import (
    Periodic1DFourierLocalityCalculationResult,
)
```

## Pages

- [Schematics](schematics.md)
- [Numerics](numerics.md)
- [Scientific interpretation](scientifics.md)
- [Owning result module](../index.md)
