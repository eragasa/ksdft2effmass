# Implementation

## Typed result

`Qho1dConfiguration` owns the nondimensional parameters, ordered sweep, and one
state-resolved selection. `Qho1dAnalyzer` produces `Qho1dCalculationResult`, composed
from ordered `Qho1dCaseResult` values and one `Qho1dStateComparisonResult`.

Each case retains the realized grid, sampled-state injection, Gram factors,
common-coordinate Hamiltonians, signed difference, discrepancy components, and
full-space residual norm. The selected state comparison retains analytical samples and
the sign-aligned finite eigensolution once.

Every successor record inherits the shared final `to_dict`, `from_dict`, `to_json`, and
`from_json` boundaries. Concrete records implement only `_mapping` and `_from_mapping`.
The QHO1D successor has no custom NumPy transport or `.tolist()` serialization.

## Calculation

`run_01_calculation.py` declares its controls in Python and invokes `Qho1dAnalyzer`.
The analyzer composes reusable analytical, finite-difference, ladder-operator, and
common-coordinate owners. It writes the typed configuration and result through
incomplete-stage paths before exposing the execution directory.

## Independent verification

`Qho1dIndependentReferenceAnalyzer` does not call `Qho1dAnalyzer` or
`Qho1dComparator`. It evaluates Hermite polynomials with SciPy, forms the tridiagonal
Hamiltonian directly in NumPy, reconstructs the Gram orthonormalization, and compares
every case and selected eigensolution through typed maximum-error comparisons.

`Qho1dVerifier` derives `Qho1dVisualizationData`, hashes its canonical shared-codec JSON
bytes, composes operation-named verification components, and returns the aggregate and
authenticated projection together.

## Rendering

`Qho1dVisualizer` accepts only passing `Qho1dVerification` values whose projection
digest matches the supplied typed data. It returns exactly one validated
`ModelAnalysisPngVisualization` for each `Qho1dVisualizationPlotEnum` member.
`run_03_render.py` publishes figures through an incomplete-stage directory and copies
report source, bibliography, and authenticated figures into an execution-bound
technical-report directory.

## Historical boundary

The JSON-authored `study/` package and `dev_*` scripts remain historical development
interfaces. They do not define successor serialization, verification, or rendering.
Their removal requires a separate authorized destructive tranche.
