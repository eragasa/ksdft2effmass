# Numerical contract

The enum has no numerical algorithm. Its members use internal integer discriminants
`1`, `2`, and `3`. A serializer must provide explicit versioned text mappings rather than
persisting `.value` as an external contract.
