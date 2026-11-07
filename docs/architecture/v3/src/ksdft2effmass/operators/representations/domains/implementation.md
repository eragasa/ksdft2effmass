# Implementation

`FiniteDomainABC` defines only `identity` and `cardinality`. The two concrete leaves are
final frozen/slotted dataclasses. `MomentumSampleRole` is a standard enum with internal
integer discriminants. `_require_nonempty_exact_string` centralizes exact text validation
within this module.

The module depends inward on `projectkoios.numerics.finite_periodic.meshes` and does not
import spaces, identities, fields, transformations, analysis, campaigns, or wire owners.
Its `__all__` contains the ABC, enum, and two leaves; the validator remains private.
