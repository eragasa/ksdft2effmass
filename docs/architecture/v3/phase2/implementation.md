# Phase 2 proposed implementation boundary

## Bounded source proposal

```text
python/src/ksdft2effmass/operators/representations/nodes.py
```

No other production module is proposed for this checkpoint.

## Proposed types

`OperatorRepresentationABC` would expose read-only `identity` and `field` properties.
`BlochOperatorRepresentation` and `CellHoppingRepresentation` would be final, frozen,
slotted DataObjects implementing that common interface.

Under the recommended substitution policy, constructors accept the applicable Phase 1
field ABC and validate domain and dimensions. They do not require an exact NumPy leaf and
do not copy field storage.

## Required tests

Focused tests must cover valid rank-three Bloch and cell-hopping nodes plus rejection of:

- carrier-family mismatch;
- unequal domains with equal cardinality;
- source-dimension mismatch;
- target-dimension mismatch;
- inappropriate field role; and
- forbidden inward or outward imports.

The package initializer and operators root must remain free of re-exports. Verification
must include focused tests, strict affected mypy, Ruff check and format, dependency tests,
and a package/import smoke check if package discovery changes.

## Explicit exclusions

This phase excludes numerical transformation Actions, graph containers, traversal,
registries, evidence references, Paper 3 adapters, alignment policy, Fourier conventions,
support decisions, schemas, serializers, retained execution, dependency changes, and
formal runtime integration.
