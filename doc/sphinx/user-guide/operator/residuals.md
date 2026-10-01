# Operator residual analysis

`OperatorRecordResidualAnalyzer` calculates three absolute, unnormalized norms of a
signed `OperatorRecordDifferenceResult`. This page defines the metrics and the scale-safe binary64
policy used to evaluate them.

## Residual metrics

For the represented difference $\Delta\mathbf H\in\mathbb C^{N\times N}$ defined on
the [differencing page](differencing.md), the metrics are

$$
\varepsilon_{\max}
=
\max_{0\leq i,j<N}|\Delta H_{ij}|,
$$

$$
\varepsilon_{\mathrm F}
=
\|\Delta\mathbf H\|_{\mathrm F}
=
\left(
\sum_{i=0}^{N-1}\sum_{j=0}^{N-1}|\Delta H_{ij}|^2
\right)^{1/2},
$$

$$
\varepsilon_2
=
\|\Delta\mathbf H\|_2
=
\sigma_{\max}(\Delta\mathbf H).
$$

The symbols are:

- $\Delta\mathbf H$: the signed candidate-minus-reference matrix;
- $\Delta H_{ij}$: row-$i$, column-$j$ entry of $\Delta\mathbf H$;
- $N$: the common represented state-space dimension;
- $i,j\in\{0,\ldots,N-1\}$: zero-based matrix indices;
- $\varepsilon_{\max}$: maximum absolute matrix-entry residual;
- $\varepsilon_{\mathrm F}$: Frobenius residual;
- $\varepsilon_2$: induced matrix 2-norm, or spectral residual;
- $\|\cdot\|_{\mathrm F}$: Frobenius norm;
- $\|\cdot\|_2$: induced matrix 2-norm;
- $\sigma_{\max}(\Delta\mathbf H)$: largest singular value of
  $\Delta\mathbf H$; and
- $\sum_{i=0}^{N-1}\sum_{j=0}^{N-1}$: the sum over all $N^2$ entries.

For every finite square matrix, the mathematical ordering is

$$
0
\leq
\varepsilon_{\max}
\leq
\varepsilon_2
\leq
\varepsilon_{\mathrm F}.
$$

All three values have the same energy unit as the compatible input matrices. The
implementation does not divide by a reference norm, matrix dimension, energy scale,
or scientific acceptance threshold.

## Scale-safe Frobenius evaluation

The implementation operates on stored binary64 numerical coefficients after exact
compatibility has established one common energy-unit string $u$. In this section,
$\Delta H_{ij}$ and the residual symbols denote numerical coefficients measured in
$u$; the result carries $u$ separately as metadata. Define

$$
s=\max_{i,j}|\Delta H_{ij}|.
$$

The additional symbols are:

- $u$: the exact common energy-unit string carried by the compatible records,
  represented difference, and residual result; and
- $s$: the largest stored entry-magnitude coefficient measured in $u$.

If $s=0$, all three residual coefficients are exactly zero. For $s>0$, the
Frobenius norm coefficient is evaluated as

$$
\varepsilon_{\mathrm F}
=
s
\left(
\sum_{i,j}
\left|\frac{\Delta H_{ij}}{s}\right|^2
\right)^{1/2}.
$$

The ratios $\Delta H_{ij}/s$ are dimensionless. Scaling before the sum of squares
reduces avoidable binary64 overflow and underflow.

## Scale-safe spectral evaluation

For the spectral norm, write the positive finite scale coefficient in binary form as

$$
s=m\,2^e,
\qquad
\tfrac12\leq m<1,
$$

and form

$$
\widetilde{\mathbf H}=2^{-e}\Delta\mathbf H,
\qquad
\varepsilon_2=2^e\sigma_{\max}(\widetilde{\mathbf H}).
$$

The additional symbols are:

- $m$: the dimensionless binary significand of the stored numerical coefficient
  $s$;
- $e$: the integer binary exponent of that coefficient;
- $2^e$: an exact dimensionless power-of-two scale in binary floating-point
  arithmetic; and
- $\widetilde{\mathbf H}$: the power-of-two-scaled numerical coefficient matrix
  used for singular-value computation. Multiplication by the separately carried
  unit $u$ restores its unit-bearing interpretation.

## Metric-order roundoff policy

The implementation evaluates the norms independently and permits only a small ordering
discrepancy attributable to binary64 roundoff. Define

$$
s_{\mathrm m}
=
\max(\varepsilon_{\max},\varepsilon_2,\varepsilon_{\mathrm F}),
\qquad
d=4\max(1,N),
$$

$$
\ell
=
s_{\mathrm m}-\operatorname{nextafter}(s_{\mathrm m},0),
$$

$$
a_{\mathrm{rel}}=d\,\epsilon_{\mathrm{mach}}\,s_{\mathrm m},
\qquad
a_{\mathrm{ulp}}=d\,\ell,
\qquad
a=\max(a_{\mathrm{rel}},a_{\mathrm{ulp}}).
$$

The symbols are:

- $s_{\mathrm m}$: the largest raw residual numerical coefficient measured in
  $u$;
- $d$: a dimensionless factor depending on represented dimension $N$;
- $\operatorname{nextafter}(s_{\mathrm m},0)$: the next representable binary64
  value from $s_{\mathrm m}$ toward zero;
- $\ell$: the spacing from $s_{\mathrm m}$ to that lower binary64 neighbor;
- $\epsilon_{\mathrm{mach}}$: binary64 machine epsilon;
- $a_{\mathrm{rel}}$: the relative roundoff allowance;
- $a_{\mathrm{ulp}}$: the lower-unit-in-the-last-place allowance; and
- $a$: the analyzer-owned metric-order allowance.

When $s_{\mathrm m}=0$, the allowance is exactly zero. An ordering inversion no
larger than $a$ is canonicalized upward so the stored result satisfies the exact norm
ordering. A larger inversion raises the structured `METRIC_ORDER_VIOLATION` numerical
error. This allowance is numerical roundoff policy, not an operator-comparison
tolerance, scientific acceptance criterion, or uncertainty estimate.

## Python usage

Continue with `difference` from the differencing page:

```python
import numpy as np

from ksdft2effmass.operators import OperatorRecordResidualAnalyzer

metrics = OperatorRecordResidualAnalyzer().execute(difference)

assert metrics.energy_unit == "eV"
assert metrics.maximum_absolute_residual == 0.25
assert metrics.spectral_residual == 0.25
np.testing.assert_allclose(metrics.frobenius_residual, np.sqrt(5.0) / 8.0)
```

`OperatorRecordComparisonNumericalError` reports a nonfinite metric, singular-value
failure, nonfinite scaled matrix, or material norm-order violation through a closed
structured code. A successful result establishes the numerical software contract only.

Next, use the [composed comparison Workflow](comparison.md). Return to the
[operator-analysis overview](index.md).
