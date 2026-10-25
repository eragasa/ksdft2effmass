# Implementation

`CellHoppingRepresentationRole` is a standard Python `Enum` with snake-case members and
explicit internal integer discriminants. `RepresentationIdentity` accepts the enum member
directly and rejects raw strings and integers.

Phase 1 defines no serializer. A future serializer must map the enum members to explicit,
versioned wire tokens. Internal `.value` integers and Python names are not wire contracts.
