# Numerical contract

The module performs no matrix allocation or arithmetic. It validates exact enum
membership, nonempty textual identities, domain/role family agreement, and exact composed
space types.

`domain_id`, `rank`, `space_id`, and `basis_id` are derived from complete owners. Enum
`.value` integers are internal discriminants only. Domain code compares members directly;
it does not consume raw string or integer substitutes.

Matrix dimensions, carrier-pair contracts, transformation witnesses, and numerical
qualification belong to fields, transformation operations, and evidence owners.
