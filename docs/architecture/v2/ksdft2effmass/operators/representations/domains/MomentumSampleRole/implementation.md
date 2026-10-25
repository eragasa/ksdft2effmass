# Implementation

`MomentumSampleRole` is a standard Python `Enum` with explicit internal integer
discriminants. Constructors require exact enum membership and reject raw strings and
integers.

Domain code uses the member directly, for example
`MomentumSampleRole.construction`; it does not branch on `.value`. The enum has no
serializer in Phase 1. A future schema adapter must define an explicit versioned mapping
from enum members to wire tokens rather than treating the internal integers or Python
member names as a wire contract.
