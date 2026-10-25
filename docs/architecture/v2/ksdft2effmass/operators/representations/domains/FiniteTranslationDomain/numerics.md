# Numerical contract

The inventory is

\[
T=(R_0,\ldots,R_{m-1}),\qquad R_j\in\mathbb Z^d,
\]

with `m > 0`, `d > 0`, common vector dimension, exact uniqueness, and retained caller
order. Components are exact built-in integers; Boolean and numeric strings are rejected.
Python integer magnitude is unbounded and no fixed-width conversion is performed.

No modulo reduction, sorting, norm, metric, or symmetry completion occurs.
