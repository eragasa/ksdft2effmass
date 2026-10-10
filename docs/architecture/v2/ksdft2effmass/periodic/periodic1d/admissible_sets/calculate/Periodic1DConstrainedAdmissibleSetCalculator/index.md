# `Periodic1DConstrainedAdmissibleSetCalculator`

## Purpose

Stateless Action executing the M3 finite-family admissible-set protocol.

## Public operation

`execute(definition)` requires the exact M3 definition and returns one correlated M3
result. It executes the composed M2 baseline, constructs analytic loss quadratics for
each frozen angle over the continuous parameter rectangle, retains the prospective
common witness,
computes certificate points and bounds, summarizes locality, and assigns bounded
dispositions. Class-specific detail is split into
[implementation](implementation/index.md),
[mathematics](implementation/mathematics/index.md), and
[testing](implementation/testing/index.md).

## Mathematical ownership

Private methods own the normalized spectral/operator RMS formulas, quadratic feature
construction, axis extremes, domain-constrained minima, feasible-angle selection,
rotation/conjugation, and splitting-axis separation logic. Their equations and premises
are documented in [scientific](../../scientific.md) and [numeric](../../numeric.md).

## Failures and state spaces

Wrong definition type raises `TypeError`; invalid geometry, infeasible expected witness,
clipped certificate premises, or correlation failures raise explicit exceptions. All
represented matrices act on the identified M2 rank-two frame and parent energy scale.

## Evidence and limitations

Tests retain both compatible and certified-separated cases and independently reconstruct
them. The Action proves nothing outside the frozen parameter rectangle and finite angle
family and performs no
external calculation.
