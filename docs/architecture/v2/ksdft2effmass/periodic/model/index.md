# `periodic.model` nominal scientific-model hierarchy

## Purpose and status

This implemented module owns nominal runtime membership for scientific models with one,
two, or three periodic spatial directions. It identifies model category, dimension, and
pristine-parent identity for defect branches. It does not own a Hamiltonian matrix,
retained space, represented operator, campaign, solver, serializer, tolerance, or
scientific acceptance decision.

## Public contract inventory

| Symbol | Kind | Contract |
|---|---|---|
| `SpatialDimension` | Type alias | Closed literal dimension set `1 | 2 | 3` |
| `PeriodicModelRole` | Enum | Exact `TOY` or `MATERIAL_REFERENCE` evidentiary role |
| `PeriodicModel` | Abstract class | Requires stable model identity, exact role, and nominal dimension |
| `Periodic1DModel` | Abstract class | Enforces exact built-in dimension `1` |
| `Periodic2DModel` | Abstract class | Enforces exact built-in dimension `2` |
| `Periodic3DModel` | Abstract class | Enforces exact built-in dimension `3` |
| `Periodic1DDefectModel` | Abstract class | Adds explicit pristine-parent identity to the 1D branch |
| `Periodic2DDefectModel` | Abstract class | Adds explicit pristine-parent identity to the 2D branch |
| `Periodic3DDefectModel` | Abstract class | Adds explicit pristine-parent identity to the 3D branch |

All symbols are supported through `ksdft2effmass.periodic`.

## Scientific and software boundary

Nominal membership answers what category a concrete model claims. It does not define the
model's operator, basis, gauge, energy reference, units, geometry, finite representation,
or provenance. Concrete owners must document those contracts. `MATERIAL_REFERENCE`
means only that a model is intended to represent an explicitly specified material; it
does not imply physical completeness or scientific validation.

Defect membership adds a stable pristine-parent identity. It does not establish that
parent and defect operators have compatible state spaces or representations. Alignment
and compatibility must be demonstrated before subtraction or comparison.

## Invariants and failures

Dimension branches implement a final `spatial_dimension` property and reject a subclass
that defines the property again. Concrete models remain abstract until they implement
`model_id` and `model_role`; concrete defect models must also implement
`parent_model_id`. Intrinsic validation of a concrete identity belongs to its concrete
owner.

## Dependencies and neighboring owners

The module depends only on Python nominal typing and abstract-base machinery.
`periodic.retention` owns parent-qualified retained spaces and operators.
`periodic.catalog` owns explicit toy-model registration. Campaign packages may depend on
this hierarchy; this module must not import campaign definitions or execution policy.

## Class navigation

- [`PeriodicModelRole`](PeriodicModelRole/index.md)
- [`PeriodicModel`](PeriodicModel/index.md)
- [`Periodic1DModel`](Periodic1DModel/index.md)
- [`Periodic2DModel`](Periodic2DModel/index.md)
- [`Periodic3DModel`](Periodic3DModel/index.md)
- [`Periodic1DDefectModel`](Periodic1DDefectModel/index.md)
- [`Periodic2DDefectModel`](Periodic2DDefectModel/index.md)
- [`Periodic3DDefectModel`](Periodic3DDefectModel/index.md)

## Code mapping

| Code path | Symbol kind | Qualified name | Responsibility |
|---|---|---|---|
| `python/src/ksdft2effmass/periodic/model.py` | Module | `ksdft2effmass.periodic.model` | Nominal periodic scientific-model hierarchy |
| `python/src/ksdft2effmass/periodic/__init__.py` | Package export | `ksdft2effmass.periodic` | Supported public routes |

## Test mapping

| Test path | Pytest node | Evidence class | Established behavior |
|---|---|---|---|
| `python/tests/software_verification/ksdft2effmass/periodic/test__PeriodicModel.py` | `TestPeriodicModel` | Software verification | Nominal membership, exact dimensions, abstract identity/role contract, defect parent identity, and override rejection |
| `python/tests/software_verification/ksdft2effmass/periodic/test__PeriodicToyModelCatalog.py` | `TestPeriodicToyModelCatalog` | Software verification | Exact runtime role, identity, and dimension-membership use by the catalog |

The fixtures are synthetic software examples. They are not material models or scientific
validation data.

## Sphinx mapping

| Sphinx path | Documented route | Role |
|---|---|---|
| `doc/sphinx/api/ksdft2effmass/periodic/model.rst` | `ksdft2effmass.periodic` | Public API and scientific-category explanation |
| `doc/sphinx/concepts/periodic-migration-crosswalk.rst` | Periodic object categories | Scientist-facing distinction among model, retention, representation, campaign, and evidence objects |

## Provenance

Original local work under the repository license.

## Evidence

| Evidence kind | Status | Evidence or reason | Reference |
|---|---|---|---|
| Software verification | Supported | Nominal inheritance and exact-dimension behavior | `TestPeriodicModel` |
| Numerical verification | Not applicable | The hierarchy performs no numerical algorithm | Not applicable |
| Scientific validation | Not evaluated | Nominal membership does not test physical adequacy | Not applicable |
| Uncertainty quantification | Not applicable | No uncertain quantity is propagated | Not applicable |
| Human acceptance | Not evaluated | Architecture status is not scientific-result acceptance | Not applicable |

## Limitations and deviations

This module deliberately provides no generic model evaluator or structural protocol.
The concrete 3D material-reference and defect program remains separate future work.
