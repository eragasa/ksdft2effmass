# Software realization of the higher-rank study

## Python modules

| Module | Scientific role |
|---|---|
| `rankN/_record_admission.py` | Centralizes exact-type, immutable-array, and nested-mapping admission shared by rank-$N$ records. |
| `rankN/diagnostics/frame.py` | Stores shared frame-recovery diagnostics. |
| `rankN/diagnostics/matrix.py` | Stores shared matrix-field error and comparison diagnostics. |
| `rankN/band_alignment/protocol.py` | Owns the shared frozen rank, depth, and construction-mesh inventories. |
| `rankN/band_alignment/configuration.py` | Stores the complete frozen study configuration, supports, phase convention, and tolerances. |
| `rankN/band_alignment/request.py` | Selects one rank/depth/construction-mesh transport and its physical identities. |
| `rankN/band_alignment/calculation.py` | Defines calculation controls and the complete frozen calculation request. |
| `rankN/band_alignment/model.py` | Constructs the analytic parent spectrum, retained frame, identity sewing, and gauge circuit. |
| `rankN/gauge_alignment/definition.py` | Defines the four gauge-alignment identities as strict `StringWireEnum` values. |
| `rankN/gauge_alignment/status.py` | Stores gauge-alignment outcomes, backend codes, and bounded downstream applicability. |
| `rankN/gauge_alignment/nyquist.py` | Defines the odd-mesh Nyquist disposition as a strict `StringWireEnum` value. |
| `rankN/gauge_alignment/procrustes/analysis.py` | Builds bounded global and pointwise Procrustes selection evidence. |
| `rankN/gauge_alignment/procrustes/result.py` | Stores complete Procrustes rank and integrity evidence. |
| `rankN/gauge_alignment/fields.py` | Constructs nominal immutable gauge-aligned operators and frames. |
| `rankN/gauge_alignment/request.py` | Correlates one complete gauge-alignment construction and analysis request. |
| `rankN/gauge_alignment/recovery.py` | Evaluates frame and represented-operator recovery. |
| `rankN/gauge_alignment/fourier.py` | Owns odd-mesh transforms and Fourier structural evidence. |
| `rankN/gauge_alignment/interpolation.py` | Owns direct and complete-series shifted-mesh evaluation. |
| `rankN/hopping_locality/analysis.py` | Measures coefficient tails and nested-range monotonicity without removing Fourier support. |
| `rankN/hopping_locality/result.py` | Owns immutable hopping-tail values without inheriting support-truncation semantics. |
| `rankN/support_truncation/analysis.py` | Constructs finite-support operators and owns the consequences of irreversible support removal. |
| `rankN/support_truncation/result.py` | Preserves the historical combined wire record while exposing admitted hopping-locality values without recomputation. |
| `rankN/band_alignment/composite/analysis/gauge_alignment.py` | Executes the gauge-alignment stages in scientific order as composite orchestration. |
| `rankN/band_alignment/composite/assembly.py` | Correlates stage evidence and assembles one aggregate alignment result. |
| `rankN/band_alignment/composite/result/frame_transport.py` | Stores request-bound closed-loop frame-transport evidence and bounded failures. |
| `rankN/band_alignment/composite/result/gauge_alignment.py` | Stores aggregate transform, recovery, interpolation, locality, and truncation evidence for one alignment. |
| `rankN/band_alignment/composite/result/mesh.py` | Correlates common transport, Procrustes selection, and alignment evidence for one mesh. |
| `rankN/band_alignment/composite/result/model.py` | Stores analytic-model integrity evidence owned by the composite result. |
| `rankN/band_alignment/composite/provenance.py` | Stores mesh-role separation and global-selection provenance. |
| `rankN/band_alignment/composite/refinement_results.py` | Stores block and scalar refinement results. |
| `rankN/band_alignment/composite/scalar_diagnostics.py` | Owns the scalar-diagnostic inventory used by refinement and aggregate admission. |
| `rankN/band_alignment/composite/refinement.py` | Analyzes correlated evidence across construction meshes. |
| `rankN/band_alignment/composite/calculation_result.py` | Stores and correlates the aggregate request-bound calculation result. |
| `rankN/band_alignment/composite/reference.py` | Independently reconstructs the analytic model and attack core invariants with direct NumPy formulas. |
| `rankN/band_alignment/composite/fourier_reference.py` | Independently reconstructs all four bounded Fourier controls with direct NumPy sums. |
| `rankN/band_alignment/composite/procrustes_reference.py` | Verifies aggregate Procrustes evidence with a producer-independent construction. |
| `rankN/band_alignment/composite/transport_reference.py` | Independently reconstructs the constant-frame closed route without the producer transporter. |
| `rankN/band_alignment/composite/analysis/calculation.py` | Composes Optimization, PhysKit, gauge alignment, transport, locality, truncation, and refinement owners. |
| `rankN/band_alignment/composite/analysis/mesh.py` | Owns construction coordinates and typed mesh/alignment dispositions. |
| `rankN/band_alignment/composite/analysis/evaluation.py` | Proves exact construction/evaluation mesh separation. |

The rank-first migration uses the scientific bases installed directly under
`ksdft2effmass`: representation equivalence, real-space support truncation, and
subspace reduction. It does not introduce duplicate bases beneath `periodic1d`.
The first migrated concrete slices are rank-N hopping locality and support
truncation. Hopping locality characterizes the unchanged Fourier coefficient field;
support truncation constructs a different finite-support representation and measures
its errors. Gauge identities, status, Procrustes selection, and fieldwise actions
reside under `periodic1d.rankN.gauge_alignment`; shared rank-$N$ diagnostics reside
under `periodic1d.rankN.diagnostics`; composite orchestration and aggregate records
reside under `periodic1d.rankN.band_alignment.composite`. The public calculation bytes
remain unchanged, and obsolete source paths are removed rather than retained as aliases.

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

`Periodic1DRankNAlignmentTransportOwnerResult.from_owner_outcome` converts one
PhysKit closed-loop transport result into immutable KSD evidence. It validates the
unshifted one-dimensional mesh, retained rank, ambient dimension, action conventions,
phase branch, tolerance, ordered links, and exact basis, frame, and sewing identities.
A deficient overlap stops transport and emits no fabricated later-link evidence.

Transport is computed from the analytic reference frame once per construction mesh. It
is neither fitted separately for each gauge alignment nor appended to pointwise-unitary
selection. Its evidence is correlated into the aggregate calculation result as a common
control.

## Gauge-alignment action decomposition

`Periodic1DRankNAlignmentAnalyzer` receives one complete immutable calculation
request and explicit Optimization, PhysKit, and KSD collaborators. Its zero-argument
`execute()` constructs an analytic case, performs the sole global selection at
$M=2049$, evaluates all construction meshes, delegates each prescribed gauge alignment
to the composite-owned `Periodic1DRankNGaugeAlignmentAnalyzer`, and delegates
mesh-pair comparisons to `Periodic1DRankNRefinementAnalyzer`.

For one gauge alignment and mesh, the typed stages are:

1. `Periodic1DRankNGaugeAlignmentConstructor` constructs the represented operator
   and aligned frame as one nominal immutable field record.
2. `Periodic1DRankNGaugeAlignmentRecoveryAnalyzer` checks recovery against the
   declared analytic or solver-owned construction.
3. `Periodic1DRankNGaugeAlignmentFourierAnalyzer` applies the PhysKit odd-mesh
   transform and evaluates coefficient-index, Parseval, and Hermiticity evidence.
4. `Periodic1DRankNGaugeAlignmentInterpolationAnalyzer` evaluates the complete
   Fourier series and direct analytic field on the shifted mesh.
5. `Periodic1DRankNHoppingLocalityAnalyzer` measures every frozen symmetric-range
   coefficient tail and its nested-range monotonicity without removing support.
6. `Periodic1DRankNSupportTruncationAnalyzer` constructs every frozen finite-support
   representation and keeps interpolation, truncation, and total error channels
   separate.
7. The composite-owned `Periodic1DRankNGaugeAlignmentResultAssembler` admits only
   evidence derived from the same exact analysis request and assembles the unchanged public mesh wire
   without recomputing scientific values.

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
Those combined fields remain solely for historical wire stability. The
`hopping_locality_tails` property projects admitted stored translations and tail values
into the separate diagnostic owner without rerunning Fourier analysis or truncation.
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

`Periodic1DRankNCoreInvariantReferenceAnalyzer` is the first bounded
producer-independent slice. It admits one exact calculation result and reconstructs the
analytic retained and exterior energies, constant frame, real Givens circuit, parent and
represented operators, projectors, isolation certificate, attack-angle certificate, and
all model-structure and recovery diagnostics with direct NumPy formulas. It does not
directly import or invoke the producer, the producer-owned analytic model, or the
reusable producer diagnostic actions. Scalar comparisons use the protocol's
$10^{-11}$ tolerance and sampled diagnostic arrays use $10^{-10}$.

`Periodic1DRankNFourierReferenceAnalyzer` is a second bounded slice. It performs
explicit negative-exponent, $1/M$-normalized Fourier sums for all four gauge-aligned
fields on every construction mesh. The global field uses an independently reconstructed
polar factor and the pointwise field uses the direct analytic inverse. It compares the
retained block norms, construction-mesh reconstruction, Parseval defect, and odd-mesh
Hermitian pairing. For every alignment it evaluates the complete series by direct
positive-exponent sums on the shifted mesh and compares the six stored tail measures for
every frozen support. For the oracle it also compares the five analytic coefficient matrices at
$R=0,\pm1,\pm2$ and bounds every coefficient outside $|R|\le2$. The reference imports
only calculation records, gauge identities, and quantity/comparison types; it does not
invoke producer Fourier, interpolation, locality, model, or reusable diagnostic actions.

`Periodic1DRankNProcrustesReferenceAnalyzer` is a third bounded slice. It constructs
the global cross matrix directly at the frozen $M=2049$ selection mesh and obtains its
unique right polar factor from an Hermitian eigendecomposition of the cross Gram matrix,
not the producer SVD solver. At each construction mesh it reconstructs the pointwise
right unitaries directly as the analytic attack adjoints. It compares singular spectra,
strict numerical ranks and cutoffs, rank margins, condition numbers, normalized
residuals, all retained integrity defects, deficient-point counts, and the selected
global right unitary. It does not import Optimization or invoke the producer model,
selection, or analysis actions.

`Periodic1DRankNTransportReferenceAnalyzer` is a fourth bounded slice. Because the
protocol reference frame and endpoint sewing map are constant identities, it constructs
the closed route directly. On every construction mesh it compares complete link singular
spectra, strict rank cutoffs and margins, ranks, unitary defects, closure phases, all three
closure right actions, closure validation residuals, normalized endpoint/primitive
closure defects, and deficient/unattempted counts. It does not import or invoke the
PhysKit transporter or producer analysis actions.

These slices do not implement the protocol's complete direct-formula verifier. They do
not independently reconstruct support-truncated and total-error fields, error-channel
decompositions, or refinement, and they do not own canonical result bytes.
Producer-independent denotes a separate direct-formula action path, not a separate
numerical-library stack: the references share NumPy/LAPACK and typed quantity/comparison
infrastructure with maintained code. Shared value and comparison types provide units and
admission but do not supply the reconstructed scientific values.

## Work remaining

Separately authorized work must complete producer-independent numerical recomputation,
add byte-owning complete-result verification, authenticated visualization data, and
retained execution composition. The direct development runner is replaceable and
explicitly emits no scientific evidence. Passing producer or bounded-reference tests
does not establish scientific validation.
