# `Periodic1DFourierLocalityVerification`

## Responsibility

Immutable aggregate containing subject identity, complete named comparison
results, authenticated projection identity, and the aggregate verification disposition.

## Owned values

- exact SHA-256 digest of admitted result bytes;
- supported result and verification schema identities;
- ordered complete comparison inventory;
- counts by comparison disposition;
- authenticated visualization-projection SHA-256 digest; and
- aggregate pass value recomputed from every required comparison.

It does not embed the subject bytes or duplicate the complete projection.

## Public import

```python
from ksdft2effmass.periodic1d.fourier_locality import (
    Periodic1DFourierLocalityVerification,
)
```

## Pages

- [Schematics](schematics.md)
- [Numerics](numerics.md)
- [Scientific interpretation](scientifics.md)
- [Owning module](../index.md)
