# `periodic1d.campaign.composite.adoption`

## Purpose and status

This canonical row-059 module retains the implemented row-024/025 scientific-adoption
behavior beside the campaign family that owns its source records. The instantiated
Action adopts already correlated Appendix G composite records into a finite-parent
scientific graph without rerunning or rewriting the historical calculation. No former
underscored or publication compatibility alias is retained.

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
reciprocal matrices are unavailable and are not inferred. The reported retained
smooth-projector digest remains a source-result field, but projector bytes are
unavailable, so adoption cannot authenticate it against projector content.

## Evidence and provenance

The exact historical source group retains isolation, Wilson, gauge, range, route, and
artifact diagnostics. Adoption references rather than reclassifies them. Source and
test paths are `python/src/ksdft2effmass/periodic1d/campaign/composite/adoption.py`
and `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/composite/test__Periodic1DCompositeScientificAdoption.py`; Sphinx coverage is in
`doc/sphinx/api/research-monograph-campaigns.rst`. The exact claim-bearing pytest node
is `python/tests/software_verification/ksdft2effmass/periodic1d/campaign/composite/test__Periodic1DCompositeScientificAdoption.py::TestPeriodic1DCompositeScientificAdoption`.

Original local work under the repository license. Passing establishes source
correlation, authentication of the retained matrix/hopping arrays, and software
ownership only—not projector-content authentication, untruncated-parent accuracy, gauge
validation, scientific validation, UQ, or acceptance.
