# `Periodic1DFourierLocalityRangeResult`

## Responsibility

Implemented immutable section for one ordinary symmetric support. It keeps
transform-mediated truncation and equal-weight direct fitting distinct while storing the
candidates and diagnostics needed to compare both routes.

## Owned values

- the maximum range and derived representatives `-R,...,R`;
- mediated and direct complex coefficient vectors;
- route-specific construction and evaluation candidates;
- truncation, total, Parseval, direct-design, and route-agreement diagnostics; and
- bandwidth, zone-center curvature, and imaginary-residual summaries.

Application passage and direct identifiability are not duplicated as range wire fields.
The root result derives them from the configured threshold and direct-design values,
binds each candidate to its own coefficient vector, and correlates decisive errors
against the authoritative evaluation field.

## Pages

- [Schematics](schematics.md)
- [Numerics](numerics.md)
- [Scientific interpretation](scientifics.md)
- [Owning result module](../index.md)
