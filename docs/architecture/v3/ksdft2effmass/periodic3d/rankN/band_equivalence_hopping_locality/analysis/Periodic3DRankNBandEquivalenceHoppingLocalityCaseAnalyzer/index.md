# `Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalyzer`

## Status and responsibility

Implemented request-bound action object in
`ksdft2effmass.periodic3d.rankN.band_equivalence_hopping_locality.analysis`.
It composes one exact periodic-3D PhysKit `DenseBlockHoppingModel` parent with the
independently applicable `Periodic3DRankNGivensGaugeAttack`, gauge-alignment routes, frame transport, Fourier
reconstruction, physical-metric shell powers, support decisions, and immutable case
analysis without filesystem effects. The attack owner accepts arbitrary admitted
periodic-3D finite-rank frame and represented-operator fields; it is not a parent-model
operation. `Periodic3DRankNBandEquivalenceFieldSamples` is the parent-independent
analysis boundary. `Periodic3DRankNBandEquivalenceHoppingLocalityFieldAnalyzer`
consumes that boundary together with parent-independent numerical policy and geometry.
The construction field remains a regular centered tensor mesh for the finite transform;
the evaluation field may instead be any ordered reciprocal-point inventory. The
analyzer does not admit a synthetic case or parent model. Its field result excludes parent
scale, attack coefficient, external-gap evidence, and synthetic case identity.
`Periodic3DRankNAnalyticCaseFieldSampler` retains its v1 public name while adapting the
synthetic study case to the field boundary. `Periodic3DRankNWannierFieldProducer`
adapts immutable in-memory Wannier frames and represented operators, with explicit
frame-isometry and operator-Hermiticity tolerances and an optional independent Givens
attack. It makes no provenance, convergence, or material-validation claim. The existing
case analyzer is now a thin
adapter that restores the unchanged v1 synthetic result envelope.
`Periodic3DRankNBlockHoppingParentBuilder` constructs the parent onsite and finite-range
hopping blocks; the attack is not an input to that construction. Synthetic lattice and
metric controls are selected through
`Periodic3DRankNLatticeControlEnum`, not tuple position.

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
- Parent source: `python/src/ksdft2effmass/periodic3d/rankN/band_equivalence_hopping_locality/parent.py`
- Attack source: `python/src/ksdft2effmass/periodic3d/rankN/gauge_alignment/attack.py`
- Sampled-field source: `python/src/ksdft2effmass/periodic3d/rankN/band_equivalence_hopping_locality/represented_fields.py`
- Field-geometry source: `python/src/ksdft2effmass/periodic3d/rankN/band_equivalence_hopping_locality/field_geometry.py`
- Generic policy source: `python/src/ksdft2effmass/periodic3d/rankN/band_equivalence_hopping_locality/policy.py`
- Wannier adapter source: `python/src/ksdft2effmass/periodic3d/rankN/band_equivalence_hopping_locality/wannier_fields.py`
- Analyzer test: `python/tests/ksdft2effmass/periodic3d/rankN/test__Periodic3DRankNBandEquivalenceHoppingLocalityAnalyzer.py`
- Parent test: `python/tests/ksdft2effmass/periodic3d/rankN/test__Periodic3DRankNBlockHoppingParentBuilder__contracts.py`
- Attack test: `python/tests/ksdft2effmass/periodic3d/rankN/test__Periodic3DRankNGivensGaugeAttack.py`
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
