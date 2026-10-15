# Historical 64/257 computational regression fixture

This directory is a non-decisive regression fixture. It is not an experiment version,
retained run, evidence package, scientific protocol, or publication reference. Its
purpose is to detect unintended changes to historically matched finite-mesh software
channels while the maintained experiment uses continuous global alignment and
convergence-qualified controls.

## Baseline

The parity baseline excludes the separate post-hoc threshold-sensitivity family. It is
bound to:

- Git revision: `6afbdb211dc20a2de619096ebac66f4dea9dafdc`
- repository path: `calculations/ICMSEP2026/conference/paper_1/constrained-admissible-sets/`
- path tree: `557604ba0893b0f02ec8f69f89e8bfa4cb7786b4`
- `input.json`: `sha256:9cf95d111856f5dd92e8018ed019c59eed5c55cb18e33d3ee464839bcc7f9606`
- `result.json`: `sha256:9d95da829b84743386f627c32e9b4a740f2ff602d77a1ff225f295e17f98d2f9`
- `verification.json`: `sha256:a2a051ba458f2ab6294e0aec59d5f7029c823f38662b277ba7a08f6ae411faa2`
- `standalone-verification.json`: `sha256:5e635cdf5ff93bd4c48a8a7ff84d6b7ba9c9b60ee18a51b2035d837610442892`
- `SHA256SUMS`: `sha256:552e93aced1d1771a54878600e9aa667c06bbfd1a4512f56d30f3f7ebcae7ca9`

Git retains that historical source and evidence unchanged.

## Capability matrix

| Computational capability | Pre-migration baseline | Regression implementation | Parity disposition |
|---|---|---|---|
| Exact rank-two parent derivation | Composed M2 producer | Composed `Periodic1DMultibandAlignmentCalculator` | Recovered |
| Parent gap, transport-overlap, and projector diagnostics | Retained summary | Typed composed-parent diagnostics | Recovered |
| Trace/shift/traceless-splitting candidate family | Local M3 implementation | Experiment-owned candidate construction | Recovered |
| Spectral objective-construction quadratic | Local direct completion | Optimization-owned weighted complex affine-residual construction | Recovered and owner-integrated |
| Nine angle-resolved operator quadratics | Local direct completion | Same owner construction with KSD labels | Recovered and owner-integrated |
| Closed-rectangle component feasibility | Local two-dimensional enumeration | Optimization rectangle minimizer | Recovered and owner-integrated |
| Compatible common witness | `(0, 1)` constructive witness | Same prospective witness and first-on-tie selection | Recovered |
| Full-ellipsoid containment premise | Checked in local certificate code | Explicit KSD containment after owner support | Recovered |
| Splitting-axis separation certificate | Lower/upper bounds and resolution | Same bounded certificate and dispositions | Recovered |
| Disjoint 257-point evaluation diagnostics | Retained spectral/operator losses | Explicit objective-evaluation fields | Recovered with clearer role identity |
| Range-resolved reference/attacked/candidate locality | Seven ranges | Same seven ranges and three channels | Recovered |
| Immutable typed records | Installed-package records | Experiment-local frozen records | Recovered |
| Historical serialization | Historical M3 schema | Historical files remain unchanged under `calculations/` | Bound by digest only |
| Active strict schemas | Not applicable | Maintained smooth-continuum schemas outside this fixture | Intentionally separate |
| Independent numerical reconstruction | Library and standalone verifiers | Producer-independent typed verifier | Recovered |
| Retained evidence package | Historical package exists | None | Historical lookup only |

## Numerical gate

`test_historical_parity__matches_every_retained_numerical_channel` executes the exact
64/257-point controls and compares every retained parent summary, quadratic center,
quadratic matrix, minimum, disposition, feasible-angle inventory, certificate point,
construction loss, evaluation loss, locality norm, and separation bound with historical
`result.json`. The gate requires the maximum absolute defect to be at most `1e-11`.

The focused parity test passes. This establishes computational-capability and finite-
precision parity for the declared channels; it is not scientific validation.
