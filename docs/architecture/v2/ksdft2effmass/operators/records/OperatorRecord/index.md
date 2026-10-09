# `OperatorRecord`

## Purpose and status

This implemented row-028 DataObject is the general dense finite represented-operator
record. It combines a matrix with enough explicit metadata to interpret its coordinates.

## Contract

The record owns exact nonempty identity and operator-kind strings; a defensively owned,
C-contiguous, non-writeable complex128 finite square matrix; actual `StateSpace`,
`Basis`, `Geometry`, and `EnergyReference` objects; and a defensively copied read-only
string provenance mapping. Matrix dimension, state-space dimension, and basis ordering
length agree, and schema version one requires an orthonormal basis declaration.

General non-Hermitian matrices are valid. Booleans, numeric strings, ragged data,
nonfinite components, conversion overflow, semantic substitutes, mutable aliases, and
metadata contradictions fail explicitly.

## Operation boundary

The record performs no Hermiticity analysis, compatibility inference, unit conversion,
energy alignment, gauge/basis alignment, subtraction, residual analysis, or scientific
equivalence decision. Named Actions own those operations. JSON is a serializer concern.

## Evidence and claim boundary

Class-facet tests separately document construction, matrix/metadata invariants,
defensive ownership, and exact value semantics. Verification pages cover serializers
and Actions. Passing establishes represented software state only—not provenance truth,
physical equivalence, scientific validation, UQ, or acceptance.
