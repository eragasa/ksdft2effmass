# Numerical contract

The enum performs no compression, conjugation, optimization, Fourier transform,
truncation, reconstruction, residual evaluation, or tolerance comparison. Its explicit
integer `.value` is an internal Python discriminant only; domain code selects and compares
the enum member itself.

Source/target family compatibility, matrix dimensions, transformation witnesses, and
numerical qualification belong to later typed transformation requests and results.
