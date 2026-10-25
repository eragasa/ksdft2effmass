# Implementation

`RepresentationTransformationKind` is a standard Python `Enum` with snake-case members
and explicit internal integer discriminants. `TransformationIdentity.kind` requires an
exact member, for example `RepresentationTransformationKind.gauge_conjugation`; raw
strings and integers are rejected.

Phase 1 defines no serializer. A future owner-side adapter must map each enum member to an
explicit versioned wire token. The internal integer `.value` and Python member name do not
silently become schema contracts.
