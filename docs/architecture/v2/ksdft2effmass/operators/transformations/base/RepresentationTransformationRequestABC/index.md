# `RepresentationTransformationRequestABC`

## Status and role

Nominal Phase 1 ABC for operation-specific representation-transformation requests.

## Public contract

Every concrete request implements:

```python
@property
def transformation_kind(self) -> RepresentationTransformationKind:
    ...
```

The returned object is the enum member itself, not a string or serializer token.

## Five-way detail

- [Scientific interpretation](scientifics.md)
- [Numerical contract](numerics.md)
- [Implementation](implementation.md)
- [Schematics](schematics.md)
