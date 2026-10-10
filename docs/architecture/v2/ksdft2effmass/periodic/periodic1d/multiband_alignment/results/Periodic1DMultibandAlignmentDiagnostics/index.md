# `Periodic1DMultibandAlignmentDiagnostics`

## Purpose

Immutable M2 summary of frame transport, alignment, external-gap, and represented-
operator diagnostics before finite-range truncation.

## Fields and invariants

The record binds polar transport, pointwise alignment, the one-global-unitary matrix,
finite-mesh external gap, attack-frame defect, pointwise rotation-recovery defect,
global frame defect, and attacked/pointwise/global represented-operator defects.
Dimensionless values are finite nonnegative built-in floats; operator and gap values are
finite nonnegative energy quantities. Matrix rank, mesh, and unit identities must agree
when correlated by the aggregate result.

## Interpretation

Projector/spectrum invariance and represented-matrix defects are distinct evidence
channels. A small pointwise defect does not imply a small globally constrained defect or
finite-range locality.
