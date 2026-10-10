# `Periodic1DMultibandAlignmentVerificationResult`

## Purpose and contract

Immutable summary of independent M2 reconstruction. It binds the exact calculation,
maximum dimensionless defect, maximum energy defect, dimensionless absolute tolerance,
and final pass flag.

All defects/tolerances are finite and nonnegative; energy defect units must match the
parent. `passes` must exactly equal both comparisons against the same declared
tolerance after the M2 normalized convention. Inconsistent summaries are rejected.

## Interpretation

Passing establishes bounded internal numerical consistency only. It is not material
validation, uncertainty quantification, or a human decision.
