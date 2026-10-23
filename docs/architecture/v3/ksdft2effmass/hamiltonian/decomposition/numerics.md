# Numerical contract

`ReducedHamiltonian` binds a reduced matrix to an abstract spectral subspace and a
parent-coordinate Hamiltonian embedding. For the orthogonal PIAB1D instance, with
full-space Hamiltonian $H\in\mathbb{R}^{N\times N}$ and basis
$\Phi_M\in\mathbb{R}^{N\times M}$, the aligned representations are

$$
P_M=\Phi_M\Phi_M^{\mathsf T},
$$

$$
H_{\mathrm{red}}=\Phi_M^{\mathsf T}H\Phi_M
\in\mathbb{R}^{M\times M},
$$

and

$$
H_{\mathrm{embedded}}
=\Phi_M H_{\mathrm{red}}\Phi_M^{\mathsf T}
=P_M H P_M
\in\mathbb{R}^{N\times N}.
$$

The object stores the concrete `OrthogonalSpectralSubspace`, whose `basis_vectors` are
$\Phi_M$ and whose `projector()` derives $P_M$. It stores $H_{\mathrm{red}}$ as the
inherited `matrix` and stores $H_{\mathrm{embedded}}$ as `embedded.matrix`. The
constructor checks types, units, and dimensions. Numerical identities among these
representations require an explicit verifier with a declared tolerance. The abstract
`SpectralSubspace` contract does not require a general Hamiltonian's spectral projector
to be orthogonal.

For one finite real-symmetric $H_{\mathrm{red}}$ and one shape- and unit-compatible
real-symmetric shift $\Delta\in\mathbb{R}^{M\times M}$, the runner evaluates the
established decomposition-freedom and reduced model-class-fit calculation owned by
`analysis.operators`.

The default absolute tolerance is $2.0\times10^{-14}$. It governs input symmetry checks
and the independent verification comparisons. It is a finite nonnegative built-in
float; Booleans and numeric strings are rejected. Visualization DPI is a positive
built-in integer and also rejects Booleans.

The verifier independently checks:

- reconstruction by the reference kinetic and zero-potential decomposition;
- reconstruction by Hamiltonian-minus-shift and shift;
- matrix shapes and units;
- scalar-identity, reduced-basis diagonal, real-symmetric tridiagonal, and arbitrary
  real-symmetric fits; and
- their unexplained residual matrices and Frobenius norms.

It returns all observed issues rather than using runtime `assert` statements. The
facade refuses visualization when any issue is present.

The visualizer consumes verified finite arrays, renders the shift and four fit residual
norms, and returns PNG bytes. It does not recalculate or replace the calculation or
verification result.
