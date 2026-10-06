# `Periodic1DRangeEffectiveModelAdoption`

## Purpose and status

This implemented row-023 aggregate binds two distinct finite-range reduction routes for
one exact retained operator: truncation of the complete hopping family and direct
reciprocal-space least-squares fitting.

## Contract

The declared nonnegative range must match the truncation Action and both models'
representatives. Each route retains its own typed result, replay comparison, and finite
nonnegative built-in-float absolute energy allowance. Each comparison must own its
actual adopted candidate and its coefficient defect must not exceed the corresponding
allowance.

## Scientific boundary

Route agreement establishes reproducibility within the declared finite mesh and model
class. Truncation and fitting remain distinct constructions even when coefficients
agree numerically. Their errors are model-reduction comparisons and are not merged with
parent discretization or parent-model adequacy.

The route-separation, calculated-tolerance, explicit-tolerance, and contradictory-range
tests are the maintained evidence. They do not establish physical accuracy, validation,
UQ, or acceptance.
