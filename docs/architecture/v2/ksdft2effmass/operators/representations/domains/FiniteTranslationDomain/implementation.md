# Implementation

The class is a final frozen, slotted dataclass implementing `FiniteDomainABC`. It validates
exact tuple containers at both inventory and vector levels, positive dimension, common
dimension, exact built-in integer components, and uniqueness.

Wrong container or component types raise `TypeError`. Empty, dimension-inconsistent, or
duplicate inventories raise `ValueError`. Validation never canonicalizes a list to a
tuple or reorders vectors.
