# Model-adequacy numerical contract

## Initial bounded scope

The exact-pinned Optimization facade
`projectkoios.optimization.quadratic.quadratic.PositiveDefiniteQuadraticLoss` fixes the external
scalar, shape, backend-selection, arithmetic, and failure boundary. It is not a local
KSD API. This page also fixes the numerical
ownership split between the spectral loss $L_E$, the operator residual $R_H$, and the
normalized operator loss $L_H$ without prematurely selecting their Python types.

It does not freeze a direct spectral-loss API, an operator path-aggregation API,
threshold policy, optimizer, or certificate backend.

## Channel numerical identities

For $L_E$:

- target and candidate energies have the same nonzero sample count and retained rank;
- sample coordinates are checked by an explicit domain contract, never array position
  alone;
- target energies, candidate energies, and the positive scale $E_0$ are converted to one
  declared energy unit before subtraction;
- weights are finite and strictly positive, with one weight per sample;
- $R_E$ uses the weighted sum over every sample and retained band divided by
  $r\sum_i w_i$; and
- $L_E=R_E/E_0$ is finite and dimensionless.

For $L_H$:

- `operators` rejects incompatible represented samples before subtraction;
- the outward loss definition selects the sample set and scientific weights;
- reusable dimensionful hopping/Frobenius residual and unit mechanics belong to
  PhysKit, which retains the common energy unit and physical result $R_H$;
- the adequacy layer accepts that result and an explicitly compatible finite positive
  $E_0$;
- the adequacy layer computes $L_H=R_H/E_0$ without repeating operator subtraction or
  physical aggregation; and
- nonfinite conversion, accumulation, square root, or normalization is a structured
  numerical failure, never a NaN/Inf result.

Training and withheld sets are evaluated independently. Their values are not pooled
unless a separate definition declares that pooled set before evaluation.

A completed-square object may represent $L_E^2$ or $L_H^2$ over a declared affine
parameter family. Its wrapper retains the channel; its primitive does not infer one.

## Public scalar policy

The Optimization owner applies its `finite_float` convention to every center entry,
minimum, evaluation coordinate, and tuple-matrix entry. Each must be a non-Boolean
`numbers.Real` representable as finite binary64 and normalizes to built-in `float`.
Booleans, numeric strings, complex values, non-Reals, NaN, infinities, and integer-
overflow conversions fail. Existing SciPy sparse objects follow a distinct backend path:
they require matching square shape, a supported non-Boolean real numeric dtype,
successful float64 conversion, finite canonical CSR data, and exact represented
symmetry. This generic target behavior does not alter the stricter exact-built-in-float
wire contract of maintained M3 records.

## Shape and ordering

Let the center have length $n$.

- The center is a nonempty `tuple[float, ...]`.
- Dense construction uses a `tuple` of exactly $n$ row tuples.
- Sparse construction accepts the same tuple form or a supported SciPy sparse object;
  sparse objects follow shape/dtype/conversion/data validation rather than per-entry
  `finite_float` calls, then retain canonical private CSR storage.
- Every retained backend entry is finite binary64.
- Parameter coordinates supplied to evaluation are a tuple of exactly $n$ accepted real
  values and normalize to built-in floats.
- Coordinate order is owned by the outward wrapper or definition. The generic object
  does not attach names or reorder entries.
- Dimension zero is rejected.

The dense backend exposes immutable tuples and retains private read-only arrays. The
sparse backend returns a defensive CSR copy. The facade selects dense NumPy behavior by
default or SciPy CSR behavior with exact built-in `sparse=True`; it does not silently
densify sparse input.

## Symmetry and curvature

The represented matrix must be exactly symmetric in its backend representation: tuple
entries for dense/tuple input or canonical CSR values after sparse conversion. The
constructor does not average cross terms or repair asymmetry.

The dense backend uses NumPy Cholesky acceptance. The sparse backend uses the smallest
algebraic eigenvalue returned by SciPy ARPACK `eigsh` with `tol=0.0` and requires it to
be finite and strictly positive; solver failure fails closed. These are backend
numerical acceptance rules, not exact positive-definiteness certificates. Neither
backend adds scientific tolerances, jitter, regularization, or eigenvalue clipping.
Domain wrappers may retain stronger conditioning margins without weakening the owner
invariant.

## Minimum and evaluation

`minimum_squared_loss` is finite and nonnegative. For validated coordinate tuple $x$,
the implementation evaluates

```text
delta = x - center
squared = minimum_squared_loss + delta.T @ matrix @ delta
```

using the selected NumPy dense or SciPy sparse binary64 backend.

The result contract is:

- `squared_loss(x)` returns one finite built-in `float` greater than or equal to zero;
- `root_loss(x)` returns `sqrt(squared_loss(x))` as one finite built-in `float`;
- the generic object makes no RMS claim because it does not select mean-square
  normalization;
- no negative value is clamped, including one attributed to binary64 roundoff; and
- a negative or nonfinite evaluated quadratic, or a nonfinite final result, raises
  `ValueError` rather than returning NaN or infinity.

KSD retains no stronger exception claim than the accepted owner API.

## Operational immutability

The owner facade exposes read-only properties. Its dense implementation is a frozen,
slotted value object with tuple state and private read-only arrays; its sparse
implementation stores private canonical CSR data and returns a defensive copy.
Evaluation does not alter represented state.

Outward wrappers must also remain operationally immutable. A serializer owns wire
mechanics; neither the generic quadratic nor its wrappers read files or discover retained
artifacts.

## Unit and normalization boundary

The facade coordinates and returned loss are unit-free by contract. The generic
object stores no physical dimension or unit string and performs no unit conversion.

A wrapper consuming energy-valued parameters must retain a positive energy scale and
unit, convert every coordinate and center to a declared dimensionless ratio, and
construct the generic object only after that conversion. Changing the scale changes the
coordinate identity and must not be hidden as a serializer detail.

## Threshold and domain boundary

The generic quadratic evaluates the unconstrained quadratic. It does not own:

- parameter lower or upper bounds;
- inactive-coordinate constraints;
- channel thresholds;
- separation resolution;
- box-constrained minima;
- nonemptiness;
- witness membership; or
- certificate arithmetic.

Consequently, center membership in a bounded domain is neither required nor inferred.
A domain-specific analyzer evaluates clipping and feasibility separately.

## Independent verification

Producer calculations may use the exact-pinned facade. An evidence-bearing independent
verifier must reconstruct quadratic
coefficients and direct loss values through a separate implementation path. It may
decode the external value object for comparison but
must not establish correctness by invoking the same constructor/evaluator on both sides
of the comparison.

Owner and consuming-project tests establish software behavior only. M3 and future HSH
verification retain their own scientific formulas, source correlation, and premise
checks.

## Direct tests

Current owner quadratic tests cover selected dense and sparse construction/evaluation
paths, asymmetric and indefinite matrices, nonfinite evaluation, and defensive sparse
matrix copying. KSD adds exact installed-commit provenance plus one hand-derived dense
and sparse facade value. These bounded cases do not imply an exhaustive scalar or
adversarial matrix.

Future M3/HSH wrapper suites must add their own malformed-dimension, inactive-coordinate,
normalization, backend-correlation, curvature-margin, direct-formula agreement, and
producer/verifier-independence cases. An M3 agreement test does not replace the retained
independent verifier.

## Deferred numerical contracts

The following remain deferred:

- semidefinite or singular quadratics;
- mixed-unit coordinates;
- complex coordinates or matrices;
- automatic differentiation;
- batch evaluation;
- direct weighted $L_E$ construction;
- PhysKit-owned dimensionful represented-hopping aggregation and adequacy-owned $L_H$
  normalization;
- interval or directed-rounding support arithmetic; and
- serialization schema shared across calculations.
