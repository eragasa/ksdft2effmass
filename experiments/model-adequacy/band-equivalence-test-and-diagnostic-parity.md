# Band-equivalence test and diagnostic parity contract

## Purpose

This document defines the minimum common software-test and diagnostic surface for the
band-equivalence-versus-hopping-locality families. It makes cross-dimensional figures
and tables structurally comparable without sharing numerical outcomes, tolerances,
versions, runs, or evidence.

Covered families:

| Dimension and geometry | Family system segment | Status |
|---|---|---|
| 1-D | `periodic1d` | maintained development predecessor |
| 2-D orthogonal | `periodic2d` | prospective square protocol |
| 2-D non-orthogonal | `periodic2d-nonorthogonal` | prospective graphene-inspired honeycomb-basis protocol |
| 3-D orthogonal | `periodic3d` | prospective simple-cubic protocol |
| 3-D non-orthogonal | `periodic3d-nonorthogonal` | prospective silicon-inspired diamond-basis protocol |

There is no separate 1-D non-orthogonal geometry: a one-vector primitive basis has no
inter-vector angle, so orthogonality is vacuous. The 1-D family supplies the common
specialization fixture for both parent forms rather than a fictitious
`periodic1d_nonorthog` experiment.

## Required test layers

Every implemented family must provide the same named behavioral layers, specialized only
where geometry requires it.

| Layer | Common behavior | Geometry-specific specialization |
|---|---|---|
| Input validation | Reject unknown fields, booleans in numeric APIs, nonfinite values, invalid ranks, incomplete inventories, and inconsistent identities | Primitive-matrix shape, positive determinant/volume, metric and orbit constraints |
| Geometry | Direct/reciprocal duality, positive-definite Gram matrix, displacement-to-physical-vector map | Signed-permutation group for orthogonal cases; exact integer metric group, multi-site basis positions, basis-aware pair distances, and unimodular relabeling for non-orthogonal cases |
| Parent representation | Finite Kronecker parent equals the direct sum of Bloch fibers; complete eigensystems reconstruct every fiber | Directed-hopping parent for the orthogonal sequence; inspired bipartite parent plus matched Hermitian-bond Bravais controls for each non-orthogonal family |
| Retained subspace | Correct rank-two projector, positive external-gap gate, frame isometry, projector lift, and reconstruction | One closure in 1-D; boundary and plaquette consistency on 2-D/3-D tori |
| Gauge equivalence | Pointwise spectra agree; full covariant subtraction vanishes; one-global-rotation residual is reconstructed independently | Axis-separable analytic correlation or bond-orbit constrained correlation |
| Fourier conversion | Nodal reconstruction, block Hermiticity, Parseval, centered-index convention, and cyclic-to-ordinary accounting | One Nyquist point, two boundary lines, or three boundary planes |
| Support | Complete, nested, conjugate-closed shell inventory with no skipped attainable shell | Absolute range in 1-D; Euclidean square/cubic shells; triangular/FCC metric shells |
| Withheld evaluation | Construction/evaluation disjointness; interpolation, truncation, and total field pairs | Dimension-qualified tensor mesh and resource policy |
| First-passing decision | Passing and preceding errors, retained block count, stable refinement, and `unresolved` on cap failure | Geometry-specific shell label and physical radius |
| Independent verification | Reconstruct decisive values without producer reuse or trust in serialized dispositions | Reconstruct orbit, metric, comparator, and resource premises applicable to the family |
| Tamper/failure behavior | Reject altered identities, hashes, shapes, orderings, omitted shells, and stale dispositions | Geometry and comparator fields specific to the family |

Tests establish software behavior and finite-contract consistency only. They do not
establish scientific validation.

## Required diagnostic categories

Every result schema and diagnostic bundle must expose the same categories, units, and
normalization semantics. A family may add diagnostics but may not silently omit an
applicable common channel. In particular, every quantity in the maintained 1-D
`analysis/diagnostic-catalog.csv` must be independently recomputed or derived from
independently recomputed fields for every Paper 2 family. A genuinely inapplicable row
must be serialized as `not-applicable` with its geometric reason. Renaming, plotting, or
placing a value only in narrative prose does not satisfy calculation parity.

### Geometry and resolution

- dimension and geometry identifier;
- primitive and reciprocal matrices, Gram matrix, cell measure, and reciprocal-duality
  defect;
- construction and evaluation mesh sizes and minimum mesh separation;
- bond-orbit size, basis-site count, physical bond-length spread, point-group order,
  shell multiplicities, shell cap, retained block count, and basis-aware entry-distance
  ranges when a multi-site basis is present;
- basis-relabeling defect for non-orthogonal families; `not-applicable` with a reason for
  the 1-D specialization.

### Parent, subspace, frame, and sewing

- minimum sampled external gap plus the separately identified continuous gap certificate;
- maximum parent/direct-sum and eigensystem reconstruction defects;
- maximum projector, frame-orthonormality, and projector-lift defects;
- minimum transport-overlap singular value and maximum Procrustes residual;
- reciprocal-boundary sewing, path, plaquette, closure-holonomy, and unitarity defects as
  applicable. For retained rank two, let \(W_\alpha(\mathbf k_\perp)\) be the ordered
  product of full-rank Procrustes links around reciprocal direction \(\alpha\), based at
  transverse mesh point \(\mathbf k_\perp\). Order the principal eigenphases as
  \(-\pi\le\phi_{\alpha,0}(\mathbf k_\perp)\le
  \phi_{\alpha,1}(\mathbf k_\perp)\le\pi\), and report
  \(\Phi_j=\max_{\alpha,\mathbf k_\perp}|\phi_{\alpha,j}(\mathbf k_\perp)|\) for
  \(j\in\{0,1\}\). These two worst-case phase magnitudes are the multidimensional
  counterparts of the two ordered one-dimensional closure phases. They are applicable
  only when every contributing link is full rank and must be accompanied by closure
  unitarity and plaquette diagnostics. They are sewing diagnostics, not continuum
  topological claims.

### Alignment and analytic comparator

- maximum direct band defect between reference and comparison fields;
- maximum covariant operator defect;
- splitting scale, finite-mesh maximum correlation, selected global angle and its
  unique-or-degenerate status;
- minimum restricted operator threshold after the positive splitting-scale optimization,
  the exact-spectrum joint threshold at unit splitting scale, and their reconstruction
  defects; merely optimizing a global rotation at fixed unit scale is not equivalent;
- analytic flat correlation, finite-mesh correlation, quadrature defect, and series-tail
  bound where a constrained Bessel sum is used;
- exact-spectrum and minimum-alignment threshold diagnostics under the declared
  normalization.

### Locality and Fourier consistency

For reference and comparison fields separately:

- total, onsite, non-onsite, Nyquist, ordinary omitted, and total omitted normalized
  Frobenius power;
- shell-resolved block norm and cumulative tail;
- nodal reconstruction, Hermiticity, and Parseval defects;
- flat residual-minus-tail identity defect.

### Hamiltonian and spectral consequences

For interpolation, deliberate truncation, and total channels separately:

- maximum and RMS normalized Hamiltonian Frobenius errors;
- maximum and RMS normalized sorted-band errors;
- pointwise Weyl-bound defect and the band-to-Hamiltonian bound ratio;
- first passing shell, preceding error, passing error, physical radius, and retained
  block count under both Hamiltonian and spectral criteria;
- reference-to-comparison block inflation and shell-radius inflation;
- construction/evaluation refinement changes and final `converged` or `unresolved`
  disposition.

### Resource and provenance

- sparse/matrix-free execution contract: never materialize the full
  $(4N^d)\times(4N^d)$ cell--orbital operator or a dense withheld-point-by-all-block
  phase matrix; use block-sparse hopping inventories, tensor FFTs, separable tensor
  contractions, and streamed complete-shell accumulation while verifying equality to
  direct dense formulas on bounded software fixtures;
- evaluated momentum, amplitude, parent, and shell counts;
- peak-memory and runtime records for 3-D families and whenever a reviewed cap applies;
- exact family/version/run identities, implementation and dependency revisions, input,
  result and verification digests, and producer/verifier separation.

## Comparable diagnostic products

When a family reaches analysis status, it should produce geometry-qualified versions of
the same products used by the 1-D predecessor:

1. frame and sewing diagnostics;
2. Hamiltonian-versus-spectral error channels;
3. shell-resolved hopping-power and tail maps;
4. interpolation/truncation/total error decomposition;
5. first-passing shell decision map under both matrix and spectral criteria;
6. mesh and amplitude refinement summaries;
7. analytic-comparator and residual--tail identity checks; and
8. a machine-readable diagnostic catalog declaring quantity, category, aggregation,
   unit, normalization, and role.

Plot layouts may change with dimension, but quantity meanings and normalization may not.
A missing applicable diagnostic is a protocol failure, not an empty plot. A genuinely
inapplicable diagnostic must be serialized as such with a reason rather than fabricated
as zero.

## Cross-family comparison boundary

Cross-family summaries may compare only diagnostics with identical definitions and
qualified units. They must retain family-specific parent, geometry, mesh, shell,
tolerance, convergence, and evidence identities. Similar tests and diagnostics do not
make results directly subtractable and do not authorize transferring a cutoff,
tolerance, or convergence outcome between dimensions or geometries.

The separate
[dimensional comparison composition](band-equivalence-dimensional-comparison/)
consumes this contract when producing cross-protocol development summaries. It does not
own or replace any family protocol, tolerance, convergence decision, or evidence
identity.
