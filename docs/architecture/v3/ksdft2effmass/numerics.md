# `ksdft2effmass` package numerics

Public numerical contracts identify scalar types, units, state spaces, bases, coordinate
orders, energy references, and finite geometry before arithmetic. Booleans, numeric
strings, nonfinite values, incompatible units, and malformed shapes are rejected unless
a narrower documented contract explicitly admits them.

Canonical PhysKit owners supply represented linear algebra, lattice primitives,
quantities, and matrix norms. Project Koios Optimization supplies unit-free numerical
algorithms. KSD owns scientific composition, family-specific diagnostics, thresholds,
wires, verification, and interpretation.

Sparse values remain sparse unless a bounded public contract authorizes materialization.
Operationally immutable records prevent mutation after constructor validation. Shared
typed serialization preserves dtype, shape, units, and complex values without acquiring
scientific policy or hashing responsibility.

Parent-model, discretization, eigensolver, projection, alignment, fitting, truncation,
and evaluation errors remain separate channels. Passing binary64 comparisons establishes
bounded numerical agreement only; it does not establish exact arithmetic, uncertainty,
continuum convergence, or material validity.
