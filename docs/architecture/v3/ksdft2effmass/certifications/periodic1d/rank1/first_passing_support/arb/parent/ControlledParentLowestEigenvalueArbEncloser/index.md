# `ControlledParentLowestEigenvalueArbEncloser`

## Contract

Frozen, slotted ActionObject enclosing the lowest eigenvalue of the exact controlled
four-state parent at one exact coordinate. Supported import:
`ksdft2effmass.certifications.periodic1d.rank1.first_passing_support.arb.ControlledParentLowestEigenvalueArbEncloser`.

## Identity and invariants

Inputs are an `ExactRational` dimensionless coordinate and built-in integer precision of
at least 64 bits. The action accepts no alternate parent coefficients, basis, unit, or
energy reference.

## Dependencies and flow

The action imports optional `python-flint==0.9.0`, forms the exact rational 4-by-4 parent,
uses the Rump eigenvalue enclosure, requires four real-axis balls, and fails unless one
lowest ball is isolated. It exports midpoint-radius balls to exact rational endpoints
with guard digits.

## Serialization

The action is not serialized. Its output is
`ControlledParentLowestEigenvalueEnclosure`, using the shared final record boundary.

## Scientific boundary

The action encloses one finite represented operator eigenvalue. It does not establish
continuum isolation, direct or mediated locality, model adequacy, or material validity.

## Code, test, and Sphinx mappings

| Surface | Mapping |
|---|---|
| Code | `python/src/ksdft2effmass/certifications/periodic1d/rank1/first_passing_support/arb/parent.py` |
| Test | `TestPeriodic1DRank1FirstPassingSupportArb::test__parent_encloser__agrees_with_binary64_control` |
| Sphinx | `doc/sphinx/api/certifications.rst` |

## Provenance and evidence

Original local implementation adapted from reviewed feasibility work under the
repository license. The software test comparator is absolute `1e-14 E_ref` against a
binary64 control and does not certify the control value.

## Limitations

Python-FLINT precision is process-global; threaded concurrent use is unsupported. No
independent implementation verifies the returned interval in this tranche.

## Navigation

- [Parent module](../index.md)
- [Arb capability](../../index.md)
