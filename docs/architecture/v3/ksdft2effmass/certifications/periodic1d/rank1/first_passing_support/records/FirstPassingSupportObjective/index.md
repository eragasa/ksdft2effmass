# `FirstPassingSupportObjective`

## Purpose and status

Implemented closed Enum identifying the two decisive error objectives in the finite
first-passing-support proposition. Supported import:
`ksdft2effmass.certifications.periodic1d.rank1.first_passing_support.FirstPassingSupportObjective`.

## Public contract

`MEDIATED_TOTAL_MAXIMUM` identifies the transform-mediated candidate's total maximum
evaluation error. `DIRECT_TOTAL_MAXIMUM` identifies the equal-weight direct-fit
candidate's total maximum evaluation error. `to_wire()` and `from_wire()` provide exact
built-in string mapping through `StrWireEnum`.

## State and identity

Member declaration order is scientifically significant: every support contributes the
mediated entry followed by the direct entry. The exact wire labels are retained contract
values and are not aliases or display text.

## Invariants and failure behavior

Only the two declared members are accepted. `from_wire()` rejects non-string values and
unknown labels with `TypeError` or `ValueError`; no normalization or fallback occurs.

## Dependencies and collaborators

The enum depends only on the shared `StrWireEnum` boundary. `FirstPassingIntervalEntry`
and `FirstPassingSupportResult` consume it. It does not depend on Fourier-locality
analysis or an interval provider.

## Data and action flow

Producer and verifier records select one exact member; result classification consumes
both members for every support.

## Serialization and compatibility

Records explicitly project members with `to_wire()` and reconstruct them with
`from_wire()`. Version 1 provides no aliases or dual reads.

## Scientific and numerical boundary

The enum names objectives; it does not calculate either error or establish enclosure
containment.

## Code mapping

| Code path | Symbol kind | Qualified name | Responsibility |
|---|---|---|---|
| `python/src/ksdft2effmass/certifications/periodic1d/rank1/first_passing_support/records.py` | Enum | `ksdft2effmass.certifications.periodic1d.rank1.first_passing_support.FirstPassingSupportObjective` | Closed objective vocabulary and wire labels |

## Test mapping

| Test path | Pytest node | Evidence class | Established behavior |
|---|---|---|---|
| `python/tests/ksdft2effmass/certifications/periodic1d/rank1/test__Periodic1DRank1FirstPassingSupportCertification.py` | `TestFirstPassingSupportCertification::test__result__round_trips_all_32_entries` | Software verification | Both objective labels survive the typed record round trip in canonical order |

## Sphinx mapping

| Sphinx path | Documented route | Role |
|---|---|---|
| `doc/sphinx/api/certifications.rst` | `ksdft2effmass.certifications.periodic1d.rank1.first_passing_support` | Canonical API page |

## Provenance

Original local work under the repository license.

## Evidence

| Evidence kind | Status | Evidence or reason | Reference | Comparator/tolerance | Environment | Validity domain | Accepting authority |
|---|---|---|---|---|---|---|---|
| Software verification | Supported | Typed round-trip and closed result inventory | Mapped pytest node | Exact equality | Python test environment | Two declared labels | Not applicable |
| Numerical verification | Not evaluated | No independent objective-value oracle is run | None | Not applicable | Not applicable | Not evaluated | Not applicable |
| Scientific validation | Not evaluated | Labels do not validate model adequacy | None | Not applicable | Not applicable | Not evaluated | Not applicable |
| Uncertainty quantification | Not applicable | Vocabulary has no uncertainty model | None | Not applicable | Not applicable | Enum identity | Not applicable |
| Human acceptance | Not evaluated | No acceptance decision is encoded | None | Not applicable | Not applicable | Not evaluated | Named human authority required |

## Limitations and deviations

The vocabulary is proposition-specific and cannot represent additional objectives
without a new reviewed contract version.

## Detail navigation

- [Records module](../index.md)
- [Shared numerics](../../../../../numerics.md)
- [Shared scientific interpretation](../../../../../scientifics.md)
