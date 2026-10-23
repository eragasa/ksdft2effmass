# Silicon-inspired bounded development calculation

Status: **replaceable development diagnostics; not retained evidence, silicon
validation, or scientific validation**.

The canonical JSON outputs described below are intentionally excluded from this source
integration. The numerical summary reports a completed bounded local development run;
rerun the maintained action to recreate replaceable artifacts.

This directory documents a bounded end-to-end repetition for three independently named
cases inside the non-orthogonal 3-D family:

1. matched simple-cubic Bravais control;
2. FCC Bravais control; and
3. silicon-inspired diamond parent.

Resource preflight selected an `8 x 8 x 8` tensor Monkhorst--Pack construction mesh, a
disjoint shifted `17 x 17 x 17` evaluation mesh, parent scales `0` and `1`, three RMS
gauge amplitudes through `pi/(4*sqrt(12))`, complete FCC metric shells through index `7`,
and development-only band thresholds `1e-3` and `1e-5`.

No dense global Hamiltonian was materialized. The calculation repeats all bounded
parent/subspace, graph-frame, alignment, Fourier, twisted-Nyquist,
ordinary-Hermiticity, interpolation, truncation, total-error, Parseval, basis-distance,
metric-covariance, resource, and first-passing diagnostics. The independent development
verifier reports `passes: true`; its maximum stored identity defect is about `4.5e-15`.
The input, result, and verification documents validate against the immutable
family-bound schemas packaged by
the aggregation workflow under `calculations/band-equivalence-dimensional-comparison/band_equivalence_workflow/`; the verification
document binds the canonical input and result bytes by SHA-256.

Several sampled first-passing decisions remain unresolved at the declared shell cap. No
threshold, shell cap, or model was changed in response. The inspired parent is a
synthetic diamond-connectivity control, not an `sp3s*`, valley, effective-mass, or
first-principles silicon model.

Reproduce from the repository root with:

```bash
python/.venv/bin/python calculations/periodic3d/rank2/nonorthogonal/band-equivalence-locality/run_development.py
```

These records do not establish mesh or shell convergence, certify the FCC triple-Bessel
series tail, authorize the draft `16/32/64` ladder, or constitute publication evidence.
