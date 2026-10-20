# Implementation

The class derives from `abc.ABC`, has empty slots, and declares one abstract read-only
property. It provides nominal membership rather than structural protocol conformance.

Concrete request classes should be cohesive immutable DataObjects owned by their
operation module. Wire mapping remains a serializer responsibility.
