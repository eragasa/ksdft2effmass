# Implementation

The module defines one final frozen/slotted DataObject and one private exact-string
validator. It composes the existing metadata owners from `operators.records` instead of
introducing replacement classes.

Only `RepresentationSpaceIdentity` is listed in `__all__`. The module imports neither
carrier domains nor transformation contracts.
