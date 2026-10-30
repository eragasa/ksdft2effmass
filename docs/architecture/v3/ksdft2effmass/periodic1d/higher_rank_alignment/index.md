# Higher-rank gauge alignment in periodic one-dimensional models

This package supports the rank-$r$ gauge-alignment study for periodic one-dimensional
Hamiltonians. The frozen D1 specialization compares four prescribed retained-space
gauge alignments for $r\in\{3,4,8,16\}$ and circuit depths
$L\in\{1,2,4,8\}$:

- `identity`;
- `global-unitary`;
- `pointwise-unitary`; and
- `known-inverse-oracle`.

These descriptive values are the only wire identities. They are not physical channels
or diagnostic error channels, and the former opaque identifiers are not accepted.

## Physical and numerical scope

The calculation separates four questions:

1. Can neighboring retained frames be transported around the reciprocal-space period
   without a rank-deficient overlap?
2. Can the endpoint mismatch be distributed smoothly so that the transported analytic
   reference frame is periodic?
3. How do the four prescribed gauge alignments affect represented-operator locality?
4. How do interpolation, truncation, and total error behave under frozen symmetric
   supports and mesh refinement?

Closed-loop transport acts on the analytic reference frame and is common to every gauge
alignment. The global-unitary selection occurs only on the $M=2049$ construction mesh
and is reused without refitting. Pointwise-unitary selection is performed separately on
each construction mesh. The known-inverse-oracle uses the analytic inverse and is a
control, not an admissible fitted solution.

## Available implementation

The maintained package provides:

- immutable configuration, calculation, transport, provenance, and result records;
- a plain domain enum separated from explicit immutable wire mappings;
- an analytic parent Hamiltonian and depth-dependent nearest-neighbor gauge circuit;
- Project Koios Optimization Procrustes selection, PhysKit closed-loop transport, and
  PhysKit odd-mesh finite-periodic transforms;
- nominal immutable gauge-aligned field construction;
- request-bound recovery, Fourier, shifted-interpolation, locality, and result-assembly
  actions under `higher_rank_alignment/gauge_alignment/`;
- rank-deficiency, integrity-failure, backend-failure, and downstream-inapplicability
  outcomes with fail-closed absence of downstream values;
- Parseval, Hermiticity, support-tail, error-decomposition, recovery, and scalar- and
  block-refinement diagnostics; and
- canonical typed record bytes whose SHA-256 digest establishes identity and provenance,
  not scientific validity.

A calculation-local direct development runner composes these maintained owners and writes
only a replaceable non-evidence summary. Independent recalculation, byte-owning complete
result verification, authenticated rendering, and retained execution remain unimplemented
and separately authorized. Software tests establish producer behavior only.

## Numerical responsibilities

- Project Koios Optimization owns unit-free numerical algorithms and nominal immutable
  NumPy storage.
- PhysKit owns physical frame, sewing, finite-periodic, mesh, and transport semantics.
- `ksdft2effmass` owns the study inventory, scientific diagnostics, request correlation,
  failure policy, schemas, and retained-evidence policy.

The calculation-local `workflow/` directory is immutable historical provenance. The
maintained package, tests, and direct runner neither import nor adapt it.

## Dimensional and metric boundary

Only periodic-1D orthonormal science is implemented. Fiberwise right-unitary gauge
alignment is mathematically independent of spatial dimension, but meshes, Fourier
indices, inversion closure, support geometry, and interpolation domains are
dimension-specific. A later 2-D or 3-D study must therefore provide reviewed
dimension-specific mesh and support contracts rather than parameterizing the present
1-D owners.

The present actions assume orthonormal frames and $U(r)$ right actions. A future
nonorthonormal study requires an explicit positive-definite fiber metric, metric-aware
adjoints and isometries, and a separately reviewed alignment objective. No metric-aware,
2-D, or 3-D implementation or placeholder API is provided here.

## Further details

- [Software realization](implementation.md)
- [Numerical formulation](numerics.md)
- [Physical interpretation](scientifics.md)
- [Calculation flow](schematics.md)
