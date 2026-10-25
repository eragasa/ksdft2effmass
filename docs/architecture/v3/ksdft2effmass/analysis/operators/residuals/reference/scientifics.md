# Scientific interpretation

The reference residual asks how the finite operator acts on prescribed trial states
relative to an analytical retained operator. It differs from Galerkin leakage:

- `H J - J D` includes disagreement with the analytical reference; while
- `H J - J(J^T H J)` measures departure from invariance of the trial space.

For QHO1D the reference residual can contain finite-box, finite-difference, sampling,
Gram-correction, and binary64 contributions. For pristine PIAB1D it compares the
represented stencil action with the selected analytical reference.

The residual is a finite a-posteriori quantity. It is not by itself a continuum error
bound, uncertainty interval, or attribution of error mechanisms.
