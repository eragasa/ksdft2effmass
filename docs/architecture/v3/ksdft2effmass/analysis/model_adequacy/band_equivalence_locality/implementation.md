# Implementation

## Typed request and result boundary

`BandEquivalenceLocalityCase` and `BandEquivalenceLocalityRequest` are domain-owned
`BaseTypedRecord` values. Their canonical mappings retain the family identity, spatial
dimension, parent and gauge selections, complete positive-bond inventory, direct-lattice
primitive basis with column-vector convention, basis offsets, mesh controls, sampled
parent scales and amplitudes, decreasing band tolerances, shell cap, amplitude-resolution
ladder, and transport-rank thresholds.

Canonical reconstruction requires the exact field inventory and built-in scalar and
tuple types. Constructors then enforce the scientific request invariants. The serializer
owns representation only; request meaning and validation remain with these records.

`BandEquivalenceLocalityAnalysis` is a plain immutable scientific result. It owns the
exact request and plain case results but no JSON or mapping behavior. Each point result
composes a `BandEquivalenceLocalityRepresentationEquivalenceAnalysis`, an immutable
`RepresentationEquivalence` result that owns the exact spatial dimension, retained rank,
direct-band, covariance, restricted-rotation, correlation, and operator-threshold
channel. Historical point attributes remain read-only projections of that result. Each
case result retains a
`BandEquivalenceLocalityMetricCovarianceDefectResult`; the result records the
ordinary-`Enum` probe identity and maximum absolute squared-length defect. The enum
inherits the common `StringWireEnum` behavior, whose `to_wire()` and `from_wire()`
methods explicitly map between enum members and stable built-in strings without making
members strings themselves. The retained record projection continues to
emit only the historical scalar defect, so existing
canonical result mappings and bytes do not change.
`BandEquivalenceLocalityAnalysisRecorder` binds one completed analysis and projects it
into `BandEquivalenceLocalityCalculationResult`, which passively binds the exact request
to retained `BandEquivalenceLocalityDiagnostics`. Construction checks family, mesh sizes,
and case ordering. Deserializing the retained result executes neither the analyzer nor
the recorder.

## Production composition

`BandEquivalenceLocalityAnalyzer` binds one immutable request at construction and exposes
zero-argument `execute()`. It returns `BandEquivalenceLocalityAnalysis` and composes:

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

`BandEquivalenceLocalityMetricCovarianceDefectAnalyzer` binds the nominal geometry and
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

`BandEquivalenceLocalityAnalysisRecorder` is the only production boundary that walks the
plain analysis graph to create these retained records. Record reconstruction never
recreates a scientific analyzer or replays the producer. Missing, unresolved,
inapplicable, rank-deficient, exact-zero, and positive-roundoff states are not collapsed
into one numeric sentinel.

## Exact-byte verification

`BandEquivalenceLocalityVerifier` binds both the immutable request and the retained
diagnostics before zero-argument `execute()`. `BandEquivalenceLocalityResultVerifier`
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
values, and named representation-equivalence result. The analyzer, recorder, concrete
diagnostic analyzers, and verifier are imported from their owning `analysis.py`,
`result.py`, `diagnostics.py`, and `verification.py` modules rather than re-exported from
the package root in this stage.

## Authenticated visualization

`BandEquivalenceLocalityVisualizationData` contains only case names, parent scales,
amplitudes, minimum operator thresholds, joint operator thresholds, and optional
normalized excess nonzero-hopping weights. It is not a second scientific result.

`BandEquivalenceLocalityVisualizationPlotEnum` closes the current inventory at one PNG:
`band-equivalence-locality-requirements.png`. The visualizer requires the typed
projection and typed passing verification before it constructs the figure. Figure code
maps authenticated values to marks and performs no parent construction, frame transport,
Fourier transformation, truncation, or new threshold calculation.

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
