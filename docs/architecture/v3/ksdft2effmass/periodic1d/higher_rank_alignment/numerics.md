# Numerical formulation of higher-rank frame alignment

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
