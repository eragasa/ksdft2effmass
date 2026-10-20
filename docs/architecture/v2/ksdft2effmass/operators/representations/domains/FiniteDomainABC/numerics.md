# Numerical contract

`cardinality` is a positive built-in integer supplied by a concrete implementation. The
ABC performs no allocation, coordinate construction, quadrature, modulo arithmetic, or
fixed-width conversion.

A consumer may use cardinality to validate the first axis of a correlated field, but it
must use the concrete domain contract to recover ordering or geometry. Equal cardinality
does not imply equal domains.
