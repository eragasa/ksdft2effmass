# Implementation

`FiniteDomainABC` derives from `abc.ABC`, has empty slots, and declares two abstract
properties: `identity` and `cardinality`. It stores no state and implements no validation.

Concrete leaves must validate their own intrinsic identity, ordering, dimension, and
owner-specific state. The ABC must not acquire filesystem, serialization, analysis, or
campaign behavior.

Substitutability is checked with `isinstance(value, FiniteDomainABC)` inside generic field
contracts; schema boundaries, if later introduced, must retain explicit concrete tags.
