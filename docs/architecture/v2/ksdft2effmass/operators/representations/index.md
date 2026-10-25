# `ksdft2effmass.operators.representations` package

## Purpose and status

This source-mirrored architecture node documents the uncommitted Phase 1 owner for
finite carrier domains, represented spaces, intrinsic representation-node identities,
and immutable matrix fields. It extends `ksdft2effmass.operators` without replacing
`StateSpace`, `Basis`, `Geometry`, `EnergyReference`, or `OperatorRecord`.

Directed edge identity and operational transformation contracts are owned by the sibling
[`ksdft2effmass.operators.transformations`](../transformations/index.md) package. The
required dependency direction is `transformations -> representations`; this package does
not import transformations.

## Five-way architecture bundle

- [Scientific objects and interpretation](scientifics.md)
- [Numerical representation](numerics.md)
- [Implementation and ownership](implementation.md)
- [Schematics](schematics.md)
- This index owns status, navigation, source mapping, and bounded evidence status.

## Contract inventory

The initializer is documentation-only. Consumers import from defining modules:

| Source module | Architecture page | Responsibility |
|---|---|---|
| `domains.py` | [`domains`](domains/index.md) | momentum and translation domains |
| `spaces.py` | [`spaces`](spaces/index.md) | represented-space metadata composition |
| `identities.py` | [`identities`](identities/index.md) | carrier-local role enums and intrinsic node identities |
| `fields.py` | [`fields`](fields/index.md) | matrix-field ABC hierarchy and immutable NumPy leaves |
| `nodes.py` | prospective | future generic representation nodes; not implemented in Phase 1 |

A reachable direct-module import is not a frozen schema or retained-evidence contract.

## Source mapping

```text
python/src/ksdft2effmass/operators/representations/__init__.py
    docs/architecture/v2/ksdft2effmass/operators/representations/index.md

python/src/ksdft2effmass/operators/representations/domains.py
    docs/architecture/v2/ksdft2effmass/operators/representations/domains/index.md

python/src/ksdft2effmass/operators/representations/spaces.py
    docs/architecture/v2/ksdft2effmass/operators/representations/spaces/index.md

python/src/ksdft2effmass/operators/representations/identities.py
    docs/architecture/v2/ksdft2effmass/operators/representations/identities/index.md

python/src/ksdft2effmass/operators/representations/fields.py
    docs/architecture/v2/ksdft2effmass/operators/representations/fields/index.md
```

No name is re-exported from either package initializer or from
`python/src/ksdft2effmass/operators/__init__.py`.

## Test mapping

- `python/tests/software_verification/ksdft2effmass/operators/representations/`
- `test__RepresentationIdentity__dependency_boundary.py` verifies the inward package
  boundary, absence of a reverse representations-to-transformations dependency, and
  documentation-only initializers.
- Module-specific tests are linked from each child page.

The tests establish software contracts only. They do not validate a physical model,
formalize a theorem, or qualify retained scientific evidence.

## Concrete-operator boundary

Concrete mathematical operator families belong in first-class sibling packages such as
`ksdft2effmass.operators.hamiltonian`, not in representations. Such a package may consume
representations and transformations. Neither generic package may import a concrete
operator family. The package unit is a cohesive operator family, never a runtime object,
derivation-graph node, paper stage, or campaign case.

## Evidence status and limitations

Phase 1 has focused software-verification, strict typing, and lint coverage. It remains
uncommitted and has no serializer, schema, generic representation node, operation-specific
transformation Action, certificate export, or retained-evidence binding.
