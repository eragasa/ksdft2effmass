# `ScalarFiniteLatticeOperator`

## Purpose and status

This implemented row-029 DataObject is the specialized sparse scalar finite-periodic
represented-operator record. It is not replaced by the general dense `OperatorRecord`.

## Contract

The record owns a nonempty identity; immutable canonical complex128 CSR matrix and unit;
`FiniteLatticeShape` with explicit tensor-product order; correlated `TwistFiber` with
unreduced lift, quotient representative, and gauge; scalar basis identity; energy-zero
identity; and a sorted unique tuple of nonempty provenance key/value pairs.

Exactly one basis state exists per finite lattice cell, so matrix shape equals
`(cell_count, cell_count)`. Twist and lattice dimensions agree. Short delegated
invariant methods preserve the original type, shape, correlation, and provenance
failure order.

## Scientific boundary

The record supports sparse finite-periodic scalar operators without densification.
Multi-orbital, spin, overlap, atomic-to-reduced maps, Hermiticity, gauge equivalence,
compatibility, addition, and scientific interpretation remain separate records or
Actions. PhysKit supplies reusable lattice primitives and must not depend on this
project's scientific owners.

## Evidence and limitations

`TestScalarFiniteLatticeOperator` documents complete metadata retention and shape,
twist, and provenance failures. Separate compatibility and addition suites test
operations. Passing establishes represented software behavior only—not physical model
adequacy, provenance truth, validation, UQ, or acceptance.
