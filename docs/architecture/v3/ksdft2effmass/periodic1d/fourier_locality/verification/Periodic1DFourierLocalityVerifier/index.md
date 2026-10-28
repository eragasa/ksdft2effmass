# `Periodic1DFourierLocalityVerifier`

## Responsibility

Byte-owning action object. Its constructor accepts immutable result bytes;
its result method returns the verification aggregate together with the exact
authenticated visualization projection.

## Verification sequence

1. hash and strictly decode the exact admitted bytes;
2. validate the complete typed calculation result;
3. construct the typed visualization projection from the admitted result;
4. independently recompute the declared exact, numerical, decision, and qualification
   channels and compare them through named paths;
5. compare every projection field with its corresponding admitted-result field;
6. construct the verification aggregate and bind the canonical projection digest; and
7. return verification and projection without writing files.

When stored verification outputs are consumed, the shared admission behavior repeats
this sequence from the exact result bytes and requires canonical byte equality with the
stored aggregate and projection. The freshly recomputed aggregate and freshly projected
data are returned for rendering. No separate literal list of every dynamically named
comparison is maintained.

The class never invokes `Periodic1DFourierLocalityAnalyzer`.

## Public import

```python
from ksdft2effmass.periodic1d.fourier_locality import (
    Periodic1DFourierLocalityVerifier,
)
```

## Pages

- [Schematics](schematics.md)
- [Numerics](numerics.md)
- [Scientific interpretation](scientifics.md)
- [Owning module](../index.md)
