# Architecture v3 component-construction and visualization audit

## Scientific and software question

Which concrete Architecture v3 actions bind a complete scientific request before
execution, which installed predecessors still expose context-free action objects, and
where should authenticated visualization mechanics live so that model-system and
Periodic1D families do not depend on the wrong domain owner?

## Status and claim boundary

This is a manually classified architecture audit of source commit
`8555cb3200b86e5b160d75ae80db04e173ba066f`. It records current source behavior and a
target construction rule. It changes no runtime, result wire, numerical method,
tolerance, retained artifact, or scientific conclusion.

The audit establishes neither scientific validation nor authorization to execute a
calculation. It does not authorize rewriting historical result, verification,
rendering, or provenance bytes.

## Scope and method

The primary scope is the implemented Architecture v3 vertical slices and their direct
reusable dependencies:

- PIAB1D;
- QHO1D;
- Mathieu1D;
- Periodic1D rank-one Fourier locality; and
- Periodic1D rank-two composite-band alignment and locality.

A secondary source scan covered action-like classes under the installed `analysis`,
`hamiltonian`, `model_systems`, `operators`, `periodic1d`, `serialization`, and `spaces`
owners. An action-like class name contains `Analyzer`, `Calculator`, `Comparator`,
`Constructor`, `Fitter`, `Interpolator`, `Selector`, `Solver`, `Transformer`,
`Transporter`, `Truncator`, `Verifier`, `Visualizer`, or `Writer`. Each reported class
was then inspected rather than accepted solely from its name.

A concrete action is *empty-callable* when its runtime constructor accepts no required
argument because it inherits `object.__init__`, declares an explicit no-argument
constructor, makes every constructor argument optional, or supplies defaults for every
dataclass field. Abstract bases, enumerations, immutable scientific value records, unit
values, exceptions, and third-party classes are outside this action-construction rule.

The initial heuristic inventory contained 75 names. Manual constructor inspection
removed record false positives and inspection of direct V3 call sites added five
`solidstate` actions omitted by the initial package filter. The classified inventory
below therefore contains 78 installed KSD actions:

- 39 in the current V3 migration boundary;
- 4 transitional Periodic1D predecessor actions to remove rather than migrate; and
- 35 adjacent installed actions deferred to their own architecture owner.

The five direct lifecycle source trees and their calculation/report scripts contain 54
empty-action construction sites covering 36 unique actions. Counts describe software
structure only; they are not scientific evidence.

## Frozen construction rule

Every maintained concrete V3 action must bind and admit its complete request before its
terminal operation:

```python
result = DomainAction(request).execute()
```

The following rules apply.

1. A concrete action constructor has at least one required, explicitly typed domain
   argument. There is no supported empty construction.
2. The constructor performs local type and invariant admission and stores the admitted
   request or required collaborator. It performs no scientific calculation.
3. The terminal operation accepts no scientific request arguments. Top-level lifecycle
   analyzers, calculators, and independent reference actions use `execute()`.
4. A request is family-owned and immutable. This audit does not introduce a universal
   request, configuration, result, or dependency container.
5. An upstream scientific result is supplied as exact immutable bytes where byte
   identity matters. An action must not construct or invoke another family's producer
   to obtain that result.
6. A collaborator that selects an algorithm, tolerance, backend, or policy is explicit
   constructor state. `None` must not silently select a required scientific
   collaborator.
7. A child action may be constructed internally only with its complete explicit domain
   request. Context-free `ChildAction().execute(request)` composition is not the target.
8. Verifiers bind exact subject bytes at construction. Visualization actions bind the
   authenticated projection and the passing verification at construction.
9. Historical implementations are removed after consumer migration; compatibility
   aliases and empty-constructor facades are not added.

Prospective V3 action pages already demonstrate the intended shape with
`OrthogonalSubspaceComparator(request).compare()`,
`RealSymmetricReferenceResidualAnalyzer(request).analyze()`,
`RealSymmetricRetainedOperatorComparator(request).compare()`, and
`SymmetricGramOrthonormalizer(request).orthonormalize()`. Their domain-specific terminal
verbs remain prospective owner decisions; they do not justify empty construction.

## Current V3 migration boundary

The following 40 installed actions were identified directly in an implemented V3
family or among the reusable dependencies composed by those families. The rows not
superseded by completed slices below require request-bound migration before the direct
families are construction-coherent with Phase 4.

| Source | Initially empty-callable concrete actions | Disposition |
|---|---|---|
| `analysis/convergence.py` | `RelativeErrorConvergenceAnalyzer` | Bind the convergence request. |
| `analysis/hopping_diagnostics.py` | `HoppingParsevalAnalyzer1D`; `ScalarHoppingBandShapeAnalyzer1D`; `BlockHoppingHermiticityAnalyzer1D` | Bind each declared diagnostic request. |
| `analysis/hopping_fits.py` | `BlockHoppingLeastSquaresFitter1D`; `ScalarHermitianHoppingLeastSquaresFitter1D`; `BlockHoppingModelComparator1D` | Bind samples, basis/range controls, and declared comparison inputs. |
| `analysis/operators/decomposition.py` | `KineticPotentialDecompositionAnalyzer` | Require its decomposition request and policy-bearing fitter; do not synthesize the fitter from `None`. |
| `analysis/operators/eigenpair_diagnostics.py` | `RealSymmetricEigenpairDiagnosticAnalyzer` | Bind the eigensystem and represented operator request. |
| `analysis/operators/model_fitting.py` | `RetainedModelClassFitter` | Bind the retained-model fitting request. |
| `analysis/periodic_bands.py` | `BandApproximationErrorAnalyzer1D` | Bind candidate and reference band samples. |
| `analysis/probability_selection.py` | `TailProbabilitySelector` | Bind the probability-selection request. |
| `hamiltonian/blocks.py` | `OrthogonalHamiltonianBlockAnalyzer` | Bind Hamiltonian and subspace inputs. |
| `hamiltonian/subspaces.py` | `OrthogonalSpectralSubspaceSelector` | Bind the eigensystem and retained dimension. |
| `model_systems/mathieu1d/analysis.py` | `Mathieu1dAnalyzer` | Bind the complete Mathieu1D configuration and result identity; rename `calculate()` to zero-argument `execute()`. |
| `model_systems/periodic_1d/finite_differences.py` | `PeriodicFiniteDifferenceFiberHamiltonian1DConstructor` | Bind the finite-difference fiber request. |
| `model_systems/periodic_1d/plane_waves.py` | `PlaneWaveFiberHamiltonian1DConstructor` | Bind the plane-wave fiber request. |
| `model_systems/piab1d/analysis/core.py` | `Piab1dAnalyzer` | Bind the PhysKit solution and retained dimension. |
| `model_systems/piab1d/analysis/grid_sweep.py` | `Piab1dGridSweepAnalyzer` | Bind the grid-sweep request. |
| `model_systems/piab1d/analysis/verification/core.py` | `Piab1dCoreReferenceAnalyzer` | Bind admitted PIAB1D result data. |
| `model_systems/piab1d/analysis/verification/decomposition.py` | `Piab1dKineticPotentialDecompositionReferenceAnalyzer` | Bind admitted decomposition inputs. |
| `model_systems/piab1d/analysis/verification/eigenpair_convergence.py` | `Piab1dEigenpairSweepReferenceAnalyzer` | Bind admitted sweep inputs. |
| `model_systems/piab1d/analysis/verification/finite_algebraic_diagnostics.py` | `Piab1dFiniteAlgebraicDiagnosticsReferenceAnalyzer` | Bind admitted finite-algebra inputs. |
| `model_systems/piab1d/analysis/verification/reference.py` | `Piab1dIndependentReferenceAnalyzer` | Bind the complete independently admitted result subject; do not synthesize five empty reference actions. |
| `model_systems/piab1d/analysis/verification/residual_norms.py` | `Piab1dResidualNormSweepReferenceAnalyzer` | Bind admitted residual-sweep inputs. |
| `model_systems/qho1d/analysis.py` | `Qho1dAnalyzer` | Bind configuration and result identity; construct each request-bound comparator only after the exact case models exist. |
| `model_systems/qho1d/comparison.py` | `Qho1dComparator` | Bind the common-coordinate comparison request. |
| `model_systems/qho1d/cross_grid.py` | `Qho1dCrossGridAnalyzer`; `Qho1dCrossGridVerifier` | Bind the calculation, and bind the analysis as an additional verifier subject. |
| `model_systems/qho1d/parameters.py` | `Qho1dNondimensionalizer` | Bind the exact positive finite normalized scalars before explicit Unitless adaptation. |
| `model_systems/qho1d/verification.py` | `Qho1dIndependentReferenceAnalyzer` | Bind the admitted result subject. |
| `periodic1d/fourier_locality/analysis.py` | `Periodic1DFourierLocalityAnalyzer` | Bind the Fourier-locality configuration. |
| `periodic1d/fourier_locality/verification_values.py` | `Periodic1DFourierLocalityIndependentVerifier` | Bind the admitted result reconstructed from exact bytes. |
| `periodic1d/composite_band_alignment/analysis.py` | `Periodic1DCompositeBandAlignmentAnalyzer` | Bind the composite-alignment configuration. |
| `periodic1d/composite_band_alignment/verification_values.py` | `Periodic1DCompositeBandAlignmentIndependentVerifier` | Bind the admitted result reconstructed from exact bytes. |
| `solidstate/band_frames.py` | `PolarBandFrameTransporter1D` | Bind the frame path and transport threshold. |
| `solidstate/hopping_transforms.py` | `BandProjectedOperatorPathConstructor1D`; `BlockHoppingInterpolator1D`; `ReciprocalOperatorFourierTransformer1D`; `BlockHoppingTruncator1D` | Bind each complete represented-operator, mesh, interpolation, transform, or truncation request. |

The first bottom-up remediation slice implements the `solidstate/hopping_transforms.py`
row with four immutable request records, request-bound constructors, and zero-argument
`execute()` methods. Direct family and transitional predecessor consumers now construct
complete requests. The obsolete `analysis.single_band_reduction` package and the
campaign-level `Periodic1DHoppingReductionWorkflow` surface were retired instead of
being adapted to the new action API; no compatibility facade remains. The next
bottom-up slice implements the `solidstate/band_frames.py` row with an immutable
polar-transport request, a request-bound transporter, and a zero-argument terminal
operation. The next two analysis slices implement the `analysis/hopping_diagnostics.py`
and `analysis/hopping_fits.py` rows with six immutable request records, request-bound
actions, and zero-argument `execute()` methods. Their direct-family and transitional
predecessor consumers now provide complete requests, and no empty construction of
those six actions remains. The following slice implements the targeted
`analysis/periodic_bands.py` row with an immutable band-approximation error request and
a request-bound analyzer. Mathieu1D, composite alignment, and the transitional
multiband predecessor now bind each target/candidate sample pair independently. The
PIAB1D analysis slice then implements the `analysis/convergence.py` and
`analysis/probability_selection.py` rows with complete immutable requests and
zero-argument terminal operations. Its reusable observed-order child action is also
request-bound so the convergence analyzer composes only complete child requests. The
next bottom-up slice implements `analysis/operators/model_fitting.py` before its
`analysis/operators/decomposition.py` consumer. The decomposition analyzer now requires
its complete matrix request and an explicit fitter bound to the exact admitted shift;
it no longer synthesizes a fitter from `None`. The subsequent leaf slice binds each
real-symmetric eigensystem and optional reference-vector set in an immutable diagnostic
request; PIAB1D core and grid-sweep composition now construct complete per-eigensystem
diagnostic actions instead of retaining one empty reusable action. The following
Hamiltonian leaf slice binds the ordered real eigensystem and retained dimension in an
immutable `OrthogonalSpectralSubspaceSelectionRequest`; PIAB1D constructs the complete
selector only after its eigensystem request exists. The next Hamiltonian leaf slice
binds the finite Hamiltonian and exact orthogonal subspace in an immutable
`OrthogonalHamiltonianBlockRequest`; PIAB1D no longer retains an empty block analyzer.
With those leaf dependencies complete, the PIAB1D core slice binds the exact PhysKit
solution and retained dimension in `Piab1dAnalysisRequest`; the top-level analyzer now
has a zero-argument terminal operation. The companion grid-sweep slice uses the
existing immutable `Piab1dGridSweepDefinition` as its complete request and makes the
analyzer constructor-bound with a zero-argument `execute()`. Verification migration
then proceeds leaf-first: `Piab1dCoreReferenceAnalyzer` binds the exact typed result and
verifier-derived visualization projection in `Piab1dCoreReferenceRequest`, and the
aggregate constructs that complete child action only after both subjects exist. The
next verifier leaf binds the exact typed eigenpair-sweep result in
`Piab1dEigenpairSweepReferenceRequest` before independent dispersion reconstruction.
The following leaf likewise binds the exact residual-norm sweep in
`Piab1dResidualNormSweepReferenceRequest` before independent operator reconstruction
and norm comparison. The finite-algebraic verifier leaf then binds its exact typed
result in `Piab1dFiniteAlgebraicDiagnosticsReferenceRequest` before applying
independently derived floating-point bounds. The final verifier leaf binds the exact
decomposition result and authoritative reduced Hamiltonian in
`Piab1dKineticPotentialDecompositionReferenceRequest`, including local shape and unit
correlation, before independent projection reconstruction. The aggregate reference
analyzer now binds the complete result and verifier-derived visualization projection
in `Piab1dIndependentReferenceRequest`; its zero-argument `execute()` constructs each
complete child request only from that admitted subject. The QHO1D remediation begins
at the common-coordinate leaf: `Qho1dComparator` now binds the existing complete
`Qho1dComparisonRequest`, and the sweep composition constructs each request-bound
comparator only after the exact case models exist. `Qho1dAnalyzer` then binds the
configuration and full result identity in `Qho1dAnalysisRequest`; its zero-argument
`execute()` owns only deterministic calculation composition. The adjacent-grid
analysis then binds the complete calculated subject in
`Qho1dCrossGridAnalysisRequest` before deriving its ordered finite-representation
change diagnostics. `Qho1dCrossGridVerificationRequest` subsequently correlates that
analysis with the exact calculated subject before direct recomputation. Both actions
share a cohesive case inventory rather than a dangling lookup function. The QHO1D
independent-reference route binds the result and verifier-derived projection in
`Qho1dIndependentReferenceRequest`; its internal scientific operations are cohesive
instance methods rather than static or class utility methods. A follow-up completeness
audit identified the previously omitted `Qho1dNondimensionalizer`; it now binds
positive finite built-in floats in `Qho1dNondimensionalizationRequest` before
explicit Unitless adaptation.

Two current sources also construct empty third-party numerical actions:
`NumpyUniformClosedIntervalTrapezoidalRule()` in
`model_systems/piab1d/analysis/core.py:243` and
`NumpyBatchedComplexUnitaryProcrustesSolver()` in
`periodic1d/composite_band_alignment/analysis.py:123`. Those external class contracts
are outside the 78-class KSD inventory, but the selected collaborator must become an
explicit required dependency at the KSD composition boundary rather than remain a
hidden default.

The direct composition roots currently expose the empty top-level calls at
`calculations/piab1d/run_01_calculation.py:55`,
`calculations/qho1d/run_01_calculation.py:49`,
`calculations/mathieu1d/run_01_calculation.py:96`,
`calculations/periodic1d/rank1/fourier-locality/run_01_calculation.py:53`, and
`calculations/periodic1d/rank2/composite-band-alignment-locality/run_01_calculation.py:55`.
The rank-two review renderer repeats the pattern at
`calculations/periodic1d/rank2/composite-band-alignment-locality/technical-report/render_review_figures.py:49`.

## Transitional Periodic1D predecessors

These four actions are not migration targets. Phase 4 must replace their consumers and
then remove them under the existing predecessor-retirement gate.

| Source | Empty-callable concrete action | Disposition |
|---|---|---|
| `periodic1d/multiband_alignment/calculate.py` | `Periodic1DMultibandAlignmentCalculator` | Remove after all admissible-set consumers migrate. |
| `periodic1d/multiband_alignment/verify.py` | `Periodic1DMultibandAlignmentResultVerifier` | Remove with the predecessor result contract. |
| `periodic1d/admissible_sets/calculate.py` | `Periodic1DConstrainedAdmissibleSetCalculator` | Replace with request-bound Phase 4 actions. |
| `periodic1d/admissible_sets/verify.py` | `Periodic1DConstrainedAdmissibleSetResultVerifier` | Replace with exact-byte-owning Phase 4 verification. |

The installed defect is explicit at
`periodic1d/admissible_sets/calculate.py:77`, where
`Periodic1DMultibandAlignmentCalculator().execute(...)` implicitly produces an upstream
baseline. Phase 4 must instead receive independently admitted upstream bytes and their
calculated digest as explicit dependencies. A stored pass label is not an upstream
subject.

## Adjacent installed actions

The following 35 installed actions are genuinely empty-callable, but they are not in
the current five-family direct lifecycle. They remain defects relative to the frozen V3
construction rule, but changing them in the Phase 4 preparation slice would combine
unrelated owners. Each must be revisited when its owner receives a V3 migration or when
a current V3 caller begins depending on it.

| Owner | Empty-callable concrete actions | Revisit condition |
|---|---|---|
| `analysis/_band_comparison.py` | `BandStructureComparator` | Band-comparison V3 migration. |
| `analysis/bound_subspaces.py` | `BoundStateProjectorConstructor`; `BoundSubspaceLocalizationAnalyzer` | Bound-subspace V3 migration. |
| `analysis/finite_domain_locality.py` | `SparseLocalityResidualAnalyzer` | Finite-domain locality migration. |
| `analysis/finite_domain_spectra.py` | `HostEdgeBoundStateAnalyzer` | Finite-domain spectrum migration. |
| `analysis/matrix_field/diagnostics/comparison.py` | `MatrixFieldErrorAnalyzer`; `MatrixFieldComparisonAnalyzer`; `MatrixErrorDecompositionAnalyzer` | Matrix-field diagnostic migration. |
| `analysis/matrix_field/diagnostics/locality.py` | `FourierMatrixBlockNormInventoryAnalyzer1D`; `SymmetricRangeTailAnalyzer1D`; `SymmetricRangeTailMonotonicityAnalyzer1D` | Matrix-field locality migration. |
| `analysis/matrix_field/diagnostics/refinement.py` | `ScalarRefinementAnalyzer` | Matrix-field refinement migration. |
| `analysis/matrix_field/diagnostics/structure.py` | `MatrixFieldHermiticityAnalyzer`; `MatrixFieldIsometryAnalyzer`; `MatrixProjectorFieldAnalyzer` | Matrix-field structure migration. |
| `analysis/model_adequacy/band_equivalence_locality/` | `BandEquivalenceLocalityCalculator`; `BandEquivalenceLocalityVerifier`; `ShellScaleDecisionLandscapeCalculator`; `ShellScaleDecisionLandscapePlotWriter`; `BandEquivalenceLocalityPlotWriter`; `BandEquivalenceToleranceMapWriter`; `BandEquivalenceLocalityRefinementAnalyzer`; `SyntheticStrainCalculator`; `SyntheticStrainScanPlotWriter` | Separate band-equivalence owner decision; these are not Phase 3 composite-alignment APIs. |
| `analysis/periodic_bands.py` | `BandGapAnalyzer1D` | A V3 family adopts this action. |
| `analysis/wannier_localization.py` | `BornVonKarmanLocalizationAnalyzer1D` | Wannier-localization V3 migration. |
| `model_systems/periodic2d/plane_waves.py` | `PlaneWaveBlochHamiltonian2DConstructor` | Periodic2D model-system migration. |
| `model_systems/periodic2d/reciprocal_mesh.py` | `ReciprocalMeshNeighbor2DConstructor`; `PlaneWaveReciprocalSewing2DConstructor` | Periodic2D reciprocal-mesh migration. |
| `operators/comparison.py` | `OperatorRecordComparator` | Operator-record comparison migration; remove default dependency factories. |
| `operators/compatibility.py` | `OperatorRecordCompatibilityAnalyzer` | Operator compatibility migration. |
| `operators/complex_eigenpairs.py` | `ComplexHermitianEigenpairResidualAnalyzer` | Complex-eigenpair diagnostic migration. |
| `operators/complex_eigensolvers.py` | `ComplexHermitianSparseEigenpairSolver` | Sparse-eigensolver boundary migration. |
| `operators/residuals.py` | `OperatorRecordResidualAnalyzer` | Operator residual migration. |
| `operators/sparse_hermiticity.py` | `ComplexSparseHermiticityAnalyzer` | Sparse-Hermiticity migration. |

Deferral means only that these actions do not block the bounded five-family and Phase 4
coherence milestone. It does not declare their empty constructors acceptable target
architecture.

## Already conforming construction boundaries

The shared exact-byte verifier boundary is already request-bound:
`BaseModelAnalysisVerifier.__init__` requires `result_wire: bytes`. Concrete PIAB1D,
QHO1D, Mathieu1D, rank-one, and rank-two aggregate verifiers inherit that final subject
constructor.

The five family visualizers already require authenticated projection data and a concrete
verification aggregate. Their construction behavior is conforming even though their
module placement is not. The shared `BaseModelAnalysisVisualizer` is abstract and is not
a concrete empty-callable action.

The four prospective request-bound actions named above are also conforming at the
architecture-contract level. No implementation or software evidence is claimed for
those prospective pages.

## Visualization ownership audit

Current visualization modules combine immutable projection wires, closed plot
enumerations, plot/subplot actions, figure composition, PNG rendering, and aggregate
visualization:

| Current module | Lines at the audited commit | Target |
|---|---:|---|
| `model_systems/visualization.py` | 394 | Root shared package. |
| `model_systems/piab1d/visualization.py` | 1,237 | PIAB1D family package. |
| `model_systems/qho1d/visualization.py` | 572 | QHO1D family package. |
| `model_systems/mathieu1d/visualization.py` | 668 | Mathieu1D family package. |
| `periodic1d/fourier_locality/visualization.py` | 739 | Rank-one family package. |
| `periodic1d/composite_band_alignment/visualization.py` | 547 | Rank-two family package. |

The shared module is under the wrong owner because Periodic1D imports presentation
infrastructure from `ksdft2effmass.model_systems`. Shared domain-neutral mechanics must
move to:

```text
python/src/ksdft2effmass/visualizations/
    __init__.py
    data.py
    figures.py
    records.py
    rendering.py
    visualizer.py
```

That root owns only typed visualization-data serialization, admitted visualization
records, plot/subplot/figure composition contracts, image encoding, authentication, and
closed-inventory enforcement. It must not import a model system, Periodic1D family, or
calculation package.

Family scientific projections and figure inventories move to:

```text
model_systems/piab1d/visualizations/
model_systems/qho1d/visualizations/
model_systems/mathieu1d/visualizations/
periodic1d/fourier_locality/visualizations/
periodic1d/composite_band_alignment/visualizations/
```

Each family package owns `data.py`, `inventory.py`, `visualizer.py`, and cohesive figure
modules. Larger families may use a `figures/` child grouped by scientific figure family.
No `helpers.py`, `utils.py`, one-file-per-class split, singular-module compatibility
shim, or scientific calculation in rendering is admitted.

The root visualization package may depend on generic serialization and an explicit
authentication contract owned at the root verification boundary. It must not depend on
`BaseModelAnalysisVerification` through a reverse import from `model_systems`.
Family-root public imports may deliberately re-export supported family types; this is a
public API, not a compatibility facade.

The adopted target is documented before runtime migration in:

- [`ksdft2effmass.visualizations`](visualizations/index.md);
- [`piab1d.visualizations`](model_systems/piab1d/visualizations/index.md);
- [`qho1d.visualizations`](model_systems/qho1d/visualizations/index.md);
- [`mathieu1d.visualizations`](model_systems/mathieu1d/visualizations/index.md);
- [`fourier_locality.visualizations`](periodic1d/fourier_locality/visualizations/index.md);
  and
- [`composite_band_alignment.visualizations`](periodic1d/composite_band_alignment/visualizations/index.md).

## Migration sequence and gates

The audit freezes this order:

1. land this audit and its architecture rule without runtime changes;
2. move shared and family visualization modules without changing scientific behavior,
   result wires, authenticated projection bytes, figure inventories, or PNG policy;
3. migrate reusable actions bottom-up to request-bound construction;
4. migrate independent reference analyzers and exact-byte verifiers;
5. migrate PIAB1D, QHO1D, Mathieu1D, rank-one, and rank-two composition roots, direct
   scripts, tests, public imports, and documentation;
6. implement Phase 4 with explicit upstream bytes and no predecessor producer call; and
7. remove the M2/M3 predecessor surfaces only after every consumer is absent.

The visualization move and request-bound action migration require separate reviewed
changes. The 35 adjacent actions require separate owner-scoped changes. No migration
may rewrite historical retained artifacts merely to match current source organization.

Phase 4 is blocked until the current five-family top-level actions are request-bound,
the root visualization owner exists, and the exact upstream-result byte contract is
selected. Whether Phase 4 consumes the direct composite result or a separately
implemented band-equivalence result remains a distinct scientific-family decision.

## Verification required by later implementation slices

Each implementation slice must update source, direct scripts, tests, Sphinx API pages,
and Architecture v3 pages together. At minimum it must establish:

- empty construction fails for every migrated concrete action;
- the constructor requires the exact declared request type;
- the terminal operation takes no scientific request arguments;
- canonical result and visualization JSON bytes remain stable unless a separately
  reviewed wire migration explicitly changes them;
- independent verification does not call the production analyzer;
- rendering rejects failed or digest-mismatched projections;
- the family figure inventory remains exact; and
- no old module, alias, facade, or predecessor import remains.

Software checks establish only the declared software behavior. They do not establish
continuum convergence, uncertainty quantification, material validity, scientific
validation, publication acceptance, release, or evidence sealing.
