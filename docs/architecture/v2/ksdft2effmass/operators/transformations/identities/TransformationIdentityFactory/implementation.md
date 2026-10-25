# Implementation

`TransformationIdentityFactory` is a final stateless slotted class with one typed
`create` method. It requires the `RepresentationTransformationKind` enum member itself
and exact source and target `RepresentationIdentity` leaves.

The class is intentionally named an identity factory. It does not implement
`RepresentationTransformationABC`, dispatch numerical algorithms, or return operational
results.
