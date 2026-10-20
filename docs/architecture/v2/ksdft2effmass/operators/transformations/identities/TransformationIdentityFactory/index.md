# `TransformationIdentityFactory`

## Status and role

`TransformationIdentityFactory` is the implemented Phase 1 canonical constructor for
carrier-compatible transformation-edge identities.

## Public contract

```python
edge = TransformationIdentityFactory().create(
    transformation_id="fourier-conversion-r3",
    kind=RepresentationTransformationKind.finite_fourier_conversion,
    method_id="finite-fourier.v1",
    orientation="bloch-to-cell",
    source_identity=retained_bloch,
    target_identity=complete_cell_hopping,
)
```

The explicit enum choice remains visible in code.

## Five-way detail

- [Scientific interpretation](scientifics.md)
- [Numerical contract](numerics.md)
- [Implementation](implementation.md)
- [Schematics](schematics.md)

## Tests

- `test__TransformationIdentityFactory.py`
