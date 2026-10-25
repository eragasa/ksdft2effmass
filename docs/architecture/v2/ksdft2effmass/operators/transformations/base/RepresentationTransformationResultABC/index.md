# `RepresentationTransformationResultABC`

## Status and role

Nominal Phase 1 ABC for operation-specific representation-transformation results.

## Public contract

Every concrete result implements:

```python
@property
def transformation_kind(self) -> RepresentationTransformationKind:
    ...
```

The enum member must agree with the request and Action before the public transform method
returns it.

## Five-way detail

- [Scientific interpretation](scientifics.md)
- [Numerical contract](numerics.md)
- [Implementation](implementation.md)
- [Schematics](schematics.md)
