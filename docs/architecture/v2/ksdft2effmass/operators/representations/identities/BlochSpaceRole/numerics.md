# Numerical contract

`BlochSpaceRole` performs no arithmetic and carries no matrix shape, rank, domain,
precision, norm, or tolerance. Its explicit integer `.value` is an internal Python
discriminant only; domain code uses the enum member directly.

Rank and represented-space compatibility are checked separately by
`RepresentationIdentity`. Momentum-domain binding belongs to a later typed
representation node.
