# `Periodic1DIsolatedBandCalculator`

## Purpose

Stateless Action that executes the deterministic M1 finite protocol.

## Public operation

`execute(definition)` accepts the exact
`Periodic1DIsolatedBandCalculationDefinition` type and returns a
`Periodic1DIsolatedBandCalculationResult`. It performs the ten stages documented in the package-level
[implementation](../../implementation.md). Class-specific detail is split into
[implementation](implementation/index.md),
[mathematics](implementation/mathematics/index.md), and
[testing](implementation/testing/index.md).

## Mathematical ownership

The class owns orchestration and cross-channel identity. Its nontrivial private methods
construct plane-wave/finite-difference spectra, convert reduced to physical reciprocal
coordinates, select scalar operator samples, calculate maximum spectral error, and
assemble each finite-range comparison. Reusable eigensolvers, transforms, fits,
truncations, and diagnostics remain delegated.

## Units and state spaces

Parent spectra, scalar retained samples, complete hopping blocks, and finite-range
models retain explicit coordinates, energy units, and representation identities.
Training and evaluation samples are never interchanged.

## Failures

Wrong definition type raises `TypeError`; violated domain preconditions surface as
explicit constructor/action exceptions. The calculator performs no fallback to external
tools.

## Evidence and limitations

Direct tests cover separation of roles, binary64 determinism, and verifier
reconstruction. The calculation is finite synthetic work, not material validation or a
physical-isolation proof.
