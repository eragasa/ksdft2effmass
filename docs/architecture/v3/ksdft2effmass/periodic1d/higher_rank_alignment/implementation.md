# Software realization of the higher-rank study

## Python modules

| Module | Scientific role |
|---|---|
| `definition.py` | Names the four alignment families and the possible alignment and numerical outcomes. |
| `configuration.py` | Stores the fixed ranks, depths, construction, global-unitary-selection and evaluation meshes, phase convention, and tolerances. |
| `request.py` | Selects one rank/depth/construction-mesh transport and its ambient-basis, retained-frame, and endpoint-sewing identities. |
| `result.py` | Stores link diagnostics, backend failures, channel outcomes, and request-bound periodic-frame transport results. |
| `model.py` | Constructs the analytic parent spectrum, retained frame, identity sewing, and depth-dependent gauge circuit. |
| `calculation.py` | Defines frozen calculation controls, the complete request, and typed model, alignment, Fourier, support, mesh, refinement, and case results. |
| `analysis.py` | Composes Optimization Procrustes, PhysKit transport and odd-mesh Fourier owners, and KSD matrix-field diagnostics into one zero-argument calculation action. |
| `__init__.py` | Defines the supported public imports. |

The records are immutable and serialize deterministically. This makes a saved result
reconstructible without relying on mutable NumPy arrays or a process-wide serializer
registry.

## Fixed parameter study

The first study uses

$$
r\in\{3,4,8,16\},
\qquad
L\in\{1,2,4,8\},
$$

with construction-mesh sizes

$$
M\in\{513,1025,2049\}.
$$

The final construction mesh has $M=2049$ points. The explicit
`global_unitary_selection_mesh_size` is also $2049$. The shifted direct-evaluation mesh
has $8191$ points. The global-unitary alignment is selected once on the final
construction mesh and then reused on the other construction meshes and at
direct-evaluation points.

Frame transformations act on the retained space from the right. Reciprocal-endpoint
sewing acts on the ambient space from the left. Principal phases lie in $(-\pi,\pi]$.
The numerical-rank threshold is

$$
\tau_{\mathrm{rank}}
 = \max\!\left(10^{-12},10^{-10}\sigma_{\max}\right).
$$

Boolean values, numeric strings, nonfinite tolerances, alternative rank-cutoff rules,
and parameter inventories outside the frozen study are rejected.

## Transport results

`Periodic1DHigherRankAlignmentTransportOwnerResult.from_owner_outcome` converts a PhysKit
frame-transport result into immutable KSD data. It requires a one-dimensional,
unshifted `CenteredUniformMesh` and checks its size, retained rank, ambient dimension,
left/right actions, phase branch, tolerance, ordered link progression, and exact basis,
frame, and sewing identities against the immutable transport request.

A successful result contains:

- singular values and rank evidence for every required link;
- the principal phases of the endpoint mismatch;
- the right-unitary mapping from the primitive transported endpoint to the sewn initial
  frame;
- its reverse-direction adjoint; and
- the per-step right-unitary whose $M$-th power supplies periodic closure.

The final three quantities are stored as unitless complex matrices with descriptive field
names; see the [numerical formulation](numerics.md). A rank-deficient result stops at the
first deficient overlap and contains no closure matrices or Schur evidence.

## Calculation action and records

`Periodic1DHigherRankAlignmentAnalyzer` receives the complete immutable calculation
request and concrete Optimization and PhysKit owners in its constructor. Its
zero-argument `execute()` method constructs one analytic case, selects the global
unitary at $M=2049$, evaluates all three construction meshes, and returns a
`Periodic1DHigherRankAlignmentCalculationResult`.

The result retains the exact request and a closed hierarchy:

- one model-integrity record with the exact $2.1E_{\mathrm{ref}}$ analytic isolation
  certificate, sampled separation, the rank-dependent exact and sampled attack-angle
  maxima, gauge-unitarity evidence, and attacked/reference projector equality on every
  construction mesh;
- one global-selection result with every singular value, applied cutoff, strict rank
  margin, finite full-rank condition number, normalized residual, and unitarity,
  stationarity, objective-identity, and positive-semidefinite defect;
- three construction-mesh results;
- four channel results per mesh, including aligned-frame and represented-operator
  recovery diagnostics, with explicit known-recovery gates only for the pointwise and
  analytic known-inverse channels;
- nine support results per qualified channel; and
- blockwise refinement arrays for both adjacent mesh pairs and the complete frozen
  scalar diagnostic ledger for the mandatory $1025\rightarrow2049$ pair.

Each support record keeps interpolation, truncation, and total errors separate. It also
records the ordinary omitted tail, the construction-mesh Parseval defect, perturbation
bounds, the explicit decomposition residual, and gate dispositions against the frozen
request tolerances. Channel records similarly retain the complete odd-mesh Fourier
representative count and canonical-index checks, the explicit no-Nyquist disposition,
and dispositions for reconstruction, withheld interpolation, Parseval, ordinary and
twisted Hermiticity, and tail monotonicity. The enclosing result confirms exact
construction/evaluation coordinate disjointness and the evaluation mesh's exclusion
from selection; refinement records retain signed margins and an aggregate pass flag.
Coefficient arrays are not retained in
the public wire; the complete bounded block-norm inventory $|R|\le128$ is retained.

Documented Procrustes backend failures become numerically-unresolved selections with
empty scientific arrays, one stable exception code, and no selected unitary or backend
claim. Documented transport backend failures become typed transport-failure records;
all four channel results on that mesh are numerically unresolved and contain no
transform or locality values. Rank-deficient global and pointwise selections likewise
emit no downstream values for the affected channel. Runtime exception messages and
tracebacks are not serialized.

All arrays are defensively copied by their records and serialized with explicit dtype
and shape metadata, including empty multidimensional arrays used by bounded failure
records. Calculation requests and complete results round-trip through the canonical
typed JSON bytes.

## Work remaining

The next separately authorized stages must add independent numerical recalculation,
byte-owning complete result verification, authenticated scientific plotting data, and
direct calculation scripts. Those stages will use explicit calculation inputs and will
not reconstruct the historical Workflow implementation. Passing producer tests does not
establish scientific validation.
