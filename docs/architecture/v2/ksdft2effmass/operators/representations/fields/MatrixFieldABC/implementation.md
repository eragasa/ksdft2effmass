# Implementation

`MatrixFieldABC` derives from `abc.ABC`, has empty slots, and declares four abstract
properties. It implements exact equality by requiring the same concrete type, equal
domain metadata, and `numpy.array_equal` values.

The ABC stores no state and performs no constructor validation. Concrete leaves own
storage, domain correlation, shape, dtype, and finiteness checks.
