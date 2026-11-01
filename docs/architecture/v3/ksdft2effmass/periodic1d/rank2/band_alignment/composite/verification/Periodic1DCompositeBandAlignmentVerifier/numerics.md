# Numerical contract

The constructor requires built-in immutable result bytes. `result()` hashes and deserializes those same bytes, executes independent comparisons, derives projection bytes, and returns correlated values. `admit_stored()` requires exact aggregate and projection equality.