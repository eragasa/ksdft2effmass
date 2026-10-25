# Implementation

The class is a final frozen, slotted dataclass implementing `FiniteDomainABC`. It requires
exact nonempty built-in strings, an exact `CenteredUniformMesh`, and an exact
`MomentumSampleRole`.

Wrong nominal types raise `TypeError`; empty identifiers raise `ValueError`. The class
delegates mesh validation instead of copying it. It performs no coordinate allocation,
filesystem access, or serialization.
