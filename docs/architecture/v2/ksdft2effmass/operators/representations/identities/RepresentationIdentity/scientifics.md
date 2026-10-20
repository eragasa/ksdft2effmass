# Scientific interpretation

A representation identity names a matrix-field graph node in explicitly identified
coordinates. The complete domain object, finite represented space, ordered basis,
family-local enum role, and source remain distinct.

A `FiniteMomentumMeshDomain` requires `BlochSpaceRole.ambient` or
`BlochSpaceRole.retained`. A `FiniteTranslationDomain` requires
`CellHoppingRepresentationRole.complete_declared_inventory` or
`CellHoppingRepresentationRole.support_truncated`. Gauge, alignment, Fourier, and
truncation history belongs to transformation edges rather than the node role.

Identity is provenance and interpretation metadata. It does not establish array equality,
source correctness, basis equivalence, gauge equivalence, or physical equivalence.
