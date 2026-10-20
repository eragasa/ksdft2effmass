# Numerical contract

The represented rank is derived:

\[
r=\dim(\text{space}).
\]

The domain identity is also derived from `domain.identity`. Callers cannot provide
parallel rank or domain-ID values that disagree with the composed owners.

Construction performs no rank-sized allocation, coordinate conversion, field-shape
validation, or numerical property check. Domain cardinality and mesh arithmetic remain
owned by the composed domain object.
