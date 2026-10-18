# Isotropic 2-D numerical method

## Orbit and transform calculation

The numerical construction reconstructs the complete finite hopping target before
reducing it to square-symmetry orbit coordinates.

- Enumerate the exact eight signed-permutation operations, canonical representatives, and first-occurrence members selected by the [maintained inventory](../../../../../../../experiments/model-adequacy/periodic2d/hopping-shell-hierarchy/orbit-support-inventory.md).
- Verify 36 disjoint orbits, complete coverage, multiplicity sum 225, and the eight prefix counts.
- Apply the positive-exponent, no-forward-normalization Fourier convention.
- Reconstruct the projected source-mesh band and retain its defect.
- Keep raw-source and symmetry-projected diagnostics separate.

## Loss calculation

Both channel losses are represented on the active slice of one maximal coefficient
space.

- Construct spectral design rows from orbit Fourier functions.
- Apply the selected positive square-symmetric weights $1+\frac{3}{4}[2+\cos(2\pi k_x)+\cos(2\pi k_y)]$; all active designs have the disclosed full column rank.
- Construct operator loss from complete block multiplicities.
- Retain omitted target content when a smaller class fixes coefficients to zero.
- Verify direct residual sums against any completed-square representation.

## Sample-role calculation

The [selected role design](../../../../../../../experiments/model-adequacy/periodic2d/hopping-shell-hierarchy/sample-role-design.md) uses:

- 225 ordered objective-construction points on the centered 15-grid;
- 480 even-index-parity evaluation points on the centered 31-grid after removing the origin;
- 480 odd-index-parity withheld points on the centered 31-grid; and
- the complete 225-block/36-orbit real-space inventory for locality diagnostics.

The verifier reconstructs pairwise disjointness, symmetry closure, counts, and ordering.
Diagnostic roles are evaluated only after decisive evidence is fixed and cannot feed any
quadratic or disposition.

## Distance calculation

All classes use the restriction of one normalized complete-block metric.

- Do not renormalize by active parameter count.
- Retain feasible pairs as upper-bound evidence.
- Retain common points as compatibility evidence.
- Reconstruct directional support gaps for lower-bound evidence.
- Compare conservative lower bounds with one frozen resolution.

## Numerical controls still open

The orbit/member ordering, support prefixes, projected coefficients, source tolerances,
coefficient box, spectral weights, maximal-space metric, prospective channel thresholds,
and resolution are selected, but the task must freeze the remaining numerical choices
before source implementation.

- Active-quadratic reconstruction and acceptance tolerances.
- Outward-rounding or exact-enclosure method.
- Producer and verifier tolerances.

## Sources and references

Detailed formulas remain in the legacy design bundle until their implementing classes
are selected and mirrored here.

- [Maintained prospective protocol](../../../../../../../experiments/model-adequacy/periodic2d/hopping-shell-hierarchy/protocol.md).
- [Projection and loss design](../../../../../../../experiments/model-adequacy/periodic2d/hopping-shell-hierarchy/projection-and-loss-design.md).
- [Sample-role design](../../../../../../../experiments/model-adequacy/periodic2d/hopping-shell-hierarchy/sample-role-design.md).
- [Threshold and resolution design](../../../../../../../experiments/model-adequacy/periodic2d/hopping-shell-hierarchy/threshold-design.md).
- [Legacy numerical contract](../../../../ksdft2effmass/analysis/model_adequacy/hopping_shell_hierarchy/numeric.md).
- [Legacy calculation derivation](../../../../ksdft2effmass/analysis/model_adequacy/hopping_shell_hierarchy/scientific.md).
- The future certificate class must record any external convex-optimization or interval-arithmetic reference it implements.
