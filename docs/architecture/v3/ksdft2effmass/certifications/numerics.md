# Certification numerics

## Exact endpoint domain

The current wire stores every interval endpoint as a reduced rational
`numerator/denominator` with positive denominator. Error intervals are closed,
nonnegative, and ordered. JSON decimal and exponential numbers are forbidden, so the
wire does not hide a binary64 conversion.

The scalar domain is Python's built-in arbitrary-precision `int`, excluding booleans;
there is no fixed-width integer overflow in the in-memory contract. Resource exhaustion
from adversarially large wire integers remains outside this scientific record contract.
Interval endpoints use the proposition's declared `E_ref` unit, and support and precision
fields are dimensionless integers.

This exact storage does not by itself prove that a runtime quantity lies in an interval.
Containment remains an obligation of the named enclosure producer and independent
verifier.

## First-passing semantics

For supports `0` through `15`, the proposition has two decisive objectives:

- mediated total maximum evaluation error; and
- direct total maximum evaluation error.

The threshold is exactly `1/100000000 E_ref`. The selected support is accepted only if
both selected-support upper endpoints are at or below the threshold and every earlier
support has at least one objective whose lower endpoint is above the threshold. It is
rejected if the selected support definitely fails or an earlier support definitely
passes. Every overlapping or otherwise undecided case is unresolved.

The classifier does not assume support monotonicity. It evaluates every earlier support
from its own two intervals.

## Arb provider numerics

The optional provider constructs the fixed four-state parent directly from exact integer
numerators and denominator `100` inside Arb. At each requested construction or
evaluation point, Rump eigenvalue balls must isolate one lowest real eigenvalue. The
mediated action forms the 256-point discrete Fourier coefficients retained by one
requested support in `0..15` and evaluates that candidate on all 1025 staggered points.

Arb balls are exported through midpoint-radius decimal integers with precision-dependent
guard digits, then converted to exact `Fraction` endpoints. Pointwise absolute residual
intervals are aggregated as

\[
[\max_j \ell_j,\;\max_j u_j],
\]

which contains the exact finite maximum whenever each pointwise quantity lies in
`[\ell_j,u_j]`. No binary64 value enters the enclosure path.

The provider does not implement the direct least-squares objective. No equality between
direct and mediated routes is used to populate certification entries.

## Assurance boundary

Three levels remain distinct:

1. exact decision logic over supplied endpoints;
2. rigorous native outward enclosures plus separately implemented containment replay;
   and
3. formally checked or heterogeneous-toolchain numerical containment.

The core wire establishes level one over supplied endpoints. The optional local Arb
capability supplies part of a future level-two producer path for the parent and mediated
objective only. It does not yet supply a complete producer artifact or independent
containment replay, and level three is not claimed.
