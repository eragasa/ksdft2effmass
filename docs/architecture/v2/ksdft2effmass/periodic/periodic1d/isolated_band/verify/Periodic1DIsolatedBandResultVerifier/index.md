# `Periodic1DIsolatedBandResultVerifier`

## Purpose

Stateless Action that independently reconstructs a typed M1 result.

## Operation

`execute(calculation)` requires the exact M1 aggregate type. It rebuilds plane-wave and
finite-difference eigenvalues, training/evaluation band values, complete Fourier blocks,
interpolation, truncation, direct-fit, Parseval, Hermiticity, comparison, and band-shape
channels. It returns `Periodic1DIsolatedBandVerificationResult`.

## Independence boundary

The verifier does not call `Periodic1DIsolatedBandCalculator`. Private numerical
methods implement direct finite formulas and lower-level constructors. The retained
standalone verifier adds strict wire decoding and manifest checks.

## Failures and evidence

Wrong input type raises `TypeError`; malformed correlated results are rejected by their
own constructors; defects above the definition tolerance produce `passes=False`.
Tests prove reconstruction, convergence-value tamper detection, and absence of producer
imports in the retained verifier.

## Limitations

Producer and verifier share the scientific convention, NumPy/SciPy, eigensolvers, and
binary64 behavior. This is numerical verification, not an independent physical oracle.
