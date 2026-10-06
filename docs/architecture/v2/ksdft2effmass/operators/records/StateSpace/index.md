# `StateSpace`

`StateSpace` is implemented finite representation metadata: exact nonempty identifier
and kind plus a positive dimension. Python and NumPy integer scalars are canonicalized
to built-in `int`; Booleans and numeric strings are rejected.

It stores no basis, matrix, physical Hilbert-space proof, or operator semantics.
`OperatorRecord` owns cross-object dimension correlation. Construction tests establish
intrinsic software behavior only, not completeness, physical meaning, validation, UQ,
or acceptance.
