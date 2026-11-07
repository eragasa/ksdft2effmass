# Numerical behavior

Construction accepts exact `StateSpace`, `Basis`, `Geometry`, and `EnergyReference`
instances. It requires the ordered basis length to equal the state-space dimension.
Identifier, scalar-field identity, and coordinate-convention identity must be exact
nonempty built-in strings and are stored without normalization.

The derived `dimension` property delegates to `state_space.dimension`; no parallel rank
is stored.
