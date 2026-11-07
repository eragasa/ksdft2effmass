# Numerical behavior

Momentum domains require an exact `BlochSpaceRole`; translation domains require an exact
`CellHoppingRepresentationRole`. The identity rejects every other domain or role family.
Text fields must be exact nonempty strings.

`domain_id`, `rank`, `space_id`, and `basis_id` are derived from the composed domain and
space. The factory accepts complete owners and therefore cannot receive conflicting
parallel rank or domain-ID values.
