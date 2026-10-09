# Finite-mesh Wannier kinetic-decomposition specification v1

Status: **adopted for software construction; scientific interpretation not yet validated**

Scope: a typed finite-representation transformation from authenticated parent-band
arrays to three same-frame represented operator meshes.

This specification defines a mathematical transformation. It does not decode native
Quantum ESPRESSO or Wannier90 files, establish artifact identity, authorize a frame,
execute a calculator, identify a continuous scalar potential, or validate the physical
adequacy of any parent calculation or retained space.

## Ordered finite inputs

Let the unshifted uniform mesh have shape $(N_1,N_2,N_3)$ and
$N_k=N_1N_2N_3$. Samples use C-order tensor-product ordering, with the third mesh index
varying fastest:

$$
\mathbf q_{n_1n_2n_3}=
\left(\frac{n_1}{N_1},\frac{n_2}{N_2},\frac{n_3}{N_3}\right),
\qquad 0\le n_i<N_i.
$$

At every ordered mesh point, the caller supplies:

- a coefficient matrix $C\in\mathbb C^{P\times B}$, with authenticated flattened
  plane-wave/spinor coordinates in rows and ordered parent bands in columns;
- canonical kinetic energies $t\in\mathbb R^P$, with spinor rows repeating the
  corresponding spatial kinetic energy when applicable;
- ordered parent eigenvalues $\epsilon\in\mathbb R^B$;
- a disentanglement isometry $D\in\mathbb C^{B\times J}$; and
- a Wannier gauge matrix $U\in\mathbb C^{J\times J}$.

The retained frame is

$$
W=DU,
$$

mapping retained Wannier coordinates into the ordered parent-band coordinates. The
software checks $D^\dagger D\simeq I_J$ and $U^\dagger U\simeq I_J$ against the
request's frame absolute tolerance. It reports the corresponding defects and the
combined defect $\lVert W^\dagger W-I_J\rVert_F$.

The integration owner must establish coefficient-row ordering, reciprocal-vector and
FFT conventions, spinor ordering, normalization or generalized-overlap interpretation,
ordered k-point correlation, and artifact provenance before creating this request.
This transformation does not require ordinary Euclidean norms of the columns of $C$
to equal one and does not infer any omitted ultrasoft or PAW contribution.

## Same-frame operators

The parent-band canonical kinetic matrix and the two retained operators are

$$
T^{KS}=C^\dagger\operatorname{diag}(t)C,
$$

$$
H^W=W^\dagger\operatorname{diag}(\epsilon)W,
\qquad
T^W=W^\dagger T^{KS}W.
$$

Only after both matrices occupy the identical ordered retained frame is the represented
non-kinetic remainder defined:

$$
R^W=H^W-T^W.
$$

$R^W$ is a finite represented remainder. It can contain local,
nonlocal-pseudopotential, Hartree, exchange-correlation, and other represented
contributions. It is not thereby a continuous scalar potential.

All $t$, $\epsilon$, and represented matrices use physical units convertible to
joules. Input values may use different compatible energy units and are converted to
the request's declared output energy unit before construction. The request identifies
the parent Hamiltonian energy reference. The canonical kinetic values are not shifted
when that parent reference changes; consequently, a scalar shift of the parent
Hamiltonian produces the same scalar identity shift in $R^W$. The common retained
`energy_reference` metadata identifies the decomposition's parent-Hamiltonian
reference and does not assert an independently adjustable zero for the canonical
kinetic operator.

## Canonical finite Fourier representation

For a centered representative

$$
\mathbf R=(r_1,r_2,r_3),\qquad
-\lfloor N_i/2\rfloor\le r_i< -\lfloor N_i/2\rfloor+N_i,
$$

the normalized forward transform of any represented reciprocal operator $A^W$ is

$$
A^W(\mathbf R)=\frac{1}{N_k}
\sum_{n_1,n_2,n_3}
\exp\left[-2\pi i\sum_{j=1}^3\frac{n_jr_j}{N_j}\right]
A^W(\mathbf q_{n_1n_2n_3}).
$$

Representatives use lexicographic C order with $r_3$ varying fastest. Reconstruction
uses the positive phase without an additional normalization:

$$
A^W(\mathbf q_{n_1n_2n_3})=
\sum_{\mathbf R}
\exp\left[+2\pi i\sum_{j=1}^3\frac{n_jr_j}{N_j}\right]
A^W(\mathbf R).
$$

These are exact finite discrete transforms up to floating-point roundoff. They are not
an infinite-lattice convergence statement or a real-space truncation.

## Diagnostics and admission

Every reported defect is a built-in nonnegative finite `float`. Matrix defects use the
Frobenius norm. The retained maxima are:

- $\max_k\lVert U_k^\dagger U_k-I\rVert_F$;
- $\max_k\lVert D_k^\dagger D_k-I\rVert_F$;
- $\max_k\lVert W_k^\dagger W_k-I\rVert_F$;
- reciprocal Hermiticity defects for $H^W$, $T^W$, and $R^W$;
- reciprocal and lattice decomposition defects
  $\max\lVert H^W-(T^W+R^W)\rVert_F$; and
- forward/inverse round-trip defects for all three operators.

Frame factors are admitted against the request's separate frame tolerance. The
`passes` property assesses Hermiticity, reciprocal and lattice decomposition, and all
three Fourier round trips against the diagnostic absolute tolerance. It does not
replace frame admission, provenance checks, scientific validation, convergence,
uncertainty quantification, or human acceptance.

Maintained result records must reproduce the reciprocal construction from their
request, retain the exact requested identities and ordered k-point record, use the
requested energy unit, retain the canonical Fourier blocks, and correlate every
reported diagnostic with the represented values. Dimensions, filenames, spectra, and
digests alone cannot establish any of these scientific identities.

## Separation from effective models

This rank-$J$ Wannier representation is not an atomic-orbital Slater–Koster model. In
particular, a rank-four retained Wannier operator must not be padded, shape-matched, or
subtracted from a ten-orbital $sp^3s^*$ operator. Such an operator comparison requires
a separately justified common state space, metric, subspace correspondence, gauge,
geometry convention, unit, and energy-reference alignment.
