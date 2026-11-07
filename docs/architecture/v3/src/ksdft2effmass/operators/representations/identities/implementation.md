# Implementation

The two role enums deliberately remain separate because Bloch fields and cell-hopping
fields have different carrier semantics. Their integer values are internal discriminants.

`RepresentationIdentity` is final, frozen, and slotted. `RepresentationIdentityFactory`
is a stateless slotted class with explicit `create_bloch` and `create_cell_hopping`
methods; it is not an enum-dispatched universal factory. The module imports domains and
spaces only and exports the two enums, identity, and factory.
