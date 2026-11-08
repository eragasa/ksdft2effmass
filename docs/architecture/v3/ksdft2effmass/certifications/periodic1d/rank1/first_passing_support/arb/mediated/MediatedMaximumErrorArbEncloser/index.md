# `MediatedMaximumErrorArbEncloser`

## Contract

Frozen, slotted ActionObject enclosing the transform-mediated total maximum evaluation
error at one support. Supported import:
`ksdft2effmass.certifications.periodic1d.rank1.first_passing_support.arb.MediatedMaximumErrorArbEncloser`.

## Identity and invariants

Support is a built-in dimensionless integer in `0..15`; precision is at least 64 bits.
The parent, meshes, Fourier signs, evaluation shift, energy reference, and unit are fixed.

## Dependencies and flow

The action imports optional Python-FLINT and reuses the parent enclosure mechanics. It
encloses all 256 construction parent values, computes retained Fourier coefficients,
evaluates the support-restricted candidate and parent at all 1025 staggered coordinates,
and exports `[max lower, max upper]` with endpoint-driver indices.

## Serialization

The action is not serialized. It returns `MediatedMaximumErrorEnclosure` through the
repository-native record boundary.

## Scientific boundary

The action covers transform-mediated total maximum error only. It does not enclose the
equal-weight direct fit, prove joint first passage, independently verify its own output,
or persist a certification artifact.

## Code, test, and Sphinx mappings

| Surface | Mapping |
|---|---|
| Code | `python/src/ksdft2effmass/certifications/periodic1d/rank1/first_passing_support/arb/mediated.py` |
| Test | `TestPeriodic1DRank1FirstPassingSupportArb::test__mediated_encloser__separates_supports_ten_and_eleven` |
| Sphinx | `doc/sphinx/api/certifications.rst` |

## Provenance and evidence

Original local implementation adapted from reviewed feasibility work under the
repository license. Tests establish that the mediated support-10 lower endpoint exceeds
and support-11 upper endpoint does not exceed the exact `1e-8 E_ref` threshold.

## Limitations

The threshold separation is not a joint certification because the direct objective is
absent. Python-FLINT precision is process-global and no independent containment verifier
is implemented here.

## Navigation

- [Mediated module](../index.md)
- [Arb capability](../../index.md)
