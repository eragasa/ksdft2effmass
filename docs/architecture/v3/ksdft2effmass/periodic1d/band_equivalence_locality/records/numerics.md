# Numerical contract

The record uses `BaseTypedRecord` canonical JSON. Its top-level inventory is exactly `parent_family`, `momentum_refinement`, `adaptive_amplitude`, and `truncation`. Nested closed outcomes use variant-specific mappings and contain neither null padding nor a type registry.

Decoding rejects missing, extra, unknown, and cross-channel variants. Built-in scalar admission and the nested owners' finiteness, ordering, mesh, threshold, and payload checks run before a record is admitted.
