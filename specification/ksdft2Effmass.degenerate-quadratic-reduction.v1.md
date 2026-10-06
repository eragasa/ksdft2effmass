# Degenerate represented-operator quadratic reduction specification v1

Status: **adopted for software construction; scientific interpretation not yet validated**

Scope: a typed finite-dimensional Löwdin quadratic reduction of same-frame represented
Hamiltonian, canonical kinetic, and non-kinetic-remainder Cartesian derivative tensors
at one reciprocal coordinate.

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
- a unitary covariance-probe gauge on the selected coordinates; and
- an absolute frame-unitarity tolerance.

Every selected eigenvalue must lie within the degeneracy tolerance of $E_0$, and every
complement eigenvalue must lie outside it. The complement must be nonempty. These
requirements identify the finite selected eigenspace; they do not establish a physical
band label or exact symmetry degeneracy.

Let $P$ contain the selected orthonormal eigenvectors and $Q$ the complementary
ones. The complementary resolvent is

$$
G=Q\left(E_0-Q^\dagger H Q\right)^{-1}Q^\dagger.
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

It also reports the maximum selected-group splitting and minimum complement separation
from $E_0$. These diagnostics establish only the stated finite matrix identities.
They do not select an effective model, identify scalar branch masses, quantify
uncertainty, or validate physical adequacy.
