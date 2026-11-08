# `FirstPassingIntervalEntry`

## Purpose and status

Implemented immutable DataObject binding one support and objective to one claimed exact
error enclosure. Supported import:
`ksdft2effmass.certifications.periodic1d.rank1.first_passing_support.FirstPassingIntervalEntry`.

## Public contract

The constructor accepts `maximum_range`, one `FirstPassingSupportObjective`, and one
`NonnegativeExactInterval`. Final `BaseTypedRecord` methods own mapping and JSON
serialization.

## State and identity

`maximum_range` is the dimensionless ordinary-lattice support in the closed inventory
`0..15`. The objective and interval are explicit; positional inference is forbidden.
Result records nevertheless require the complete support-major canonical ordering.

## Invariants and failure behavior

Support must be an exact built-in integer excluding booleans and belong to the frozen
inventory. Objective and interval must have their exact domain types. Violations raise
`TypeError` or `ValueError` without coercion.

## Dependencies and collaborators

The record composes `FirstPassingSupportObjective` and `NonnegativeExactInterval`.
`FirstPassingSupportResult` consumes exactly 32 entries.

## Data and action flow

A producer assigns one exact support/objective key to one interval. Result construction
checks the full ordered key inventory before classification.

## Serialization and compatibility

The mapping contains exactly `maximum_range`, the objective wire label, and the nested
interval mapping. Version 1 accepts no alternate objective labels or support aliases.

## Scientific and numerical boundary

The record names a claimed enclosure; it does not establish containment or calculate the
underlying total maximum evaluation error.

## Code mapping

| Code path | Symbol kind | Qualified name | Responsibility |
|---|---|---|---|
| `python/src/ksdft2effmass/certifications/periodic1d/rank1/first_passing_support/records.py` | Class | `ksdft2effmass.certifications.periodic1d.rank1.first_passing_support.FirstPassingIntervalEntry` | Support/objective enclosure correlation |

## Test mapping

| Test path | Pytest node | Evidence class | Established behavior |
|---|---|---|---|
| `python/tests/ksdft2effmass/certifications/periodic1d/rank1/test__Periodic1DRank1FirstPassingSupportCertification.py` | `TestFirstPassingSupportCertification::test__result__rejects_noncanonical_inventory_order` | Software verification | Entry order must match the canonical support/objective inventory |
| same | `TestFirstPassingSupportCertification::test__result__rejects_incomplete_inventory` | Software verification | Missing entries are rejected |

## Sphinx mapping

| Sphinx path | Documented route | Role |
|---|---|---|
| `doc/sphinx/api/certifications.rst` | `ksdft2effmass.certifications.periodic1d.rank1.first_passing_support` | Canonical API page |

## Provenance

Original local work under the repository license.

## Evidence

| Evidence kind | Status | Evidence or reason | Reference | Comparator/tolerance | Environment | Validity domain | Accepting authority |
|---|---|---|---|---|---|---|---|
| Software verification | Supported | Complete ordered inventory checks | Mapped pytest nodes | Exact key order | Python test environment | Supports 0 through 15 and two objectives | Not applicable |
| Numerical verification | Not evaluated | No containment oracle | None | Not applicable | Not applicable | Not evaluated | Not applicable |
| Scientific validation | Not evaluated | No parent-model adequacy test | None | Not applicable | Not applicable | Not evaluated | Not applicable |
| Uncertainty quantification | Not applicable | No probability model | None | Not applicable | Not applicable | Correlation record | Not applicable |
| Human acceptance | Not evaluated | No human decision | None | Not applicable | Not applicable | Not evaluated | Named human authority required |

## Limitations and deviations

The record is closed to one scalar error interval. It cannot represent covariance,
multiple methods for one key, or an expanded support inventory.

## Detail navigation

- [Records module](../index.md)
- [Shared numerics](../../../../../numerics.md)
