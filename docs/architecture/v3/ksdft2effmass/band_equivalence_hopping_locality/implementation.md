# Implementation

## Typed request and result boundary

`BandEquivalenceHoppingLocalityCase` and `BandEquivalenceHoppingLocalityRequest` are domain-owned
`BaseTypedRecord` values. Their canonical mappings retain the family identity, spatial
dimension, parent and gauge selections, complete positive-bond inventory, direct-lattice
primitive basis with column-vector convention, basis offsets, mesh controls, sampled
parent scales and amplitudes, decreasing band tolerances, shell cap, amplitude-resolution
ladder, and transport-rank thresholds.

Canonical reconstruction requires the exact field inventory and built-in scalar and
tuple types. Constructors then enforce the scientific request invariants. The serializer
owns representation only; request meaning and validation remain with these records.

`BandEquivalenceHoppingLocalityLossDefinition` is the shared periodic-2D/3D finite-rank
scientific definition. It composes a `BandEquivalenceHoppingLocalitySampleMeasure` and a
`BandEquivalenceHoppingLocalityComparisonIdentity` rather than encoding scientific identity in
a positional tuple. The sample measure owns spatial dimension, sample shape, exactly
normalized binary64 weights in NumPy C order, and the reciprocal-sample inventory
identifier. The comparison identity separately owns retained basis, retained space,
gauge, geometry, energy unit, and common energy-zero/alignment identifiers.

The definition's normalization is `retained_rank * norm_energy_scale**2`: rank two is
exactly the Ragasa2026a definition, while arbitrary declared finite rank uses the
cross-rank quadratic normalization selected by Ragasa2026c.
`BandEquivalenceHoppingLocalityLoss` nominally inherits the common
`RepresentationEquivalence` base and composes that complete definition with the two
dimensionless calculated losses; it does not create a parallel loss hierarchy.

`BandEquivalenceHoppingLocalityLossAnalyzer` binds the typed definition and finite complex128
fields whose matrices are exactly Hermitian, then evaluates the matrix-Frobenius and
ordered-spectrum finite sums directly. Binary64 overflow, underflow, or a nonfinite
squared term, weighted term, sum, normalization, or normalized result raises
`FloatingPointError`; neither route clips arithmetic. The independent-reference analyzer
separately admits immutable fields, checks exact Hermiticity elementwise, reconstructs
the rank/energy denominator, reconstructs scalar matrix-element and weighted sums, and
obtains each ordered spectrum through the separately invoked SciPy `evr` driver. It does
not call production admission or arithmetic, `MatrixFieldErrorAnalyzer`, derived RMS
channels, or support-selection owners. Its verification value inherits the common
`NumericalConsistency` base in addition to the reusable composite-verification record
base. `BandEquivalenceHoppingLocalityLossVerifier` requires exact typed-definition identity and
compares the two loss pairs at the installed `1.0e-10` tolerance. That comparison is
conditional on the supplied values and declarations; it does not itself authenticate the
provenance or organizational independence of the supplied reference value.

`BandEquivalenceHoppingLocalityLossRecord` owns only canonical typed serialization and
round-trip projection of this scientific value through the common `BaseTypedRecord`
serialization base. Historical calculation records and the existing square execution
bytes are unchanged. This owner establishes software behavior; it does not create or
authenticate a periodic-2D/3D scientific execution.

The current lifecycle gap relative to periodic-1D complete-five-scale ownership is
explicit:

| Lifecycle field | Periodic-1D complete five scale | Periodic-2D/3D rank two |
|---|---|---|
| Typed direct request and result | Installed | Installed |
| Independent direct-result verification | Installed | Installed |
| Explicit declared normalization energy scale \(E_{\mathrm{norm}}\) and finite-rank losses | Integrated rank-two calculation value | Shared rank-general loss value, record, and independent route installed; not added to historical direct-result bytes |
| Reciprocal-mesh comparison | Typed five-scale family | Separate calculation results plus a named adjacent-mesh refinement assessment; no collection owner |
| Cross-result refinement record | Installed | Installed without embedding or replacing source calculation results |
| Independent refinement reconstruction | Installed | Reconstructs adjacent-mesh changes from admitted retained diagnostics |
| Retained canonical cross-result bytes | Installed lifecycle, without authorized complete scientific execution | No retained square refinement-assessment artifact or execution authorized |
| Authenticated visualization | Installed | Direct-result visualization only; no refinement-specific renderer installed |
| Scientific evidence created by this implementation | No | No |

The square-study boundary preserves each calculation result as its scientific owner.
Cross-result evidence is limited to the named refinement assessment; there is no generic
aggregate record, verifier, projection, renderer, or second calculation lifecycle. This
does not mutate the historical `direct-square-rank2-n16` record, claim that its
refinement entrypoints were executed together, or supply convergence classifications.

`BandEquivalenceHoppingLocalityAnalysis` is a plain immutable scientific result. It owns the
exact request and plain case results but no JSON or mapping behavior. Each point result
composes a `BandEquivalenceHoppingLocalityRepresentationEquivalenceAnalysis`, an immutable
`RepresentationEquivalence` result that owns the exact spatial dimension, retained rank,
direct-band, covariance, restricted-rotation, correlation, and operator-threshold
channel. Historical point attributes remain read-only projections of that result. Each
case result retains a
`BandEquivalenceHoppingLocalityMetricCovarianceDefectResult`; the result records the
ordinary-`Enum` probe identity and maximum absolute squared-length defect. The enum
inherits the common `StrWireEnum` behavior, whose `to_wire()` and `from_wire()`
methods explicitly map between enum members and stable built-in strings without making
members strings themselves. The retained record projection continues to
emit only the historical scalar defect, so existing
canonical result mappings and bytes do not change.
`FourierSeriesBlockHoppingRepresentation` owns the representation-only projection from
one finite Fourier matrix series into a sorted, immutable PhysKit dense block-hopping
value. It preserves coefficient bytes and assigns provider identities but does not assign
KSD scientific-model identity, infer geometry, select support, or analyze locality. The
periodic-2D and periodic-3D rank-two hopping-locality request owners instead require one
complete exact dimensional block-hopping model. This prevents a mesh-transformed
floating-point series from being silently promoted into an exact scientific model when
its opposite-displacement blocks differ from conjugate transposes by roundoff. The
historical aggregate analyzer retains its representation-level Fourier diagnostic and
therefore preserves existing numerical behavior and retained result bytes.

`BandEquivalenceHoppingLocalityAnalysisRecorder` binds one completed analysis and projects it
into `BandEquivalenceHoppingLocalityCalculationResult`, which passively binds the exact request
to retained `BandEquivalenceHoppingLocalityDiagnostics`. Construction checks family, mesh sizes,
and case ordering. Deserializing the retained result executes neither the analyzer nor
the recorder.

## Square-study refinement composition

The square calculation results remain independently owned and admitted. The
`BandEquivalenceHoppingLocalityRefinementAssessmentRecord` is the only cross-result value: it
retains adjacent-mesh changes and explicit unresolved dispositions without copying the
source results into a new root record. The
`BandEquivalenceHoppingLocalityRetainedRefinementReferenceAnalyzer` reconstructs those changes
from retained diagnostics without invoking the production analyzer.

The square study currently has no retained refinement-assessment artifact, no installed
convergence policy, and no refinement-specific visualization lifecycle. Momentum and
amplitude classifications therefore remain `unresolved`. Complete physical-metric shells
remain indivisible, and any future finite-rank loss comparison must retain its declared
basis, retained-space, gauge, geometry, reciprocal-sample inventory, energy-unit,
energy-reference, and normalization identities.

## Analyzer hierarchy guardrail

Analyzer ownership follows one explicit domain, periodicity, dimension, and rank chain:

```text
BandEquivalenceHoppingLocalityAnalyzer
└── PeriodicBandEquivalenceHoppingLocalityAnalyzer
    ├── Periodic1DBandEquivalenceHoppingLocalityAnalyzer
    │   ├── Periodic1DRank2BandEquivalenceHoppingLocalityAnalyzer
    │   └── Periodic1DRankNBandEquivalenceHoppingLocalityAnalyzer
    ├── Periodic2DBandEquivalenceHoppingLocalityAnalyzer
    │   ├── Periodic2DRank2BandEquivalenceHoppingLocalityAnalyzer
    │   └── Periodic2DRankNBandEquivalenceHoppingLocalityAnalyzer
    └── Periodic3DBandEquivalenceHoppingLocalityAnalyzer
        ├── Periodic3DRank2BandEquivalenceHoppingLocalityAnalyzer
        └── Periodic3DRankNBandEquivalenceHoppingLocalityAnalyzer
```

The periodic-2D and periodic-3D rank-N analyzer roles additionally inherit
`PeriodicRankNBandEquivalenceHoppingLocalityAnalyzerRole`. That common role owns only the
cross-dimensional periodic rank-N contract; each concrete role also retains its
corresponding dimensional branch above. The same additive ownership applies to the
rank-N capability, request, analysis, case, value, and action roles. It does not make one
dimension inherit from the other.

Rank-two and rank-N analyzers are sibling specializations. Neither rank branch inherits
from the other. `Rank2BandEquivalenceHoppingLocalityAnalyzer` separately owns the shared
rank-two arithmetic composed by the periodic-2D and periodic-3D rank-two analyzers; it is
not a rank-N parent. Dimension-neutral rank-N leaf-result parents centralize validation
without replacing the exact periodic-2D and periodic-3D result types. This hierarchy is
an enforceable ownership guardrail rather than a compatibility export tree.

## Production composition

The periodic-2D and periodic-3D rank-N case analyzers inherit one internal common
production-arithmetic parent for coordinate grids, finite-Fourier transformation and
evaluation, ordinary-mode filtering, right-unitary action, and alignment-identity sample
counting. Each dimensional analyzer still owns its exact request and model admission,
mesh and geometry selection, transport topology, gauge-alignment collaborators,
hopping-locality route, support-truncation route, result construction, and public return
type.

Independent reconstruction does not inherit that production parent. Parent and alignment
references share a separate direct-formula implementation across dimensions. Fourier,
shell, error, and support references share a separate explicit dense-sum implementation.
The reference implementations do not call the production transformer, evaluator, model,
shell classifier, hopping-locality analyzer, or support selector for the quantity being
checked.

`Rank2BandEquivalenceHoppingLocalityAnalyzer` binds one immutable rank-two request at
construction and exposes
zero-argument `execute()`. It returns `BandEquivalenceHoppingLocalityAnalysis` and composes:

1. one declared four-state synthetic parent field;
2. the lowest rank-two retained spectral frame;
3. closed frame transport and its qualification diagnostics;
4. one declared smooth real-orthogonal gauge rotation;
5. reference and comparison represented rank-two Hamiltonian fields;
6. complete multidimensional finite Fourier transforms;
7. cyclic-to-ordinary and Nyquist diagnostics;
8. PhysKit-owned raw squared Frobenius powers for each typed hopping block;
9. KSD-owned retained-rank normalization and complete physical-metric shell aggregation;
10. complete physical-metric shell truncations;
11. one dimension-selected, campaign-owned primitive-basis covariance probe; and
12. point, shell, tolerance-selection, amplitude-resolution, and case aggregates,
    with historical first-passing wire projections preserved.

`BandEquivalenceHoppingLocalityMetricCovarianceDefectAnalyzer` binds the nominal geometry and
one private immutable probe definition at construction. That correlated definition owns
the probe identity, forward integral basis transform, inverse transform, and complete
sample-displacement inventory. Execution therefore applies already-bound policy rather
than selecting or assembling campaign controls during numerical evaluation.

Optimization supplies constructor-bound, unit-free finite-periodic Fourier operations.
PhysKit supplies constructor-bound physical transform, tensor-evaluation, Parseval, and
Hermiticity actions, the direct-lattice metric, typed block-hopping model, and raw
unit-aware block-power analyzer. Each action binds its complete scientific definition
before a zero-argument result operation; the analyzer does not retain reusable
input-free transform or evaluator collaborators. `MetricShellHoppingPowerAnalyzer` binds
that PhysKit analyzer with one immutable model, exact shell-label inventory, and retained
rank before zero-argument execution. KSD
retains the state-space interpretation, shell grouping, normalization policy, and
scientific composition. Public scalar, shell, rank, displacement, and collaborator inputs
are checked by exact type; booleans are not admitted as integers. No generic solver,
workflow, registry, reflective codec, or calculation-tree import is introduced.

## Basis-distance analyzer investigation

`basis_distance_range()` is not yet promoted to an action object. Its current calculation
maps each fractional vector

```text
retained displacement + target basis offset - source basis offset
```

through the direct primitive basis and takes extrema over every supplied displacement and
every ordered source/target basis pair. It includes onsite same-basis zero vectors, so an
applicable minimum can be zero. An empty `basis_offsets` inventory currently returns the
pair `(None, None)`.

A scientifically complete successor should instead bind one nominal
`BasisResolvedMetricGeometry` and one admitted `ConjugateClosedSupport`, expose a
zero-argument operation, and return closed immutable outcomes. The recommended
inapplicable outcome records `NO_EXPLICIT_BASIS_OFFSETS`; the applicable outcome covers
all admitted-support basis-pair images, preserves the historical including-self extrema,
and may add a separately named minimum-positive distance rather than silently changing
the existing minimum.

A unit decision blocks that extraction. PhysKit's `DirectLatticeMetric` preserves one
caller-declared consistent length convention but intentionally attaches no unit. The
current KSD case mapping retains primitive-basis numbers and fractional basis offsets but
no length-convention identifier. The recommended convention for these synthetic families
is a regular enum identifying a synthetic direct-lattice length unit, with explicit
enum-to-string and string-to-enum mapping. Adding that identity to retained request bytes
requires a new schema version; it must not be inserted into the existing mapping. Until
that schema decision is authorized, the function remains a compatibility projection and
no typed analyzer claims a physical or reduced-unit interpretation for its scalars.

This distance-only projection does not establish orbital-resolved locality. It does not
retain ordered state identities or associate a distance with the corresponding
$\lvert T_{\alpha\beta}(\mathbf n)\rvert^2$. It also lacks the localization and gauge
provenance required for MLWF-resolved locality. Those peer capabilities belong to the
[`ksdft2effmass.hopping_locality`](../hopping_locality/index.md) architecture rather than
being inferred from `basis_offsets`.

## Scientific results and retained records

`results/` owns plain immutable scientific values. Representation-equivalence, point,
shell, error-channel, amplitude-resolution, tolerance-selection projection, and case
values do not inherit `BaseTypedRecord` and do not expose mapping or JSON methods. They
remain inside the scientific object graph returned by the analyzer. The dimension-
independent selection itself is owned by
`real_space_support_truncation.RealSpaceSupportTruncationToleranceSelector`; the family
result projects that typed result to its historical retained fields.

`records/` owns the corresponding retained projections rather than one untyped mapping:

- `ErrorChannels` retains rank-normalized matrix-Frobenius maximum/RMS errors and
  ordered-eigenvalue maximum-absolute/RMS errors;
- `ShellDiagnostic` separates reference/comparison truncation and total channels,
  shell power, omitted power, and Parseval defects;
- `FirstPassingDecision` preserves the historical wire names for minimum tolerance-
  satisfying shell supports and their adjacent errors;
- `PointDiagnostic` retains parent, frame, transport, gauge, Fourier, power, support,
  and applicability diagnostics for one sampled point;
- amplitude records retain flat analytic resolution and midpoint checks;
- `CaseDiagnostic` groups one geometry/parent case; and
- the calculation and verification diagnostic roots retain one family and mesh
  inventory.

`BandEquivalenceHoppingLocalityAnalysisRecorder` is the only production boundary that walks the
plain analysis graph to create these retained records. Record reconstruction never
recreates a scientific analyzer or replays the producer. Missing, unresolved,
inapplicable, rank-deficient, exact-zero, and positive-roundoff states are not collapsed
into one numeric sentinel.

## Exact-byte verification

`BandEquivalenceHoppingLocalityVerifier` binds both the immutable request and the retained
diagnostics before zero-argument `execute()`. `BandEquivalenceHoppingLocalityResultVerifier`
is constructed from built-in immutable result bytes and that fully bound independent
verifier. It:

1. hashes the exact supplied bytes internally;
2. reconstructs the passive typed result from those same bytes;
3. invokes the independent diagnostic route rather than the production analyzer;
4. constructs concrete `BaseDiagnosticAnalyzer` actions for stored identity,
   independent parent, independent band, and independent shell-power defects and obtains
   their immutable `DiagnosticObservation` results;
5. derives the visualization projection from the admitted result;
6. hashes the projection's canonical bytes; and
7. returns one typed verification/projection pair.

`admit_stored()` independently reconstructs that pair and requires exact canonical-byte
equality for both the stored verification and stored projection. A digest authenticates
identity and integrity only. The fixed verification tolerances are software comparison
controls, not physical uncertainties or scientific acceptance thresholds.

The package root deliberately exports the stable request/case enums, retained diagnostic
values, named representation-equivalence result, and shared finite-rank loss surfaces.
The direct calculation analyzer, recorder, concrete diagnostic analyzers, and direct-result verifier remain
imported from their owning `analysis.py`, `result.py`, `diagnostics.py`, and
`verification.py` modules rather than re-exported from the package root in this stage.

## Authenticated visualization

`BandEquivalenceHoppingLocalityVisualizationData` contains only case names, parent scales,
amplitudes, minimum operator thresholds, joint operator thresholds, and optional
normalized excess nonzero-hopping weights. It is not a second scientific result.

`BandEquivalenceHoppingLocalityVisualizationPlotEnum` closes the direct-result inventory at one
PNG: `band-equivalence-locality-requirements.png`. The visualizer requires its typed
projection and typed passing verification before it constructs a figure. Figure code
maps authenticated values to marks and performs no parent construction, frame transport,
Fourier transformation, truncation, loss reconstruction, or new threshold calculation.

## Direct family stages

The orthogonal periodic-2D square, nonorthogonal periodic-2D triangular/honeycomb,
orthogonal periodic-3D simple-cubic, and nonorthogonal periodic-3D FCC/diamond
calculation roots each contain:

```text
run_01_calculation.py → run_02_verification.py → run_03_render.py
```

The scripts follow the Periodic1D direct-stage guide: module-scope composition, no
functions or classes, no `main()`, no Workflow, no custom JSON transport, exact byte
hashes, no-overwrite gates, incomplete directories, and same-filesystem renames.
Calculation writes canonical request and result bytes. The execution, execution-
verification, and rendering documents are domain-owned `BaseTypedRecord` values in
`lifecycle.py`; scripts use only their final `to_json()`/`from_json()` boundary and do
not decode or assemble loose lifecycle mappings. Verification authenticates the
completed calculation and writes the typed verification/projection pair. Rendering
readmits that pair against the exact result bytes before producing the closed PNG
inventory.

The direct identities are `direct-square-rank2-n16`,
`direct-triangular-honeycomb-rank2-n16`, `direct-simple-cubic-rank2-n8`, and
`direct-fcc-diamond-rank2-n8`. All four definitions are local, deterministic, synthetic,
and unsealed. Every stage set except the square case is installed without creating an
execution. The triangular/honeycomb composition keeps matched-square and triangular
Bravais controls, honeycomb basis offsets, bond-RMS normalization, and its explicit
non-graphene claim boundary. The FCC/diamond composition keeps the matched-simple-cubic
and FCC Bravais controls, diamond basis offsets, bond-RMS normalization, and its explicit
non-silicon claim boundary. Refinement scripts and historical development rendering
remain separate until a later reviewed migration; these nominal lifecycles do not
relabel them.
