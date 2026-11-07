# Numerical behavior

Every concrete leaf owns a finite exact-`complex128` array with shape
`(domain_cardinality, target_dimension, source_dimension)`. Both matrix dimensions must
be positive. Operator, projector, gauge, and Fourier-block leaves require square matrices;
frame fields may be rectangular.

The immutable-array owner copies through bytes-backed storage, so caller mutation and
write-flag restoration cannot change the retained field. `is_exactly_equal_to` compares
only the same concrete leaf using domain equality and `numpy.array_equal`; it applies no
tolerance or coordinate conversion.
