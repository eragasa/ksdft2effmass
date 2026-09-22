# Invalid fixtures

Each fixture must be rejected by public deserialization or DataObject
construction:

- `missing-field.json`: omits a required top-level field.
- `unknown-field.json`: includes an undeclared top-level field.
- `unsupported-version.json`: uses a schema version other than `1`.
- `numeric-string.json`: provides a numeric field as a string.
- `boolean-as-number.json`: provides a boolean where a number is required.
- `duplicate-basis-label.json`: repeats a basis label.
- `nonorthogonal-basis.json`: sets `basis.orthonormal` to `false`.
- `ragged-matrix.json`: contains matrix rows of different lengths.
- `nonsquare-matrix.json`: has a rectangular matrix.
- `dimension-mismatch.json`: matrix and state-space dimensions disagree.
- `empty-string.json`: contains an empty required string.
- `singular-cell.json`: cell vectors are not sufficiently linearly independent.
- `energy-reference-value.json`: includes the forbidden historical
  `energy_reference.value` field.

Raw nonstandard JSON text containing `NaN`, `Infinity`, or `-Infinity` is not a
fixture because such text is outside standard JSON; it is tested directly by
serializer tests.
