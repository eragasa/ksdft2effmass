# Numerical contract

For mesh dimension `d`, common axis size `N`, and offsets `delta[a]`, Numerics defines

\[
q_{a,i}=-\frac12+\frac{i+\delta_a}{N},\qquad |K|=N^d.
\]

`cardinality` and `dimension` are derived from the composed mesh. No parallel size or
coordinate array is accepted. Offset, size, dimension, finiteness, and point-count
semantics remain owned by `CenteredUniformMesh`.
