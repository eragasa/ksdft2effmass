# `MediatedMaximumErrorEnclosure`

## Contract

Immutable result record for one support's mediated total maximum evaluation error.
Supported import:
`ksdft2effmass.certifications.periodic1d.rank1.first_passing_support.arb.MediatedMaximumErrorEnclosure`.

## Identity and invariants

Support is a built-in dimensionless integer in `0..15`; precision is at least 64 bits;
the error interval is nonnegative and measured in `E_ref`; endpoint-driver indices lie
inside the frozen 1025-point evaluation mesh. Properties expose the fixed 256 and 1025
mesh sizes.

## Dependencies and flow

`MediatedMaximumErrorArbEncloser.execute()` creates the record after aggregating all
pointwise residual balls. The record itself imports no interval provider.

## Serialization

The record uses domain-owned typed mappings and final canonical JSON. No standalone
schema or proposition-specific codec exists.

## Scientific boundary

It covers the mediated objective only. It is not a direct-fit enclosure, joint first-pass
decision, independently verified artifact, or retained certificate.

## Code, test, and Sphinx mappings

| Surface | Mapping |
|---|---|
| Code | `python/src/ksdft2effmass/certifications/periodic1d/rank1/first_passing_support/arb/records.py` |
| Test | `TestPeriodic1DRank1FirstPassingSupportArb::test__mediated_encloser__separates_supports_ten_and_eleven` and record round trip |
| Sphinx | `doc/sphinx/api/certifications.rst` |

## Provenance and evidence

Original local implementation under the repository license. Tests establish local
finite-mesh software behavior only.

## Limitations

Driver indices need not identify a unique physical extremum. The record has no producer
identity, source digest, or persistence path.

## Navigation

- [Arb records](../index.md)
- [Arb capability](../../index.md)
