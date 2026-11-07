# Implementation

`MomentumSampleRole` is a standard `Enum`, not a string enum. Construction of
`FiniteMomentumMeshDomain` requires `type(sample_role) is MomentumSampleRole`, so raw
strings and members of other enums are rejected.
