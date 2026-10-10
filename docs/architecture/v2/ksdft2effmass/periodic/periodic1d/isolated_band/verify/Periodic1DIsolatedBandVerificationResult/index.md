# `Periodic1DIsolatedBandVerificationResult`

## Purpose and contract

Immutable summary of independent M1 reconstruction. It binds the exact calculation,
maximum spectral defect, maximum hopping-block defect, exact diagnostic-match flag,
energy-valued absolute tolerance, and final pass flag.

Defects and tolerance must be finite nonnegative energy quantities with compatible
units. `passes` must equal the conjunction of both defect comparisons and
`diagnostics_match`; inconsistent summaries are rejected.

## Interpretation

A passing result supports internal numerical consistency of the frozen M1 protocol. It
does not establish material validity, scientific acceptance, or independence from
shared numerical libraries.
