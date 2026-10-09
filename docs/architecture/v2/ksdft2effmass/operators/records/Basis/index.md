# `Basis`

`Basis` is implemented ordered finite-representation metadata. It stores exact nonempty
identifier/kind, a defensively owned nonempty tuple of unique nonempty labels, and an
exact Boolean orthonormality declaration.

Ordering is semantic: label `i` names matrix row and column `i`. The declaration is not
a numerical proof because vectors or an overlap matrix are absent. `OperatorRecord`
requires orthonormal schema-one bases and correlates label count with dimension.
Construction tests establish software ownership and invariants only.
