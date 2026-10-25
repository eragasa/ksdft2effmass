# `TransformationIdentity`

## Status and role

`TransformationIdentity` is the implemented Phase 1 immutable identity of one directed,
enum-classified derivation edge between full representation-node identities.

## Public contract

Canonical construction uses `TransformationIdentityFactory`:

```python
edge = TransformationIdentityFactory().create(
    transformation_id="gauge-conjugation-r3",
    kind=RepresentationTransformationKind.gauge_conjugation,
    method_id="pointwise-conjugation.v1",
    orientation="gauge-dagger-source-gauge",
    source_identity=source,
    target_identity=target,
)
```

Stored fields are `transformation_id`, `kind`, `method_id`, `orientation`,
`source_identity`, and `target_identity`.

## Five-way detail

- [Scientific interpretation](scientifics.md)
- [Numerical contract](numerics.md)
- [Implementation](implementation.md)
- [Schematics](schematics.md)

## Tests

- `test__TransformationIdentity.py`
