# `CertificationToolIdentity`

## Purpose and status

Implemented immutable DataObject identifying one enclosure producer or independent
containment verifier. Supported import:
`ksdft2effmass.certifications.periodic1d.rank1.first_passing_support.CertificationToolIdentity`.

## Public contract

The constructor requires portable `identity` and `version` strings and one lowercase
SHA-256 source digest. Final `BaseTypedRecord` methods own mapping and JSON serialization.

## State and identity

Identity is the exact triple `(identity, version, source_sha256)`. The result additionally
requires producer and verifier logical identities and source digests to differ.

## Invariants and failure behavior

Identifiers use `[A-Za-z0-9][A-Za-z0-9._:-]{0,127}`. The digest uses exactly 64 lowercase
hexadecimal characters. Wrong types raise `TypeError`; malformed values raise
`ValueError`.

## Dependencies and collaborators

The value depends on `BaseTypedRecord` only. `FirstPassingSupportResult` composes one
producer and one verifier identity and enforces separation.

## Data and action flow

Implementation identity and authenticated source bytes produce the three fields. The
result correlates those fields with separately hashed producer and verifier artifacts.

## Serialization and compatibility

The mapping contains exactly `identity`, `version`, and `source_sha256`. No inferred
version, source discovery, alias, or fallback is supported.

## Scientific and numerical boundary

A source digest establishes byte identity, not correctness, independence, containment,
or scientific adequacy.

## Code mapping

| Code path | Symbol kind | Qualified name | Responsibility |
|---|---|---|---|
| `python/src/ksdft2effmass/certifications/periodic1d/rank1/first_passing_support/records.py` | Class | `ksdft2effmass.certifications.periodic1d.rank1.first_passing_support.CertificationToolIdentity` | Producer/verifier implementation identity |

## Test mapping

| Test path | Pytest node | Evidence class | Established behavior |
|---|---|---|---|
| `python/tests/ksdft2effmass/certifications/periodic1d/rank1/test__Periodic1DRank1FirstPassingSupportCertification.py` | `TestFirstPassingSupportCertification::test__result__requires_distinct_producer_and_verifier` | Software verification | Logical producer and verifier identities must differ |
| same | `TestFirstPassingSupportCertification::test__result__requires_source_distinct_producer_and_verifier` | Software verification | Producer and verifier source digests must differ |

## Sphinx mapping

| Sphinx path | Documented route | Role |
|---|---|---|
| `doc/sphinx/api/certifications.rst` | `ksdft2effmass.certifications.periodic1d.rank1.first_passing_support` | Canonical API page |

## Provenance

Original local work under the repository license.

## Evidence

| Evidence kind | Status | Evidence or reason | Reference | Comparator/tolerance | Environment | Validity domain | Accepting authority |
|---|---|---|---|---|---|---|---|
| Software verification | Supported | Producer/verifier separation assertions | Mapped pytest nodes | Exact identity and digest inequality | Python test environment | Synthetic identities | Not applicable |
| Numerical verification | Not applicable | Identity record performs no numerical method | None | Not applicable | Not applicable | Identity representation | Not applicable |
| Scientific validation | Not applicable | Digest identity is not validation | None | Not applicable | Not applicable | Identity representation | Not applicable |
| Uncertainty quantification | Not applicable | No uncertainty model | None | Not applicable | Not applicable | Identity representation | Not applicable |
| Human acceptance | Not evaluated | Distinct identities do not establish accepted independence | None | Not applicable | Not applicable | Not evaluated | Named human authority required |

## Limitations and deviations

The record authenticates source bytes only. It does not capture build flags, runtime
environment, executable bytes, or organizational independence; those belong to retained
artifacts and provenance.

## Detail navigation

- [Records module](../index.md)
- [Shared implementation](../../../../../implementation.md)
