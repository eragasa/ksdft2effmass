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
spectral errors, Parseval checks, and sampled first-passing decisions. The historical
development summary reported `passes: true` and a maximum stored identity defect of about
`4.1e-15`. Its former custom aggregation workflow and duplicate schemas have been
removed. The current typed direct execution is separately retained under
`../../../executions/direct-square-rank2-n16/`; it does not turn this historical
summary into admitted direct-lifecycle evidence.

Some strict sampled decisions remain unresolved at the declared shell cap. No threshold,
shell cap, or model was changed in response.

The maintained development runner emits replaceable typed records. The installed direct
lifecycle is a separate successor composition, not a claim that it reproduces historical
development bytes.

These records do not establish convergence, a continuous-amplitude result, an immutable
experiment version, or publication evidence.
