# `RepresentationIdentity`

## Status and role

`RepresentationIdentity` is the implemented Phase 1 immutable node identity composing an
exact carrier domain, represented space, family-local enum role, and source artifact.

## Public contract

Canonical construction uses `RepresentationIdentityFactory`:

```python
identity = RepresentationIdentityFactory().create_bloch(
    representation_id="retained-reference",
    domain=momentum_domain,
    space=represented_space,
    role=BlochSpaceRole.retained,
    source_artifact_id="analytic-parent-law.v1",
)
```

`domain_id`, `rank`, `space_id`, and `basis_id` are derived. A role cannot be paired with
the wrong carrier-domain family.

## Five-way detail

- [Scientific interpretation](scientifics.md)
- [Numerical contract](numerics.md)
- [Implementation](implementation.md)
- [Schematics](schematics.md)

## Code and tests

- Source: `operators/representations/identities.py`
- Tests: `test__RepresentationIdentity.py`
