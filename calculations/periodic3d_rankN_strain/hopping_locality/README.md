# Prospective hopping-locality capability

This directory reserves descriptive real-space hopping diagnostics along the changing
unit-volume Bain metric. The direct-length unit, reduced basis offsets, oriented bond
inventory, and exact basis-aware displacement
`A_B(s)(R + tau_beta - tau_alpha)` are selected in
[`../geometry-common-state-space.md`](../geometry-common-state-space.md). A future
protocol must still select the Fourier convention, on-site/non-site partition, complete
metric-shell labels, raw block powers, rank/energy-normalized powers, and range summaries
for every admitted rank, depth, channel, and path point.

For both selected M0 and M1N, reduced-coordinate Fourier coefficients are frozen while
the metric may reclassify their physical radii; this is geometry-driven locality, not
operator response. M0's exact Fourier-invariance obligation is owned by
[`../m0-geometry-only-control.md`](../m0-geometry-only-control.md). Hopping locality does
not remove support. Shell indices and rank-two range outcomes do not transfer across
metrics or ranks. No locality action or result is owned here.
