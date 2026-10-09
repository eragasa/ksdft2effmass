# `EnergyReference`

`EnergyReference` is implemented exact textual metadata for an energy-origin convention
and unit label. Both nonempty strings are stored without trimming, normalization,
registry lookup, conversion, or implicit shift.

Exact equality is a represented compatibility precondition, not proof of physical
alignment. Numerical offsets and conversion require separate explicit operations.
Constructor/value tests establish immutable software semantics only.
