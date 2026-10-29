# Numerical contract

All coordinates, energies, gaps, hopping magnitudes, range errors, omitted-block norms,
and refinement values are taken from the authenticated `Mathieu1dVisualizationData`.
Rendering performs no eigensolve, Fourier transform, reconstruction, truncation, fit,
Parseval check, Hermiticity check, or threshold selection.

Presentation-only operations are limited to the already documented coefficient
magnitudes, finite-series arrangement, recorded energy normalization, and axis scaling.
Connected markers join declared finite inventories and do not infer continuum curves.

The package move must retain byte-identical canonical projection JSON, the two-member
plot enum, and exact inventory closure. PNG bytes are validated as image containers;
the migration does not claim cross-platform pixel or encoding identity.
