# `FirstPassingSupportRequest`

## Purpose and status

Implemented immutable request DataObject for the frozen periodic-1D rank-one
first-passing-support proposition. Supported import:
`ksdft2effmass.certifications.periodic1d.rank1.first_passing_support.FirstPassingSupportRequest`.

## Public contract

Construction requires explicit study, execution, case, decision, certification,
repository, source, dependency-lock, native-result, numerical-verification, and selected
support identities. Numerical verification must already report a pass. Final
`BaseTypedRecord` methods own mapping and canonical JSON serialization.

## State and identity

The request binds one exact controlled four-state parent, construction mesh 256,
shifted evaluation mesh 1025, centered forward-negative Fourier convention, mediated and
direct candidate identities, both objective labels, support inventory `0..15`, exact
threshold `1/100000000 E_ref`, and the selected support. Ordered parent matrices and all
hashes are serialized explicitly.

## Invariants and failure behavior

Portable identifiers, a canonical GitHub HTTPS URL, lowercase 40-character Git objects,
lowercase 64-character SHA-256 digests, exact boolean verification state, and an exact
built-in integer support are required. No value is coerced, inferred, normalized, or
loaded from the filesystem. Violations raise `TypeError` or `ValueError`.

## Dependencies and collaborators

The request depends on `BaseTypedRecord` and exact rational nested mappings. It consumes
identities from the calculation and numerical-verification owners but does not own those
analyses. `FirstPassingSupportWireValidator` correlates it with a result.

## Data and action flow

A future certification composition authenticates source and artifact bytes, constructs
the request, serializes it canonically, and passes those exact bytes to a producer and
validator. The request performs no execution.

## Serialization and compatibility

`_mapping()` emits a closed self-identifying contract containing `contract_id`,
`schema_version`, `proposition_id`, the complete fixed problem, repository bindings, and
artifact bindings. `_from_mapping()` requires exact fields and exact fixed values.
Version 1 has no defaults, aliases, dual reads, or legacy migration.

## Scientific and numerical boundary

A valid request identifies a proposition and prerequisite numerical-verification
artifact. It does not establish enclosure containment, parent-model adequacy, continuum
convergence, or material validity.

## Code mapping

| Code path | Symbol kind | Qualified name | Responsibility |
|---|---|---|---|
| `python/src/ksdft2effmass/certifications/periodic1d/rank1/first_passing_support/records.py` | Class | `ksdft2effmass.certifications.periodic1d.rank1.first_passing_support.FirstPassingSupportRequest` | Frozen proposition and evidence identity |

## Test mapping

| Test path | Pytest node | Evidence class | Established behavior |
|---|---|---|---|
| `python/tests/ksdft2effmass/certifications/periodic1d/rank1/test__Periodic1DRank1FirstPassingSupportCertification.py` | `TestFirstPassingSupportCertification::test__request__round_trips_typed_mapping_and_json` | Software verification | Typed mapping and canonical JSON preserve the complete request |
| same | `TestFirstPassingSupportCertification::test__request__rejects_unknown_field` | Software verification | The mapping field inventory is closed |
| same | `TestFirstPassingSupportCertification::test__request__rejects_decimal_number_for_support` | Software verification | Floating support values are rejected |
| same | `TestFirstPassingSupportCertification::test__request__rejects_boolean_as_integer` | Software verification | Boolean support values are rejected |
| same | `TestFirstPassingSupportCertification::test__request__rejects_duplicate_field` | Software verification | Duplicate JSON keys are rejected |
| same | `TestFirstPassingSupportCertification::test__request__requires_passing_native_numerical_verification` | Software verification | A request cannot bind a failed numerical verification |

## Sphinx mapping

| Sphinx path | Documented route | Role |
|---|---|---|
| `doc/sphinx/api/certifications.rst` | `ksdft2effmass.certifications.periodic1d.rank1.first_passing_support` | Canonical API page |

## Provenance

Original local work under the repository license.

## Evidence

| Evidence kind | Status | Evidence or reason | Reference | Comparator/tolerance | Environment | Validity domain | Accepting authority |
|---|---|---|---|---|---|---|---|
| Software verification | Supported | Closed typed mapping, strict scalar admission, and round trip | Mapped pytest nodes | Exact equality and exception type | Python test environment | Frozen synthetic request | Not applicable |
| Numerical verification | Not evaluated | The request records a pass but tests do not independently verify the bound artifact | None | Not applicable | Not applicable | Not evaluated | Not applicable |
| Scientific validation | Not evaluated | No intended-use physical adequacy assessment | None | Not applicable | Not applicable | Not evaluated | Not applicable |
| Uncertainty quantification | Not applicable | No uncertainty propagation | None | Not applicable | Not applicable | Request identity | Not applicable |
| Human acceptance | Not evaluated | Request construction grants no execution or publication authority | None | Not applicable | Not applicable | Not evaluated | Named human authority required |

## Limitations and deviations

The request is deliberately closed to one finite controlled proposition. Any different
parent, mesh, threshold, convention, candidate, objective, unit, or support inventory
requires a new reviewed contract version.

## Detail navigation

- [Records module](../index.md)
- [Shared implementation](../../../../../implementation.md)
- [Shared numerics](../../../../../numerics.md)
- [Shared scientific interpretation](../../../../../scientifics.md)
