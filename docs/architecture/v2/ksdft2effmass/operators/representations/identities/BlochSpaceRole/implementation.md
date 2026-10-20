# Implementation

`BlochSpaceRole` is a standard Python `Enum` with snake-case members and explicit
internal integer discriminants. Constructors require exact enum membership and reject
raw strings and integers.

Phase 1 defines no serializer. A future serializer must own an explicit versioned mapping
from `BlochSpaceRole.ambient` and `BlochSpaceRole.retained` to wire tokens. Neither
`.value` nor the Python member name is implicitly a wire contract.
