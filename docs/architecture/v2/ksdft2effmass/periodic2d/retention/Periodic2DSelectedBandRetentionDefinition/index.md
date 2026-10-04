# `Periodic2DSelectedBandRetentionDefinition`

## Purpose and status

`Periodic2DSelectedBandRetentionDefinition` is an implemented immutable DataObject that
binds one inclusive contiguous parent-band interval to the general parent-qualified
retention contract for exactly two periodic dimensions.

## Public contract

```python
Periodic2DSelectedBandRetentionDefinition(
    retention: PeriodicRetentionDefinition,
    selection: ContiguousBandSelection,
)
```

The supported import route is:

```python
from ksdft2effmass.periodic2d import Periodic2DSelectedBandRetentionDefinition
```

The `band_indices` property returns inclusive ascending zero-based parent-band indices.
Position `i` corresponds to `retention.ordered_state_labels[i]`.

## State and identity

| Field | Meaning |
|---|---|
| `retention` | Stable retention, parent-model, parent-operator, ambient-space, retained-space, reciprocal-domain, construction-record, assumption, and provenance identities |
| `selection` | Inclusive contiguous zero-based parent-band interval |

The object is frozen and slotted. It contains no floating-point values and performs no
unit conversion or overflow-prone arithmetic. Band indices and rank are exact built-in
integers owned and validated by the composed records; booleans and numeric strings are
not accepted by those public contracts.

## Invariants and failure behavior

Construction requires exact public field types, spatial dimension two,
`PeriodicRetentionKind.SELECTED_BANDS`, and equality between retained rank and selected
band count. Semantic type substitutions raise `TypeError`; dimension, kind, and rank
contradictions raise `ValueError`.

Validation is decomposed into `_check_args_types` and
`_check_args_retention_semantics`. These private methods protect distinct invariant
families and do not perform scientific calculations.

## Dependencies and collaborators

The class composes `PeriodicRetentionDefinition` and `ContiguousBandSelection`. It does
not depend on campaign definitions, encoded documents, serializers, represented
operators, or filesystem state.

## Data and action flow

```text
PeriodicOperatorReference
        |
        v
PeriodicRetentionDefinition + ContiguousBandSelection
        |
        v
Periodic2DSelectedBandRetentionDefinition
```

The final arrow is immutable composition, not band selection, projection,
disentanglement, basis transformation, or truncation.

## Serialization and compatibility

No serializer or compatibility alias is defined. This change does not alter historical
periodic2d payload bytes, filenames, identifiers, digests, or schemas.

## Scientific and numerical boundary

The class declares selected-band metadata. It does not establish band isolation,
construct or authenticate a projector or frame, select a gauge, represent an operator,
or define an effective model. Equal rank or compatible matrix shapes cannot supply
those meanings.

Parent-model, numerical or discretization, and model-reduction errors remain separate.
Software tests establish only the declared construction contract, not numerical
verification, physical adequacy, scientific validation, or uncertainty quantification.

## Code mapping

| Code path | Symbol kind | Qualified name | Architecture responsibility |
|---|---|---|---|
| `python/src/ksdft2effmass/periodic2d/retention.py` | Class | `ksdft2effmass.periodic2d.retention.Periodic2DSelectedBandRetentionDefinition` | Defining two-dimensional parent-qualified contiguous-band class |
| `python/src/ksdft2effmass/periodic2d/__init__.py` | Class | `ksdft2effmass.periodic2d.Periodic2DSelectedBandRetentionDefinition` | Supported package-root re-export of the defining class |

## Test mapping

| Test path | Pytest node | Evidence class | Established behavior |
|---|---|---|---|
| `python/tests/software_verification/ksdft2effmass/periodic2d/test__Periodic2DSelectedBandRetentionDefinition.py` | `TestPeriodic2DSelectedBandRetentionDefinition::test_construction__fields__binds_parent_selection_and_order` | Software verification | Exact fields and index-to-label ordering |
| `python/tests/software_verification/ksdft2effmass/periodic2d/test__Periodic2DSelectedBandRetentionDefinition.py` | `TestPeriodic2DSelectedBandRetentionDefinition::test_construction__types__rejects_semantic_substitutes` | Software verification | Exact semantic type boundary |
| `python/tests/software_verification/ksdft2effmass/periodic2d/test__Periodic2DSelectedBandRetentionDefinition.py` | `TestPeriodic2DSelectedBandRetentionDefinition::test_construction__parent__rejects_non_two_dimensional_reference` | Software verification | Exact two-dimensional parent requirement |
| `python/tests/software_verification/ksdft2effmass/periodic2d/test__Periodic2DSelectedBandRetentionDefinition.py` | `TestPeriodic2DSelectedBandRetentionDefinition::test_construction__kind__rejects_non_band_retention` | Software verification | Selected-band construction kind |
| `python/tests/software_verification/ksdft2effmass/periodic2d/test__Periodic2DSelectedBandRetentionDefinition.py` | `TestPeriodic2DSelectedBandRetentionDefinition::test_construction__rank__rejects_selection_count_mismatch` | Software verification | Rank and selected-count agreement |
| `python/tests/software_verification/ksdft2effmass/periodic2d/test__Periodic2DSelectedBandRetentionDefinition.py` | `TestPeriodic2DSelectedBandRetentionDefinition::test_data_object__mutation__is_rejected` | Software verification | Frozen field behavior |
| `python/tests/software_verification/ksdft2effmass/periodic2d/test__Periodic2DSelectedBandRetentionDefinition.py` | `TestPeriodic2DSelectedBandRetentionDefinition::test_public_api__package__exports_supported_definition` | Software verification | Deliberate public export |

## Sphinx mapping

| Sphinx path | Documented route | Role |
|---|---|---|
| `doc/sphinx/api/ksdft2effmass/periodic2d/retention.rst` | `ksdft2effmass.periodic2d.Periodic2DSelectedBandRetentionDefinition` | Public API and scientific boundary |

## Provenance

Original local work under the repository license.

## Evidence

| Evidence kind | Status | Evidence or reason | Reference | Comparator/tolerance | Environment | Validity domain | Accepting authority |
|---|---|---|---|---|---|---|---|
| Software verification | Supported | Seven exact behavior tests | Mapped pytest nodes | Exact assertions and exception classes | Supported Python environment | Synthetic definition inputs | Not applicable |
| Numerical verification | Not applicable | No numerical algorithm | Source contract | Not applicable | Not applicable | Not applicable | Not applicable |
| Scientific validation | Not evaluated | Selection adequacy is not assessed | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable |
| Uncertainty quantification | Not evaluated | No uncertainty model | Not applicable | Not applicable | Not applicable | Not applicable | Not applicable |
| Human acceptance | Not evaluated | Review and merge remain separate | Review record when available | Not applicable | Not applicable | Changed contract | Named human authority required |

## Limitations and deviations

The class cannot be promoted to a retained-space or retained-operator owner without an
authenticated projector or frame contract and explicit parent-operator binding. No
optional detail pages are needed because the implementation and mathematics are small
and fully stated here.
