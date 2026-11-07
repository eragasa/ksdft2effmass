# Numerical behavior

The check is exact: `type(value) is str` and `value != ""`. Whitespace-only strings are
retained because this layer defines no textual grammar. No stripping, case conversion,
Unicode normalization, parsing, or numeric coercion occurs.
