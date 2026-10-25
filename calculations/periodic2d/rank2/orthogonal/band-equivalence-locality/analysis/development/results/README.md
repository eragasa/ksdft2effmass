# Square-lattice bounded development calculation

Status: **replaceable development diagnostics; not retained evidence or scientific validation**.

The canonical JSON outputs described below are intentionally excluded from this source
integration. The numerical summary reports a completed bounded local development run;
rerun the maintained action to recreate replaceable artifacts.

This directory documents the first bounded end-to-end repetition of the methodology for
the orthogonal 2-D square family. It used:

- a `16 x 16` tensor Monkhorst--Pack construction mesh;
- a disjoint shifted `33 x 33` evaluation mesh;
- parent scales `0` and `1`;
- amplitudes `0`, `pi/8`, and `pi/4`;
- every attainable square shell through squared radius `25`; and
- development-only band thresholds `1e-3` and `1e-5`.

The calculation stores parent/subspace qualification, graph-frame closure, covariant and
restricted alignment, exact mesh-origin-aware Fourier reconstruction, twisted Nyquist
and ordinary Hermiticity checks, interpolation, deliberate truncation, total matrix and
spectral errors, Parseval checks, and sampled first-passing decisions. The independent
development verifier reports `passes: true`; its maximum stored identity defect is about
`4.1e-15`. The input, result, and verification documents validate against the immutable
family-bound schemas owned by the aggregation workflow under
`calculations/band-equivalence-dimensional-comparison/band_equivalence_workflow/`; the verification
document binds the canonical input and result bytes by SHA-256.

Some strict sampled decisions remain unresolved at the declared shell cap. No threshold,
shell cap, or model was changed in response.

Reproduce from the repository root with:

```bash
python/.venv/bin/python calculations/periodic2d/rank2/orthogonal/band-equivalence-locality/run_development.py
```

These records do not establish convergence, a continuous-amplitude result, an immutable
experiment version, or publication evidence.
