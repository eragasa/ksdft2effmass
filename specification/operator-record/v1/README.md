# Operator-record schema version 1

This directory is the public, language-neutral validation surface for finite
operator records. `operator-record.schema.json` defines all structurally
expressible JSON constraints for schema version 1. The `valid/` and `invalid/`
fixtures are independently executable examples for Python, Rust, and future
implementations.

Cross-field and numeric constraints that are not completely expressible in JSON
Schema are part of the public contract and must be enforced by DataObjects or by
the JSON serializer/deserializer:

- `N = state_space.dimension = len(basis.ordering)`;
- `matrix` is square with shape `N x N`;
- every matrix and cell component is finite;
- geometry cell rows are linearly independent according to the implementation
  tolerance documented by the `Geometry` DataObject;
- JSON text must not contain duplicate object keys or nonstandard constants such
  as `NaN`, `Infinity`, or `-Infinity`.

Valid fixtures must deserialize successfully. Invalid fixtures must be rejected
by a conforming implementation without relying on private method names.
