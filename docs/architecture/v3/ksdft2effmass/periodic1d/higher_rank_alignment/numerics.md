# Numerical formulation of higher-rank frame alignment

## Analytic parent and attacked representations

For retained orbital $a=1,\ldots,r$, define
$x_{r,a}=(2a-r-1)/(r-1)$ and let the physical reciprocal coordinate be
$k=2\pi x$. The analytic retained and exterior energies are

$$
\varepsilon_a(k)=0.4x_{r,a}+0.25(1+0.2x_{r,a})
\left(0.75\cos k+0.25\cos 2k\right),
$$

and

$$
\varepsilon_a^{\mathrm{ext}}(k)=3+0.3x_{r,a}+0.1
\left(0.75\cos k+0.25\cos 2k\right).
$$

The ambient basis orders all $r$ retained orbitals before the $r$ exterior orbitals.
The reference frame embeds the retained coordinate axes into this $2r$-dimensional
basis, and endpoint sewing is the ambient identity. A depth-$L$ product of disjoint
nearest-neighbor real rotations defines $G_{r,L}(k)$. For one-indexed pair start $j$ in
layer $\ell$,

$$
y_{r,j}=\frac{2j-r}{r-1},\qquad
s_\ell(k)=\frac34\sin k+\frac14(-1)^\ell\sin 2k,
$$

and

$$
\theta_{\ell j}(k)=0.35(-1)^{\ell+j}
(1+0.15y_{r,j})s_\ell(k).
$$

Pairs satisfy $j\equiv\ell\pmod 2$, factors within a layer commute, and layers are
multiplied in increasing order. All pair and diagonal phases vanish, so
$G_{r,L}(k)\in SO(r)$. The attacked frame and represented retained operator are

$$
F'_{r,L}(k)=F_r(k)G_{r,L}(k),
\qquad
H'_{r,L}(k)=G_{r,L}^{\dagger}(k)D_r(k)G_{r,L}(k),
$$

where $D_r(k)=\operatorname{diag}(\varepsilon_0(k),\ldots,
\varepsilon_{r-1}(k))$. The known-inverse channel applies $G_{r,L}^{\dagger}(k)$
on the right and therefore recovers $D_r(k)$ up to binary64 arithmetic.

## Global and pointwise Procrustes selection

The global matrix minimizes the uniformly weighted construction-mesh objective at
$M=2049$. In the implementation, stacking the $M$ frame matrices and scaling both
stacked inputs by $M^{-1/2}$ makes the Optimization cross matrix equal to the declared
mesh average. This preserves the absolute part of the strict rank threshold. The one
selected matrix is then applied without refitting at $M=513$, $1025$, and all shifted
evaluation points.

Pointwise selection is one batched Procrustes solve per construction mesh. Complete
singular spectra, applied cutoffs, numerical ranks, normalized residuals, unitarity,
stationarity, and positive-semidefinite defects are retained. A rank-deficient selection
has no downstream operator-locality values.

## Parallel transport and periodic closure

Let $F_j\in\mathbb{C}^{d\times r}$ contain an orthonormal basis for the retained
$r$-dimensional subspace at construction-mesh point $j$. Transport uses the unshifted
one-dimensional centered mesh `CenteredUniformMesh(1, M, (0.0,))`; the shifted
evaluation mesh is not a transport route. Neighboring frames are joined by
polar-Procrustes alignment. This produces a sequentially transported frame
$\widetilde F_j$ around the periodic reciprocal-space route.

Endpoint sewing acts on the ambient space from the left. Let $S_{\mathrm{amb}}$ denote
that sewing map. The right-unitary transformation that aligns the primitive transported
endpoint with the sewn initial frame is defined by

$$
\widetilde F_M U_{\mathrm{p\to s}}
 \approx S_{\mathrm{amb}}\widetilde F_0,
$$

where $M$ is the number of construction-mesh points. The reverse endpoint mismatch is

$$
U_{\mathrm{s\to p}}=U_{\mathrm{p\to s}}^\dagger.
$$

Periodic closure is distributed uniformly around the route through a right-unitary step
$U_{\mathrm{step}}$ satisfying

$$
U_{\mathrm{step}}^M=U_{\mathrm{p\to s}}.
$$

The corrected frames are therefore

$$
F_j^{\mathrm{closed}}
 = \widetilde F_j U_{\mathrm{step}}^j,
\qquad j=0,\ldots,M.
$$

The endpoint mismatch is decomposed as

$$
U_{\mathrm{s\to p}}
 = Z\,\operatorname{diag}
   \left(e^{i\gamma_1},\ldots,e^{i\gamma_r}\right)Z^\dagger,
\qquad \gamma_a\in(-\pi,\pi].
$$

Consequently,

$$
U_{\mathrm{step}}
 = Z\,\operatorname{diag}
   \left(e^{-i\gamma_1/M},\ldots,e^{-i\gamma_r/M}\right)Z^\dagger.
$$

The branch $(-\pi,\pi]$ assigns phase $+\pi$ to an eigenvalue $-1$. This convention is
part of the calculation definition because the opposite half-open branch would select a
different distributed root. Stored phases are sorted only for deterministic output;
their order does not label physical bands.

The corresponding result fields are deliberately descriptive:

| Quantity | Result field |
|---|---|
| $U_{\mathrm{p\to s}}$ | `primitive_last_to_sewn_first_right_unitary` |
| $U_{\mathrm{s\to p}}$ | `sewn_first_to_primitive_last_right_unitary` |
| $U_{\mathrm{step}}$ | `distributed_closure_correction_right_unitary_step` |

Successful transport stores all three unitless matrices. Rank-deficient transport stores
none of them because periodic closure was not established.

## Singular-value rank test

For each neighbor overlap and for the sewn closure overlap, let $X$ be the matrix to
which polar-Procrustes alignment is applied. Its numerical-rank threshold is

$$
\tau_{\mathrm{rank}}(X)
 = \max\!\left(10^{-12},10^{-10}\sigma_{\max}(X)\right).
$$

A link is full rank only when

$$
\sigma_{\min}(X)>\tau_{\mathrm{rank}}(X).
$$

Equality is classified as rank deficient. The signed rank margin is

$$
m_{\mathrm{rank}}
 = \sigma_{\min}(X)-\tau_{\mathrm{rank}}(X).
$$

A deficient link terminates frame transport. Later links are recorded as unattempted;
no singular values or transported frames are fabricated for them.

## Numerical residuals and physical error measures

The transport backend validates matrix identities using the maximum absolute entry

$$
\lVert R\rVert_{\max}=\max_{a,b}|R_{ab}|.
$$

This is an implementation-level check, not the scientific error measure used to compare
ranks. The higher-rank study uses the normalized Frobenius residual

$$
\varepsilon_F(R)=\frac{\lVert R\rVert_F}{\sqrt r}
$$

for frame, transport, and closure diagnostics. For an operator residual with energy
reference $E_{\mathrm{ref}}$, the dimensionless measure is

$$
\varepsilon_H(R)
 = \frac{\lVert R\rVert_F}{\sqrt r\,E_{\mathrm{ref}}}.
$$

These quantities must remain distinct. Alignment error is also kept separate from
interpolation error, Fourier reconstruction error, cyclic-to-ordinary conversion,
truncation error, and the ordinary omitted tail. Pointwise residual identities may
telescope, but maxima over reciprocal space are not additive.

## Odd-mesh Fourier locality and shifted evaluation

For every qualified channel and construction size $M$, PhysKit transforms the complete
matrix field on the unshifted odd centered mesh. The represented translations are

$$
R=-\frac{M-1}{2},\ldots,\frac{M-1}{2},
$$

so there is no Nyquist singleton and ordinary inversion pairs cover the complete
inventory. The producer records all block norms with $|R|\le128$ and evaluates the
complete Fourier series on the shifted $8191$-point mesh. Direct analytic values on that
same shifted mesh define interpolation error.

For every declared support $S\in\{0,1,2,4,8,16,32,64,128\}$, truncation retains exactly
$|R|\le S$. The record keeps three different matrix fields:

$$
E_{\mathrm{interp}}=H_{\mathrm{full}}-H_{\mathrm{direct}},
$$

$$
E_{\mathrm{trunc}}=H_S-H_{\mathrm{full}},
$$

and

$$
E_{\mathrm{total}}=H_S-H_{\mathrm{direct}}.
$$

The producer records the numerical defect in
$E_{\mathrm{total}}=E_{\mathrm{interp}}+E_{\mathrm{trunc}}$ but never replaces the
three channels by a sum of their maxima. Ordinary omitted-tail weights and norms are
computed from the complete matrix coefficients. Construction-mesh Parseval and
successive-tail monotonicity are separate diagnostics.

## Refinement rule

Blockwise and final-ledger refinement use the shared KSD
`ScalarRefinementAnalyzer`. For nonnegative coarse and fine values $q_c$ and $q_f$,

$$
\Delta=|q_f-q_c|,
\qquad
\Delta_{\mathrm{rel}}=
\frac{\Delta}{\max(|q_c|,|q_f|,d_{\min})},
$$

and the inclusive threshold is

$$
\tau=\tau_{\mathrm{abs}}+	au_{\mathrm{rel}}
\max(|q_c|,|q_f|).
$$

The signed margin is $\tau-\Delta$. Calculation records recompute these quantities from
the retained coarse and fine values rather than trusting supplied changes or margins.
