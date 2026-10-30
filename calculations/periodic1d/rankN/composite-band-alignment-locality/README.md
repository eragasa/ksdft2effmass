# Higher-rank gauge alignment and hopping locality in one dimension

**Status:** maintained typed producer with an integrity-admitted reusable calculation
cache; scientific acceptance and publication remain separate decisions.

This synthetic calculation asks a concrete question: if a momentum-dependent change of
retained basis preserves the represented energy bands, how much can it lengthen the
real-space hopping matrices, and how much locality can prescribed gauge alignments
recover? It compares retained ranks `3`, `4`, `8`, and `16`; circuit depths `1`, `2`,
`4`, and `8`; and four gauge alignments: identity, one global unitary, pointwise complete
unitaries, and the known inverse oracle.

Maintained behavior belongs to
`ksdft2effmass.periodic1d.higher_rank_alignment`. The source package owns immutable
configuration, request, transport, provenance, calculation-result, refinement, and
failure records together with the analytic producer. Gauge-alignment construction,
recovery, Fourier transformation, interpolation, locality analysis, and result assembly
are decomposed under its `gauge_alignment/` child.

- [`run_01_calculation.py`](run_01_calculation.py) directly composes the maintained KSD,
  PhysKit, and Optimization owners for all 16 cases once, writes a
  `scientific_evidence: false` summary, and stores one canonical typed result per case.
  The cache manifest records one SHA-256 identity for the explicitly selected scientific
  calculation infrastructure; plotting sources are excluded.
- [`run_02_verification.py`](run_02_verification.py) performs canonical-byte, SHA-256,
  exact-round-trip, and complete-inventory verification. It explicitly records
  `independent_scientific_verification: false`.
- [`run_03_render.py`](run_03_render.py) regenerates the fixed nine-figure
  technical-report snapshot repeatedly from the integrity-admitted cache without
  recalculating the scientific grid. Plot and report changes therefore do not require
  the approximately 30-minute calculation stage.
- [`verify_analytic_controls.py`](verify_analytic_controls.py) checks two formulas on a
  finite grid. It is a sanity check, not independent verification of the full result.
- [`protocol/`](protocol/README.md) contains the authoritative detailed plan, frozen
  controls, future evidence schemas, and retained-execution policy.
- [`technical-report/technical_report.tex`](technical-report/technical_report.tex) is the
  calculation-facing scientific report.
- [`workflow/`](workflow/) is read-only historical provenance. Maintained source, tests,
  and direct execution do not import, adapt, or execute it.

Canonical typed calculation bytes and four bounded producer-independent references now
exist. The core slice reconstructs analytic-model and attack invariants. The Fourier slice
covers all four gauge controls on all three construction meshes and independently
compares block norms, reconstruction, Parseval, Hermitian pairing, shifted interpolation,
and support tails; for the oracle it also compares analytic $|R|\le2$
coefficients. The Procrustes slice reconstructs the single global selection with an
Hermitian-eigendecomposition polar factor and all three pointwise selections directly
from the analytic attack, including rank, residual, integrity, and selected-unitary
evidence. The transport slice directly reconstructs the exact constant-frame closed
route on all three meshes, including link rank evidence and closure actions. These
references do not reconstruct complete locality error channels or refinement evidence
and do not own result bytes. Here producer-independent means direct NumPy reconstruction
that bypasses the corresponding producer scientific actions. It does not mean an
independent numerical-library stack: the references share NumPy/LAPACK and typed
quantity/comparison infrastructure. Exhaustive recomputation and authenticated rendering
are not required by the study's direct calculate-once, integrity-check, render-many
lifecycle.
Proposed two- and three-dimensional and nonorthonormal studies remain outside this
periodic-1D orthonormal contract.

Ranks `1` and `2` are also intentionally outside the D1-v1 case inventory. Rank one is
the separate scalar Fourier-locality specialization because $U(1)$ phases do not change
a scalar represented Hamiltonian. Rank two can reuse orthonormal matrix mechanisms but
retains its own model, controls, verification, and evidence identity; this higher-rank
family is not its replacement. The Architecture v3
[rank-specialization crosswalk](../../../../docs/architecture/v3/ksdft2effmass/periodic1d/higher_rank_alignment/rank-specialization-crosswalk.md)
records the boundary.

Migration records:

- [`experiment-migration-crosswalk.md`](experiment-migration-crosswalk.md) records where
  each of the five removed experiment files went and distinguishes historical migration
  state from the maintained Architecture v3 successor.
- [`experiment-removal-manifest.json`](experiment-removal-manifest.json) records their
  exact hashes and calculation destinations.
- [`experiment-removal-readiness.md`](experiment-removal-readiness.md) records the
  review and the separately authorized five-file removal.
- [`migration.md`](migration.md) tracks the remaining lifecycle slices.

## Architecture inventory

| Part | Current disposition |
|---|---|
| One-dimensional analytic parent and 16 rank/depth cases | Implemented by the maintained higher-rank package; one development calculation writes canonical replaceable cache bytes that subsequent renders reuse. |
| Four gauge alignments | Identity, global-unitary, pointwise-unitary, and known-inverse-oracle are implemented with strict descriptive wire identities. |
| Model and numerical operations | Family policy remains in KSD; canonical finite-periodic and transport operations come from PhysKit; unit-free Procrustes operations come from Optimization. |
| Gauge-alignment stages | Construction, recovery, Fourier transformation, shifted interpolation, locality analysis, and correlated assembly have typed request-bound owners. |
| Failure semantics | Rank deficiency, transport or Procrustes backend failure, integrity failure, and downstream absence are distinct typed outcomes. |
| Canonical calculation bytes | Implemented through `BaseTypedRecord`; SHA-256 establishes byte identity and provenance, not scientific validity. |
| Independent reference and verification | Bounded direct-formula core-invariant, all-gauge Fourier, global/pointwise Procrustes, and constant-frame transport references are implemented; cache integrity verification is the direct stage-two lifecycle. |
| Figures and execution | Nine views are regenerated from the admitted calculation cache without recalculation. Retained execution and publication remain separately authorization-gated. |
| Historical Workflow source | Preserved as read-only provenance and excluded from maintained runtime and tests. |
| Rank specializations | Rank one remains scalar Fourier locality; rank two remains a separate composite-alignment study. Neither is admitted by widening the D1-v1 inventory. |
| Future variants | Moving-subspace, complex-rotation, restricted-optimizer, 2-D, 3-D, and nonorthonormal variants are absent and cannot inherit this result. |
