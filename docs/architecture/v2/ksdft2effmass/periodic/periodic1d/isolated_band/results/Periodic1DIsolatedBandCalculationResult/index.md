# `Periodic1DIsolatedBandCalculationResult`

## Purpose

Immutable aggregate M1 result and correlation boundary.

## Fields

The result binds the exact definition, parent reference spectrum, ordered plane-wave and
finite-difference observations, training and evaluation scalar targets, complete
reciprocal-to-hopping transform, complete-model Hermiticity result, and ordered
range-study records.

## Invariants

Definition identity, parent/reference coordinates, selected band count, energy units,
training/evaluation mesh roles, transform source, representative modulus, Hermiticity
model, declared range sequence, and every diagnostic target must agree. The aggregate
rejects cross-wired but shape-compatible records.

## Mapping and evidence

Source: `.../isolated_band/results.py`; serialized by the M1 serializer and reconstructed
by the M1 verifier. Direct execution, determinism, serialization, and tamper tests cover
this boundary.

## Limitations

The result is evidence for the frozen finite synthetic protocol only and carries no
human acceptance state.
