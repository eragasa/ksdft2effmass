# Rank-N composite-band alignment in periodic one-dimensional models

This package supports the rank-$r$ composite-band alignment study for periodic
one-dimensional Hamiltonians. The frozen D1 specialization compares four prescribed
retained-space gauge alignments for $r\in\{3,4,8,16\}$ and circuit depths
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
- strict domain enums implemented through `StringWireEnum`;
- an analytic parent Hamiltonian and depth-dependent nearest-neighbor gauge circuit;
- Project Koios Optimization Procrustes selection, PhysKit closed-loop transport, and
  PhysKit odd-mesh finite-periodic transforms;
- nominal immutable gauge-aligned field construction;
- request-bound recovery, Fourier, and shifted-interpolation actions under
  `rankN/gauge_alignment/`;
- scientifically distinct hopping-locality and support-truncation actions under their
  rank-first capability namespaces;
- composite-owned orchestration and aggregate-result assembly under
  `rankN/band_alignment/composite/`;
- rank-deficiency, integrity-failure, backend-failure, and downstream-inapplicability
  outcomes with fail-closed absence of downstream values;
- Parseval, Hermiticity, support-tail, error-decomposition, recovery, and scalar- and
  block-refinement diagnostics; and
- canonical typed record bytes whose SHA-256 digest establishes identity and provenance,
  not scientific validity; and
- a bounded producer-independent direct-formula reference for analytic-model and attack
  core invariants; and
- a bounded direct-sum Fourier reference for all four gauge controls, including shifted
  interpolation and support-tail measures for every alignment and exact support for the
  oracle; and
- a bounded global/pointwise Procrustes reference that uses an independent global polar
  construction and direct analytic pointwise inverses; and
- a bounded constant-frame transport reference that reconstructs link rank and identity
  closure evidence without the producer transporter.

A calculation-local direct development runner composes these maintained owners and writes
only a replaceable non-evidence summary. The bounded references do not reconstruct
complete locality error channels or refinement evidence. Complete independent
recalculation, byte-owning
result verification, authenticated rendering, and retained execution remain
unimplemented and separately authorized. Software tests establish bounded software
behavior only.

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

The present actions expose a typed unitary group identity in represented dimension $r$
and assume orthonormal frames and $U(r)$ right actions. The group family does not stand
in for a metric: the Euclidean-orthonormal convention remains separately declared. The
underlying orthonormal matrix mechanisms are meaningful at rank two, but the maintained
rank-two study has its own model, controls, verification, and evidence identity and is not
implicitly admitted here. Rank one is a distinct scalar specialization: its represented
Hamiltonian is invariant under $U(1)$ phase changes, and the D1 analytic formulas that
normalize by $r-1$ are undefined. The frozen tuple `(3, 4, 8, 16)` is therefore an
intentional D1-v1 protocol boundary rather than a claim about the capabilities of the
shared numerical kernels.

A future nonorthonormal study requires an explicit positive-definite fiber metric,
metric-aware adjoints and isometries, and a separately reviewed alignment objective. No
metric-aware, 2-D, or 3-D implementation or placeholder API is provided here.

## Further details

- [Software realization](implementation.md)
- [Numerical formulation](numerics.md)
- [Physical interpretation](scientifics.md)
- [Rank-specialization crosswalk](rank-specialization-crosswalk.md)
- [Calculation flow](schematics.md)
