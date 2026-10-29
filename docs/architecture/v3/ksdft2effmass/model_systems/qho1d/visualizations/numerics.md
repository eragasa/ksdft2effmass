# Numerical contract

The visualization package consumes only the independently authenticated QHO1D
projection. It performs no finite-difference construction, eigensolve, analytical-state
sampling, common-coordinate alignment, normalization, Gram analysis, or residual-norm
calculation.

State curves use recorded coordinates and already aligned state arrays. Energy and
state distortion panels use recorded discrepancies and component values. Diagnostic
panels display the declared finite box/grid inventory and do not fit an asymptotic rate
or interpolate an uncalculated grid.

The source move must preserve canonical projection JSON bytes, the three-member enum,
and exact renderer-inventory equality. PNG container admission does not imply pixel or
cross-platform byte equality.
