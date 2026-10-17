# Simple-cubic bounded development calculation

Status: **replaceable development diagnostics; not retained evidence or scientific validation**.

The canonical JSON outputs described below are intentionally excluded from this source
integration. The numerical summary reports a completed bounded local development run;
rerun the maintained action to recreate replaceable artifacts.

This directory documents the first bounded end-to-end repetition of the methodology for
the orthogonal 3-D simple-cubic family. Resource preflight selected:

- an `8 x 8 x 8` tensor Monkhorst--Pack construction mesh;
- a disjoint shifted `17 x 17 x 17` evaluation mesh;
- parent scales `0` and `1`;
- amplitudes `0`, `pi/8`, and `pi/4`;
- every attainable cubic shell through squared radius `9`; and
- development-only band thresholds `1e-3` and `1e-5`.

No dense global Hamiltonian was materialized. The calculation stores the full bounded
parent/subspace, frame, alignment, Fourier, twisted-Nyquist, ordinary-Hermiticity,
interpolation, truncation, total-error, Parseval, resource-safe shell, and first-passing
channels. The independent development verifier reports `passes: true`; its maximum
stored identity defect is about `6.0e-15`. The input, result, and verification documents
validate against the immutable family-bound schemas packaged by
`ksdft2effmass.campaigns.model_adequacy.band_equivalence_locality`; the verification
document binds the canonical input and result bytes by SHA-256.

The rotated endpoint remains unresolved at the sampled shell cap. This is the required
failure-safe outcome, not a negative scientific result.

Reproduce from the repository root with:

```bash
python/.venv/bin/python experiments/model-adequacy/periodic3d/band-equivalence-versus-hopping-locality/run_development.py
```

These records do not establish convergence, authorize the draft `16/32/64` ladder, or
constitute publication evidence.
