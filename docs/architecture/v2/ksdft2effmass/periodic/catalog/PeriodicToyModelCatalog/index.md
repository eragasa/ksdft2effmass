# `PeriodicToyModelCatalog`

## Purpose and status

`PeriodicToyModelCatalog` is an implemented immutable DataObject that stores an explicit
ordered snapshot of nominal toy models. It enables deterministic iteration without
discovery or a generic model execution interface.

## Public contract

Supported import: `from ksdft2effmass.periodic import PeriodicToyModelCatalog`.

### Constructor

`PeriodicToyModelCatalog(*, models: tuple[PeriodicModel, ...])`

`models` is an exact nonempty tuple. Its order is semantically retained. The read-only
`model_ids` and `spatial_dimensions` properties return tuples in the same order.

## State and identity

The object stores the model instances themselves. Each model's exact `model_id` is the
registration identity, and identities must be unique within one catalog. No new catalog
content digest or scientific compatibility identity is inferred from the tuple.

## Invariants and failure behavior

Construction checks, in order:

1. exact tuple type and nonempty inventory;
2. nominal `PeriodicModel` membership;
3. exact `PeriodicModelRole` type and `TOY` value;
4. exact nonempty string identity and uniqueness; and
5. exact built-in dimension in `{1, 2, 3}` matching nominal branch membership.

Wrong semantic types raise `TypeError`; violated value or membership invariants raise
`ValueError`. The frozen, slotted dataclass prevents replacing the tuple after
construction. The short `__post_init__` delegates the inventory and member-invariant
families without changing validation order.

## Data flow and exclusions

```text
explicit concrete toy models
            |
            v
PeriodicToyModelCatalog
            |
            +--> ordered model identities
            +--> ordered spatial dimensions
```

The class performs no model evaluation, serialization, filesystem scan, subclass
discovery, comparison, thresholding, or acceptance. A future campaign must preserve the
exact snapshot it consumes and represent incompatible or unavailable observations
explicitly.

## Code mapping

| Code path | Symbol kind | Qualified name | Responsibility |
|---|---|---|---|
| `python/src/ksdft2effmass/periodic/catalog.py` | Class | `ksdft2effmass.periodic.PeriodicToyModelCatalog` | Explicit immutable toy inventory |
| `python/src/ksdft2effmass/periodic/__init__.py` | Re-export | `ksdft2effmass.periodic.PeriodicToyModelCatalog` | Supported route |

## Test mapping

| Pytest node | Established behavior |
|---|---|
| `TestPeriodicToyModelCatalog::test_constructor__models__preserves_explicit_deterministic_order` | Exact caller order and exact dimensions |
| `TestPeriodicToyModelCatalog::test_constructor__models__requires_an_exact_nonempty_tuple` | Immutable nonempty inventory type |
| `TestPeriodicToyModelCatalog::test_constructor__models__requires_periodic_model_members` | Nominal root membership |
| `TestPeriodicToyModelCatalog::test_constructor__models__requires_toy_role` | Toy-only registration |
| `TestPeriodicToyModelCatalog::test_constructor__model_role__requires_exact_enum_type` | No string role substitute |
| `TestPeriodicToyModelCatalog::test_constructor__model_id__requires_exact_string_type` | No numeric identity substitute |
| `TestPeriodicToyModelCatalog::test_constructor__spatial_dimension__rejects_boolean` | Boolean is not an integer dimension |
| `TestPeriodicToyModelCatalog::test_constructor__models__requires_unique_nonempty_identity` | Identity nonemptiness and uniqueness |
| `TestPeriodicToyModelCatalog::test_constructor__models__requires_nominal_dimension_membership` | Reported dimension and nominal branch agree |
| `TestPeriodicToyModelCatalog::test_instance__catalog__is_immutable` | Tuple cannot be replaced |

All nodes are under
`python/tests/software_verification/ksdft2effmass/periodic/test__PeriodicToyModelCatalog.py`
and use synthetic fixtures. They establish software behavior only.

## Sphinx mapping

`doc/sphinx/api/ksdft2effmass/periodic/catalog.rst` documents the public route,
requirements, and exclusions.

## Provenance and evidence

Original local work under the repository license.

| Evidence kind | Status | Reason |
|---|---|---|
| Software verification | Supported | Direct constructor, property, and immutability tests |
| Numerical verification | Not applicable | No numerical algorithm |
| Scientific validation | Not evaluated | Registration does not validate models |
| Uncertainty quantification | Not applicable | No uncertainty model |
| Human acceptance | Not evaluated | Registration is not scientific acceptance |

## Limitations and deviations

No catalog-consuming campaign exists yet. The catalog does not prove that two members
share compatible observables, units, representations, or validation domains.
