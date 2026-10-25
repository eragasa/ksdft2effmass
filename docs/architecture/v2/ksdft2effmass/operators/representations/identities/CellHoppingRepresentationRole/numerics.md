# Numerical contract

The enum performs no Fourier transform, support selection, zero extension, reconstruction,
or tolerance comparison. It carries no coefficient count or translation domain.

Its explicit integer `.value` is an internal Python discriminant only. Domain code uses
the enum member directly. Inventory coverage and domain cardinality require separate
objects and evidence.
