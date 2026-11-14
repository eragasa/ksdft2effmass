# `SignedExactInterval`

## Contract

Immutable `BaseTypedRecord` storing one signed closed exact interval. Supported import:
`ksdft2effmass.certifications.periodic1d.rank1.first_passing_support.arb.SignedExactInterval`.

## Identity and invariants

Both endpoints are reduced `ExactRational` values and the lower endpoint cannot exceed
the upper endpoint. Arbitrary-precision Python integers avoid fixed-width overflow.

## Dependencies and flow

The record depends only on the core exact-rational value and shared serialization. Parent
Arb output is converted into this record after eigenvalue isolation.

## Serialization

Domain-owned `_mapping()` and `_from_mapping()` use final `BaseTypedRecord` dictionary
and canonical JSON methods. No parallel schema or codec exists.

## Scientific boundary

The value can represent signed energy intervals in `E_ref`; construction validates
structure and ordering, not numerical containment.

## Code, test, and Sphinx mappings

| Surface | Mapping |
|---|---|
| Code | `python/src/ksdft2effmass/certifications/periodic1d/rank1/first_passing_support/arb/records.py` |
| Test | `TestPeriodic1DRank1FirstPassingSupportArb::test__enclosure_records__round_trip_canonical_bytes` |
| Sphinx | `doc/sphinx/api/certifications.rst` |

## Provenance and evidence

Original local implementation under the repository license. Software tests establish
canonical round trips only.

## Limitations

The record has no unit field because the enclosing proposition fixes `E_ref`. It is not a
generic interval-arithmetic type.

## Navigation

- [Arb records](../index.md)
- [Arb capability](../../index.md)
