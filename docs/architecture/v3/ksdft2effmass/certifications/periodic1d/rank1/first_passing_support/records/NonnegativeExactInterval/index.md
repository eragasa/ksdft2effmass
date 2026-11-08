# `NonnegativeExactInterval`

## Purpose and status

Implemented immutable DataObject for one closed nonnegative exact error interval in the
proposition's `E_ref` unit. Supported import:
`ksdft2effmass.certifications.periodic1d.rank1.first_passing_support.NonnegativeExactInterval`.

## Public contract

The constructor accepts exact `lower` and `upper` endpoints. Both endpoints are
inclusive. Final `BaseTypedRecord` methods provide typed mapping and JSON round trips.

## State and identity

Identity is the ordered endpoint pair. Ordering, units, and closed-endpoint semantics
are fixed; the interval is not represented by midpoint and radius.

## Invariants and failure behavior

Both fields must be `ExactRational`; the lower endpoint must be nonnegative and no
greater than the upper endpoint. Type violations raise `TypeError`; ordering or sign
violations raise `ValueError`.

## Dependencies and collaborators

The interval composes two `ExactRational` values. `FirstPassingIntervalEntry` adds the
support and objective identity.

## Data and action flow

Exact endpoints enter construction, pass structural checks, serialize as nested typed
mappings, and later participate in threshold comparison through `as_fraction()`.

## Serialization and compatibility

The mapping contains exactly `lower` and `upper`. No decimal endpoint, endpoint swap,
default, widening, or compatibility fallback is applied.

## Scientific and numerical boundary

Construction validates endpoint structure, not outward containment. An interval may be
structurally valid while its producer claim is scientifically or numerically unsound.

## Code mapping

| Code path | Symbol kind | Qualified name | Responsibility |
|---|---|---|---|
| `python/src/ksdft2effmass/certifications/periodic1d/rank1/first_passing_support/records.py` | Class | `ksdft2effmass.certifications.periodic1d.rank1.first_passing_support.NonnegativeExactInterval` | Closed nonnegative rational interval record |

## Test mapping

| Test path | Pytest node | Evidence class | Established behavior |
|---|---|---|---|
| `python/tests/ksdft2effmass/certifications/periodic1d/rank1/test__Periodic1DRank1FirstPassingSupportCertification.py` | `TestFirstPassingSupportCertification::test__exact_interval__rejects_reversed_endpoints` | Software verification | Reversed endpoints are rejected |
| same | `TestFirstPassingSupportCertification::test__result__round_trips_all_32_entries` | Software verification | All nested exact intervals survive typed serialization |

## Sphinx mapping

| Sphinx path | Documented route | Role |
|---|---|---|
| `doc/sphinx/api/certifications.rst` | `ksdft2effmass.certifications.periodic1d.rank1.first_passing_support` | Canonical API page |

## Provenance

Original local work under the repository license.

## Evidence

| Evidence kind | Status | Evidence or reason | Reference | Comparator/tolerance | Environment | Validity domain | Accepting authority |
|---|---|---|---|---|---|---|---|
| Software verification | Supported | Endpoint rejection and nested round trip | Mapped pytest nodes | Exact equality | Python test environment | Closed nonnegative rational intervals | Not applicable |
| Numerical verification | Not evaluated | No independent containment oracle | None | Not applicable | Not applicable | Not evaluated | Not applicable |
| Scientific validation | Not evaluated | No model adequacy assessment | None | Not applicable | Not applicable | Not evaluated | Not applicable |
| Uncertainty quantification | Not applicable | Interval is a bound record, not a probability model | None | Not applicable | Not applicable | Bound representation | Not applicable |
| Human acceptance | Not evaluated | No acceptance decision | None | Not applicable | Not applicable | Not evaluated | Named human authority required |

## Limitations and deviations

Only nonnegative scalar errors are represented. Signed, complex, vector, or
multidimensional intervals require different reviewed values.

## Detail navigation

- [Records module](../index.md)
- [Shared numerics](../../../../../numerics.md)
- [Shared scientific interpretation](../../../../../scientifics.md)
