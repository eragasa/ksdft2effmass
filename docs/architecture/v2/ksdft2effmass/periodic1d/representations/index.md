# `periodic1d.representations`

## Purpose and status

This implemented module binds an exact one-dimensional retained operator to complete
finite reciprocal-mesh or real-space hopping coordinates. It owns represented scientific
meaning, not the underlying reusable arrays or their numerical transform.

## Public inventory

| Symbol | Category | Responsibility |
|---|---|---|
| `Periodic1DRetainedOperatorReciprocalRepresentation` | Represented retained operator | Complete ordered reciprocal matrices with basis, gauge, energy reference, map, provenance, and content identity |
| `Periodic1DRetainedOperatorHoppingRepresentation` | Represented retained operator | Complete centered Born--von Karman hopping family with the same explicit interpretation metadata |

## Class navigation

- [`Periodic1DRetainedOperatorReciprocalRepresentation`](Periodic1DRetainedOperatorReciprocalRepresentation/index.md)
- [`Periodic1DRetainedOperatorHoppingRepresentation`](Periodic1DRetainedOperatorHoppingRepresentation/index.md)

## Scientific separation

`ReciprocalOperatorSamples1D` and `BlockHoppingModel1D` remain role-neutral numerical
data. These bindings state which exact retained operator they represent and in which
ordered basis and gauge. The complete hopping-family binding is distinct from
`Periodic1DCompleteHoppingRepresentationResult`: the latter owns an actual Fourier
construction route, source samples, reconstruction, and numerical diagnostics.

## Code, tests, and Sphinx

| Kind | Path | Responsibility |
|---|---|---|
| Code | `python/src/ksdft2effmass/periodic1d/representations.py` | Intrinsic represented-operator bindings |
| Tests | `python/tests/software_verification/ksdft2effmass/campaigns/periodic_1d/test__Periodic1DCompositeScientificAdoption.py` | Retained composite represented forms and negative metadata cases |
| Sphinx | `doc/sphinx/api/ksdft2effmass/periodic1d/representations.rst` | Public API and exact-versus-route distinction |

## Provenance and claim boundary

Original local work under the repository license. Composite adoption authenticates
historical retained arrays. Successful construction establishes exact software
correlation and observed-content identity, not independent historical provenance,
gauge quality, convergence, physical adequacy, scientific validation, uncertainty
quantification, or acceptance.
