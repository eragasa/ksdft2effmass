# `FirstPassingSupportResult`

## Purpose and status

Implemented immutable ResultObject retaining the complete exact interval table, distinct
producer/verifier identities and artifacts, enclosure-method metadata, and conservative
endpoint disposition. Supported import:
`ksdft2effmass.certifications.periodic1d.rank1.first_passing_support.FirstPassingSupportResult`.

## Public contract

Construction requires one certification identity, request digest, two distinct artifact
digests, distinct producer/verifier identities and source digests, enclosure method,
working precision, directed-rounding and error-budget identities, selected support, all
32 interval entries, and the reported disposition. `classify()` returns the exact
disposition implied by the endpoints.

## State and identity

Intervals are support-major: for every support `0..15`, mediated precedes direct. Error
endpoints use `E_ref`; support and precision are dimensionless integers. The exact
threshold is `1/100000000 E_ref`, with endpoint equality counted as passing.

## Invariants and failure behavior

Digests and identifiers are lexically strict. Producer and verifier artifact digests,
logical identities, and source digests must differ. Precision is at least 64 bits. The
interval inventory must be complete and canonically ordered. The reported disposition
must equal `classify()`. Violations raise `TypeError` or `ValueError`.

## Dependencies and collaborators

The result composes `CertificationToolIdentity`, `FirstPassingIntervalEntry`, and
`FirstPassingSupportDisposition`. It uses exact `fractions.Fraction` comparisons and is
correlated to a request by `FirstPassingSupportWireValidator`.

## Data and action flow

A future producer supplies claimed intervals and an artifact; a distinct verifier
supplies a containment-verification artifact. Construction checks record structure and
endpoint logic. The wire validator then authenticates request/result byte correlation.

## Serialization and compatibility

The closed typed mapping includes contract and proposition identity, method metadata,
nested tool identities, a tuple of all entries, request digest, selected support, and
disposition. Version 1 has no partial inventories, alternate ordering, inferred
producer, aliases, or compatibility fallback.

## Scientific and numerical boundary

`classify()` does not assume monotone error with support. Acceptance requires both
selected upper bounds to pass and every earlier support to have at least one lower bound
that fails. Rejection requires selected definite failure or an earlier definite joint
pass. All other cases are unresolved. Construction and tests do not establish outward
containment.

## Code mapping

| Code path | Symbol kind | Qualified name | Responsibility |
|---|---|---|---|
| `python/src/ksdft2effmass/certifications/periodic1d/rank1/first_passing_support/records.py` | Class | `ksdft2effmass.certifications.periodic1d.rank1.first_passing_support.FirstPassingSupportResult` | Complete proposition result record |
| same | Method | `FirstPassingSupportResult.classify` | Exact conservative endpoint classification |

## Test mapping

| Test path | Pytest node | Evidence class | Established behavior |
|---|---|---|---|
| `python/tests/ksdft2effmass/certifications/periodic1d/rank1/test__Periodic1DRank1FirstPassingSupportCertification.py` | `TestFirstPassingSupportCertification::test__result__round_trips_all_32_entries` | Software verification | Complete result round trip and accepted classification |
| same | `TestFirstPassingSupportCertification::test__result__rejects_incomplete_inventory` | Software verification | Incomplete tables are rejected |
| same | `TestFirstPassingSupportCertification::test__result__rejects_noncanonical_inventory_order` | Software verification | Noncanonical tables are rejected |
| same | `TestFirstPassingSupportCertification::test__result__classifies_earlier_overlap_as_unresolved` | Software verification | Earlier overlap remains unresolved |
| same | `TestFirstPassingSupportCertification::test__result__classifies_selected_overlap_as_unresolved` | Software verification | Selected overlap remains unresolved |
| same | `TestFirstPassingSupportCertification::test__result__rejects_an_earlier_definite_joint_pass` | Software verification | Earlier joint passage rejects the claim |
| same | `TestFirstPassingSupportCertification::test__result__rejects_selected_definite_failure` | Software verification | Selected definite failure rejects the claim |
| same | `TestFirstPassingSupportCertification::test__result__rejects_false_reported_disposition` | Software verification | A false reported disposition is rejected |
| same | `TestFirstPassingSupportCertification::test__result__requires_distinct_retained_artifacts` | Software verification | Producer and verifier artifacts must differ |

## Sphinx mapping

| Sphinx path | Documented route | Role |
|---|---|---|
| `doc/sphinx/api/certifications.rst` | `ksdft2effmass.certifications.periodic1d.rank1.first_passing_support` | Canonical API page |

## Provenance

Original local work under the repository license.

## Evidence

| Evidence kind | Status | Evidence or reason | Reference | Comparator/tolerance | Environment | Validity domain | Accepting authority |
|---|---|---|---|---|---|---|---|
| Software verification | Supported | Complete synthetic interval-table and separation cases | Mapped pytest nodes | Exact rational and enum equality | Python test environment | Frozen supports, objectives, and threshold | Not applicable |
| Numerical verification | Not evaluated | No independent enclosure containment replay exists | None | Not applicable | Not applicable | Not evaluated | Not applicable |
| Scientific validation | Not evaluated | No parent-model or material adequacy assessment | None | Not applicable | Not applicable | Not evaluated | Not applicable |
| Uncertainty quantification | Not applicable | Intervals are rigorous-bound claims, not uncertainty distributions | None | Not applicable | Not applicable | Bound representation | Not applicable |
| Human acceptance | Not evaluated | Endpoint acceptance is not human acceptance | None | Not applicable | Not applicable | Not evaluated | Named human authority required |

## Limitations and deviations

No maintained producer or independent containment verifier currently exists, and the
checked runtime-certification count is zero. The result cannot support continuum,
off-mesh, material, rank-two, or publication claims.

## Detail navigation

- [Records module](../index.md)
- [Shared implementation](../../../../../implementation.md)
- [Shared numerics](../../../../../numerics.md)
- [Shared scientific interpretation](../../../../../scientifics.md)
