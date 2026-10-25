# `FiniteDomainABC`

## Status and role

`FiniteDomainABC` is the implemented Phase 1 abstract contract for an identified finite
ordered domain. It is an ABC, not a DataObject or serializer.

## Public contract

```python
from ksdft2effmass.operators.representations.domains import FiniteDomainABC
```

Implementations provide read-only `identity: str` and `cardinality: int` properties.
Concrete leaves own ordering and any additional geometry.

## Five-way detail

- [Scientific interpretation](scientifics.md)
- [Numerical contract](numerics.md)
- [Implementation](implementation.md)
- [Schematics](schematics.md)

## Code and tests

- Source: `python/src/ksdft2effmass/operators/representations/domains.py`
- Tests: concrete-domain tests verify nominal `FiniteDomainABC` membership.

## Limitations

The interface alone supplies neither coordinates nor an iteration protocol. It establishes
no units, topology, integration weights, support semantics, or scientific validity.
