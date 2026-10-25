# Scientific interpretation

The factory constructs derivation-edge identity metadata. It uses the explicit
`RepresentationTransformationKind` member and full endpoints to reject role-incompatible
edges.

It does not apply frame compression, conjugation, alignment, Fourier conversion,
truncation, or reconstruction. Operational transformations belong to
`operators.transformations.base` and its operation-specific Actions.
