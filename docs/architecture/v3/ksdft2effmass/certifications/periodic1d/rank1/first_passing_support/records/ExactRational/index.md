# `ExactRational`

## Purpose and status

Implemented immutable DataObject for one reduced exact rational endpoint. Supported
import:
`ksdft2effmass.certifications.periodic1d.rank1.first_passing_support.ExactRational`.

## Public contract

The constructor accepts exact built-in integer `numerator` and positive built-in integer
`denominator`. `as_fraction()` returns the equivalent `fractions.Fraction`. Final
`BaseTypedRecord` methods provide typed mapping and JSON round trips.

## State and identity

Identity is the unique reduced pair `(numerator, denominator)`. Zero is canonicalized as
`0/1`. Python integers are arbitrary precision; booleans and NumPy integer scalars are
not admitted.

## Invariants and failure behavior

Construction rejects wrong scalar types, nonpositive denominators, nonreduced values,
and noncanonical zero. It raises `TypeError` for type violations and `ValueError` for
value violations.

## Dependencies and collaborators

The value depends on `BaseTypedRecord`, `math.gcd`, and `fractions.Fraction` only.
`NonnegativeExactInterval` composes two values.

## Data and action flow

Integer fields enter the constructor, are normalized only by rejection, map to the
shared typed JSON boundary, and reconstruct without a binary floating-point conversion.

## Serialization and compatibility

The typed mapping is exactly `numerator` plus `denominator`. No decimal, float, alias,
default, or compatibility read is supported.

## Scientific and numerical boundary

The class preserves exact endpoint arithmetic. It does not establish that an endpoint
is a valid outward bound. There is no fixed-width arithmetic overflow; adversarial wire
size remains an operational resource concern.

## Code mapping

| Code path | Symbol kind | Qualified name | Responsibility |
|---|---|---|---|
| `python/src/ksdft2effmass/certifications/periodic1d/rank1/first_passing_support/records.py` | Class | `ksdft2effmass.certifications.periodic1d.rank1.first_passing_support.ExactRational` | Reduced exact rational record |
| same | Method | `ExactRational.as_fraction` | Exact standard-library rational projection |

## Test mapping

| Test path | Pytest node | Evidence class | Established behavior |
|---|---|---|---|
| `python/tests/ksdft2effmass/certifications/periodic1d/rank1/test__Periodic1DRank1FirstPassingSupportCertification.py` | `TestFirstPassingSupportCertification::test__exact_rational__rejects_nonreduced_value` | Software verification | Nonreduced rationals are rejected |
| same | `TestFirstPassingSupportCertification::test__request__round_trips_typed_mapping_and_json` | Software verification | Exact threshold numerator and denominator survive JSON serialization |

## Sphinx mapping

| Sphinx path | Documented route | Role |
|---|---|---|
| `doc/sphinx/api/certifications.rst` | `ksdft2effmass.certifications.periodic1d.rank1.first_passing_support` | Canonical API page |

## Provenance

Original local work under the repository license.

## Evidence

| Evidence kind | Status | Evidence or reason | Reference | Comparator/tolerance | Environment | Validity domain | Accepting authority |
|---|---|---|---|---|---|---|---|
| Software verification | Supported | Constructor rejection and exact wire round trip | Mapped pytest nodes | Exact integer equality | Python test environment | Reduced integer pairs | Not applicable |
| Numerical verification | Not applicable | The record performs exact rational construction only | None | Exact arithmetic | Python integers | Representable wire values | Not applicable |
| Scientific validation | Not applicable | No physical model claim is represented | None | Not applicable | Not applicable | Data representation | Not applicable |
| Uncertainty quantification | Not applicable | No uncertainty model | None | Not applicable | Not applicable | Data representation | Not applicable |
| Human acceptance | Not applicable | No human decision | None | Not applicable | Not applicable | Data representation | Not applicable |

## Limitations and deviations

The value has no unit field; the enclosing proposition supplies `E_ref` where the
rational is used as an error endpoint.

## Detail navigation

- [Records module](../index.md)
- [Shared numerics](../../../../../numerics.md)
