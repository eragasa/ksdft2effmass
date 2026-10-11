# M2 scientific boundary

## Scientific question

M2 asks how a momentum-dependent change of frame can preserve invariant spectral and
projector information while changing represented matrices and their finite-range
hopping locality. Every represented-matrix comparison identifies a common retained
state space and frame.

## Parent and retained frame

Let $H(k)$ be the finite parent Bloch matrix and $F(k)$ an orthonormal frame for the
retained rank-two subspace. The represented operator is

<a id="eq-m2-projection-001"></a>

$$
H_F(k)=F(k)^\dagger H(k)F(k).
\tag{EQ-M2-PROJECTION-001}
$$

The external-gap diagnostic separates the retained eigenvalue group from the excluded
parent states on the declared mesh. It is a finite-mesh diagnostic, not a general
spectral-isolation theorem.

## Gauge attack

M2 constructs a periodic real rotation

<a id="eq-m2-attack-002"></a>

$$
A(k)=\exp[-i\theta(k)\sigma_y],
\qquad
\theta(k)=\theta_0+\sum_{q=1}^{Q}c_q\sin(2\pi qk),
\tag{EQ-M2-ATTACK-002}
$$

and an attacked frame $F_A(k)=F(k)A(k)$. The projector $F_AF_A^\dagger$ and represented
eigenvalues are invariant, but the matrix $H_{F_A}(k)=A(k)^\dagger H_F(k)A(k)$ is
frame-dependent.

## Pointwise and constrained alignment

Pointwise Procrustes alignment selects a separate unitary $U(k)$ at every momentum.
The constrained channel selects one unitary $U_0$ for the entire path. These are
distinct feasible sets and must never be reported as the same recovery claim.

## Hopping convolution and locality

If $A(k)=\sum_m A_m e^{2\pi i mk}$ and
$H_F(k)=\sum_Q T_Qe^{2\pi iQk}$, the attacked hopping blocks satisfy

<a id="eq-m2-hopping-convolution-003"></a>

$$
\widetilde T_Q
 =\sum_{m,n}A_m^\dagger T_{Q+m-n}A_n.
\tag{EQ-M2-HOPPING-CONVOLUTION-003}
$$

Consequently, exact spectra and projectors do not protect a finite hopping range under
a momentum-dependent frame rotation.

## Sample roles

The $N$-point training mesh constructs frames, alignments, and hopping blocks. The
staggered evaluation mesh uses offset $1/(N+1)$ and is diagnostic only. It cannot alter
the frame transport, attack, unitary choices, ranges, or tolerances.

## Claims and exclusions

M2 demonstrates bounded synthetic behavior for a declared parent, finite mesh, attack,
and alignment families. It does not establish a material result, generic localization
failure, a globally optimal nonconvex gauge, continuum convergence, or uncertainty
bounds.

## Code and evidence mapping

| Equation | Implementing owner | Evidence |
|---|---|---|
| `EQ-M2-PROJECTION-001` | `BandProjectedOperatorPathConstructor1D`, composed by M2 | projection and independent-verifier channels |
| `EQ-M2-ATTACK-002` | `Periodic1DMultibandAlignmentCalculator._attack_rotations` | deterministic attack and recovery tests |
| `EQ-M2-HOPPING-CONVOLUTION-003` | Fourier transform of attacked represented operators | range-resolved locality evidence |

## Provenance

These equations state repository-owned finite conventions. General gauge and operator
definitions remain governed by `specification/` and the referenced Paper 1 derivation.
