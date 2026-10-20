# `ksdft2effmass.operators.transformations.base` module

## Purpose and status

This implemented Phase 1 module supplies the stable nominal computational skeleton for
operation-specific representation transformations. It is not a universal transformation
factory and contains no numerical transformation implementation yet.

## Contract inventory

| Symbol | Role |
|---|---|
| [`RepresentationTransformationRequestABC`](RepresentationTransformationRequestABC/index.md) | nominal operation-specific request with explicit enum kind |
| [`RepresentationTransformationResultABC`](RepresentationTransformationResultABC/index.md) | nominal operation-specific result with explicit enum kind |
| [`RepresentationTransformationABC`](RepresentationTransformationABC/index.md) | generic request-to-result Action enforcing enum agreement |

Supported imports come from the defining module:

```python
from ksdft2effmass.operators.transformations.base import (
    RepresentationTransformationABC,
    RepresentationTransformationRequestABC,
    RepresentationTransformationResultABC,
)
```

## Stable behavior

`RepresentationTransformationABC.transform(request, /) -> result` is the abstract public
operation implemented by each concrete Action. Request, Action, and result expose
`transformation_kind: RepresentationTransformationKind`. Concrete implementations must
reject disagreement; final protected validators provide the common exact checks.

Concrete operations define their own nominal requests, results, and Actions. No shared
numerical payload or enum-dispatched algorithm is implied.

## Five-way detail

- [Scientific interpretation](scientifics.md)
- [Numerical contract](numerics.md)
- [Implementation](implementation.md)
- [Schematics](schematics.md)

## Code and tests

- Source: `python/src/ksdft2effmass/operators/transformations/base.py`
- Tests: `test__RepresentationTransformationABC.py`
