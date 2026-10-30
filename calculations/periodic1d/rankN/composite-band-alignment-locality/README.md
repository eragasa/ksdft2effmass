# Higher-rank gauge alignment and hopping locality in one dimension

**Status:** maintained typed development producer with no independently verified or
checksum-bound retained execution.

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

- [`run_development.py`](run_development.py) directly composes the maintained KSD,
  PhysKit, and Optimization owners for one replaceable development case. Its JSON summary
  declares `scientific_evidence: false`.
- [`verify_analytic_controls.py`](verify_analytic_controls.py) checks two formulas on a
  finite grid. It is a sanity check, not independent verification of the full result.
- [`protocol/`](protocol/README.md) contains the authoritative detailed plan, frozen
  controls, future evidence schemas, and retained-execution policy.
- [`technical-report/technical_report.tex`](technical-report/technical_report.tex) is the
  calculation-facing scientific report.
- [`workflow/`](workflow/) is read-only historical provenance. Maintained source, tests,
  and direct execution do not import, adapt, or execute it.

Canonical typed calculation bytes and a bounded producer-independent reference for
analytic-model and attack core invariants now exist. That reference does not reconstruct
transport, Procrustes, Fourier, locality, or refinement evidence and does not own result
bytes. Complete independent numerical recomputation, byte-owning verification, strict
retained-artifact schemas, authenticated plotting data, direct calculate → verify →
render composition, and a resource-qualified retained run remain separate work.
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
| One-dimensional analytic parent and 16 rank/depth cases | Implemented by the maintained higher-rank package; development composition executes one selected case at a time. |
| Four gauge alignments | Identity, global-unitary, pointwise-unitary, and known-inverse-oracle are implemented with strict descriptive wire identities. |
| Model and numerical operations | Family policy remains in KSD; canonical finite-periodic and transport operations come from PhysKit; unit-free Procrustes operations come from Optimization. |
| Gauge-alignment stages | Construction, recovery, Fourier transformation, shifted interpolation, locality analysis, and correlated assembly have typed request-bound owners. |
| Failure semantics | Rank deficiency, transport or Procrustes backend failure, integrity failure, and downstream absence are distinct typed outcomes. |
| Canonical calculation bytes | Implemented through `BaseTypedRecord`; SHA-256 establishes byte identity and provenance, not scientific validity. |
| Independent reference and verification | A bounded direct-formula core-invariant reference is implemented; complete protocol-wide recomputation and byte-owning verification are not. |
| Authenticated figures and retained execution | Not implemented and separately authorization-gated. |
| Historical Workflow source | Preserved as read-only provenance and excluded from maintained runtime and tests. |
| Rank specializations | Rank one remains scalar Fourier locality; rank two remains a separate composite-alignment study. Neither is admitted by widening the D1-v1 inventory. |
| Future variants | Moving-subspace, complex-rotation, restricted-optimizer, 2-D, 3-D, and nonorthonormal variants are absent and cannot inherit this result. |
