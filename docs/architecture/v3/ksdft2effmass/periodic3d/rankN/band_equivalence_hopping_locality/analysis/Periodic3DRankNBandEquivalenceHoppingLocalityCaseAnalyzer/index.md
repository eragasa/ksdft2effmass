# `Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalyzer`

## Status and responsibility

Implemented request-bound action object in
`ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.analysis`.
It consumes one explicit `Periodic3DRankNParentGaugeCase`, composing a supplied
`Periodic3DRankNParentModel` with an independently applicable
`Periodic3DRankNGivensGaugeTransformation`, gauge-alignment routes, frame transport,
Fourier reconstruction, physical-metric shell powers, support decisions, and immutable
case analysis without filesystem effects. The transformation owner accepts arbitrary
admitted periodic-3D finite-rank frame and represented-operator fields; it is not a
parent-model operation. `Periodic3DRankNBandEquivalenceFieldSamples` is the
parent-independent
analysis boundary. `Periodic3DRankNBandEquivalenceHoppingLocalityFieldAnalyzer`
consumes that boundary together with parent-independent numerical policy and geometry.
The construction field remains a regular centered tensor mesh for the finite transform;
the evaluation field may instead be any ordered reciprocal-point inventory. The
parent-independent policy also carries an explicit axis-ordered
`ReciprocalEndpointSewingInventory`. Frame transport validates three axis maps and the
ambient field dimension, then consumes the supplied sewing without constructing
identity internally. The field result excludes parent scale, transformation coefficient,
external-gap evidence, and study-case identity.
`Periodic3DRankNParentGaugeCaseFieldSampler` adapts the supplied correlated case to the
field boundary and carries the parent-owned structured basis display identity.
`Periodic3DRankNWannierFieldProducer` adapts immutable in-memory Wannier frames and
represented operators, with explicit frame-isometry and operator-Hermiticity tolerances
and an optional independent Givens transformation. It makes no provenance, convergence,
or material-validation claim. The case analyzer is a thin adapter that restores the
study-specific result envelope. Concrete analytic formulas, basis inventories, PhysKit
block-hopping construction, and request cross-product expansion are not reusable-source
owners; they remain calculation or verification support. Synthetic lattice and metric
controls are selected through `Periodic3DRankNLatticeControlEnum`, not tuple position.

## Deferred numerical limitation

The locality summary currently derives normalized non-onsite power as
`max(0.0, total_power - onsite_power)` after total and onsite powers have been rounded
separately. Under the selected bounded baseline this can suppress only roundoff-scale
power and does not affect support selection, which uses direct shell sums. A reported
zero is therefore not proof that all nonzero-displacement hopping blocks vanish.

This limitation is tracked as
[`TD-BEL-003`](../../../../../../../../tasks/tech_debt/band-equivalence-locality/index.md#td-bel-003-rank-n-non-onsite-summary-subtraction).

## Mapping and evidence

- Analyzer source: `python/src/ksdft2effmass/periodic3d/rankN/band_equivalence_hopping_locality/analysis.py`
- Parent contract: `python/src/ksdft2effmass/periodic/periodic3d/rankN/models/base.py`
- Correlated case source: `python/src/ksdft2effmass/periodic3d/rankN/band_equivalence_hopping_locality/case.py`
- Transformation source: `python/src/ksdft2effmass/periodic3d/rankN/gauge_alignment/transformation.py`
- Sampled-field source: `python/src/ksdft2effmass/periodic3d/rankN/band_equivalence_hopping_locality/represented_fields.py`
- Field-geometry source: `python/src/ksdft2effmass/periodic3d/rankN/band_equivalence_hopping_locality/field_geometry.py`
- Generic policy source: `python/src/ksdft2effmass/periodic3d/rankN/band_equivalence_hopping_locality/policy.py`
- Wannier adapter source: `python/src/ksdft2effmass/periodic3d/rankN/band_equivalence_hopping_locality/wannier_fields.py`
- Analyzer test: `python/tests/ksdft2effmass/periodic3d/rankN/test__Periodic3DRankNBandEquivalenceHoppingLocalityAnalyzer.py`
- Test-owned analytic support: `python/tests/periodic3d_rankn_analytic_case_support.py`
- Test-owned block-hopping support: `python/tests/periodic3d_rankn_block_hopping_parent_support.py`
- Case test: `python/tests/ksdft2effmass/periodic3d/rankN/test__Periodic3DRankNParentGaugeCase.py`
- Transformation test: `python/tests/ksdft2effmass/periodic3d/rankN/test__Periodic3DRankNGivensGaugeTransformation.py`
- Sampled-field test: `python/tests/ksdft2effmass/periodic3d/rankN/test__Periodic3DRankNBandEquivalenceFieldSamples.py`
- Generic analyzer tests: `python/tests/ksdft2effmass/periodic3d/rankN/test__Periodic3DRankNBandEquivalenceHoppingLocalityAnalyzer.py`
- Wannier adapter test: `python/tests/ksdft2effmass/periodic3d/rankN/test__Periodic3DRankNWannierFieldProducer.py`
- Sphinx: `doc/sphinx/api/band-equivalence-hopping-locality.rst`
- Evidence status: bounded software and numerical verification only; no retained
  production execution or scientific validation is authorized.

## Related pages

- [Numerics](numerics.md)
- [Scientific interpretation](scientifics.md)
- [Schematic](schematics.md)
