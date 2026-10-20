# Implementation

The class is a final frozen, slotted dataclass. It imports the four existing metadata
leaves directly from `operators.records`, requires their exact nominal types, validates
exact nonempty built-in identity strings, and checks basis/state-space dimension.

Wrong nominal types raise `TypeError`; empty strings or dimension mismatch raise
`ValueError`. It owns no arrays, actions, analyzers, serializers, or compatibility
algorithm.
