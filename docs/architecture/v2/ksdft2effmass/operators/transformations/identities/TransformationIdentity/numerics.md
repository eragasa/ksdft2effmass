# Numerical contract

The class performs no matrix multiplication, optimization, Fourier conversion, support
operation, solve, residual calculation, or tolerance comparison. It checks exact nominal
types and enum-compatible source/target roles only.

`kind` must be the enum member itself; raw strings and integer discriminants are rejected.
Orientation remains textual convention metadata. Dimension, basis-map, finite-Fourier,
and numerical qualification checks belong to later operation-specific transformations.
