# Implementation

The class derives from `abc.ABC`, has empty slots, and declares one abstract read-only
property. It establishes nominal result membership.

Concrete result classes should be immutable operation-owned DataObjects. Failure results
must remain explicit and must not fabricate target fields or downstream evidence.
