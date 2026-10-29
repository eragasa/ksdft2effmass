# Implementation

## Typed result

`Qho1dConfiguration` owns the nondimensional parameters, ordered sweep, and one
state-resolved selection. `Qho1dAnalysisRequest` binds that configuration together
with the complete immutable result identity. `Qho1dAnalyzer` admits the request at
construction and its zero-argument `execute()` produces `Qho1dCalculationResult`,
composed from ordered `Qho1dCaseResult` values and one
`Qho1dStateComparisonResult`.

The reusable model surface is partitioned by scientific responsibility:
`parameters.py` owns unit-aware parameters and nondimensionalization,
`analytical.py` owns the exact real-line solution, `finite_difference.py` owns the
finite Dirichlet-grid representation, `ladder_operators.py` owns the retained
number-state representation, and `comparison_records.py` owns the typed request and
aligned result contracts. The package root remains the deliberate public import
surface; there is no compatibility model-module facade.

Each maintained case constructor owns and serializes four typed semantic sections:

- `Qho1dSpatialRepresentationResult` owns the box, requested and realized spacing,
  dimensions, and ordered coordinates;
- `Qho1dSampledStateAlignmentResult` owns the Gram correction, injection, and map
  diagnostics;
- `Qho1dHamiltonianComparisonResult` owns the two aligned Hamiltonians, signed
  difference, and discrepancy decomposition; and
- `Qho1dResidualResult` owns the full-space intertwining-residual norm.

`Qho1dComparisonResult` constructor-owns the first three sections, and
`Qho1dAnalyzer` reuses those immutable values when it adds the residual section. Flat
read-only projections remain available for concise numerical consumers without
creating a second authoritative value owner.

The selected state comparison retains analytical samples and the sign-aligned finite
eigensolution once. The earlier flat-case execution remains byte-exact; decoding and
reserializing it preserves its retained layout, while newly produced results use the
semantic-section schema.

Every successor record inherits the shared final `to_dict`, `from_dict`, `to_json`, and
`from_json` boundaries. Concrete records implement only `_mapping` and `_from_mapping`.
The QHO1D successor has no custom NumPy transport or `.tolist()` serialization.

## Adjacent-grid diagnostic

`Qho1dCrossGridAnalysisRequest` binds one complete immutable direct result before
`Qho1dCrossGridAnalyzer.execute()` groups cases at fixed box half-width and retained
dimension, then compares each adjacent authored coarse/fine grid pair.
`Qho1dCrossGridComparisonResult` retains both requested and realized spacings,
represented dimensions, and the coarse-minus-fine Frobenius norm. The complete
ordered inventory is a typed `Qho1dCrossGridAnalysisResult` and does not alter the
wire contract of previously retained direct executions.

`Qho1dCrossGridVerificationRequest` binds the exact calculation and its correlated
analysis before `Qho1dCrossGridVerifier.execute()` recomputes each derived value
directly from the authoritative pulled-back case matrices without invoking the
production QHO1D analyzer, comparator, or cross-grid analyzer. It depends on
`Qho1dVerifier` for independent reconstruction
of those authoritative matrices.

## Calculation

`run_01_calculation.py` declares its controls in Python, constructs the complete
`Qho1dAnalysisRequest`, and invokes `Qho1dAnalyzer.execute()` without scientific
arguments. The analyzer composes reusable analytical, finite-difference,
ladder-operator, and request-bound common-coordinate owners. It writes the typed
configuration and result through
incomplete-stage paths before exposing the execution directory.

## Independent verification

`Qho1dIndependentReferenceAnalyzer` does not call `Qho1dAnalyzer` or
`Qho1dComparator`. It evaluates Hermite polynomials with SciPy, forms the tridiagonal
Hamiltonian directly in NumPy, reconstructs the Gram orthonormalization, and compares
every case and selected eigensolution through typed maximum-error comparisons.

`Qho1dVerifier` gives the final `BaseModelAnalysisVerifier` subject constructor the
exact result bytes. The base computes their digest and reconstructs
`Qho1dCalculationResult` from those same bytes. It derives
`Qho1dVisualizationData`, hashes its canonical shared-codec JSON bytes, and composes
six operation-named verification components: spatial representation, sampled-state
alignment, Hamiltonian comparison, residual, state comparison, and visualization
projection. The aggregate retains 468 comparisons. The retained flat-case
three-component verification remains decodable without changing its bytes.

## Rendering

`Qho1dVisualizer` accepts only passing `Qho1dVerification` values whose projection
digest matches the supplied typed data. QHO1D plot actions draw model-specific data
relations on caller-owned axes; subplot actions own axis-local composition and
presentation; figure actions own layout and figure-wide presentation; and the root
`PngFigureRenderer` owns PNG encoding and figure closure. The visualizer returns exactly
one validated `PngVisualization` for each `Qho1dVisualizationPlotEnum` member.
`run_03_render.py` publishes figures through an incomplete-stage directory and copies
report source, bibliography, and authenticated figures into an execution-bound
technical-report directory.

## Removed predecessor

The adjacent-grid diagnostic was the only predecessor capability selected for the
direct successor. After that migration, the JSON-authored `study/` package, `dev_*`
scripts, custom wire, source-coupled verifier, replaceable execution path, predecessor
report, and compatibility aliases were removed under explicit authorization. Commit
`7e3331eb3addd8034cdf97cc2a65e64c4f74ac67` retains their last complete tree state;
the [legacy disposition](legacy-disposition.md) records recovery identities and the
historical report qualification.
