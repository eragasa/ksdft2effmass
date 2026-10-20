# Implementation

The class is a final frozen, slotted dataclass. It requires an exact
`RepresentationTransformationKind`, exact nonempty textual identity/convention fields,
and exact source and target `RepresentationIdentity` leaves.

Raw kind strings and integer discriminants, wrong endpoint types, and wrong text types
raise `TypeError`; empty text and role-incompatible directed edges raise `ValueError`.
`TransformationIdentityFactory` is the canonical construction path, while intrinsic
validation prevents direct construction from bypassing the role-transition invariant.
