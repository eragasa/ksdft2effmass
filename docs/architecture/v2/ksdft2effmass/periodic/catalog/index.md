# `periodic.catalog` explicit toy-model catalogs

## Purpose and status

This implemented module owns immutable, explicitly populated catalogs of nominal toy
models. It provides deterministic iteration without module scanning, subclass discovery,
plugins, factories, or structural fallback.

The catalog owner is implemented. The phase-6 campaign that consumes a frozen catalog
snapshot is not implemented, so catalog availability must not be described as campaign
completion.

## Public contract inventory

| Symbol | Kind | Contract |
|---|---|---|
| `PeriodicToyModelCatalog` | Immutable DataObject | Stores one nonempty ordered tuple of uniquely identified nominal toy models |

The class is supported through `ksdft2effmass.periodic`.

## Represented software object

The catalog represents caller-owned registration order and exact model identities. It
is supporting inventory, not a scientific model, a registry with discovery behavior,
or evidence that the members are mutually comparable. A catalog snapshot contains
objects, not serialized provenance; any campaign consuming it must retain the exact
snapshot or an explicitly defined identity for that snapshot.

## Invariants and failure behavior

- `models` is an exact nonempty tuple.
- Every member is a nominal `PeriodicModel` with exact `PeriodicModelRole.TOY`.
- Every `model_id` is an exact nonempty string and is unique in the tuple.
- Every spatial dimension is an exact built-in integer in `{1, 2, 3}`.
- Reported dimension agrees with nominal dimension-branch membership.
- Wrong semantic types raise `TypeError`; valid semantic types violating catalog
  invariants raise `ValueError`.

Catalog order is preserved. The object is frozen and slotted.

## Dependencies and neighboring owners

The module depends inward on `periodic.model`. It does not import concrete model
packages or campaigns. Callers explicitly compose concrete models into a catalog.
Campaign observation routing and unavailable outcomes belong to phase 6, not this
DataObject.

## Class navigation

- [`PeriodicToyModelCatalog`](PeriodicToyModelCatalog/index.md)

## Code mapping

| Code path | Symbol kind | Qualified name | Responsibility |
|---|---|---|---|
| `python/src/ksdft2effmass/periodic/catalog.py` | Module | `ksdft2effmass.periodic.catalog` | Immutable explicit catalog and intrinsic checks |
| `python/src/ksdft2effmass/periodic/__init__.py` | Package export | `ksdft2effmass.periodic.PeriodicToyModelCatalog` | Supported public route |

## Test mapping

| Test path | Pytest node | Evidence class | Established behavior |
|---|---|---|---|
| `python/tests/software_verification/ksdft2effmass/periodic/test__PeriodicToyModelCatalog.py` | `TestPeriodicToyModelCatalog` | Software verification | Order, immutability, role, identity, uniqueness, exact scalar types, and nominal membership |

The test models are synthetic fixtures used only to establish software behavior.

## Sphinx mapping

| Sphinx path | Documented route | Role |
|---|---|---|
| `doc/sphinx/api/ksdft2effmass/periodic/catalog.rst` | `ksdft2effmass.periodic.PeriodicToyModelCatalog` | Public API and exclusions |

## Provenance

Original local work under the repository license.

## Evidence

| Evidence kind | Status | Evidence or reason | Reference |
|---|---|---|---|
| Software verification | Supported | Intrinsic catalog invariants and immutability | `TestPeriodicToyModelCatalog` |
| Numerical verification | Not applicable | No numerical operation is performed | Not applicable |
| Scientific validation | Not evaluated | Registration does not validate a model | Not applicable |
| Uncertainty quantification | Not applicable | No uncertainty is represented | Not applicable |
| Human acceptance | Not evaluated | Catalog membership is not acceptance of a scientific claim | Not applicable |

## Limitations and deviations

No production catalog snapshot or catalog-consuming campaign is supplied. Explicit
unavailability and cross-model observation compatibility remain phase-6 work.
