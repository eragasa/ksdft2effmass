# `ksdft2effmass.operators.transformations` package

## Purpose and status

This uncommitted Phase 1 package owns typed directed representation edges and the stable
nominal computational skeleton for transformation requests, results, and Actions. It
depends inward on `operators.representations`; that dependency must never be reversed.

## Five-way architecture bundle

- [Scientific interpretation](scientifics.md)
- [Numerical contract](numerics.md)
- [Implementation and ownership](implementation.md)
- [Schematics](schematics.md)

## Contract inventory

| Source module | Architecture page | Responsibility |
|---|---|---|
| `identities.py` | [`identities`](identities/index.md) | transformation-kind enum and directed edge identity |
| `base.py` | [`base`](base/index.md) | enum-discriminated request, result, and Action ABCs |
| operation modules | prospective | operation-specific request/result/Actions; none in Phase 1 |

The package initializer is documentation-only. There is no universal enum-dispatched
operational factory. `TransformationIdentityFactory` constructs identity metadata only.

## Source and tests

```text
python/src/ksdft2effmass/operators/transformations/__init__.py
python/src/ksdft2effmass/operators/transformations/identities.py
python/src/ksdft2effmass/operators/transformations/base.py

python/tests/software_verification/ksdft2effmass/operators/transformations/
```

## Boundaries

Concrete mathematical operator families may depend on this package and on
`operators.representations`. Operator-specific transformations remain with their concrete
operator family unless reusable across operator families. Campaign thresholds,
qualification, provenance, serializers, retained evidence, and formal proof remain
outward owners.

Phase 1 tests establish nominal enum agreement and identity construction only. They do
not prove transformation correctness, property preservation, qualification, evidence, or
formal correspondence.
