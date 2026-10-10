# M1 calculator mathematics

The parent fiber, Fourier transform, and staggered evaluation equations are
`EQ-M1-PARENT-FIBER-001`, `EQ-M1-FOURIER-002`, and
`EQ-M1-WITHHELD-MESH-003` in [the M1 scientific page](../../../../scientific.md).

`_maximum_spectrum_error` evaluates a maximum absolute energy norm only after exact
coordinate and shape correlation. `_scalar_operator_samples` embeds each selected band
value as a $1\times1$ represented operator. `_physical_coordinates` applies the model's
reciprocal vector and retains inverse-length units. `_calculate_range` compares
$\sum_{|R|\leq L}T_Re^{2\pi ikR}$ from truncation with an independently inferred
least-squares model using the same representatives.

The calculator does not identify transformation, truncation, and fitting as equivalent
operations; it reports their differences.
