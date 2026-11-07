# Numerical behavior

`FiniteMomentumMeshDomain` accepts an exact `CenteredUniformMesh`. Its cardinality is the
mesh tensor-product point count and its dimension is the mesh dimension; no parallel
coordinate array is accepted.

`FiniteTranslationDomain` requires a nonempty exact tuple of unique, nonempty integer
tuples with one common dimension. Components must be exact built-in integers, so booleans
and numeric strings are rejected. The retained order is not sorted, reduced modulo a
period, or completed into shells.
