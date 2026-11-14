# `FirstPassingSupportWireValidation`

## Purpose and status

Implemented immutable ResultObject reporting structural correlation of one canonical
request/result wire pair. Supported import:
`ksdft2effmass.certifications.periodic1d.rank1.first_passing_support.FirstPassingSupportWireValidation`.

## Public contract

Construction requires the shared certification identity, exact request and result
SHA-256 digests, correlated selected support, and endpoint disposition. Final
`BaseTypedRecord` methods provide typed mapping and canonical JSON serialization.

## State and identity

The record identifies exact admitted bytes, not merely equivalent decoded values.
`selected_support` is dimensionless; `disposition` retains the exact endpoint decision
from the result.

## Invariants and failure behavior

The certification identity and digests must satisfy their lexical contracts. Support
must be an exact built-in integer in `0..15`, excluding booleans. Disposition must be the
exact domain enum. Violations raise `TypeError` or `ValueError`.

## Dependencies and collaborators

The record depends on `BaseTypedRecord` and `FirstPassingSupportDisposition`.
`FirstPassingSupportWireValidator.validate()` constructs it.

## Data and action flow

Canonical request and result bytes are decoded and reserialized, hashed, correlated,
and summarized in this immutable value.

## Serialization and compatibility

The mapping contains exactly `certificate_id`, both digests, `selected_support`, and the
explicit disposition wire label. No artifact content, defaults, aliases, or legacy
fields are inferred.

## Scientific and numerical boundary

This result establishes structural byte correlation only. It does not establish
outward containment, independent numerical verification, scientific validation, or
human acceptance.

## Code mapping

| Code path | Symbol kind | Qualified name | Responsibility |
|---|---|---|---|
| `python/src/ksdft2effmass/certifications/periodic1d/rank1/first_passing_support/validation.py` | Class | `ksdft2effmass.certifications.periodic1d.rank1.first_passing_support.FirstPassingSupportWireValidation` | Immutable structural-correlation result |

## Test mapping

| Test path | Pytest node | Evidence class | Established behavior |
|---|---|---|---|
| `python/tests/ksdft2effmass/certifications/periodic1d/rank1/test__Periodic1DRank1FirstPassingSupportCertification.py` | `TestFirstPassingSupportCertification::test__wire_validator__correlates_request_and_result_bytes` | Software verification | Exact request/result digests, support, disposition, and typed result round trip are retained |
| same | `TestFirstPassingSupportCertification::test__wire_validator__reports_unresolved_without_promoting_it` | Software verification | Unresolved disposition remains unresolved in validation output |

## Sphinx mapping

| Sphinx path | Documented route | Role |
|---|---|---|
| `doc/sphinx/api/certifications.rst` | `ksdft2effmass.certifications.periodic1d.rank1.first_passing_support` | Canonical API page |

## Provenance

Original local work under the repository license.

## Evidence

| Evidence kind | Status | Evidence or reason | Reference | Comparator/tolerance | Environment | Validity domain | Accepting authority |
|---|---|---|---|---|---|---|---|
| Software verification | Supported | Canonical synthetic wire correlation and result round trip | Mapped pytest nodes | Exact digest and field equality | Python test environment | Frozen certification wire pair | Not applicable |
| Numerical verification | Not evaluated | Structural correlation does not replay containment | None | Not applicable | Not applicable | Not evaluated | Not applicable |
| Scientific validation | Not evaluated | No intended-use adequacy assessment | None | Not applicable | Not applicable | Not evaluated | Not applicable |
| Uncertainty quantification | Not applicable | No uncertainty model | None | Not applicable | Not applicable | Correlation result | Not applicable |
| Human acceptance | Not evaluated | Validation output grants no acceptance authority | None | Not applicable | Not applicable | Not evaluated | Named human authority required |

## Limitations and deviations

The record does not identify filesystem locations or inspect artifact contents. Those
remain provenance and retained-evidence responsibilities.

## Detail navigation

- [Validation module](../index.md)
- [Shared implementation](../../../../../implementation.md)
- [Shared scientific interpretation](../../../../../scientifics.md)
