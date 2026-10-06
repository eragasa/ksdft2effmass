# `Geometry`

`Geometry` is implemented finite cell and boundary metadata. It preserves three ordered
row lattice vectors, system, boundary-condition and coordinate conventions, and length
unit. Accepted finite real components are defensively canonicalized to built-in floats;
the cell must satisfy the documented scale-relative linear-independence rule.

It performs no unit conversion, coordinate transformation, relaxation, handedness
selection, crystallographic classification, or physical validation. Geometry tests use
explicit software/numerical criteria and do not establish material correctness or UQ.
