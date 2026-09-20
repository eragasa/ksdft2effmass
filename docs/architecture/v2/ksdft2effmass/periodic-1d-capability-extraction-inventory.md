# Appendix G periodic-1D capability-extraction inventory

## Status and evidence boundary

This inventory governs extraction from the calculated Appendix G package under
`calculations/research-monograph/periodic-1d/`. It is an implementation map, not a
new calculation, reinterpretation of retained evidence, or authorization to rerun
Wannier90. The retained inputs, results, reports, verifiers, figures, execution
records, and checksum catalog remain immutable historical evidence.

The authoritative scientific definitions remain Appendix G and the retained
`protocol.md`. Extraction preserves their state spaces, reciprocal-index ordering,
sewing convention, gauges, units, tolerances, error separation, and negative evidence.
Passing software tests for extracted classes does not reproduce or strengthen the
retained numerical-verification claims.

## Implemented extraction boundary

The current extraction implements the reusable Appendix G lower layers:

- finite real Fourier potentials, plane-wave and periodic finite-difference fibers;
- centered half-open reciprocal meshes, finite-cutoff sewing, scalar/composite frame
  transport, projectors, pointwise frame alignment, and projected operators;
- complete reciprocal-to-hopping transforms, inverse interpolation, symmetric
  truncation, weighted or incomplete least-squares fitting, route comparison,
  block-Hermiticity, Parseval, sampled gap/error, bandwidth, and curvature diagnostics;
- finite Born--von Karman isolated-band localization with norm, center, spread, sample
  encoding, and density identity;
- calculation-producing isolated- and composite-band campaign Workflows: the
  isolated Workflow retains plane-wave, finite-difference, reference, reciprocal,
  scalar Fourier, finite-range, and observable channels, while the composite Workflow
  retains parent fibers, transported and attacked rank-two frames, projectors, Wilson
  spectra, projected operators, complete block hoppings, and separate truncation,
  training, withheld, Hermiticity, and direct-route diagnostics;
- an independent stress-result verifier and integrated Workflow that reconstruct every
  retained amplitude, shape, mesh/band/isolation, deterministic gauge-covariance, and
  complete/incomplete/weighted fitting-route channel from correlated retained bytes;
  and
- execution-independent `.nnkp`, `.eig`, `.amn`, `.mmn`, `_u.mat`, `_hr.dat`, and
  `.wout` parsing, plus deterministic preparation of the demonstrated `.win`, `.eig`,
  `.amn`, and `.mmn` interface subset correlated with parsed `.nnkp` records, under
  `integration.wannier90`.

The native adapters were checked read-only against authenticated initial and
preconditioned Appendix G artifacts as recorded in the
[periodic native-evidence audit](periodic-native-evidence-presence-audit.md). They do
not discover roots or execute Wannier90.

Campaign-specific input/result serializers and read-only correlation Workflows now
preserve the historical wire formats and exact controls. The isolated-band and
composite-band calculation Workflows compile accepted definitions directly into
execution-local NumPy/SciPy calculations. The composite Workflow retains parent
operators and eigenframes, both gauge attacks, transport/alignment provenance, Wilson
phase multisets, complete smooth/rough hoppings, and separate approximation channels;
its independent numerical evidence reconstructs the finite mathematics without
importing the production construction algorithms. Neither calculation Workflow reads
retained results, discovers files, executes external software, or claims
scientific/material validation or UQ. The stress verifier instead consumes an already
correlated retained result and
uses a separate direct NumPy/SciPy implementation for every retained stress channel.
Its integrated Workflow keeps correlation and numerical-verification ResultObjects
separate and performs no historical calculation, filesystem discovery, external
execution, material validation, or UQ. The integration preparation Workflow now owns
native text representation and compatibility checks; selection of Appendix-G-specific
scientific settings and construction of the supplied matrices remain campaign-owned.

## Owning surfaces

| Demonstrated responsibility | Public owner | Extraction disposition |
|---|---|---|
| One-dimensional periodic model parameters and finite Fourier potentials | `analysis.model_systems.periodic_1d` | Extract immutable model records |
| Uniform half-open reciprocal meshes and centered cell representatives | `solid_state` | Extract dimension-specific records and deterministic enumeration |
| Plane-wave fiber matrices and twisted periodic finite-difference fibers | `analysis.model_systems.periodic_1d` consuming `operators` quantities | Extract model construction Actions; preserve sparse input where applicable |
| Retained scalar and composite band frames with reciprocal sewing | `solid_state` | Extract explicit frame-path and sewing records |
| Isolated-band parallel transport and composite polar transport | `solid_state` | Extract gauge-construction Actions and correlated Results |
| Pointwise frame alignment, projectors, and projected fiber operators | `solid_state` | Extract compatibility-checked Actions |
| Scalar and block reciprocal-to-cell Fourier transforms | `solid_state` | Extract exact uniform-mesh transforms and inverse reconstruction |
| Finite-range truncation, omitted hopping norms, band errors, gap diagnostics, and route comparison | `analysis` | Extract ResultObjects and analysis Actions without pooled acceptance |
| Born--von Karman density, center, spread, and content identity | `analysis` | Extract localization diagnostics with explicit finite-supercell convention |
| Appendix G input/result wire formats and orchestration | `campaigns.research_monograph.periodic_1d` | Versioned records, serializers, retained-correlation Workflows, and isolated/composite execution-local calculation Workflows extracted |
| Wannier90 `.win`, `.eig`, `.amn`, `.mmn`, `_u.mat`, `_hr.dat`, and `.wout` adaptation | `integration.wannier90`; campaign owns setting selection and matrix construction | Extract native wire adaptation and `.nnkp`-correlated preparation only; do not implement localization or execution policy |
| Process execution, retries, resource bounds, and attempt authority | `workflows` plus a future exact calculator/integration composition | Preserve historical records; no execution extraction or rerun in this work |
| CLI argument parsing and filesystem writes | calculation scripts | Leave as thin historical adapters; do not migrate domain behavior back into scripts |

## Reusable demonstrated contracts

### Periodic model and representations

1. A real finite Fourier potential retains one constant coefficient and equal-length
   cosine and sine coefficient inventories.
2. A plane-wave basis retains the ordered reciprocal indices `-P,...,P` and the
   reciprocal sewing map used under `k -> k + G`.
3. A one-dimensional fiber Hamiltonian identifies momentum, basis, energy unit,
   potential, and represented matrix.
4. A periodic finite-difference fiber identifies the cell grid, conjugate Bloch
   boundary phase, point ordering, and sparse represented matrix.
5. Plane-wave cutoff error, finite-difference error, transported low-mode operator
   error, reciprocal-sampling error, and model-truncation error remain separate.

### Reciprocal paths and gauges

1. Uniform meshes are half-open and ordered, with the last point sewn to the first
   through an explicit reciprocal sewing map.
2. Scalar transport requires every neighbor and closure overlap to exceed a declared
   threshold; it retains overlap magnitudes and closure holonomy.
3. Composite transport uses the unitary polar factor of each overlap and distributes
   the unitary closure through a declared matrix logarithm/eigenphase branch.
4. Projectors and Wilson eigenphase sets are gauge-covariant diagnostics; individual
   vectors are not compared before alignment.
5. Pointwise alignment retains the exact unitary map and reports frame and represented-
   operator residuals separately.
6. Controlled smooth and rough gauge attacks remain authored campaign controls, not
   generic scientific policies.

### Hopping transforms and reduction

1. Scalar and block transforms use a complete uniform reciprocal mesh and centered
   Born--von Karman cell representatives.
2. The complete transform and inverse reconstruction are one correlated result.
3. Scalar hoppings obey the real-band conjugacy implied by the represented data;
   block hoppings test `T[-R] = T[R]^dagger` explicitly.
4. Finite-range truncation is a separate Action over a complete transform and never
   changes the full transform.
5. Equal-weight complete-mesh least squares agrees with transform truncation only for
   the same Fourier class and mesh. Weighted or incomplete fits remain distinct route
   contracts and may disagree.
6. Training errors, withheld-mesh errors, omitted coefficient/block norms, Parseval
   residuals, bandwidth, and curvature remain separate metrics.

### Localization and subspaces

1. Isolated-band density is formed by a finite Born--von Karman inverse Bloch
   transform in a declared periodic gauge.
2. Quadrature norm, center modulo the lattice, spread, sample count, encoding, and
   SHA-256 density identity are retained without requiring dense profile persistence.
3. Composite subspaces retain internal and external gaps, neighbor and sewn overlap
   singular values, projectors, Wilson phases, represented operators, and matrix-valued
   hoppings.
4. Smooth-versus-rough locality is a gauge demonstration; exact spectra do not imply
   equal finite-range accuracy.

### Native Wannier90 boundary

1. Interface preparation owns deterministic native text adaptation, shared-dimension
   checks, explicit-tolerance `.win`/`.nnkp` reciprocal-point comparison, and exact
   ordered `.nnkp`/`.mmn` compatibility checks only.
2. Native extraction must preserve file identities, iteration and convergence status,
   selected centers and spreads, unitary matrices, real-space Hamiltonians, and the
   comparison estimator convention.
3. Initial preprocessing failure, iteration-bound failures, and preconditioned
   convergence are different outcomes and cannot be pooled or overwritten.
4. Production Wannier localization remains owned by Wannier90. The package may adapt
   inputs and observations but must not reproduce its optimization algorithm.

## Study-specific material that remains in the campaign

- the exact cosine amplitudes, cutoff sequences, grid sequences, band groups, mesh
  sizes, hopping ranges, and acceptance tolerances;
- Mathieu comparisons selected for the cosine model;
- named translated, shifted, higher-harmonic, inversion-breaking, and multi-harmonic
  stress cases;
- deterministic phase, controlled `U(2)`, rough-gauge, weighted-fit, and incomplete-
  training attacks;
- the exact Wannier90 bounded-attempt history and preconditioner decision;
- Appendix G result schemas, reports, plots, and acceptance conclusions.

## Deferred boundaries

- Appendix H tensor-product, coupled-2D, topology, non-Abelian 2D Wilson-loop,
  effective-mass-tensor, and optimizer-basin additions are a later delta extraction.
- General dimensions are not inferred from the one-dimensional exercise unless an
  already accepted language-independent contract supplies them.
- Nonorthogonal representation bases, generalized eigenproblems, spin, magnetic
  phases, atomic structures, DFT, and material claims are not introduced here.
- Historical runners and verifiers are not rewritten merely to use extracted APIs.
  Conformance adapters require a separate byte-preservation and oracle-independence
  plan.

## Implementation order

1. Periodic-1D model, reciprocal mesh, plane-wave basis, and sewing records.
2. Plane-wave and periodic finite-difference fiber constructors.
3. Scalar frame paths, parallel transport, and scalar Fourier hopping transforms.
4. Composite frame paths, polar transport, alignment, projection, and block transforms.
5. Truncation, gap, locality, localization, and route-comparison analyses.
6. Campaign input/result records, serializers, and execution-free Workflows.
7. Wannier90 native adapters and historical-result compatibility checks.
8. Appendix H delta inventory and extraction.

Each increment requires class-owned software evidence. Numerical-verification tests
must use independent analytical or independently assembled oracles and must not import
calculation-runner algorithms as their oracle.
