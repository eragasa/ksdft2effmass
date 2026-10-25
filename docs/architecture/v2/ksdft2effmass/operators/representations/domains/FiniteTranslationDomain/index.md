# `FiniteTranslationDomain`

## Status and role

`FiniteTranslationDomain` is the implemented Phase 1 DataObject for an identified,
ordered, unique finite inventory of integer translations.

## Public contract

```python
from ksdft2effmass.operators.representations.domains import FiniteTranslationDomain
```

Constructor state is `identifier`, `translations`, and `coordinate_convention_id`.
Derived properties are `identity`, `cardinality`, and common vector `dimension`.

## Five-way detail

- [Scientific interpretation](scientifics.md)
- [Numerical contract](numerics.md)
- [Implementation](implementation.md)
- [Schematics](schematics.md)

## Code and tests

- Source: `operators/representations/domains.py`
- Tests: `test__FiniteTranslationDomain.py`
