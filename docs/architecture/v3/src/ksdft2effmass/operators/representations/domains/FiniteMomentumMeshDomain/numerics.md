# Numerical contract

`mesh` must have exact type `CenteredUniformMesh`; subclasses and alternate mesh objects
are rejected. `cardinality` delegates to `mesh.point_count`, and `dimension` delegates to
`mesh.dimension`. Coordinates, offsets, and axis size are not duplicated in this object.

Both textual identities must be exact and nonempty. `sample_role` must be an exact
`MomentumSampleRole`.
