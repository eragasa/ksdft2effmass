# `Periodic1DMultibandAlignmentCalculationDefinition`

## Purpose

Immutable complete control record for one M2 calculation.

## Inputs

It binds a nonempty calculation identity, block-Hamiltonian parent, rank-two retention,
training/evaluation mesh extents, ordered hopping ranges, constant and sine-harmonic
attack coefficients, external-gap lower bound, overlap threshold, orthonormality,
coordinate and reconstruction tolerances, energy-valued Hermiticity tolerance, and final
verification tolerance.

## Invariants

M2 v1 requires exact built-in `retained_rank == 2`; training extent is even and at least
four; evaluation extent is at least three; ranges are unique, increasing, and below
half the training extent. Attack/tolerance floats are finite; overlap threshold lies in
$[0,1)$; nonnegative controls reject Booleans and numeric strings. Quantity units must
match the parent energy unit.

`withheld_reduced_momenta` returns the read-only $1/(N+1)$-offset mesh.

## Failures and evidence

Wrong types raise `TypeError`; invalid values, units, rank, range, or mesh relations
raise `ValueError`. Tests cover generic identity attacks, Boolean rejection,
immutability, and aggregate threshold binding.

## Limitations

The definition freezes a finite rank-two family and does not imply physical isolation or
optimal gauge choice.
