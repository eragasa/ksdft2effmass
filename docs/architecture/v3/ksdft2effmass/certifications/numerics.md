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

## Assurance boundary

Three levels remain distinct:

1. exact decision logic over supplied endpoints;
2. rigorous native outward enclosures plus independent containment replay; and
3. formally checked numerical containment.

The implemented tranche establishes level-one wire and classification behavior only.
It neither promotes existing binary64 values nor claims levels two or three.
