# From spectral Hamiltonians to tight binding in two and three dimensions: isotropic locality on orthogonal and non-orthogonal lattices

> **Pre-results working manuscript.** This document defines the intended scientific
> argument and the evidence required to complete it. Bounded smoke diagnostics exist,
> but it reports no qualified 2-D, 3-D, or non-orthogonal scientific result.

## Abstract

Band eigenvalues do not determine a matrix-valued tight-binding representation or its
real-space locality. We formulate a multidimensional validation sequence that begins
with a finite cell--orbital Hamiltonian, converts it unitarily to complete Bloch and
spectral representations, selects a qualified retained subspace and periodic frame, and
then constructs its complete Wannier/tight-binding representation. The construction
makes explicit the state-space identifications required before Hamiltonian subtraction.
A Laurent-polynomial obstruction proves that spectral projection does not preserve
finite hopping support in general. For the orthogonal flat-parent master family, a
factorized Bessel identity proves that the irreducible restricted-alignment residual is
exactly the normalized Fourier weight outside the onsite block in both two and three
dimensions. A shell-resolved Jacobi--Anger formula and factorial bound certify the
orthogonal Fourier tail without fitting a decay law. Square and simple-cubic rank-two
systems provide the corresponding isotropic baselines.
Non-orthogonal but physically isotropic extensions replace coordinate-radius shells by
metric-complete lattice shells and replace axis permutations by the applicable lattice
point group. Gauge-covariant equivalence, restricted global alignment, cyclic Fourier
conversion, interpolation, deliberate hopping truncation, and total consequences are
reported as separate channels. Numerical results and cross-lattice conclusions remain
conditional on independently verified, dimension-specific calculations.

## I. Introduction

Paper 1 establishes that pointwise band equivalence does not determine hopping locality
under a fixed identification of retained coordinates. Paper 2 asks how that distinction
extends across spatial dimension and lattice geometry while the retained rank remains
two. The purpose is not to infer a Hamiltonian from eigenvalues alone. It is to compare
complete Hamiltonian representations connected by declared isometries and gauges, and
to quantify the representation cost introduced by a finite hopping support.

The gauge dependence and localization of Wannier representations are established
subjects, from analytic and exponential localization results [[1](#ref-kohn),
[2](#ref-brouder)] through practical maximally localized constructions and Wannier90
[[3](#ref-mostofi), [4](#ref-marzari)]. Compact support is a stronger algebraic property
and need not coincide with maximal localization [[5](#ref-sathe)]. Material-specific
Wannier and strained-Hamiltonian models likewise exist for graphene and other hexagonal
systems [[6](#ref-jung), [7](#ref-fang)], while environment-dependent Hamiltonian
mappings address geometry-responsive electronic structure [[8](#ref-zhang)]. The
present work does not claim any of those ingredients individually as new. Its narrower
target is a controlled separation of pointwise spectral equivalence, declared gauge
alignment, metric-complete truncation, and the physical hopping range needed at a fixed
tolerance.

The study separates two questions:

1. How are a finite cell--orbital operator, its Bloch representation, its complete
   eigensystem, a retained periodic frame, and its Wannier/TB blocks related?
2. After those spaces have been aligned, how does a restricted representation choice
   alter the hopping support required at the same sampled spectral accuracy?

The orthogonal square and simple-cubic systems are controlled baselines. Non-orthogonal
cases remain physically isotropic: their controls depend on the real-space metric and
complete point-group bond orbits rather than arbitrary coordinate labels. Direction-
dependent coupling laws belong to a later anisotropy study, while retained rank greater
than two belongs to Paper 3.

## II. Complete representation chain

For dimension $d\in\{2,3\}$ and finite periodic size $N$, define

$$
\mathcal L_N^{(d)}=(\mathbb C^N)^{\otimes d},\qquad
\mathcal H_{p,N}^{(d)}=\mathcal L_N^{(d)}\otimes\mathbb C^4,\qquad
\mathcal H_{r,N}^{(d)}=\mathcal L_N^{(d)}\otimes\mathbb C^2.
$$

Kronecker translation operators act on $\mathcal L_N^{(d)}$. They do not tensor the
four-dimensional orbital fiber. With $\mathsf S_{\alpha,N}$ denoting the translation on
axis $\alpha$, the orthogonal finite parent is

$$
\widehat K_{\rho,N}^{(d)}
=I_{N^d}\otimes T_0+
\frac{\rho}{d}\sum_{\alpha=1}^d
\left(\mathsf S_{\alpha,N}\otimes T_+
+\mathsf S_{\alpha,N}^\dagger\otimes T_-\right).
$$

The centered tensor Fourier transform $\mathcal F_{d,N}$ produces the complete Bloch
direct sum

$$
(\mathcal F_{d,N}\otimes I_4)\widehat K_{\rho,N}^{(d)}
(\mathcal F_{d,N}^\dagger\otimes I_4)
=\bigoplus_{\mathbf q}K_\rho^{(d)}(\mathbf q).
$$

For complete fiber eigensystems

$$
K(\mathbf q)=Q(\mathbf q)E(\mathbf q)Q^\dagger(\mathbf q),
$$

$E(\mathbf q)$ is a diagonal spectral representation only together with the eigenvector
map $Q(\mathbf q)$. An eigenvalue array without its state-space map is not an operator in
orbital coordinates and cannot be subtracted from a TB Hamiltonian.

A qualified periodic frame $F(\mathbf q):\mathbb C^2\to\mathbb C^4$ for the retained
projector defines

$$
H(\mathbf q)=F^\dagger(\mathbf q)K(\mathbf q)F(\mathbf q).
$$

The inverse tensor Fourier transform of $\bigoplus_{\mathbf q}H(\mathbf q)$ gives the
complete retained Wannier/TB operator. Its block-circulant entries are the finite Fourier
hopping blocks $T_{\mathbf R}^{(N)}$.

### Spectral projection is not finite-range compression

For a spectral projector $P_I$ with isometry $V_I$, the embedded retained operator is
$V_I(V_I^\dagger H V_I)V_I^\dagger=P_IHP_I$. It preserves the selected eigenpairs but
need not preserve finite hopping support. The following elementary example makes that
statement exact.

**Proposition (spectral projection can destroy finite hopping support).** Let

$$
H(k)=\begin{pmatrix}\Delta&t(1+e^{-ik})\\t(1+e^{ik})&-\Delta\end{pmatrix},
\qquad \Delta t\ne0.
$$

Then $H$ has nearest-neighbor Fourier support and eigenvalues $E_\pm(k)=\pm d(k)$,
where

$$
d(k)=\sqrt{\Delta^2+4t^2\cos^2(k/2)}.
$$

The embedded lower-band operator

$$
P_-(k)H(k)P_-(k)=\tfrac12[H(k)-d(k)I]
$$

is not a matrix-valued finite Fourier polynomial.

*Proof.* Set $z=e^{ik}$. If $d(k)$ were a finite Fourier polynomial, there would be a
Laurent polynomial $f(z)$ whose restriction to the unit circle equals $d(k)$. Squaring
on the unit circle and using equality on infinitely many points would give

$$
f(z)^2=\Delta^2+2t^2+t^2(z+z^{-1}).
$$

If $m$ and $n$ are the smallest and largest exponents with nonzero coefficients in
$f$, then the extreme exponents in $f^2$ are $2m$ and $2n$. Their coefficients cannot
cancel because each is the square of an extreme coefficient. For $t\ne0$, the right-hand
side has extreme exponents $-1$ and $1$, which is impossible because $2m$ and $2n$ are
even. Thus $d$ is not a finite Fourier polynomial. The diagonal entries of
$[H(k)-d(k)I]/2$ contain $-d(k)/2$ plus finite Fourier terms, so the embedded projected
operator is not finite range. $\square$

The condition $\Delta\ne0$ keeps the two bands separated. The proposition does not
claim that every spectral projection of every finite-range parent is long ranged; it
shows that finite support is not preserved as an operation. Projection, frame selection,
Fourier conversion, hopping truncation, and model-class restriction are therefore
distinct operations.

## III. Orthogonal isotropic baselines

The square and simple-cubic baselines use

$$
K_\rho^{(d)}(\mathbf q)=T_0+\frac{\rho}{d}
\sum_{\alpha=1}^d
\left(e^{2\pi iq_\alpha}T_+
+e^{-2\pi iq_\alpha}T_-\right)
$$

and the retained-space rotation

$$
U_a^{(d)}(\mathbf q)=R\!\left[
\frac{a}{d}\sum_{\alpha=1}^d\sin(2\pi q_\alpha)
\right].
$$

The flat-parent correlations are $J_0(a)^2$ in two dimensions and
$J_0(2a/3)^3$ in three dimensions. The next theorem proves these formulas and their
exact real-space meaning. They are continuum analytic comparators and do not replace
finite-mesh correlations. Square and cubic truncations retain every attainable metric
shell through the declared cap using complete signed-permutation orbits.

### Flat-parent residual--locality theorem

Throughout, $E_{\mathrm{ref}}>0$ is an arbitrary reference-energy normalization, not a
band gap. Give $\mathbb T^d=[-1/2,1/2)^d$ normalized Lebesgue measure. Let
$D\in\mathbb R^{2\times2}$ be nonzero, symmetric, and traceless, and let the flat
retained parent be $H(\mathbf q)=\bar E I_2+D$. Define

$$
\begin{aligned}
B_a^{(d)}(\mathbf q)
 &=U_a^{(d)}(\mathbf q)^\dagger D U_a^{(d)}(\mathbf q),\\
B_{\mathbf R}^{(d)}
 &=\int_{\mathbb T^d}e^{-2\pi i\mathbf q\cdot\mathbf R}
 B_a^{(d)}(\mathbf q)\,d\mathbf q,
 \qquad \mathbf R\in\mathbb Z^d,\\
\kappa&=\frac{\lVert D\rVert_F^2}{2E_{\mathrm{ref}}^2}.
\end{aligned}
$$

For one momentum-independent real rotation $R(\phi)$, centroid shift $s$, and the
nonnegative closure $\lambda\ge0$ of the splitting-scale domain, define

$$
L_{\mathrm{op},\phi}^2(s,\lambda)
=\frac{1}{2E_{\mathrm{ref}}^2}\int_{\mathbb T^d}
\left\lVert sE_{\mathrm{ref}}I_2+\lambda R(\phi)^\dagger D R(\phi)
-B_a^{(d)}(\mathbf q)\right\rVert_F^2\,d\mathbf q.
$$

The normalized best global-rotation correlation is

$$
\mu_{\max}^{(d)}(a)=
\max_{\phi\in\mathbb R}
\frac{1}{\lVert D\rVert_F^2}
\int_{\mathbb T^d}\operatorname{tr}\!\left[
R(\phi)^\dagger D R(\phi)B_a^{(d)}(\mathbf q)
\right]d\mathbf q.
$$

**Theorem (multidimensional flat-parent residual--locality identity).** For
$d\in\{2,3\}$ and $0\le a\le\pi/4$, set

$$
c_d(a)=J_0\!\left(\frac{2a}{d}\right)^d.
$$

Then $c_d(a)>0$ and

$$
\int_{\mathbb T^d}e^{2i\theta_a^{(d)}(\mathbf q)}\,d\mathbf q=c_d(a),
\qquad
B_{\mathbf0}^{(d)}=c_d(a)D.
$$

The best global-rotation correlation is
$\mu_{\max}^{(d)}(a)=c_d(a)$, and the exact restricted-alignment residual satisfies

$$
\begin{aligned}
\inf_{s\in\mathbb R,\,\lambda\ge0,\,\phi\in\mathbb R}
L_{\mathrm{op},\phi}^2(s,\lambda)
&=\kappa\left[1-c_d(a)^2\right]\\
&=\frac{1}{2E_{\mathrm{ref}}^2}
\sum_{\mathbf R\ne\mathbf0}\left\lVert B_{\mathbf R}^{(d)}\right\rVert_F^2.
\end{aligned}
$$

If exact spectral agreement additionally fixes $s=0$ and $\lambda=1$, then

$$
\inf_{\phi\in\mathbb R}L_{\mathrm{op},\phi}^2(0,1)
=2\kappa\left[1-c_d(a)\right].
$$

Thus $c_2(a)=J_0(a)^2$ and $c_3(a)=J_0(2a/3)^3$.

*Proof.* A constant real rotation diagonalizes $D$ without changing any Frobenius norm,
Fourier weight, or minimization in the statement, so take $D=\delta\sigma_z$ with
$\delta\ne0$. Conjugation through a real rotation gives

$$
B_a^{(d)}(\mathbf q)=\delta\left[
\cos\!\left(2\theta_a^{(d)}(\mathbf q)\right)\sigma_z
-\sin\!\left(2\theta_a^{(d)}(\mathbf q)\right)\sigma_x
\right].
$$

Using the normalized integral representation

$$
J_0(x)=\int_{-1/2}^{1/2}e^{ix\sin(2\pi q)}\,dq
$$

and the product structure of $\mathbb T^d$,

$$
\begin{aligned}
\int_{\mathbb T^d}e^{2i\theta_a^{(d)}(\mathbf q)}\,d\mathbf q
&=\prod_{\alpha=1}^d\int_{-1/2}^{1/2}
 e^{i(2a/d)\sin(2\pi q_\alpha)}\,dq_\alpha\\
&=J_0\!\left(\frac{2a}{d}\right)^d=c_d(a).
\end{aligned}
$$

Global inversion $\mathbf q\mapsto-\mathbf q$ makes the sine average vanish, so
$B_{\mathbf0}^{(d)}=c_d(a)D$. Moreover, $0\le2a/d\le\pi/4$, and the real part of the
integrand defining $J_0(2a/d)$ is at least $\cos(2a/d)>0$; hence $c_d(a)>0$.

For any constant matrix $C$, the zero-mean property of
$B_a^{(d)}-B_{\mathbf0}^{(d)}$ gives

$$
\int_{\mathbb T^d}\left\lVert C-B_a^{(d)}(\mathbf q)\right\rVert_F^2\,d\mathbf q
=\int_{\mathbb T^d}\left\lVert B_a^{(d)}(\mathbf q)-B_{\mathbf0}^{(d)}\right\rVert_F^2\,d\mathbf q
+\left\lVert C-B_{\mathbf0}^{(d)}\right\rVert_F^2.
$$

The constant $B_{\mathbf0}^{(d)}=c_d(a)D$ belongs to the allowed family: choose $s=0$,
$\lambda=c_d(a)$, and $\phi=0$. It is therefore the best constant restricted alignment,
and the normalized maximum correlation is $c_d(a)$.

Parseval's identity applied entrywise gives

$$
\int_{\mathbb T^d}\left\lVert B_a^{(d)}-B_{\mathbf0}^{(d)}\right\rVert_F^2
=\sum_{\mathbf R\ne\mathbf0}\left\lVert B_{\mathbf R}^{(d)}\right\rVert_F^2.
$$

Pointwise unitary invariance gives
$\lVert B_a^{(d)}(\mathbf q)\rVert_F=\lVert D\rVert_F$. A second use of Parseval then
yields

$$
\sum_{\mathbf R\ne\mathbf0}\left\lVert B_{\mathbf R}^{(d)}\right\rVert_F^2
=\lVert D\rVert_F^2-\left\lVert B_{\mathbf0}^{(d)}\right\rVert_F^2
=\lVert D\rVert_F^2[1-c_d(a)^2].
$$

Division by $2E_{\mathrm{ref}}^2$ proves the residual--tail identity. Finally, fixing $s=0$ and
$\lambda=1$ leaves the non-onsite weight plus the onsite mismatch,

$$
\begin{aligned}
\inf_\phi L_{\mathrm{op},\phi}^2(0,1)
&=\kappa[1-c_d(a)^2]+\kappa[1-c_d(a)]^2\\
&=2\kappa[1-c_d(a)].
\end{aligned}
$$

This proves the theorem. $\square$

**Theorem (shell-resolved coefficients and factorial Fourier-tail bound).** Use the
constant real rotation from the preceding proof so that $D=\delta\sigma_z$, and set

$$
z=\frac{2a}{d},\qquad
j_{\mathbf R}(z)=\prod_{\alpha=1}^dJ_{R_\alpha}(z),\qquad
p(\mathbf R)=\sum_{\alpha=1}^dR_\alpha\pmod 2.
$$

Every Fourier block is then known exactly:

$$
B_{\mathbf R}^{(d)}=\delta j_{\mathbf R}(z)
\begin{cases}
\sigma_z,&p(\mathbf R)=0,\\
i\sigma_x,&p(\mathbf R)=1.
\end{cases}
$$

For each complete squared-radius shell $s\in\mathbb N_0$, define

$$
W_{d,s}(z)=
\sum_{\substack{\mathbf R\in\mathbb Z^d\\\lVert\mathbf R\rVert_2^2=s}}
\prod_{\alpha=1}^dJ_{R_\alpha}(z)^2.
$$

Its normalized hopping-block power and the total shell inventory obey

$$
\frac{1}{2E_{\mathrm{ref}}^2}
\sum_{\lVert\mathbf R\rVert_2^2=s}\lVert B_{\mathbf R}^{(d)}\rVert_F^2
=\kappa W_{d,s}(z),
\qquad
\sum_{s=0}^{\infty}W_{d,s}(z)=1.
$$

For integer shell cap $S\ge0$, let

$$
L=\left\lfloor\sqrt{\frac{S}{d}}\right\rfloor+1,
\qquad x=\frac{|z|}{2}.
$$

Whenever $x<L+1$, the omitted normalized power satisfies the rigorous bound

$$
\frac{1}{2E_{\mathrm{ref}}^2}
\sum_{\lVert\mathbf R\rVert_2^2>S}\lVert B_{\mathbf R}^{(d)}\rVert_F^2
\le
\kappa\frac{2d\,e^{z^2/2}x^{2L}}
{(L!)^2[1-x^2/(L+1)^2]}.
$$

Thus this orthogonal Fourier tail is certified directly from $a$, $d$, and $S$, without
fitting a decay law.

*Proof.* Jacobi--Anger factorization gives

$$
e^{2i\theta_a^{(d)}(\mathbf q)}
=\sum_{\mathbf R\in\mathbb Z^d}
 j_{\mathbf R}(z)e^{2\pi i\mathbf q\cdot\mathbf R}.
$$

Since $J_{-n}(z)=(-1)^nJ_n(z)$, even parity supplies the cosine/$\sigma_z$
coefficient and odd parity supplies the sine/$i\sigma_x$ coefficient. Both Pauli
matrices have squared Frobenius norm two, so

$$
\lVert B_{\mathbf R}^{(d)}\rVert_F^2
=\lVert D\rVert_F^2\prod_{\alpha=1}^dJ_{R_\alpha}(z)^2.
$$

Grouping complete shells proves the shell-power identity. Parseval applied to
$e^{iz\sin(2\pi q)}$ gives $\sum_{n\in\mathbb Z}J_n(z)^2=1$, and its $d$-fold product
proves the shell partition.

If $\lVert\mathbf R\rVert_2^2>S$, some $|R_\alpha|\ge L$. Hence a union bound gives

$$
\sum_{\lVert\mathbf R\rVert_2^2>S}
\prod_{\alpha=1}^dJ_{R_\alpha}(z)^2
\le2d\sum_{n=L}^{\infty}|J_n(z)|^2.
$$

The defining Bessel series implies
$|J_n(z)|\le e^{x^2}x^n/n!$. Also
$(L+m)!\ge L!(L+1)^m$, so

$$
\sum_{n=L}^{\infty}\frac{x^{2n}}{(n!)^2}
\le\frac{x^{2L}}{(L!)^2[1-x^2/(L+1)^2]}.
$$

Combining these inequalities with $e^{2x^2}=e^{z^2/2}$ proves the tail bound.
$\square$

**Corollary (monotonicity and the small-amplitude dimension law).** Define

$$
\tau_{\min,d}^2(a)=\kappa[1-c_d(a)^2],
\qquad
\tau_{\mathrm{exact},d}^2(a)=2\kappa[1-c_d(a)].
$$

Both thresholds are strictly increasing for $0<a\le\pi/4$. As $a\to0$,

$$
\begin{aligned}
c_d(a)
&=1-\frac{a^2}{d}+\frac{2d-1}{4d^3}a^4+O(a^6),\\
\tau_{\min,d}^2(a)
&=\frac{2\kappa}{d}a^2
-\frac{\kappa(4d-1)}{2d^3}a^4+O(a^6),\\
\tau_{\mathrm{exact},d}^2(a)
&=\frac{2\kappa}{d}a^2
-\frac{\kappa(2d-1)}{2d^3}a^4+O(a^6).
\end{aligned}
$$

Thus both thresholds have leading slope $\sqrt{2\kappa/d}$ with respect to the maximum
rotation amplitude $a$.

*Proof.* For $x>0$, $J_0'(x)=-J_1(x)$. On $0<x\le\pi/4$, the alternating series

$$
J_1(x)=\sum_{m=0}^{\infty}
\frac{(-1)^m}{m!(m+1)!}\left(\frac{x}{2}\right)^{2m+1}
$$

has strictly decreasing term magnitudes because their successive ratio is at most
$\pi^2/128<1$. Hence $J_1(x)>0$. Positivity of $J_0(2a/d)$ and

$$
c_d'(a)=-2J_0(2a/d)^{d-1}J_1(2a/d)<0
$$

prove strict threshold monotonicity. Finally,
$J_0(x)=1-x^2/4+x^4/64+O(x^6)$. Substitution of $x=2a/d$ and direct expansion prove the
three asymptotic formulas. $\square$

The two theorems and corollary apply to the orthogonal flat-parent master family. The
factorial bound certifies its complete-shell Fourier tail, but it must not be transferred
to a dependent non-orthogonal bond orbit. The bond-orbit theorem below supplies that
comparator's analytic form; a lattice-specific constrained-series tail still requires a
separate certificate.

The orthogonal calculations belong to separate publication-independent 2-D and 3-D
experiment families. Their mesh sizes, shell caps, tolerances, convergence outcomes, and
evidence identities are not shared merely because this paper compares them.

### Extracted two-dimensional precursor evidence

An earlier retained scalar calculation used

$$
\widehat H_{2\mathrm D}=-\nabla^2+0.5\cos x+0.5\cos y
+\lambda_{xy}\cos x\cos y.
$$

At $\lambda_{xy}=0$, its represented Kronecker-sum discrepancy was zero and its
product-spectrum discrepancy was $3.55\times10^{-14}E_{\mathrm{ref}}$. At $\lambda_{xy}=0.30$, the
mixed-direction hopping norm was $1.94\times10^{-3}E_{\mathrm{ref}}$, compared with a
$3.00\times10^{-15}E_{\mathrm{ref}}$ floor at zero coupling. The withheld RMS interpolation error at
the strongest retained coupling decreased from $5.75\times10^{-2}E_{\mathrm{ref}}$ for the onsite
shell to $1.70\times10^{-6}E_{\mathrm{ref}}$ for the complete finite transform. The latter
reconstructed its $15\times15$ construction mesh within $1.11\times10^{-15}E_{\mathrm{ref}}$ while
retaining nonzero error on an independent $31\times31$ mesh.

These historical finite-mesh values are not results of the new rank-two square-lattice
protocol and do not establish a 3-D or non-orthogonal outcome.

## IV. Non-orthogonal but physically isotropic extension

Let the direct-lattice basis be the columns of $A$ and let

$$
G=A^{\mathsf T}A
$$

be its metric in reduced lattice coordinates. The reciprocal basis is
$B=2\pi A^{-\mathsf T}$. For $\mathbf R\in\mathbb Z^d$, physical squared distance is

$$
r_G^2(\mathbf R)=\mathbf R^{\mathsf T}G\mathbf R.
$$

Consequently, Euclidean coordinate radii such as $R_x^2+R_y^2$ are not used for a
non-orthogonal cell unless they equal the declared physical metric. The integer lattice
point group is

$$
\Gamma_G=\{M\in GL(d,\mathbb Z):M^{\mathsf T}GM=G\}.
$$

An isotropic hopping inventory retains complete $\Gamma_G$ orbits and every attainable
metric shell through its cap. Equal coefficients are required only when imposed by the
model's point-group representation; support symmetry alone does not imply coefficient
equality.

A selected non-orthogonal parent must declare an inversion-complete, point-group-complete
bond orbit $\mathcal B$. A possible dimension-normalized form is

$$
K_{\rho,G}(\mathbf q)=T_0+
\frac{\rho}{|\mathcal B_+|}
\sum_{\mathbf b\in\mathcal B_+}
\left(e^{2\pi i\mathbf q\cdot\mathbf b}T_{\mathbf b}
+e^{-2\pi i\mathbf q\cdot\mathbf b}T_{\mathbf b}^\dagger\right),
$$

subject to the selected internal point-group representation. The associated smooth
rotation must likewise be built from a complete bond orbit rather than from privileged
coordinate axes.

### Bond-orbit analytic comparator

Let the chosen positive bond inventory be
$\mathcal B_+=\{\mathbf b_1,\ldots,\mathbf b_m\}\subset\mathbb Z^d\setminus\{\mathbf0\}$.
For real orbit weights $\eta_j$, set $W=\sum_j|\eta_j|>0$ and define

$$
\theta_{a,\mathcal B}(\mathbf q)
=\frac{a}{W}\sum_{j=1}^m\eta_j
\sin(2\pi\mathbf q\cdot\mathbf b_j),
\qquad |\theta_{a,\mathcal B}(\mathbf q)|\le a.
$$

The weights must be fixed by the selected symmetry contract; the theorem does not by
itself declare them isotropic.

**Theorem (bond-orbit flat-parent comparator).** For $0\le a\le\pi/4$, define

$$
c_{\mathcal B,\boldsymbol\eta}(a)
=\int_{\mathbb T^d}e^{2i\theta_{a,\mathcal B}(\mathbf q)}\,d\mathbf q.
$$

Then $c_{\mathcal B,\boldsymbol\eta}(a)$ is real and strictly positive. If

$$
\begin{aligned}
D_{a,\mathcal B}(\mathbf q)
&=R(\theta_{a,\mathcal B}(\mathbf q))^\dagger
D R(\theta_{a,\mathcal B}(\mathbf q)),\\
D_{\mathbf R}^{\mathcal B}
&=\int_{\mathbb T^d}e^{-2\pi i\mathbf q\cdot\mathbf R}
D_{a,\mathcal B}(\mathbf q)\,d\mathbf q,
\end{aligned}
$$

then

$$
\begin{aligned}
D_{\mathbf0}^{\mathcal B}
&=c_{\mathcal B,\boldsymbol\eta}(a)D,\\
\inf_{s,\lambda\ge0,\phi}L_{\mathcal B,\phi}^2(s,\lambda)
&=\kappa[1-c_{\mathcal B,\boldsymbol\eta}(a)^2]\\
&=\frac{1}{2E_{\mathrm{ref}}^2}\sum_{\mathbf R\ne\mathbf0}
\left\lVert D_{\mathbf R}^{\mathcal B}\right\rVert_F^2,\\
\inf_\phi L_{\mathcal B,\phi}^2(0,1)
&=2\kappa[1-c_{\mathcal B,\boldsymbol\eta}(a)].
\end{aligned}
$$

Here $L_{\mathcal B,\phi}$ is the flat-parent operator loss with
$B_a^{(d)}$ replaced by $D_{a,\mathcal B}$. Moreover,

$$
c_{\mathcal B,\boldsymbol\eta}(a)
=\sum_{\substack{\mathbf n\in\mathbb Z^m\\
\sum_{j=1}^m n_j\mathbf b_j=\mathbf0}}
\prod_{j=1}^m J_{n_j}\!\left(\frac{2a\eta_j}{W}\right).
$$

If the bond vectors have no nontrivial integer relation, this reduces to

$$
c_{\mathcal B,\boldsymbol\eta}(a)
=\prod_{j=1}^mJ_0\!\left(\frac{2a\eta_j}{W}\right).
$$

*Proof.* The bond-orbit phase is odd under $\mathbf q\mapsto-\mathbf q$, so the imaginary
part of its exponential integrates to zero. Since
$|2\theta_{a,\mathcal B}|\le\pi/2$, its cosine is nonnegative and is positive near
$\mathbf q=\mathbf0$. Thus the correlation is strictly positive. Diagonalizing $D$ by
one constant rotation gives
$D_{\mathbf0}^{\mathcal B}=c_{\mathcal B,\boldsymbol\eta}D$. The constant-projection
identity and entrywise Parseval then prove the residual formulas as in the orthogonal
theorem.

For the explicit comparator, apply Jacobi--Anger to every bond harmonic:

$$
e^{i(2a\eta_j/W)\sin(2\pi\mathbf q\cdot\mathbf b_j)}
=\sum_{n_j\in\mathbb Z}
J_{n_j}\!\left(\frac{2a\eta_j}{W}\right)
e^{2\pi i n_j\mathbf q\cdot\mathbf b_j}.
$$

Multiply the absolutely convergent series and integrate termwise. Torus orthogonality
retains exactly the tuples satisfying
$\sum_jn_j\mathbf b_j=\mathbf0$. If the integer kernel is trivial, only
$\mathbf n=\mathbf0$ remains. $\square$

**Theorem (constrained-series complete-shell tail certificate).** Define the scalar
Fourier coefficient

$$
g_{\mathbf R}=
\sum_{\substack{\mathbf n\in\mathbb Z^m\\
\sum_jn_j\mathbf b_j=\mathbf R}}
\prod_{j=1}^mJ_{n_j}\!\left(\frac{2a\eta_j}{W}\right).
$$

In the constant basis where $D=\delta\sigma_z$,

$$
D_{\mathbf R}^{\mathcal B}
=\frac{\delta}{2}\left[
(g_{\mathbf R}+g_{-\mathbf R})\sigma_z
+i(g_{\mathbf R}-g_{-\mathbf R})\sigma_x
\right].
$$

Let $\mathcal S_S$ contain every displacement in the complete physical-metric shells
through $S$. If finite constrained sums $\widetilde g_{\mathbf R}$ satisfy
$|g_{\mathbf R}-\widetilde g_{\mathbf R}|\le\epsilon_{\mathbf R}$ on
$\mathcal S_S$, then

$$
\frac{1}{2E_{\mathrm{ref}}^2}
\sum_{\mathbf R\notin\mathcal S_S}\lVert D_{\mathbf R}^{\mathcal B}\rVert_F^2
\le\kappa\left\{1-
\sum_{\mathbf R\in\mathcal S_S}
[\max\{0,|\widetilde g_{\mathbf R}|-\epsilon_{\mathbf R}\}]^2
\right\}.
$$

For the equal-weight triangular orbit, with $z=2a/3$,

$$
g_{(r_1,r_2)}=
\sum_{\ell\in\mathbb Z}
J_{r_1-\ell}(z)J_{r_2+\ell}(z)J_\ell(z).
$$

For the equal-weight six-bond FCC orbit, with $z=2a/6$,

$$
\begin{aligned}
g_{(r_1,r_2,r_3)}=\sum_{u,v,w\in\mathbb Z}
&J_{r_1+u+v}(z)J_{r_2-u+w}(z)J_{r_3-v-w}(z)\\
&\times J_u(z)J_v(z)J_w(z).
\end{aligned}
$$

Set $x=|z|/2$ and

$$
A_0(z)=e^{x^2}(2e^x-1),\qquad
A_K(z)=\frac{2e^{x^2}x^{K+1}}{(K+1)![1-x/(K+2)]}.
$$

Truncation to $|\ell|\le K$ has
$\epsilon_{\mathbf R}=A_K(z)$; truncation to
$|u|,|v|,|w|\le K$ has
$\epsilon_{\mathbf R}=3A_K(z)A_0(z)^2$.

*Proof.* Jacobi--Anger expansion gives the constrained coefficient. Inversion symmetry
makes it real. Splitting its cosine and sine parts proves the matrix-block formula, and

$$
\frac{\lVert D_{\mathbf R}^{\mathcal B}\rVert_F^2}{\lVert D\rVert_F^2}
=\frac{g_{\mathbf R}^2+g_{-\mathbf R}^2}{2}.
$$

Parseval gives $\sum_{\mathbf R}g_{\mathbf R}^2=1$; inversion completeness and the
reverse triangle inequality then prove the certificate. Solving the triangular kernel
gives $(n_1,n_2,n_3)=(r_1-\ell,r_2+\ell,\ell)$. Taking
$(u,v,w)=(n_4,n_5,n_6)$ solves the FCC kernel. Finally,
$|J_n(z)|\le e^{x^2}x^{|n|}/|n|!$ gives $A_0$ and $A_K$; a union bound over the three
FCC kernel indices gives $3A_KA_0^2$. $\square$

At $a=\pi/4$, bounded binary64 evaluations with a declared $10^{-13}$
per-coefficient numerical margin give normalized scalar-tail upper bounds
$2.8760\times10^{-9}$ for triangular shell cap $S=21$ at $K=10$, and
$5.5358\times10^{-6}$ for FCC shell cap $S=7$ at $K=9$. These evaluate the proved
certificate but are not formal interval results, convergence evidence, or material
claims.

The metric and point group select the physically admissible complete bond orbit; the
integer relations among the selected reduced-coordinate bond vectors determine whether
the comparator factorizes. Thus the square and cubic products arise from independent
primitive-axis harmonics, whereas an orbit with integer dependencies generally has the
constrained Bessel sum above.

Separate non-orthogonal families now select a graphene-inspired triangular/honeycomb
2-D parent and a silicon-inspired FCC/diamond 3-D parent, together with matched Bravais-
control pairs at equal reciprocal-torus RMS gauge amplitude. “Inspired” denotes only the
declared Bravais geometry, two-site basis, and bipartite connectivity; neither parent is
a material parametrization. The dependent triangular and FCC control orbits give
respectively a one-index and a three-index constrained Bessel sum under the bond-orbit
and constrained-tail theorems. Bounded Monkhorst--Pack development actions and
independent development verifiers now exist for all four 2-D/3-D families. The
constrained-series certificate is evaluated at the development caps, but qualified shell
caps, full mesh ladders, control-parent gap certification, formal interval evaluation,
final tolerances and schemas, and frozen revisions remain open. The square and cubic
products must not be
transferred unchanged to these dependent bond orbits.

> **Prospective synthetic-deformation extension.** A publication-independent protocol
> now specifies frozen-gauge controls along a unit-area rhombic triangular--square
> deformation and a unit-volume FCC--BCC Bain path. The latter uses the crystallographic
> deformation associated with Bain's classic martensite construction [[9](#ref-bain)],
> but freezes the reduced-coordinate Hamiltonian and is therefore only a synthetic
> geometry stress test. It is not a phase-stability, elastic, or material prediction.
> Strain-responsive hopping laws, including material-specific and environment-dependent
> models represented by [[7](#ref-fang), [8](#ref-zhang)], are separate robustness
> controls rather than corrections to the frozen-gauge result.

## V. Aligned Hamiltonian subtraction

For the block gauge $\mathcal U=\bigoplus_{\mathbf q}U(\mathbf q)$,

$$
\widehat A_B=\mathcal U^\dagger\widehat H_B\mathcal U.
$$

The corresponding Wannier-space unitary

$$
\mathcal G_W=(\mathcal F_{d,N}^\dagger\otimes I_2)
\mathcal U(\mathcal F_{d,N}\otimes I_2)
$$

is generally nonlocal, and

$$
\widehat A_W=\mathcal G_W^\dagger\widehat H_W\mathcal G_W.
$$

This covariantly aligned subtraction vanishes by construction. The restricted scientific
comparison replaces $\mathcal G_W$ by one cell-local global rotation
$I_{N^d}\otimes R(\phi)$. Parent-space comparison requires the retained projector and an
explicit lift. Every reported subtraction must state its source and target spaces,
basis, gauge, energy reference, units, geometry, and normalization.

## VI. Error and evidence ledger

The calculations report the following channels separately:

1. parent--retained reconstruction after projector lifting;
2. covariant representation equivalence;
3. restricted global-alignment residual;
4. cyclic Nyquist conversion power;
5. finite interpolation error;
6. deliberate truncation error; and
7. total reconstructed-Hamiltonian and spectral consequences.

Writing $H^{\mathrm{dir}}$ for the direct withheld-mesh field,
$H_N^{\mathrm{ord}}$ for the full ordinary Fourier interpolant, and
$H_{N,R}^{\mathrm{ord}}$ for its complete-radius truncation, the three approximation
channels are

$$
\begin{aligned}
\mathcal E_{\mathrm{interp}}&=\mathcal E(H_N^{\mathrm{ord}},H^{\mathrm{dir}}),\\
\mathcal E_{\mathrm{trunc}}&=\mathcal E(H_{N,R}^{\mathrm{ord}},H_N^{\mathrm{ord}}),\\
\mathcal E_{\mathrm{total}}&=\mathcal E(H_{N,R}^{\mathrm{ord}},H^{\mathrm{dir}}).
\end{aligned}
$$

Here $\mathcal E$ is reported independently as maximum/RMS normalized Frobenius error
and maximum/RMS sorted-band error. These channels are not assumed additive because
interpolation and truncation may reinforce or cancel. Omitted hopping-block power is a
locality diagnostic, not a universal spectral-error bound. First-passing support
decisions are sampled decisions and use hatted notation. For a future strain-responsive
perturbation, the same decomposition must be applied to the gauge-aligned difference
field $\Delta H_s$ after constructing it in one common state space. The M0 strain plots
report Fourier-tail locality only and are not a three-channel strain-potential
calculation; the separately labeled M1/M2 smoke controls repeat the three channels
without upgrading their evidence status. Each dimensional or lattice realization
requires its own convergence and independent verification.

Calculation parity with Paper 1 requires every applicable predecessor diagnostic, not
only the three error channels. In particular, numerical alignment must report the
splitting scale and finite-mesh maximum correlation, minimize over one global rotation
*and* the positive splitting scale for the minimum operator threshold, and report the
distinct unit-splitting exact-spectrum joint threshold. A fixed-unit-scale rotation fit
cannot substitute for those two Paper 1 quantities. The complete predecessor catalog
also requires frame/sewing, locality-power, Weyl, first-passing-context, refinement, and
provenance counterparts in every family.

## VII. Results

Replaceable bounded development records exercise a partial numerical channel sequence
from square lattice through the silicon-inspired diamond target. A strict Paper 1
catalog audit initially found missing or incompletely serialized predecessor channels.
The regenerated records now map all 110 predecessor quantities as implemented,
explicitly unresolved, explicitly inapplicable, or multidimensional-partial, including
the corrected positive-splitting alignment and analytic amplitude-resolution ladder.
Row-level parity verification and scalar closure-phase aggregation remain open and still
preclude quantitative scientific use. The sparse actions use three construction levels: $16^2$, $32^2$, and $64^2$ in 2-D and $8^3$,
$16^3$, and $32^3$ in 3-D, with separately shifted evaluation meshes and unchanged
models, thresholds, and shell caps. All development verifiers pass with stored identity
defects below $2.0\times10^{-14}$; this envelope now includes the newly serialized
transport and closure-unitarity channels. One of the 18 graphene-family pointwise first-passing
decision sets moves by one shell between the first two levels, while every decision is
unchanged on the final refinement in all four families. Several strict decisions remain
unresolved at the deliberately small shell caps. These records establish software and
bookkeeping behavior only; row-level Paper 1 parity verification, frozen tolerances, and
cap policy remain open, so the three mesh levels do not yet populate the paper's qualified
scientific results. The following figures show the four distinct
model-family development summaries. They must not be read as four strain-responsive
models.

![Replaceable square-lattice family development summary.](../../../../../experiments/model-adequacy/periodic2d/band-equivalence-versus-hopping-locality/analysis/band-equivalence-locality-scientific-story.png)

*Square-lattice family. Withheld interpolation, external retained-subspace isolation,
hopping-tail power, withheld spectral consequence, and tail-power/consequence
comparison remain separate channels.*

![Replaceable graphene-inspired family development summary.](../../../../../experiments/model-adequacy/periodic2d_nonorthog/band-equivalence-versus-hopping-locality/analysis/band-equivalence-locality-scientific-story.png)

*Graphene-inspired family and matched Bravais controls. “Inspired” denotes geometry and
connectivity only, not a graphene parametrization or validation result.*

![Replaceable simple-cubic family development summary.](../../../../../experiments/model-adequacy/periodic3d/band-equivalence-versus-hopping-locality/analysis/band-equivalence-locality-scientific-story.png)

*Simple-cubic family. The two displayed mesh levels establish software behavior only,
not convergence.*

![Replaceable silicon-inspired family development summary.](../../../../../experiments/model-adequacy/periodic3d_nonorthog/band-equivalence-versus-hopping-locality/analysis/band-equivalence-locality-scientific-story.png)

*Silicon-inspired family and matched Bravais controls. “Inspired” denotes geometry and
connectivity only, not a silicon parametrization, material calculation, or Paper 4
substitute.*

The following refined-mesh figures show interpolation, deliberate-truncation, and total
errors separately. Near overlap of the latter two curves means interpolation is much
smaller at these sampled points; it does not make the channels definitionally identical.

![Square-lattice three-channel error decomposition.](../../../../../experiments/model-adequacy/periodic2d/band-equivalence-versus-hopping-locality/analysis/three-channel-error-decomposition.png)

![Graphene-inspired-family three-channel error decomposition.](../../../../../experiments/model-adequacy/periodic2d_nonorthog/band-equivalence-versus-hopping-locality/analysis/three-channel-error-decomposition.png)

![Simple-cubic three-channel error decomposition.](../../../../../experiments/model-adequacy/periodic3d/band-equivalence-versus-hopping-locality/analysis/three-channel-error-decomposition.png)

![Silicon-inspired-family three-channel error decomposition.](../../../../../experiments/model-adequacy/periodic3d_nonorthog/band-equivalence-versus-hopping-locality/analysis/three-channel-error-decomposition.png)

**Bounded M0 observation.** Separate frozen-parent geometry-stress diagnostics use nine
unit-area rhombic and unit-volume Bain metrics. The reduced-coordinate Hamiltonian,
gauge, Fourier-block weights, and restricted-alignment residual are invariant by
construction. Nevertheless, the changing physical metric reorders complete hopping
shells and changes the sampled first-passing physical radius and retained block count.
At tail-power tolerance $10^{-5}$, the endpoint radius changes from $3.7224$ to
$4.2426$ in 2-D and from $2.9698$ to $3.2734$ in 3-D; the corresponding block counts
change from 43 to 61 and from 135 to 169. At the looser 3-D tolerance $10^{-3}$, the
endpoint radius instead changes from $2.2449$ to $2.1822$ while the block count changes
from 55 to 59. Physical range and parameter count are therefore distinct locality costs
even when the abstract reduced-coordinate operator is unchanged. A unimodular map
identifies the existing FCC primitive coordinates with the Bain endpoint coordinates.

![Replaceable 2-D frozen-gauge M0 development diagnostic. The panels separate bond-orbit splitting, invariant restricted residual, first-passing physical radius, and retained block count.](../../../../../experiments/model-adequacy/periodic2d/gauge-locality-under-synthetic-strain/analysis/development/gauge-locality-under-synthetic-strain.png)

*Replaceable 2-D frozen-gauge M0 development diagnostic. The parent, gauge, Fourier
weights, and unit cell area remain fixed while the rhombic metric moves from triangular
to square. Tail-power thresholds are locality diagnostics, not universal spectral-error
bounds.*

![Replaceable 3-D frozen-gauge M0 development diagnostic along the unit-volume FCC--BCC Bain metric path.](../../../../../experiments/model-adequacy/periodic3d/gauge-locality-under-synthetic-strain/analysis/development/gauge-locality-under-synthetic-strain.png)

*Replaceable 3-D frozen-gauge M0 development diagnostic. The looser threshold shows that
first-passing physical radius and retained block count need not move together. This
synthetic geometry stress test is not a phase-stability, elasticity, strain-potential,
or material result.*

**Bounded M1/M2 response controls.** A separately labeled smoke action applies the
sampled-qualified four-state bipartite parent. M1 freezes its onsite and hopping
matrices; its pointwise gauge-aligned strain difference remains below
$1.4\times10^{-15}E_{\mathrm{ref}}$ on both paths. M2 changes only the parent-bond
amplitudes through the prospectively fixed dimensionless radial law

$$
\frac{t_j(s)}{t_j(0)}=
\exp\!\left[-\left(\frac{d_j(s)}{d_j(0)}-1\right)\right].
$$

At the final 2-D metric, the responses span 0.81758–1.27146 and the maximum aligned
retained-space perturbation is $0.063575E_{\mathrm{ref}}$. At the BCC endpoint, the
four selected bonds share response 0.97564 and the corresponding maximum is
$0.007289E_{\mathrm{ref}}$. The stored trace/traceless decomposition is dominated by the
traceless channel in both smoke records. At the $10^{-5}$ tail support, the 2-D endpoint
interpolation, deliberate-truncation, and total maximum matrix errors of $\Delta H_s$
are approximately $6.0\times10^{-8}$, $7.801\times10^{-4}$, and
$7.802\times10^{-4}$; the 3-D values are $9.36\times10^{-5}$,
$1.61\times10^{-4}$, and $1.89\times10^{-4}$. These channels are not added.

![Replaceable 2-D M1/M2 response smoke diagnostic.](../../../../../experiments/model-adequacy/periodic2d/gauge-locality-under-synthetic-strain/analysis/response-development/m1-m2-strain-response.png)

*Replaceable 2-D M1/M2 response smoke diagnostic. M1 checks the zero aligned difference
expected from the frozen parent. M2 reports its synthetic aligned perturbation,
scalar/traceless split, locality cost, and three approximation channels.*

![Replaceable 3-D M1/M2 Bain-response smoke diagnostic.](../../../../../experiments/model-adequacy/periodic3d/gauge-locality-under-synthetic-strain/analysis/response-development/m1-m2-strain-response.png)

*Replaceable 3-D M1/M2 Bain-response smoke diagnostic. The fixed M2 radial law is a
synthetic sensitivity control, not a phase-stability or material-silicon model.*

These single-transform M0 and single-smoke M1/M2 records lack retained schemas,
independent artifact verification, and convergence and therefore remain software-
development diagnostics, not a material strain potential, material prediction, or paper
evidence. The extracted scalar
2-D precursor retains its historical finite-mesh scope. New scientific claims require
qualified calculations from the cited experiment families.

## VIII. Intended bounded conclusions

If supported by future evidence, the paper may compare representation cost across the
selected orthogonal and non-orthogonal isotropic systems. It will not infer a universal
range law, claim material validity, identify eigenvalue equality with operator equality,
or transfer a cutoff or tolerance between lattice geometries without qualification.

## References

1. <a id="ref-kohn"></a>W. Kohn, “Analytic Properties of Bloch Waves and Wannier
   Functions,” *Physical Review* **115**, 809–821 (1959).
   <https://doi.org/10.1103/PhysRev.115.809>
2. <a id="ref-brouder"></a>C. Brouder, G. Panati, M. Calandra, C. Mourougane, and
   N. Marzari, “Exponential Localization of Wannier Functions in Insulators,” *Physical
   Review Letters* **98**, 046402 (2007).
   <https://doi.org/10.1103/PhysRevLett.98.046402>
3. <a id="ref-mostofi"></a>A. A. Mostofi, J. R. Yates, Y.-S. Lee, I. Souza,
   D. Vanderbilt, and N. Marzari, “wannier90: A Tool for Obtaining Maximally-Localised
   Wannier Functions,” *Computer Physics Communications* **178**, 685–699 (2008).
   <https://doi.org/10.1016/j.cpc.2007.11.016>
4. <a id="ref-marzari"></a>N. Marzari, A. A. Mostofi, J. R. Yates, I. Souza, and
   D. Vanderbilt, “Maximally Localized Wannier Functions: Theory and Applications,”
   *Reviews of Modern Physics* **84**, 1419–1475 (2012).
   <https://doi.org/10.1103/RevModPhys.84.1419>
5. <a id="ref-sathe"></a>P. Sathe and R. Roy, “Compact Wannier Functions in One
   Dimension,” *Physical Review B* **109**, 155150 (2024).
   <https://doi.org/10.1103/PhysRevB.109.155150>
6. <a id="ref-jung"></a>J. Jung and A. H. MacDonald, “Tight-Binding Model for
   Graphene π Bands from Maximally Localized Wannier Functions,” *Physical Review B*
   **87**, 195450 (2013). <https://doi.org/10.1103/PhysRevB.87.195450>
7. <a id="ref-fang"></a>S. Fang, S. Carr, M. A. Cazalilla, and E. Kaxiras,
   “Electronic Structure Theory of Strained Two-Dimensional Materials with Hexagonal
   Symmetry,” *Physical Review B* **98**, 075106 (2018).
   <https://doi.org/10.1103/PhysRevB.98.075106>
8. <a id="ref-zhang"></a>L. Zhang, B. Onat, G. Dusson, A. McSloy, G. Anand,
   R. J. Maurer, C. Ortner, and J. R. Kermode, “Equivariant Analytical Mapping of First
   Principles Hamiltonians to Accurate and Transferable Materials Models,” *npj
   Computational Materials* **8**, 158 (2022).
   <https://doi.org/10.1038/s41524-022-00843-2>
9. <a id="ref-bain"></a>E. C. Bain, “The Nature of Martensite,” *Transactions of
   the American Institute of Mining and Metallurgical Engineers* **70**, 25–35 (1924).
   <https://onemine.org/documents/the-nature-of-martensite>
