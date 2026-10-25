# Scientific interpretation

A sampled trial frame is a finite representation of caller-selected analytical or
model states. Its columns need not be orthogonal under the represented grid inner
product. Symmetric Gram orthonormalization constructs the closest polar-factor
isometry associated with that sampled map while preserving the caller's retained
coordinate labels.

For PIAB1D, the intended frame contains normalized discrete sine modes. For the
centered homogeneous-Dirichlet stencil those columns are already orthonormal and span
the represented spectral subspace in exact arithmetic.

For QHO1D, the intended frame contains square-root-quadrature-weighted samples of
real-line Hermite states on a finite Dirichlet grid. Finite interval truncation and
discrete quadrature generally make the sampled Gram matrix differ from the identity.

The module does not claim that:

- the selected analytical states are complete;
- the trial space is invariant under a Hamiltonian;
- a finite interval approximates an infinite domain within a stated error;
- the sampled frame converges as the grid changes;
- the trial space equals a numerical spectral subspace; or
- Gram orthonormalization supplies a physical identification by itself.

Those questions require model-specific construction and outward diagnostics.
