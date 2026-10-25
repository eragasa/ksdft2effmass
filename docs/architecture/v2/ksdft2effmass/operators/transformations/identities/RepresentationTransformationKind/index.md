# `RepresentationTransformationKind`

## Status and role

`RepresentationTransformationKind` is the implemented Phase 1 semantic `Enum` for the
kind of one directed derivation edge.

## Public contract

```python
from ksdft2effmass.operators.transformations.identities import (
    RepresentationTransformationKind,
)

kind = RepresentationTransformationKind.frame_compression
```

Its complete member inventory is:

- `RepresentationTransformationKind.frame_compression`;
- `RepresentationTransformationKind.gauge_conjugation`;
- `RepresentationTransformationKind.alignment`;
- `RepresentationTransformationKind.finite_fourier_conversion`;
- `RepresentationTransformationKind.support_truncation`;
- `RepresentationTransformationKind.fourier_reconstruction`.

These are enum members selected explicitly in code, not raw string discriminators and not
representation-node roles.

## Five-way detail

- [Scientific interpretation](scientifics.md)
- [Numerical contract](numerics.md)
- [Implementation](implementation.md)
- [Schematics](schematics.md)
