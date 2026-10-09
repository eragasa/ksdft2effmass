# Silicon nearest-neighbor orthogonal $sp^3s^*$ model-class specification v1

Status: **adopted for software construction; physical adequacy not yet validated**

Scope: initial model class $\mathfrak{M}_1$ for Computational Stage `04.01.01` and `04.01.02`.

This specification freezes the first executable Slater–Koster model class. It does not
supply fitted silicon parameters, validate the class against Kohn–Sham or experimental
data, accept a Wannier alignment, or mark either computational task complete.

## State space and geometry

The model is spinless and orthogonal. The diamond primitive cell has two equivalent
silicon sites and ten ordered orbitals:

```text
(A:s, A:px, A:py, A:pz, A:s*, B:s, B:px, B:py, B:pz, B:s*)
```

In conventional cubic Cartesian axes, with cubic lattice constant $a$,

$$
\mathbf a_1=\frac a2(0,1,1),\qquad
\mathbf a_2=\frac a2(1,0,1),\qquad
\mathbf a_3=\frac a2(1,1,0),
$$

and the basis sites are $\boldsymbol\tau_A=(0,0,0)$ and
$\boldsymbol\tau_B=a(1,1,1)/4$.

The four directed nearest-neighbor bonds from $A$ in cell zero to $B$ in cell
$\mathbf R$ are

| $\mathbf R$ | cubic bond direction |
|---|---|
| $(0,0,0)$ | $(1,1,1)/\sqrt{3}$ |
| $(-1,0,0)$ | $(1,-1,-1)/\sqrt{3}$ |
| $(0,-1,0)$ | $(-1,1,-1)/\sqrt{3}$ |
| $(0,0,-1)$ | $(-1,-1,1)/\sqrt{3}$ |

## Parameter span

The model has eight real energy coefficients:

$$
\theta_1=
(E_s,E_p,E_{s^*},V_{ss\sigma},V_{sp\sigma},V_{s^*p\sigma},
 V_{pp\sigma},V_{pp\pi}).
$$

Equivalent sublattices share onsite values. $E_p$ is common to $p_x,p_y,p_z$.
Only nearest-neighbor opposite-sublattice hopping is included. The following are exact
zeros of $\mathfrak M_1$:

- $s$–$s^*$ and $s^*$–$s^*$ hopping;
- same-sublattice hopping;
- second- and further-neighbor hopping;
- spin-orbit and spin-dependent terms; and
- nonorthogonal overlap corrections.

These exclusions define this model class; they are not claims that the corresponding
physical contributions vanish in silicon.

All eight coefficients use one explicitly declared physical energy unit. Their onsite
values and hopping integrals are represented relative to one explicitly identified
model energy zero. Changing that zero adds the corresponding scalar multiple of the
identity to both sublattice onsite blocks; it does not alter the hopping integrals.
The implementation accepts finite real coefficient magnitudes only and verifies that
the declared unit is convertible to joules. No numerical coefficient in this
specification is a fitted or literature value.

## Directed-bond convention

For the bond direction $\mathbf d=(l,m,n)$ from the row-site $A$ orbital to the
column-site $B$ orbital,

$$
\langle s_A|H|p_{jB}\rangle=d_jV_{sp\sigma},\qquad
\langle p_{iA}|H|s_B\rangle=-d_iV_{sp\sigma},
$$

with the same parity convention for $s^*$–$p$, and

$$
\langle p_{iA}|H|p_{jB}\rangle
=d_id_jV_{pp\sigma}+(\delta_{ij}-d_id_j)V_{pp\pi}.
$$

Reverse blocks are fixed by
$H(-\mathbf R)=H(\mathbf R)^\dagger$.

## Fourier and gauge convention

The real-space matrix is

$$
[H(\mathbf R)]_{\mu\nu}
=\langle\chi_{\mu\mathbf 0}|\hat H|\chi_{\nu\mathbf R}\rangle.
$$

For reduced reciprocal coordinates $\mathbf q$ satisfying
$\mathbf k\cdot\mathbf a_i=2\pi q_i$, the cell-periodic orbital gauge uses

$$
H(\mathbf q)=\sum_{\mathbf R}
 e^{+2\pi i\mathbf q\cdot\mathbf R}H(\mathbf R).
$$

This gauge does not insert basis-position phases. Comparison with a Wannier operator
requires an independently justified alignment and gauge transformation; equal matrix
dimension is insufficient.

## Verification boundary

Software evidence must establish, at minimum:

- exact basis and displacement ordering;
- linear reconstruction from all eight operator components;
- directed-bond parity signs;
- Hermitian displacement reversal and Bloch Hermiticity;
- a complex non-half-grid oracle that distinguishes the positive Fourier phase, plus
  reciprocal periodicity;
- tetrahedral cancellation and $p$-orbital symmetry at $\Gamma$; and
- onsite-only and omitted-channel limiting cases.

Passing these checks establishes implementation of this specification only. Fitting,
withheld validation, scientific adequacy, parameter identifiability, and compatibility
with an aligned ten-Wannier operator remain separate tasks.
