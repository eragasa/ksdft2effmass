# Software realization of the higher-rank study

## Python modules

| Module | Scientific role |
|---|---|
| `definition.py` | Names the four alignment families and the possible alignment and numerical outcomes. |
| `configuration.py` | Stores the fixed ranks, depths, construction, global-unitary-selection and evaluation meshes, phase convention, and tolerances. |
| `request.py` | Selects one rank/depth/construction-mesh transport and its ambient-basis, retained-frame, and endpoint-sewing identities. |
| `result.py` | Stores alignment statuses, link diagnostics, backend failures, and request-bound periodic-frame transport results. |
| `model.py` | Constructs the analytic parent spectrum, retained frame, identity sewing, and depth-dependent gauge circuit as a nominal periodic-1D toy model. |
| `_record_admission.py` | Centralizes exact-type, immutable-array, and nested-mapping admission shared by the typed evidence records. |
| `calculation.py` | Defines the frozen calculation controls and complete calculation request. |
| `diagnostics.py` | Stores typed model, Procrustes, matrix, comparison, and frame diagnostics. |
| `channel_results.py` | Stores typed support, channel, and construction-mesh results. |
| `refinement_results.py` | Stores typed block and scalar refinement results. |
| `scalar_diagnostics.py` | Owns the canonical scalar-diagnostic path/value inventory shared by refinement production and aggregate admission. |
| `provenance.py` | Stores exact construction/evaluation mesh separation and selection-input provenance. |
| `calculation_result.py` | Stores and correlates the aggregate request-bound calculation result. |
| `channel_analysis.py` | Owns the request-bound transform, shifted evaluation, support, and locality analysis for one qualified channel. |
| `refinement.py` | Owns request-bound block and scalar refinement analysis across the three construction meshes. |
| `analysis.py` | Composes Optimization Procrustes, PhysKit transport and odd-mesh Fourier owners, and the purpose-specific channel and refinement actions into the calculation action. |
| `__init__.py` | Defines the deliberately narrow supported public imports; internal purpose-specific actions remain module-local imports. |

The records are immutable and serialize deterministically. Maintained arrays use shared
Project Koios NumPy types and the nominal `NumpyImmutableArrayConstructor` and
`NumpyImmutableArrayValidator` owners; physical array annotations use PhysKit aliases.
The constructor creates canonical immutable bytes-backed storage, while request admission
uses the zero-copy validator and rejects noncanonical storage. This makes a saved result
reconstructible without relying on mutable NumPy storage, a competing local
immutable-storage implementation, or a process-wide serializer registry.

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
request, concrete Optimization and PhysKit owners, and the KSD scalar-refinement owner
in its constructor. Its
zero-argument `execute()` method constructs one analytic case, selects the global
unitary at $M=2049$, evaluates all three construction meshes, delegates each qualified
channel to `Periodic1DHigherRankChannelAnalyzer`, delegates mesh-pair comparisons to
`Periodic1DHigherRankRefinementAnalyzer`, and returns a
`Periodic1DHigherRankAlignmentCalculationResult`. These purpose-specific actions bind
complete immutable requests and are imported from their owning modules rather than
re-exported from the package root. Channel requests require canonical immutable
byte-backed arrays and correlate the model rank and depth, status identity, global
selection, exact unshifted mesh coordinates, aligned operator samples, and aligned frames
against the analytic channel definition or the exact pointwise solver result before
computing scientific values. Refinement requests similarly correlate every supplied mesh
with the calculation case.

The result retains the exact request and a closed hierarchy:

- one model-integrity record per mesh with repeated case, rank, depth, and construction
  mesh identity, the exact $2.1E_{\mathrm{ref}}$ analytic isolation certificate,
  sampled separation, the rank-dependent exact and sampled attack-angle maxima,
  gauge-isometry evidence from the shared matrix-field diagnostic owner, and
  attacked/reference projector equality;
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
twisted Hermiticity, and tail monotonicity. The enclosing result recomputes exact
rational construction/evaluation coordinate disjointness and the evaluation mesh's
exclusion from selection during record admission. Refinement records use the shared KSD
absolute-relative scalar diagnostic, retain signed margins and an aggregate pass flag,
and recompute all blockwise refinement arithmetic during record admission. Support
records revalidate rank/energy normalization and tail square-root identities. Channel
records revalidate nonnegative block norms and their rank/energy normalization. The
aggregate result correlates both block and scalar refinement values with their retained
source channels and correlates model and transport-failure evidence with the complete
calculation request. Coefficient arrays are not retained in
the public wire; the complete bounded block-norm inventory $|R|\le128$ is retained.

Documented Procrustes backend failures become numerically-unresolved selections with
empty scientific arrays, one stable exception code, and no selected unitary or backend
claim. Documented transport backend failures become typed transport-failure records;
all four channel results on that mesh are numerically unresolved and contain no
transform or locality values. Rank-deficient global and pointwise selections likewise
emit no downstream values for the affected channel. Runtime exception messages and
tracebacks are not serialized.

All maintained arrays are copied into immutable bytes-backed storage that prevents NumPy
write re-enablement. Integer, real, and complex arrays retain exact dtype boundaries and
serialize with explicit dtype and shape metadata, including empty multidimensional arrays
used by bounded failure records. Generated dataclass equality is disabled for
array-backed and aggregate records; canonical typed JSON bytes establish their exact
serialized identity. Calculation requests and complete results round-trip through those
bytes.

## Work remaining

The next separately authorized stages must add independent numerical recalculation,
byte-owning complete result verification, authenticated scientific plotting data, and
direct calculation scripts. Those stages will use explicit calculation inputs and will
not reconstruct the historical Workflow implementation. Passing producer tests does not
establish scientific validation.
