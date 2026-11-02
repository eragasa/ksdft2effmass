# Periodic-2D finite-rank calculations

**Status: PROSPECTIVE — NO CALCULATION OR EVIDENCE**

This root is reserved for separately reviewed periodic-2D retained-rank-\(N\)
calculations governed by the dimension-indexed arbitrary-finite-rank construction in
Ragasa2026c. It is not an alias for the installed Ragasa2026b rank-two calculations and
does not change their requests, results, verification records, or retained bytes.

The reusable finite-rank operator and ordered-spectrum loss definition is
`BandEquivalenceHoppingLocalityLossDefinition`; `BandEquivalenceHoppingLocalityLoss` composes that
definition with calculated values. The definition uses the Ragasa2026c cross-rank
quadratic normalization \(rE_{\mathrm{norm}}^2\), with `norm_energy_scale` declaring
\(E_{\mathrm{norm}}>0\); its rank-two specialization is exactly the Ragasa2026a loss.
Its typed identity separately retains the reciprocal-sample inventory, retained space,
basis, gauge, geometry, energy unit, and common energy-zero/alignment convention. Those
software values alone are not a periodic-2D rank-\(N\) calculation.

Any installed calculation below this root must compose the common scientific bases rather
than create calculation-local substitutes:

- `SubspaceReduction` for the declared parent-to-retained-space map;
- `RepresentationEquivalence` for aligned represented-operator comparisons;
- `RealSpaceSupportTruncation` for complete metric-shell support removal and
  minimum-tolerance support selection; and
- `NumericalConsistency` for reciprocal-mesh and independent-route assessments.

`BaseTypedRecord` remains a serialization boundary only. SHA-256 establishes byte
identity, not scientific validity.

## Open protocol decisions

The calculation-owned decision register is
[`protocol-selection.md`](protocol-selection.md), with an exact analytic recommendation
in [`recommended-baseline.md`](recommended-baseline.md). The prospective family boundary is
[`composite-band-alignment-locality/`](composite-band-alignment-locality/README.md).

Ragasa2026c selects a later cross-dimensional rank/depth subset but explicitly does not
select the periodic-2D harmonic coefficients, tensor meshes, support inventory, family
identity, or evidence status. Those decisions remain scientifically open and will not be
inferred from the periodic-1D higher-rank protocol or the periodic-2D rank-two controls.
Consequently, this root contains no calculation, verification, or rendering entrypoint.

Production execution, retained-result creation, sealing, promotion, and publication
require separate explicit authorization after the periodic-2D protocol and implementation
have been reviewed.
