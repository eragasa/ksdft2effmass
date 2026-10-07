# Löwdin quadratic effective-Hamiltonian specification v1

Status: **adopted for software construction; scientific interpretation not yet validated**

Scope: a typed finite-dimensional Löwdin construction of one selected-space quadratic
effective Hamiltonian from same-frame represented Hamiltonian, canonical kinetic, and
non-kinetic-remainder Cartesian derivative tensors at one reciprocal coordinate. The
partitioning terminology follows Löwdin's class-partition perturbation construction
[^lowdin1951]; the repository already cites the same work in
`docs/research/ksdft2Effmass.02.md`.

This specification does not choose a physical band manifold, infer degeneracy from a
label, decode native files, track scalar bands through a degeneracy, convert curvature
to effective mass, or establish reciprocal-mesh, interpolation, parent-model, or
scientific convergence.

## Inputs and subspace selection

The request supplies Cartesian derivative results for $H^W$, $T^W$, and $R^W$ at the
same identified source binding, retained frame, energy reference, reciprocal point,
Wigner–Seitz inventory, matrix dimension, and units. The derivative tensors must obey

$$
H= T+R,
$$

but their finite numerical closure is reported rather than presumed.

The caller explicitly supplies:

- a strictly increasing tuple of selected ordered Hamiltonian eigenvalue indices;
- a reference energy $E_0$;
- a nonnegative degeneracy tolerance in the Hamiltonian energy unit;
- a nonnegative Hamiltonian-Hermiticity tolerance in the Hamiltonian energy unit;
- a unitary covariance-probe gauge on the selected coordinates; and
- an absolute frame-unitarity tolerance.

Every selected eigenvalue must lie within the degeneracy tolerance of $E_0$, and every
complement eigenvalue must lie outside it. The complement must be nonempty. Before
these eigenvalues are computed, the anti-Hermitian Frobenius defect of the supplied
Hamiltonian value must not exceed the caller's Hamiltonian-Hermiticity tolerance. A
larger defect is a mathematical rejection: the declared Hermitian eigenspace and
Löwdin complement resolvent are not defined by that request. No operator identity is
silently reassigned.

For an accepted finite defect, the reduction explicitly uses

$$
H_{\mathrm h}=\frac{1}{2}(H+H^\dagger)
$$

for eigenspace selection and direct Hamiltonian-value projection. The result retains
$\lVert H_{\mathrm h}-H\rVert_F$ in the Hamiltonian energy unit. This is a declared
finite numerical projection within a caller-owned tolerance, not an assertion that the
input was exactly Hermitian. These requirements identify the finite selected
eigenspace; they do not establish a physical band label or exact symmetry degeneracy.

Let $P$ contain the selected orthonormal eigenvectors of $H_{\mathrm h}$ and $Q$ the
complementary ones. The complementary resolvent is

$$
G=Q\left(E_0-Q^\dagger H_{\mathrm h} Q\right)^{-1}Q^\dagger.
$$

All denominators must be nonzero under the declared degeneracy tolerance. They may
have either sign.

## Projected derivatives and remote terms

For $A\in\{H,T,R\}$, the direct projected tensors are

$$
A_P=P^\dagger A P,\qquad
(A_a)_P=P^\dagger A_aP,\qquad
(A_{ab})_P=P^\dagger A_{ab}P.
$$

For two gradient families $A_a$ and $B_b$, define

$$
\mathcal L_{ab}[A,B]=
P^\dagger\left(A_aGB_b+B_bGA_a\right)P.
$$

The total remote Hamiltonian contribution is

$$
L^{HH}_{ab}=\mathcal L_{ab}[H,H].
$$

Using $H_a=T_a+R_a$, its explicit partition is

$$
L^{HH}_{ab}=L^{TT}_{ab}+L^{RR}_{ab}+L^{TR}_{ab},
$$

where

$$
L^{TR}_{ab}=\mathcal L_{ab}[T,R]+\mathcal L_{ab}[R,T].
$$

The effective selected-space quadratic tensor is

$$
K_{ab}=(H_{ab})_P+L^{HH}_{ab}.
$$

The action retains projected values, gradients, direct Hessians, all remote terms, the
resolvent, and $K_{ab}$. Value, gradient, and quadratic quantities use energy,
energy-times-length, and energy-times-length-squared units, respectively.

## Cartesian evaluation and directional contraction

A separate typed evaluation request supplies a nonempty matrix of Cartesian reciprocal
offsets. Its unit must be dimensionally compatible with the inverse direct-lattice
unit retained by the derivative inventory. The evaluator converts those offsets into
that reciprocal unit and returns

$$
H_{\mathrm{eff}}(q)=H_P+q_a(H_a)_P+\frac{1}{2}q_aq_bK_{ab}
$$

as one selected-space energy matrix per row. It reports the maximum anti-Hermitian
Frobenius defect of the evaluated family.

A distinct directional-contraction request supplies nonempty normalized, unitless
Cartesian directions $n$. The constructor returns

$$
K(n)=n_an_bK_{ab}
$$

with energy-times-length-squared units and its maximum anti-Hermitian defect. It does
not diagonalize $K(n)$, associate its eigenvalues across directions, or convert them
to masses. Thus polynomial evaluation, directional tensor contraction, eigenspectrum
analysis, branch tracking, and physical interpretation remain separate operations.

## Diagnostics and covariance

The reduction result reports unit-carrying Frobenius defects for:

- value, gradient, and direct-Hessian $H=T+R$ closure;
- the $HH=TT+RR+TR$ remote partition;
- anti-Hermiticity of the effective quadratic tensor; and
- covariance of the projected base, gradient, and effective quadratic tensor under
  the request's explicit selected-space gauge $C$:
  $A' = C^\dagger A C$.

Both gauges in the base covariance diagnostic project the same accepted Hermitian
Hamiltonian value $(H+H^\dagger)/2$. The removed anti-Hermitian component is reported
only by the Hermitian-projection correction; it must not be reclassified as a basis-
covariance defect by projecting the original non-Hermitian value in one gauge. The
Result retains the covariance-probe base, gradient, and effective-quadratic tensors so
it can validate all three covariance diagnostics intrinsically without repeating the
eigensolve or request-to-reduction derivation.

Public reduction, model-evaluation, and directional-contraction Result constructors
accept no precomputed numerical witness. Each Action owns request-to-value derivation
and performs it once. Results validate intrinsic types, dimensions, units, retained
algebraic relations, and diagnostics derivable from their values; they do not replay
the Action. Manual Result construction therefore establishes structural validity only,
not Action execution, provenance, or scientific evidence.

It also reports the Hamiltonian Hermitian-projection correction, maximum selected-group
splitting, and minimum complement separation from $E_0$. These diagnostics establish
only the stated finite matrix identities.
They do not select an effective model, identify scalar branch masses, quantify
uncertainty, or validate physical adequacy.

## References and citation provenance

[^lowdin1951]: Per-Olov Löwdin, “A Note on the Quantum-Mechanical Perturbation
    Theory,” *The Journal of Chemical Physics*, vol. 19, no. 11, pp. 1396–1401,
    1951, doi: [10.1063/1.1748067](https://doi.org/10.1063/1.1748067). The title,
    author, journal, volume, issue, pages, publication date, and DOI were checked
    against the Crossref record for that DOI on 2026-10-07. This citation supports
    the historical origin of the class-partition construction; it does not by itself
    validate this software's derivative convention, finite-matrix implementation,
    tolerances, kinetic/remainder decomposition, or scientific application.
