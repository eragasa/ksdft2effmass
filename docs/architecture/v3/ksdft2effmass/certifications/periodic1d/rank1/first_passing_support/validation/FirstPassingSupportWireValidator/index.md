# `FirstPassingSupportWireValidator`

## Purpose and status

Implemented stateless ActionObject for canonical request/result byte admission and
cross-record correlation. Supported import:
`ksdft2effmass.certifications.periodic1d.rank1.first_passing_support.FirstPassingSupportWireValidator`.

## Public contract

`validate(request_wire, result_wire)` accepts exact built-in `bytes` values and returns
`FirstPassingSupportWireValidation`. It decodes through the records' final `from_json()`
methods, requires exact canonical reserialization, hashes admitted bytes, verifies the
result's request digest, and checks certification identity and selected support.

## State and identity

The action has no mutable state or filesystem location. `CONTRACT_ID` identifies the
single certification contract it validates.

## Invariants and failure behavior

Wrong wire or decoded field types raise `TypeError`. Invalid JSON, noncanonical bytes,
record invariants, request-digest mismatch, certification-identity mismatch, or support
mismatch raise `ValueError`. Validation fails closed and supplies no fallback or
normalization.

## Dependencies and collaborators

The action depends on `FirstPassingSupportRequest`, `FirstPassingSupportResult`,
`FirstPassingSupportWireValidation`, the shared typed JSON boundary, and standard-library
SHA-256. It performs no interval arithmetic and imports no enclosure provider.

## Data and action flow

1. Decode both wires through their domain records.
2. Reserialize and require byte equality to admit one canonical representation.
3. Hash the admitted request and compare it with `result.request_sha256`.
4. Correlate certification identity and selected support.
5. Hash the admitted result and return the typed validation record.

## Serialization and compatibility

The action owns no serializer. It consumes the final record-owned JSON boundary. Version
1 accepts no standalone JSON Schema, custom codec, legacy bytes, alias, or dual read.

## Scientific and numerical boundary

Success establishes software-level structural correlation only. The action does not
read producer or verifier artifacts, establish interval containment, rerun numerical
verification, validate the parent model, or grant scientific or human acceptance.

## Code mapping

| Code path | Symbol kind | Qualified name | Responsibility |
|---|---|---|---|
| `python/src/ksdft2effmass/certifications/periodic1d/rank1/first_passing_support/validation.py` | Class | `ksdft2effmass.certifications.periodic1d.rank1.first_passing_support.FirstPassingSupportWireValidator` | Canonical byte admission and correlation |
| same | Method | `FirstPassingSupportWireValidator.validate` | Validate one exact request/result pair |

## Test mapping

| Test path | Pytest node | Evidence class | Established behavior |
|---|---|---|---|
| `python/tests/ksdft2effmass/certifications/periodic1d/rank1/test__Periodic1DRank1FirstPassingSupportCertification.py` | `TestFirstPassingSupportCertification::test__wire_validator__correlates_request_and_result_bytes` | Software verification | Canonical correlated bytes are admitted |
| same | `TestFirstPassingSupportCertification::test__wire_validator__rejects_noncanonical_request_bytes` | Software verification | Equivalent noncanonical request bytes are rejected |
| same | `TestFirstPassingSupportCertification::test__wire_validator__rejects_request_digest_mismatch` | Software verification | Result must bind the exact request digest |
| same | `TestFirstPassingSupportCertification::test__wire_validator__rejects_certificate_identity_mismatch` | Software verification | Certification identity must correlate |
| same | `TestFirstPassingSupportCertification::test__wire_validator__rejects_selected_support_mismatch` | Software verification | Selected support must correlate |
| same | `TestFirstPassingSupportCertification::test__wire_validator__reports_unresolved_without_promoting_it` | Software verification | Unresolved endpoint state is preserved |

## Sphinx mapping

| Sphinx path | Documented route | Role |
|---|---|---|
| `doc/sphinx/api/certifications.rst` | `ksdft2effmass.certifications.periodic1d.rank1.first_passing_support` | Canonical API page |

## Provenance

Original local work under the repository license.

## Evidence

| Evidence kind | Status | Evidence or reason | Reference | Comparator/tolerance | Environment | Validity domain | Accepting authority |
|---|---|---|---|---|---|---|---|
| Software verification | Supported | Canonical, digest, identity, support, and unresolved-state cases | Mapped pytest nodes | Exact bytes, digests, and field equality | Python test environment | Frozen v1 wire pair | Not applicable |
| Numerical verification | Not evaluated | The action performs no containment replay | None | Not applicable | Not applicable | Not evaluated | Not applicable |
| Scientific validation | Not evaluated | No model adequacy assessment | None | Not applicable | Not applicable | Not evaluated | Not applicable |
| Uncertainty quantification | Not applicable | No uncertainty model | None | Not applicable | Not applicable | Structural validation | Not applicable |
| Human acceptance | Not evaluated | Validation grants no operational or publication authority | None | Not applicable | Not applicable | Not evaluated | Named human authority required |

## Limitations and deviations

Canonicality is checked by record reserialization. The action authenticates only the
provided bytes and does not discover retained artifacts or verify their contents.

## Detail navigation

- [Validation module](../index.md)
- [Shared implementation](../../../../../implementation.md)
- [Shared numerics](../../../../../numerics.md)
- [Shared scientific interpretation](../../../../../scientifics.md)
