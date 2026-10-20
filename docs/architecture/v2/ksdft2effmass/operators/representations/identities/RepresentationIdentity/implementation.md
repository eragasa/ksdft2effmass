# Implementation

The class is a final frozen, slotted dataclass. It requires an exact
`FiniteMomentumMeshDomain | FiniteTranslationDomain`, exact
`RepresentationSpaceIdentity`, compatible exact role enum member, and exact nonempty
node and source identities.

A momentum domain paired with a cell-hopping role, a translation domain paired with a
Bloch role, raw strings, integer enum discriminants, and substitute objects raise
`TypeError`. Empty textual identities raise `ValueError`.

`RepresentationIdentityFactory` is the canonical operational constructor. The DataObject
retains intrinsic validation so direct construction cannot bypass domain/role family
compatibility.
