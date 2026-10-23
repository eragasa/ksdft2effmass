# `ksdft2effmass.operators.hamiltonians`

## Purpose and status

This implemented module owns typed finite Hamiltonian representations.

Source: `python/src/ksdft2effmass/operators/hamiltonians.py`.

## Contracts

`Hamiltonian` owns one nonempty square real or complex dense or sparse finite
Hamiltonian matrix with explicit units. It does not assume Hermiticity.

[`ksdft2effmass.linalg`](../../linalg/index.md) owns dense and canonical CSR matrix
quantities and `MatrixVerifier`. `HermitianHamiltonian` refines `Hamiltonian`: both
direct construction and `from_hamiltonian()` use zero relative and absolute tolerances
for exact finite-representation Hermiticity and preserve the matrix unchanged.

`SpectralSubspace` is an abstract domain boundary for finite spectral-subspace
representations. It requires the parent dimension, subspace dimension, and represented
spectral projector. `OrthogonalSpectralSubspace` is the currently implemented concrete
case; it owns selected real eigenvalues and an orthonormal finite basis.

`ReducedHamiltonian` extends the general Hamiltonian:

```python
class ReducedHamiltonian(Hamiltonian):
    spectral_subspace: SpectralSubspace
    embedded: Hamiltonian
```

The inherited `matrix` is the reduced Hamiltonian in the spectral-subspace
coordinates. `embedded` is a Hamiltonian representing that reduced operator in the
parent coordinates. Construction requires both matrix dimensions to agree with the
abstract subspace dimensions and requires matching reduced/embedded Hamiltonian units.
It does not assume the spectral projector is orthogonal.

For PIAB1D, the concrete subspace is `OrthogonalSpectralSubspace` with basis
$\Phi_M$. Its finite projector is derived as
$P_M=\Phi_M\Phi_M^{\mathsf T}$; the embedded matrix is
$\Phi_M H_{\mathrm{red}}\Phi_M^{\mathsf T}$.

These public types are exported through `ksdft2effmass.operators`.

## Ownership boundary

These records identify aligned finite Hamiltonian representations. They do not select a
spectral subspace, compute compression, infer a physical model, or choose a reduced
dimension. Numerical construction remains with `OperatorCompression` or another
declared producer; model systems own why a subspace is selected.
`HamiltonianDecomposition` consumes `ReducedHamiltonian` but does not own it.

The records validate intrinsic types, units, and dimensions. Numerical identities among
a subspace representation, its projector, a reduced matrix, and an embedded matrix
require an explicit verifier with a declared tolerance. Exact Hermiticity and numerical
Hermiticity are distinct contracts.

## Evidence

Focused tests establish general dense and sparse Hamiltonian construction, exact
Hermitian refinement rejection, abstract spectral-subspace substitution,
reduced-Hamiltonian shape alignment, package export, and PIAB1D construction. Matrix
storage and property evidence belongs to `ksdft2effmass.linalg`. These are software
checks, not scientific validation of a reduced model.
