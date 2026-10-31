# C6-B20-W21 complete-shell spatial-truncation evaluation

This directory is the separately authorized no-calculator S100 evaluation of the
complete shell family frozen by S90. It compares every shell-truncated operator
with the fixed S30 full operator in the same rank-10 Wannier state space.

The evaluation does not select a radius, fit a Slater--Koster model, or consume
direct-parent values from either oracle set.

## Bound source and method

`run_evaluation.py` authenticates the current controlled-reduction protocol, S30
implementation and result, S90 implementation and design, the exact full-operator
artifacts authenticated by S30, and the ProjectKoios parser sources used to
reconstruct the operator. It evaluates all 18 S90 masks without changing them.

For every shell it reports:

- included/excluded representatives, pair closure, pair-Hermiticity, and the
  full-support equality control;
- the spectral triangle tail bound, Frobenius tail, and largest excluded-block
  spectral norm;
- direct operator and ordered-spectrum differences on the frozen Gamma-origin
  `21^3` grid, including the frozen larger-shell envelopes;
- indirect-gap, six signed Delta-family valley, valley-splitting, principal
  curvature, direction-matched mass, and curvature-stencil changes relative to
  the full S30 source.

These are internal `H_W - H_T` diagnostics. They are not parent-model errors or
physical-validation results.

## Result

All 18 declared shells were evaluated. Every mask preserves negative-representative
closure and has zero recorded pair-Hermiticity residual. The onsite-only control has
a flat conduction band, so its valley and effective-mass diagnostics are explicitly
undefined rather than assigned artificial finite values. All optimizers succeeded
for the 17 dispersive shells; the first three dispersive shells do not preserve all
six declared Delta identities. The full-support control reproduces the full operator,
ordered spectrum, valleys, gap, and primary masses exactly in this implementation.

Selected descriptive values near full support are:

| Radius (angstrom) | Representatives | max operator norm (eV) | max all-band error (eV) | gap change (meV) | max primary-mass relative change |
|---:|---:|---:|---:|---:|---:|
| 13.943733109 | 313 | 0.0333827653 | 0.0264242319 | -8.90406 | 43.2503% |
| 14.977972019 | 353 | 0.0175949512 | 0.0111052274 | -2.40554 | 12.0798% |
| 15.945268846 | 365 | 0.00984955325 | 0.00804356145 | -0.0779377 | 1.64969% |
| 16.407546281 | 371 | 0.00355134457 | 0.00203618655 | -0.688908 | 3.36856% |
| 16.857151341 | 383 | 0 | 0 | 0 | 0% |

The observable changes are not monotone shell by shell: for example, the 365-term
shell has smaller gap and primary-mass changes than the 371-term shell. This is a
reason to preserve the frozen direct-metric envelopes and not select a radius from
an isolated favorable observable.

No shell is accepted or rejected here. The separately authorized
[S105 disposition](../c6-b20-w21-spatial-truncation-disposition/) subsequently retained
full support, defining `H_T = H_W` without creating a post-observation threshold. The
separately authorized [S110 attempt](../c6-b20-w21-slater-koster-definition-fit/)
subsequently stopped at its rank-deficient common-space gate without fitting a model.
The 402-point parent values remain unobserved.

## Audit trail

The first launch produced no result because the KSD environment exposed the
ProjectKoios numeric and PhysKit namespaces but not its source-tree integration
namespace. [Initial analysis failure](initial-analysis-failure.md) records that
failure and the bounded import correction.

The first successful result evaluated every shell but did not retain all S90-required
summary fields and direct-metric larger-shell envelopes. It is preserved as
`truncation-evaluation-initial-incomplete-diagnostics.json`. The
[diagnostic-completeness correction](diagnostic-completeness-correction.md) explains
the additive correction; no mask or source operator changed.

## Identities

| Artifact | SHA-256 |
|---|---|
| final implementation | `5e2779945974c4c9cbdf702236d3686d937964be3bb4ff480fe7c476d582436f` |
| final evaluation | `1ac8bb59137e8dc7217df52f89c18a84e8599bcf82ec59f40a361929d4322a52` |
| initial incomplete implementation | `d96fcd6efb70748f613e6d35bf3ac1b9b66606d74642e95e9a3fd170dca3be58` |
| initial incomplete evaluation | `4a2e18d889ffc682acc2dc04cf37760aa1d662ac945d0ea8452eae814eb186de` |

No calculator executable was invoked.
