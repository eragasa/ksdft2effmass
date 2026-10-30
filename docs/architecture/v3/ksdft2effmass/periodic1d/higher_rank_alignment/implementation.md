# Software realization of the higher-rank study

## Python modules

| Module | Scientific role |
|---|---|
| `definition.py` | Names calculation and transport outcomes. |
| `configuration.py` | Stores the frozen ranks, depths, meshes, supports, phase convention, and tolerances. |
| `request.py` | Selects one rank/depth/construction-mesh transport and its physical identities. |
| `result/status.py` | Stores gauge-alignment status and bounded downstream applicability. |
| `result/frame_transport.py` | Stores request-bound closed-loop frame-transport evidence and bounded failures. |
| `result/__init__.py` | Exposes the deliberate status and transport result inventory. |
| `model.py` | Constructs the analytic parent spectrum, retained frame, identity sewing, and gauge circuit. |
| `_record_admission.py` | Centralizes exact-type, immutable-array, and nested-mapping admission. |
| `calculation.py` | Defines the complete frozen calculation request. |
| `diagnostics/model.py` | Stores analytic-model and Procrustes diagnostics. |
| `diagnostics/matrix.py` | Stores matrix-field error and comparison diagnostics. |
| `diagnostics/frame.py` | Stores frame-recovery diagnostics. |
| `diagnostics/__init__.py` | Exposes the deliberate diagnostic-record inventory. |
| `provenance.py` | Stores mesh-role separation and global-selection provenance. |
| `refinement_results.py` | Stores block and scalar refinement results. |
| `scalar_diagnostics.py` | Owns the canonical scalar-diagnostic inventory used by refinement and aggregate admission. |
| `refinement.py` | Analyzes correlated evidence across construction meshes. |
| `calculation_result.py` | Stores and correlates the aggregate request-bound calculation result. |
| `reference.py` | Independently reconstructs the analytic model and attack core invariants with direct NumPy formulas. |
| `fourier_reference.py` | Independently reconstructs bounded identity and known-inverse-oracle Fourier controls with direct NumPy sums. |
| `analysis/calculation.py` | Composes Optimization, PhysKit, gauge-alignment, transport, and refinement owners. |
| `analysis/procrustes.py` | Builds bounded global and pointwise Procrustes selection evidence. |
| `analysis/mesh.py` | Owns construction coordinates and typed mesh/alignment dispositions. |
| `analysis/evaluation.py` | Proves exact construction/evaluation mesh separation. |
| `analysis/__init__.py` | Exposes the deliberate calculation-analysis action inventory. |
| `gauge_alignment/definition.py` | Defines the four gauge-alignment domain identities and explicit wire map. |
| `gauge_alignment/nyquist.py` | Defines the odd-mesh Nyquist disposition and explicit wire mapping. |
| `gauge_alignment/fields.py` | Constructs nominal immutable gauge-aligned operators and frames. |
| `gauge_alignment/request.py` | Correlates one complete gauge-alignment analysis request. |
| `gauge_alignment/recovery.py` | Evaluates frame and represented-operator recovery. |
| `gauge_alignment/fourier.py` | Owns odd-mesh transforms and Fourier structural evidence. |
| `gauge_alignment/interpolation.py` | Owns direct and complete-series shifted-mesh evaluation. |
| `gauge_alignment/locality.py` | Owns support tails, truncation, and error decomposition. |
| `gauge_alignment/assembly.py` | Correlates stage evidence and assembles one public mesh result. |
| `gauge_alignment/analysis.py` | Executes the typed stages in scientific order. |
| `gauge_alignment/results/support.py` | Stores symmetric-support locality and error-channel records. |
| `gauge_alignment/results/alignment.py` | Stores transform, recovery, interpolation, and locality evidence for one alignment. |
| `gauge_alignment/results/mesh.py` | Correlates model, common transport, selection, and alignment evidence for one mesh. |
| `gauge_alignment/results/__init__.py` | Exposes the deliberate public gauge-alignment result inventory. |
| `gauge_alignment/__init__.py` | Exposes definitions only; purpose-specific actions remain module-local. |

The maintained records are immutable and serialize deterministically. Arrays use nominal
Project Koios immutable NumPy construction and validation. Request admission is
zero-copy and rejects noncanonical mutable or wrongly typed storage rather than coercing
it. Generated equality is disabled for array-backed records; canonical typed JSON bytes
define exact serialized identity.

## Fixed parameter study

The frozen study uses

$$
r\in\{3,4,8,16\},\qquad L\in\{1,2,4,8\},
$$

with construction meshes $M\in\{513,1025,2049\}$ and a shifted $8191$-point
evaluation mesh. The global-unitary selection mesh is explicitly $M=2049$. Its selected
unitary is reused on both coarser construction meshes and all direct-evaluation points;
it is never refitted there.

Frame transformations act from the right on the retained space. Endpoint sewing acts
from the left on the ambient space. Principal phases lie in $(-\pi,\pi]$. The numerical
rank threshold is

$$
\tau_{\mathrm{rank}}=\max\!\left(10^{-12},10^{-10}\sigma_{\max}\right),
$$

with equality classified as deficient. Booleans, numeric strings, nonfinite tolerances,
alternative cutoffs, and inventories outside the frozen study are rejected.

## Transport boundary

`Periodic1DHigherRankAlignmentTransportOwnerResult.from_owner_outcome` converts one
PhysKit closed-loop transport result into immutable KSD evidence. It validates the
unshifted one-dimensional mesh, retained rank, ambient dimension, action conventions,
phase branch, tolerance, ordered links, and exact basis, frame, and sewing identities.
A deficient overlap stops transport and emits no fabricated later-link evidence.

Transport is computed from the analytic reference frame once per construction mesh. It
is neither fitted separately for each gauge alignment nor appended to pointwise-unitary
selection. Its evidence is correlated into the aggregate calculation result as a common
control.

## Gauge-alignment action decomposition

`Periodic1DHigherRankAlignmentAnalyzer` receives one complete immutable calculation
request and explicit Optimization, PhysKit, and KSD collaborators. Its zero-argument
`execute()` constructs an analytic case, performs the sole global selection at
$M=2049$, evaluates all construction meshes, delegates each prescribed gauge alignment
to `Periodic1DHigherRankGaugeAlignmentAnalyzer`, and delegates mesh-pair comparisons to
`Periodic1DHigherRankRefinementAnalyzer`.

For one gauge alignment and mesh, the typed stages are:

1. `Periodic1DHigherRankGaugeAlignmentConstructor` constructs the represented operator
   and aligned frame as one nominal immutable field record.
2. `Periodic1DHigherRankGaugeAlignmentRecoveryAnalyzer` checks recovery against the
   declared analytic or solver-owned construction.
3. `Periodic1DHigherRankGaugeAlignmentFourierAnalyzer` applies the PhysKit odd-mesh
   transform and evaluates coefficient-index, Parseval, and Hermiticity evidence.
4. `Periodic1DHigherRankGaugeAlignmentInterpolationAnalyzer` evaluates the complete
   Fourier series and direct analytic field on the shifted mesh.
5. `Periodic1DHigherRankGaugeAlignmentLocalityAnalyzer` evaluates every frozen symmetric
   support and keeps interpolation, truncation, and total error channels separate.
6. `Periodic1DHigherRankGaugeAlignmentResultAssembler` admits only evidence derived from
   the same exact analysis request and assembles the public mesh result without
   recomputing scientific values.

The stages retain their exact source request. Equal-looking replacement requests and
same-shaped arrays are insufficient. Admission correlates case, rank, depth, gauge
alignment, construction mesh, coordinates, selection provenance, statuses, immutable
storage, and authoritative action results.

## Result and failure semantics

A complete result retains:

- model-integrity evidence for every construction mesh;
- one global-selection record with rank and residual evidence;
- common closed-loop transport evidence for each construction mesh;
- four gauge-alignment mesh results per construction mesh;
- nine support results per qualified gauge alignment;
- both adjacent block-refinement comparisons; and
- the complete scalar-refinement inventory for $1025\rightarrow2049$.

Gauge-alignment mesh results retain the canonical odd-mesh disposition
`absent-on-odd-mesh`, not a legacy Nyquist phrase. Support records keep interpolation,
truncation, and total error channels distinct and retain ordinary omitted tails,
Parseval defects, perturbation bounds, decomposition residuals, and gate dispositions.
The public wire retains the bounded block-norm inventory for $|R|\le128$ rather than the
full Fourier coefficient arrays.

Documented Procrustes or transport backend failures become typed numerically unresolved
records with stable codes, absent downstream values, and no serialized exception
messages or tracebacks. Rank deficiency and integrity failure remain distinct. A failed
global-unitary selection suppresses only that gauge alignment; a failed common transport
control is retained separately and fails closed according to the calculation contract.

## Extensibility boundary without speculative APIs

The fieldwise construction and recovery equations can later be reused conceptually in
other dimensions because they act fiber by fiber. The present mesh, Fourier,
interpolation, and locality stages are deliberately periodic-1D owners. Two- and
three-dimensional studies require their own reviewed reciprocal meshes, multi-index
Fourier representatives, inversion closure, and support geometries.

Likewise, the present Procrustes and isometry contracts assume orthonormal frames and the
Euclidean $U(r)$ metric. A nonorthonormal study must first define its fiber metric,
metric adjoint, generalized isometry group, conditioning evidence, and objective. The
package contains no speculative base class, metric parameter, or placeholder 2-D/3-D
action.

## Independent-reference boundary

`Periodic1DHigherRankCoreInvariantReferenceAnalyzer` is the first bounded
producer-independent slice. It admits one exact calculation result and reconstructs the
analytic retained and exterior energies, constant frame, real Givens circuit, parent and
represented operators, projectors, isolation certificate, attack-angle certificate, and
all model-structure and recovery diagnostics with direct NumPy formulas. It does not
directly import or invoke the producer, the producer-owned analytic model, or the
reusable producer diagnostic actions. Scalar comparisons use the protocol's
$10^{-11}$ tolerance and sampled diagnostic arrays use $10^{-10}$.

`Periodic1DHigherRankFourierReferenceAnalyzer` is a second bounded slice. It performs
explicit negative-exponent, $1/M$-normalized Fourier sums for identity and
known-inverse-oracle fields on every construction mesh. It compares the retained block
norms, construction-mesh reconstruction, Parseval defect, and odd-mesh Hermitian pairing.
For both controls it evaluates the complete series by direct positive-exponent sums on
the shifted mesh and compares the six stored tail measures for every frozen support. For
the oracle it also compares the five analytic coefficient matrices at
$R=0,\pm1,\pm2$ and bounds every coefficient outside $|R|\le2$. The reference imports
only calculation records,
gauge identities, and quantity/comparison types; it does not invoke producer Fourier,
interpolation, locality, model, or reusable diagnostic actions.

These slices do not implement the protocol's complete direct-formula verifier. They do
not independently reconstruct transport, Procrustes selection, global- or
pointwise-unitary Fourier controls, support truncation and total-error fields,
error-channel decompositions, or refinement, and they do not own canonical result
bytes.

## Work remaining

Separately authorized work must complete producer-independent numerical recomputation,
add byte-owning complete-result verification, authenticated visualization data, and
retained execution composition. The direct development runner is replaceable and
explicitly emits no scientific evidence. Passing producer or bounded-reference tests
does not establish scientific validation.
