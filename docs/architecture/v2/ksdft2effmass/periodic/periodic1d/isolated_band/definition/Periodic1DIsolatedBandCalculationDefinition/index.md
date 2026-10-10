# `Periodic1DIsolatedBandCalculationDefinition`

## Purpose

Immutable complete control record for one M1 calculation.

## Inputs

The record binds `calculation_id`, `parent_model`, plane-wave sweep/reference/production
cutoffs, finite-difference extents, parent sample coordinates, compared band count,
training mesh extent, ordered hopping ranges, evaluation mesh extent, coordinate and
reconstruction tolerances, and energy-valued Hermiticity, Parseval, and imaginary
residual tolerances.

## Contract and invariants

Identifiers are nonempty. Integer controls are exact positive built-in integers where
required; Booleans are rejected. Tuples are nonempty, ordered, unique where relevant,
and finite. The plane-wave reference is strictly larger than every convergence cutoff;
the production cutoff is one declared sweep cutoff. The training mesh is even, every
range is below half its extent, and the evaluation mesh has at least three points.
Quantities have the energy or squared-energy dimensions required by their diagnostic.

`withheld_reduced_momenta` returns a new read-only dimensionless vector on the staggered
mesh `EQ-M1-WITHHELD-MESH-003`; it never inspects results.

## Failures

Construction raises `TypeError` for wrong exact boundary types and `ValueError` for
invalid values, ordering, units, mesh/range relations, or nonfinite controls.

## Mapping and evidence

Source: `.../isolated_band/definition.py`. Tests directly cover role separation,
squared-energy Parseval tolerance, and Boolean rejection. The definition is serialized
indirectly as part of the M1 result.

## Limitations

Controls freeze a finite protocol but do not establish convergence or acceptance.
