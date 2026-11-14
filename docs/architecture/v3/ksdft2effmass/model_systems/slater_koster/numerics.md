# Slater--Koster numerics

## Geometry and the two Bloch representations

With conventional cubic lattice parameter $a$, the normalized primitive vectors are
columns

$$
A=\begin{pmatrix}
1/2&1/2&0\\
0&1/2&1/2\\
1/2&0&1/2
\end{pmatrix},
$$

with primitive-fractional orbital centers $\tau_0=(0,0,0)$ and
$\tau_{1/4}=(1/4,1/4,1/4)$. The positive determinant fixes the handedness.

PhysKit assembles the ordinary-cell representation

$$
H_{\mathrm{cell}}(q)=\sum_R H_R\exp(2\pi i q\cdot R).
$$

KSD requests the full-center representation through the explicit diagonal gauge

$$
D(q)=\operatorname{diag}\!\left(\exp(2\pi i q\cdot\tau_\alpha)\right),
\qquad
H_{\mathrm{full}}(q)=D(q)^\dagger H_{\mathrm{cell}}(q)D(q).
$$

This keeps ordinary-cell displacement separate from fractional orbital-center
embedding while preserving the positive-exponent convention. The full-center matrix
is reciprocal-gauge covariant rather than elementwise periodic; its eigenvalues are
reciprocal-lattice periodic.

The first shell contains four tetrahedral representatives from the origin center to
the body-diagonal-quarter center. The second shell contains six positive
representatives

```text
(1,0,0), (0,1,0), (0,0,1),
(1,-1,0), (1,0,-1), (0,1,-1)
```

on both centers. The PhysKit assembler generates the Hermitian reverse of every input
representative; KSD does not duplicate reverse bonds in its inventory.

## Two-center map

For normalized Cartesian bond direction $d=(l,m,n)$, rows label source orbitals and
columns label target orbitals. The PhysKit homopolar $sp^3s^*$ constructor applies

$$
\langle s|H|p_i\rangle=d_iV_{sp\sigma},\qquad
\langle p_i|H|s\rangle=-d_iV_{sp\sigma},
$$

and likewise for $s^*$--$p$. The $p$ block is

$$
T_{p_ip_j}=d_i d_j V_{pp\sigma}+
(\delta_{ij}-d_i d_j)V_{pp\pi}.
$$

Even-parity $ss$, $ss^*$, and $s^*s^*$ terms are symmetric, so
$T(-d)=T(d)^\mathsf{T}$. KSD's first-neighbor record has only five variable channels;
its composition passes explicit electron-volt zeros for first-neighbor $ss^*$ and
$s^*s^*$.

## Linear hopping representation

For each explicit shell-sharing group $g$ and all seven channels $\alpha$, PhysKit
constructs a nondimensional ordinary-cell model $B_{g,\alpha}(R)$. KSD supplies the
concrete diamond group and bond inventory, giving

$$
H_R^{\mathrm{hop}}(V)=\sum_{g,\alpha}V_{g,\alpha}B_{g,\alpha}(R),
$$

and at an ordered reciprocal sample

$$
H_{\mathrm{cell}}^{\mathrm{hop}}(q_j;V)=
\sum_{g,\alpha}V_{g,\alpha}B_{g,\alpha}(q_j).
$$

The retained order is parameter-group major, channel minor, then reciprocal-sample
major. Both first-neighbor fixed-zero channels remain explicit models. This layer does
not flatten matrix entries, add onsite terms, define a fit, or construct a residual.

## Parameter inventory

The stable eV vector order is

```text
E_s, E_p, E_s_star,
V1_ss_sigma, V1_sp_sigma, V1_pp_sigma, V1_pp_pi, V1_s_star_p_sigma,
V2_ss_sigma, V2_sp_sigma, V2_pp_sigma, V2_pp_pi, V2_s_star_p_sigma,
V2_s_s_star_sigma, V2_s_star_s_star_sigma
```

All assembled terms use the PhysKit metal unit system and KSD verifies that its energy
unit is exactly the electron volt before converting the returned matrix into the KSD
Hamiltonian wrapper. Dense accumulation is complex binary64. Nonfinite input,
direction-normalization failure, phase-argument overflow, assembly overflow, Bloch
evaluation overflow, and full-center gauge overflow fail closed.

No parameter bound, prior, fitted value, residual, or acceptance tolerance is defined
by this model-definition layer.
