# `FirstPassingSupportDisposition`

## Purpose and status

Implemented closed Enum for the conservative endpoint decision of one complete
first-passing-support result. Supported import:
`ksdft2effmass.certifications.periodic1d.rank1.first_passing_support.FirstPassingSupportDisposition`.

## Public contract

`ACCEPTED` means the selected support definitely passes both objectives and every
earlier support definitely fails at least one. `REJECTED` means the selected support
definitely fails or an earlier support definitely passes. `UNRESOLVED` retains every
remaining overlapping or undecided case.

## State and identity

The exact wire values are `accepted`, `rejected`, and `unresolved`. They classify only
the encoded finite proposition and do not identify scientific or human acceptance.

## Invariants and failure behavior

Only declared members are accepted. Unknown or non-string wire labels fail without
normalization, aliases, or fallback.

## Dependencies and collaborators

The enum depends on `StrWireEnum`. `FirstPassingSupportResult.classify()` produces it;
`FirstPassingSupportWireValidation` reports it.

## Data and action flow

Exact rational interval endpoints enter `classify()`, which returns one member. Result
construction rejects a reported member that differs from that exact classification.

## Serialization and compatibility

Records explicitly use `to_wire()` and `from_wire()`. Version 1 has no compatibility
aliases or legacy dispositions.

## Scientific and numerical boundary

`ACCEPTED` is an endpoint disposition conditional on sound containment evidence. It is
not scientific validation, publication acceptance, or release authority.

## Code mapping

| Code path | Symbol kind | Qualified name | Responsibility |
|---|---|---|---|
| `python/src/ksdft2effmass/certifications/periodic1d/rank1/first_passing_support/records.py` | Enum | `ksdft2effmass.certifications.periodic1d.rank1.first_passing_support.FirstPassingSupportDisposition` | Closed conservative decision vocabulary |

## Test mapping

| Test path | Pytest node | Evidence class | Established behavior |
|---|---|---|---|
| `python/tests/ksdft2effmass/certifications/periodic1d/rank1/test__Periodic1DRank1FirstPassingSupportCertification.py` | `TestFirstPassingSupportCertification::test__result__classifies_selected_overlap_as_unresolved` | Software verification | Overlap remains unresolved |
| same | `TestFirstPassingSupportCertification::test__result__rejects_an_earlier_definite_joint_pass` | Software verification | Earlier definite passage rejects the selected first-passing claim |
| same | `TestFirstPassingSupportCertification::test__result__round_trips_all_32_entries` | Software verification | A fully decided synthetic table is classified accepted |

## Sphinx mapping

| Sphinx path | Documented route | Role |
|---|---|---|
| `doc/sphinx/api/certifications.rst` | `ksdft2effmass.certifications.periodic1d.rank1.first_passing_support` | Canonical API page |

## Provenance

Original local work under the repository license.

## Evidence

| Evidence kind | Status | Evidence or reason | Reference | Comparator/tolerance | Environment | Validity domain | Accepting authority |
|---|---|---|---|---|---|---|---|
| Software verification | Supported | Exact synthetic endpoint cases | Mapped pytest nodes | Exact enum identity | Python test environment | Frozen finite proposition | Not applicable |
| Numerical verification | Not evaluated | Tests establish decision logic, not containment | None | Not applicable | Not applicable | Not evaluated | Not applicable |
| Scientific validation | Not evaluated | No intended-use model assessment | None | Not applicable | Not applicable | Not evaluated | Not applicable |
| Uncertainty quantification | Not applicable | No uncertainty propagation is represented | None | Not applicable | Not applicable | Decision vocabulary | Not applicable |
| Human acceptance | Not evaluated | Disposition is not human acceptance | None | Not applicable | Not applicable | Not evaluated | Named human authority required |

## Limitations and deviations

The disposition cannot express graded confidence or partial acceptance. Undecided cases
must remain `UNRESOLVED`.

## Detail navigation

- [Records module](../index.md)
- [Shared numerics](../../../../../numerics.md)
- [Shared scientific interpretation](../../../../../scientifics.md)
