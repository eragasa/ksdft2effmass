# `ControlledParentLowestEigenvalueEnclosure`

## Contract

Immutable result record for one exact reduced momentum, Arb precision, and isolated
lowest-eigenvalue interval. Supported import:
`ksdft2effmass.certifications.periodic1d.rank1.first_passing_support.arb.ControlledParentLowestEigenvalueEnclosure`.

## Identity and invariants

The coordinate is an exact dimensionless rational, precision is a built-in integer of at
least 64 bits, and the interval is a `SignedExactInterval` in `E_ref`.

## Dependencies and flow

`ControlledParentLowestEigenvalueArbEncloser.execute()` constructs this value. It depends
on core exact rationals and repository-native serialization, not on filesystem state.

## Serialization

The record owns its typed mapping and uses final canonical JSON from `BaseTypedRecord`.
No compatibility alias, custom codec, or dual read exists.

## Scientific boundary

It encloses one finite matrix eigenvalue for the frozen parent. It does not establish a
band-isolation theorem over a continuum or validate the parent physically.

## Code, test, and Sphinx mappings

| Surface | Mapping |
|---|---|
| Code | `python/src/ksdft2effmass/certifications/periodic1d/rank1/first_passing_support/arb/records.py` |
| Test | `TestPeriodic1DRank1FirstPassingSupportArb::test__parent_encloser__agrees_with_binary64_control` and record round trip |
| Sphinx | `doc/sphinx/api/certifications.rst` |

## Provenance and evidence

Original local implementation under the repository license. Tests establish software
agreement with a binary64 control within an explicit `1e-14 E_ref` tolerance, not
scientific correctness.

## Limitations

The value carries no producer source digest or retained artifact identity and therefore
cannot serve as a certification artifact by itself.

## Navigation

- [Arb records](../index.md)
- [Arb capability](../../index.md)
