# Implementation

`fields.py` owns a nominal ABC hierarchy and final frozen slotted NumPy leaves. Shared
private validation retains exact domains, storage types, shape, finiteness, ordering, and
immutable ownership without importing outward diagnostics or transformation operations.
