# `periodic1d.campaign.composite_adoption`

## Purpose and status

This is the canonical target page for the implemented row-024/025 adoption behavior.
Its source remains temporarily in legacy
`ksdft2effmass.campaigns.periodic_1d.composite_adoption` until row 059 moves the
campaign family without an alias. The Action adopts already correlated Appendix G
composite records into a finite-parent scientific graph without rerunning or rewriting
the historical calculation.

## Public inventory

| Symbol | Category | Responsibility |
|---|---|---|
| `Periodic1DCompositeScientificAdoptionRequest` | Action request | Exact correlated campaign source |
| `Periodic1DCompositeScientificAdoption` | ActionObject | Construct finite parent, retained spaces/operators, and available gauge forms |
| `Periodic1DCompositeScientificAdoptionResult` | Action result | Preserve the parent and ordered adopted groups |
| `Periodic1DCompositeOperatorGroupAdoption` | Adoption aggregate | Correlate one exact operator, source diagnostics, and three represented forms |

## Class navigation

- [`Periodic1DCompositeScientificAdoptionRequest`](Periodic1DCompositeScientificAdoptionRequest/index.md)
- [`Periodic1DCompositeScientificAdoption`](Periodic1DCompositeScientificAdoption/index.md)
- [`Periodic1DCompositeScientificAdoptionResult`](Periodic1DCompositeScientificAdoptionResult/index.md)
- [`Periodic1DCompositeOperatorGroupAdoption`](Periodic1DCompositeOperatorGroupAdoption/index.md)

## Scientific and unavailable-data boundary

The cutoff-15, dimension-31, 128-point finite plane-wave operator is distinct from the
untruncated Fourier parent. Each rank-two group defines an exact invariant restriction
only of that finite operator. Smooth reciprocal matrices and smooth/rough complete
hoppings are available. Smooth and rough frame bytes, projector coordinates, and rough
reciprocal matrices are unavailable and are not inferred. The retained smooth-projector
digest remains campaign evidence.

## Evidence and provenance

The exact historical source group retains isolation, Wilson, gauge, range, route, and
artifact diagnostics. Adoption references rather than reclassifies them. Source and
test paths are `python/src/ksdft2effmass/campaigns/periodic_1d/composite_adoption.py`
and `python/tests/software_verification/ksdft2effmass/campaigns/periodic_1d/test__Periodic1DCompositeScientificAdoption.py`; Sphinx coverage is in
`doc/sphinx/api/research-monograph-campaigns.rst`.

Original local work under the repository license. Passing establishes source
correlation, observed-content authentication, and software ownership only—not
untruncated-parent accuracy, gauge validation, scientific validation, UQ, or acceptance.
