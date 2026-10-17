# Spectral equivalence, Hamiltonian fidelity, and hopping locality in two- and three-dimensional rank-two models

## Abstract

Band eigenvalues do not determine a matrix-valued tight-binding representation or its
real-space locality. We formulate a rank-two framework that keeps the finite
cell--orbital, Bloch, spectral, retained-frame, and Wannier representations explicit and
aligns their state spaces before comparing Hamiltonians. A Laurent-polynomial
obstruction proves that spectral projection does not preserve finite hopping support in
general. For orthogonal flat-parent models, exact Bessel identities equate the
irreducible restricted-alignment residual with the normalized Fourier weight outside the
onsite block, while shell-resolved Jacobi--Anger formulas provide factorial tail bounds.
Bond-orbit identities extend the analytic comparison to non-orthogonal but physically
isotropic lattices using complete metric shells. Calculations for eight square,
triangular, honeycomb, simple-cubic, FCC, and diamond-inspired cases reveal non-collapsed
sampled Pareto sets in retained-block count, Hamiltonian error, and sorted-band error.
The optimized comparison scale ranges from 0.729890 to 0.937745; at the largest diamond
shell, restoring unit scale increases the Hamiltonian mismatch by about 2.9% while
reducing the sorted-band mismatch by about 82%. Synthetic rhombic and Bain paths
separate geometry-only reordering, a frozen-parent null response, and a prescribed
radial response. Across 201 samples, the retained subspaces remain isolated and
well-conditioned, the frozen-parent response stays at binary64 roundoff, and the radial
response is traceless dominated. Exact gauge equivalence therefore coexists with a
geometry-dependent three-way compromise once one restricts alignment and hopping
support. The numerical results apply to finite meshes and synthetic models, with no
continuum extrapolation or material parametrization.

## I. Introduction

Pointwise band equivalence does not determine hopping locality under a fixed
identification of retained coordinates. Here we extend that distinction across spatial
dimension and lattice geometry while the retained rank remains two. The purpose is not
to infer a Hamiltonian from eigenvalues alone. It is to compare
complete Hamiltonian representations connected by declared isometries and gauges, and
to quantify the representation cost introduced by a finite hopping support.

The gauge dependence and localization of Wannier representations are established
subjects, from analytic and exponential localization results [[1](#ref-kohn),
[2](#ref-brouder)] through practical maximally localized constructions and Wannier90
[[3](#ref-mostofi), [4](#ref-marzari)]. Compact support is a stronger algebraic property
and need not coincide with maximal localization [[5](#ref-sathe)]. Material-specific
Wannier and strained-Hamiltonian models likewise exist for graphene and other hexagonal
systems [[6](#ref-jung), [7](#ref-fang)], while environment-dependent Hamiltonian
mappings address geometry-responsive electronic structure [[8](#ref-zhang)]. Our
contribution is the controlled combination of pointwise spectral equivalence, declared
gauge alignment, metric-complete truncation, and a decision landscape relating hopping
complexity to operator and spectral error.

The study addresses three questions:

1. How are a finite cell--orbital operator, its Bloch representation, its complete
   eigensystem, a retained periodic frame, and its Wannier/tight-binding blocks related
   without conflating their state spaces?
2. After those spaces have been aligned, what compromises among retained hopping
   blocks, Hamiltonian agreement, and sorted-band agreement remain when alignment is
   restricted to one cell-local rotation and hopping support is finite?
3. Which parts of that compromise arise from physical-metric shell reordering, which
   vanish for an unchanged parent, and which respond to a prescribed radial change of
   bond amplitudes along synthetic deformation paths?

The calculations establish four results. Spectral projection fails to preserve finite
hopping support in general. The orthogonal flat-parent family admits exact
residual--locality identities and certified Fourier tails. All eight fixed-geometry
cases exhibit sampled trade-offs rather than a common optimum for locality, operator
fidelity, and spectral fidelity. Finally, the strain controls separate metric reordering
from Hamiltonian response: the frozen parent is a numerical null, whereas the radial
response is finite, predominantly traceless, and unaccompanied by loss of
retained-subspace isolation or frame conditioning.

The scope is rank two. Square and simple-cubic systems establish orthogonal baselines;
triangular/honeycomb and FCC/diamond-inspired systems test non-orthogonal but physically
isotropic geometry. Direction-dependent coupling laws, multiband gauges, and material
parametrizations lie outside this study.

## II. Theoretical framework and methods

This section follows the finite spectral and tight-binding realization defined in the
orthogonal family protocols.

### Finite periodic spaces and transforms

Let $d\in\{2,3\}$ be the spatial dimension and let $N$ be an even number of periodically
identified cells along each primitive direction. Define

$$
\Lambda_N^{(d)}=(\mathbb Z/N\mathbb Z)^d,
\qquad
\mathcal Q_N^{(d)}=
\left\{\mathbf q_{\mathbf j}:q_{j_\alpha}=\frac{j_\alpha-N/2}{N}\right\}.
$$

A vector $\mathbf n\in\Lambda_N^{(d)}$ labels a periodic cell;
$\mathbf q\in\mathcal Q_N^{(d)}\subset[-1/2,1/2)^d$ is a dimensionless reduced
reciprocal coordinate. Their phase pairing is $e^{2\pi i\mathbf q\cdot\mathbf n}$.
The cell-amplitude and operator spaces are

$$
\mathcal L_N^{(d)}
=\operatorname{span}\{|\mathbf n\rangle:\mathbf n\in\Lambda_N^{(d)}\}
\cong(\mathbb C^N)^{\otimes d},
\qquad
\mathcal H_{p,N}^{(d)}=\mathcal L_N^{(d)}\otimes\mathbb C^4,
\qquad
\mathcal H_{r,N}^{(d)}=\mathcal L_N^{(d)}\otimes\mathbb C^2.
$$

The subscript $p$ denotes the four-state parent orbital fiber and $r$ the rank-two
retained fiber. The parent operator acts on $\mathcal H_{p,N}^{(d)}$; retained Bloch and
Wannier operators act on $\mathcal H_{r,N}^{(d)}$. The symbol $I_m$ is the identity on
$\mathbb C^m$.

Let $\mathsf F_N$ be the unitary centered discrete Fourier transform. The one-axis cyclic
translation $\mathsf S_N$ is defined by

$$
\mathsf F_N\mathsf S_N\mathsf F_N^\dagger
=\operatorname{diag}_{q\in\mathcal Q_N^{(1)}}e^{2\pi iq}.
$$

The translation on primitive direction $\alpha$ and the tensor Fourier transform are

$$
\mathsf S_{\alpha,N}=I_N^{\otimes(\alpha-1)}\otimes\mathsf S_N
\otimes I_N^{\otimes(d-\alpha)},
\qquad
\mathcal F_{d,N}=\mathsf F_N^{\otimes d}.
$$

These Kronecker products act on cell labels only; they do not tensor the orbital fiber.

### Exact orthogonal parent

Let $E_{\mathrm{ref}}>0$ be the fixed energy unit, not a band gap. The orthogonal
protocols define

$$
T_0=E_{\mathrm{ref}}
\begin{pmatrix}
-1.20&0.06&0&0\\
0.06&-0.35&0&0\\
0&0&1.00&0.04\\
0&0&0.04&1.75
\end{pmatrix}
$$

and

$$
T_+=E_{\mathrm{ref}}
\begin{pmatrix}
0.15&0&0.12&0\\
0&-0.10&0&0.10\\
0&0&0.05&0\\
0&0&0&-0.04
\end{pmatrix},
\qquad T_-=T_+^\dagger.
$$

Here $T_0$ is the Hermitian onsite block, $T_+$ is the directed positive-axis hopping,
and $T_-$ is its reverse. The parameter $\rho\in[0,1]$ is a dimensionless hopping
homotopy: $\rho=0$ is cell local and $\rho=1$ is the declared dispersive parent. The
finite parent is

$$
\widehat K_{\rho,N}^{(d)}
=I_{N^d}\otimes T_0+
\frac{\rho}{d}\sum_{\alpha=1}^d
\left(\mathsf S_{\alpha,N}\otimes T_+
+\mathsf S_{\alpha,N}^\dagger\otimes T_-\right).
$$

The factor $1/d$ keeps the total axis-hopping scale fixed across dimension. Fourier
transformation gives

$$
\begin{aligned}
\widehat K_{B,\rho,N}^{(d)}
&=(\mathcal F_{d,N}\otimes I_4)\widehat K_{\rho,N}^{(d)}
(\mathcal F_{d,N}^\dagger\otimes I_4)\\
&=\bigoplus_{\mathbf q\in\mathcal Q_N^{(d)}}K_\rho^{(d)}(\mathbf q),\\
K_\rho^{(d)}(\mathbf q)
&=T_0+\frac{\rho}{d}\sum_{\alpha=1}^d
\left(e^{2\pi iq_\alpha}T_++e^{-2\pi iq_\alpha}T_-\right).
\end{aligned}
$$

Thus $K_\rho^{(d)}(\mathbf q)\in\mathbb C^{4\times4}$ is the parent Bloch Hamiltonian
at one mesh point.

### Complete spectrum and retained frame

Its complete eigensystem is

$$
K_\rho^{(d)}(\mathbf q)=Q(\mathbf q)E(\mathbf q)Q^\dagger(\mathbf q),
\qquad
E(\mathbf q)=\operatorname{diag}(\varepsilon_1,\ldots,\varepsilon_4),
$$

where $Q(\mathbf q)\in U(4)$ contains the eigenvectors and the real eigenvalues are
ordered increasingly. The diagonal array $E$ is an operator only in its eigenvector
coordinates. Without $Q$, it is not an operator in the orbital basis.

Let $I=\{1,2\}$ be the retained two lowest bands and
$P_I(\mathbf q)=Q_I(\mathbf q)Q_I^\dagger(\mathbf q)$ their spectral projector. A
periodic retained frame is an isometry $F(\mathbf q):\mathbb C^2\to\mathbb
C^4$ satisfying

$$
F^\dagger F=I_2,
\qquad
FF^\dagger=P_I.
$$

The retained projector is admissible only while bands two and three remain externally
isolated; a continuous lower bound is distinct from a sampled minimum. The frame
construction fixes an anchor, traversal, neighbor Procrustes rule, reciprocal-boundary
sewing, path-consistency diagnostics, and rank thresholds. If a periodic full-rank frame
cannot be constructed and verified, the protocol stops. Closure and plaquette phases
are sewing diagnostics, not topological claims.

The frame chooses coordinates inside the retained subspace. A momentum-dependent
$U(2)$ change of frame preserves retained bands but changes the hopping representation.
The retained Bloch matrix is

$$
H(\mathbf q)=F^\dagger(\mathbf q)K_\rho^{(d)}(\mathbf q)F(\mathbf q)
\in\mathbb C^{2\times2}.
$$

### Retained Bloch and Wannier operators

With $\mathcal V=\bigoplus_{\mathbf q}F(\mathbf q)$, the block isometry maps the retained
Bloch direct sum into the parent-orbital Bloch direct sum. Then

$$
\widehat H_B=\mathcal V^\dagger\widehat K_{B,\rho,N}^{(d)}\mathcal V
=\bigoplus_{\mathbf q}H(\mathbf q),
\qquad
\widehat H_W=(\mathcal F_{d,N}^\dagger\otimes I_2)\widehat H_B
(\mathcal F_{d,N}\otimes I_2).
$$

The $2\times2$ hopping block for cyclic displacement $\mathbf n$ is

$$
T_{\mathbf n}^{(N)}=\frac1{N^d}\sum_{\mathbf q\in\mathcal Q_N^{(d)}}
e^{-2\pi i\mathbf q\cdot\mathbf n}H(\mathbf q),
\qquad
H(\mathbf q)=\sum_{\mathbf n\in\Lambda_N^{(d)}}
e^{2\pi i\mathbf q\cdot\mathbf n}T_{\mathbf n}^{(N)}.
$$

“Complete” means every cyclic Fourier mode is retained. Interpolation, conversion to an
ordinary conjugate-closed inventory, and physical-radius truncation occur only after
this exact finite representation chain.

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

*Proof.* See Appendix A.1.

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

*Proof.* See Appendix A.2.

**Theorem (shell-resolved coefficients and factorial Fourier-tail bound).** Use a constant real rotation that diagonalizes $D$ as $D=\delta\sigma_z$, and set

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

*Proof.* See Appendix A.3.

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

*Proof.* See Appendix A.4.

The two theorems and corollary apply to the orthogonal flat-parent master family. The
factorial bound certifies its complete-shell Fourier tail, but it must not be transferred
to a dependent non-orthogonal bond orbit. The bond-orbit theorem below supplies that
comparator's analytic form; a lattice-specific constrained-series tail still requires a
separate certificate.

The two- and three-dimensional calculations use independent meshes and shell
inventories. Their outcomes are compared only through the common normalized diagnostics;
no shell index or convergence statement is transferred between dimensions.

### Two-dimensional scalar precursor

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

*Proof.* See Appendix A.5.

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

*Proof.* See Appendix A.6.

At $a=\pi/4$, bounded binary64 evaluations with a declared $10^{-13}$
per-coefficient numerical margin give normalized scalar-tail upper bounds
$2.8760\times10^{-9}$ for triangular shell cap $S=21$ at $K=10$, and
$5.5358\times10^{-6}$ for FCC shell cap $S=7$ at $K=9$. These evaluate the proved
certificate in binary64 arithmetic with the stated margin; no interval-arithmetic or
mesh-limit extrapolation is applied.

The metric and point group select the physically admissible complete bond orbit; the
integer relations among the selected reduced-coordinate bond vectors determine whether
the comparator factorizes. Thus the square and cubic products arise from independent
primitive-axis harmonics, whereas an orbit with integer dependencies generally has the
constrained Bessel sum above.

The non-orthogonal calculations use a graphene-inspired triangular/honeycomb 2-D
parent and a silicon-inspired FCC/diamond 3-D parent, together with matched Bravais
controls at equal reciprocal-torus RMS gauge amplitude. “Inspired” denotes the declared
geometry, two-site basis, and bipartite connectivity; neither parent is a material
parametrization. The triangular and FCC control orbits yield, respectively, one-index
and three-index constrained Bessel sums under the bond-orbit and constrained-tail
theorems. These dependent bond orbits require their own metric shells and certificates;
the square and cubic products cannot be transferred unchanged.

## V. Restricted alignment and Hamiltonian comparison

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

## VI. Synthetic-strain methods

### Scientific question and three controls

The protocol asks how homogeneous deformation affects the mechanisms and sampled
requirement coordinates associated with spectral fidelity, restricted operator
agreement, and finite-range hopping locality. It is a synthetic stress test, not an
elastic, structural-stability, or material-strain calculation. The deformation does not
make exact spectral and hopping representations inconsistent. Fixed-geometry Pareto
surfaces and strain-response scans remain separate until explicit strain-resolved
landscapes are calculated. The protocol separates:

1. a **geometry-only control**, with a constant rank-two parent, fixed Fourier
   coefficients, and a changing physical metric;
2. a **frozen-parent null-response control**, with fixed four-state onsite and hopping
   matrices, the seed-projected retained frame, and the explicit common-cell map; and
3. a **synthetic radial-response control**, which changes only selected
   inter-sublattice amplitudes according to

$$
t_j(s)=t_j(0)\exp\!\left[-\beta\left(\frac{d_j(s)}{d_j(0)}-1\right)\right],
\qquad \beta=1.
$$

No onsite response, refit, normalization, relaxation, or averaging among controls is
permitted. The three controls answer different questions.

### Shell--scale Pareto decision landscape

At strain coordinate $s$, let $H_s(\mathbf q)$ be the retained reference field,
$\bar h_s=\operatorname{tr}H_s/2$, and
$\widetilde H_s=H_s-\bar h_sI_2$. Let $B_{s,S}(\mathbf q)$ be the gauge-transformed
comparison reconstructed after retaining every complete physical-metric shell through
$S$. Restricted full-field alignment supplies one global rotation $R_{*,s}$ and
nonnegative optimized scale $\lambda_{*,s}$. We sample

$$
\lambda_s(u)=(1-u)\lambda_{*,s}+u,
\qquad 0\le u\le1,
$$

where $u=0$ is the optimized operator-scale endpoint and $u=1$ preserves the original
spectral splitting. Define

$$
A_{s,u}(\mathbf q)=\bar h_s(\mathbf q)I_2+
\lambda_s(u)R_{*,s}^{\mathsf T}\widetilde H_s(\mathbf q)R_{*,s}
$$

and

$$
\begin{aligned}
\varepsilon_H(s;S,u)
&=\max_{\mathbf q}\frac{\|B_{s,S}(\mathbf q)-A_{s,u}(\mathbf q)\|_F}
{\sqrt2E_{\mathrm{ref}}},\\
\varepsilon_E(s;S,u)
&=\max_{\mathbf q,n}\frac{|\varepsilon_n[B_{s,S}(\mathbf q)]-
\varepsilon_n[A_{s,u}(\mathbf q)]|}{E_{\mathrm{ref}}},\\
\mathcal J_s(S,u)
&=(N_s(S),\varepsilon_H(s;S,u),\varepsilon_E(s;S,u)).
\end{aligned}
$$

Lower values of all three components are preferred. A calculated point is Pareto
efficient when no other sampled pair weakly improves every component and strictly
improves at least one. Strain indexes a family of sampled decision landscapes; it is not
itself minimized. Physical radius remains separate because it need not order shells like
block count. This construction requires no acceptance tolerance. Tessellated adjacent
samples are visualization only and assert neither continuum coverage nor interpolation
validity.

### Area- and volume-preserving paths

We use the following area- and volume-preserving crystallographic paths and coordinate
bridges.

For strain fraction $s\in[0,1]$, the 2-D path is

$$
\theta(s)=\frac\pi3+s\frac\pi6,
\qquad
A_2(s)=\frac1{\sqrt{\sin\theta(s)}}
\begin{pmatrix}1&\cos\theta(s)\\0&\sin\theta(s)\end{pmatrix},
\qquad \det A_2=1.
$$

It connects triangular and square metric geometries. For the 3-D Bain path, write
$t=s\in[0,1]$ and define

$$
\gamma(t)=\sqrt2+t(1-\sqrt2),
\qquad
\ell_\perp(t)=\left(\frac2{\gamma(t)}\right)^{1/3},
\qquad
\ell_\parallel(t)=\gamma(t)\ell_\perp(t).
$$

The three primitive vectors evolve continuously as

$$
\begin{aligned}
\mathbf a_1(t)&=\frac12
(\ell_\perp(t),\ell_\perp(t),\ell_\parallel(t))^\mathsf T,\\
\mathbf a_2(t)&=\frac12
(-\ell_\perp(t),\ell_\perp(t),\ell_\parallel(t))^\mathsf T,\\
\mathbf a_3(t)&=\frac12
(\ell_\perp(t),-\ell_\perp(t),\ell_\parallel(t))^\mathsf T,
\qquad 0\le t\le1.
\end{aligned}
$$

With $A_3(t)=[\mathbf a_1(t)\ \mathbf a_2(t)\ \mathbf a_3(t)]$, the primitive-cell
volume is

$$
V(t)=|\mathbf a_1(t)\cdot[\mathbf a_2(t)\times\mathbf a_3(t)]|
=\det A_3(t)
=\frac{\ell_\perp(t)^2\ell_\parallel(t)}2=1
\qquad (0\le t\le1).
$$

Thus the full path, including both endpoints, is volume preserving. The ratio
$\ell_\parallel/\ell_\perp$ runs from $\sqrt2$ at $t=0$ to $1$ at $t=1$, giving FCC
and BCC endpoint representations of the Bain path [[9](#ref-bain)].

### FCC--Bain common-cell identification

The FCC and Bain reduced coordinates obey

$$
\mathbf n_F=U\mathbf n_B,
\qquad
U=\begin{pmatrix}1&1&0\\0&0&1\\0&-1&0\end{pmatrix},
\qquad \det U=1,
$$

with $\mathbf q_B=U^\mathsf T\mathbf q_F$ and the finite-cell bijection
$\mathbf n_B\mapsto U\mathbf n_B\pmod N$. The diamond offset
$(1/4,1/4,1/4)_F$ becomes $(1/2,-1/4,1/4)_B$; orbital and sublattice labels remain
unchanged. The metric and six bond-pair identities establish a coordinate/state-space
map only, not a material Hamiltonian identification.

### Sampling and numerical diagnostics

The bounded protocol uses $s\in\{0,1/8,\ldots,1\}$, maximum gauge angle $a=\pi/4$,
and tail tolerances $10^{-3}$ and $10^{-5}$. Geometry-only transforms use $64^2$ and
$24^3$ meshes. Response controls use construction/evaluation sizes $16^2/33^2$ and
$8^3/17^3$, with shift $1/3$, fixed $\rho=1$, onsite matrices,
$E_{\mathrm{ref}}$, and reduced-coordinate gauge. These finite meshes define the
reported synthetic scans; no continuum-mesh extrapolation is applied.

The reported channels include unit-determinant metrics, bond-length extrema, orbit
splitting, alignment, ordinary and Nyquist power, complete-shell first-passing radius
and block count, and--for response controls--the Appendix B matrix and sorted-band error
channels for both the Hamiltonian and aligned difference field $\Delta H_s$.

The bounded scan uses

$$
\widehat S_0=\{s_i=i/200:i=0,\ldots,200\}.
$$

A hat denotes a sampled maximum, not a continuum supremum. With retained splitting scale
$\kappa_i$ and maximum finite-mesh correlation $\mu_i$, the pointwise optimized and
fixed-$p_0=(0,1)$ candidate requirements are

$$
\tau_{o,\min}(s_i)=\sqrt{\kappa_i[1-\max(0,\mu_i)^2]},
\qquad
\tau_{o,p_0}(s_i)=\sqrt{2\kappa_i(1-\mu_i)}.
$$

Their maxima are reported separately from
$\widehat R_\varepsilon=\max_iR_\varepsilon(s_i)$ and
$\widehat N_\varepsilon=\max_iN_\varepsilon(s_i)$. Pointwise optimized candidates are
not one common path witness, and $p_0$ remains a prescribed candidate path until frozen
limits establish feasibility. Every adjacent base-grid interval whose endpoint block
counts or bond-degeneracy counts differ is bisected five times, producing detected
brackets no wider than $1/6400$. This cannot detect an even number of hidden changes in
an equal-endpoint interval and is not a continuum certificate. No feasibility crossing
is assigned because the protocol characterizes the sampled decision landscape rather
than classifying it against an acceptance region.

The calculations describe synthetic Hamiltonians. They contain no force, stress, strain
energy, phase-stability, realistic graphene or silicon response, or material FCC--BCC
transition model.

## VII. Diagnostic summary

The study keeps parent and retained-space reconstruction, covariant equivalence,
restricted global alignment, cyclic conversion, interpolation, deliberate truncation,
total matrix and band consequences, locality power, transport, and refinement as
distinct diagnostic layers. Appendix B defines their normalizations,
applicability conditions, and first-passing rules. The approximation channels are not
additive, and closure-phase reduction is defined only when every contributing transport
link is full rank.

Independent finite-sum reconstruction checks the declared numerical channels without
using the production Fourier implementation. Appendix B summarizes these diagnostics.

## VIII. Results

The calculations use three construction levels, $16^2$, $32^2$, and $64^2$ in two
dimensions and $8^3$, $16^3$, and $32^3$ in three dimensions, together with shifted
evaluation meshes. Reconstruction, Hermiticity, Parseval, transport, and closure
identities remain below $2.0\times10^{-14}$. One of 18 graphene-family first-passing
shell decisions changes by one shell between the first two levels; every such decision
is unchanged on the final refinement in all four families. Some strict tail cuts lie
outside the finite shell caps, so the comparison uses the full sampled decision
landscapes rather than converting those cuts into acceptance tests.

**Central result: controlled incompatibility landscape.** The exact untruncated route
preserves the retained spectrum under the declared momentum-dependent gauge. Once the
comparison is restricted to one cell-local global rotation, one scale choice, and a
finite complete-shell inventory, spectral fidelity, Hamiltonian fidelity, and locality
cannot in general be optimized simultaneously. Shell cutoff controls retained
complexity, while the path from $\lambda_{*,s}$ to unit scale resolves the compromise
between restricted operator agreement and preservation of the original splitting.
Synthetic deformation is analyzed through separate response channels, while the
reported Pareto surfaces remain fixed-geometry results. Exact gauge equivalence holds
throughout both calculations.

The geometry-only control isolates metric reordering of one Fourier inventory; the
frozen-parent control checks that coordinate deformation alone produces no Hamiltonian
response; and the radial-response control deliberately changes bond amplitudes. The
scientific output is the set of available nondominated compromises, not a self-selected
acceptance boundary. A componentwise cover assembled from different samples is not an
attainable decision and is not a Pareto representative.

The fixed-geometry calculation uses 17 scales between $\lambda_*$ and unity and every
available complete shell. The optimized scale runs from 0.729890 for the square directed
parent to 0.937745 for the diamond-inspired case. All eight cases have nonempty,
non-collapsed sampled nondominated sets. The diamond-inspired set is the most selective
in this sampling (34 of 136 calculated vertices), while the triangular and FCC controls
retain 156 of 187 and 116 of 136 vertices. At the largest diamond shell, moving from
$\lambda_*$ to unit scale increases normalized Hamiltonian mismatch from 0.211780 to
0.217933 (about 2.9%) while reducing sorted-band mismatch from 0.0193798 to 0.00341626
(about 82%). This is one sampled endpoint comparison, not a universal preference for
unit scale. The counts are properties of the declared discrete sample, not invariant
geometric measures.

![Principal sampled shell--scale decision landscapes.](figures/principal-shell-scale-decision-landscapes.png)

*Square, honeycomb, simple-cubic, and diamond-inspired fixed-geometry decision
landscapes. Orange points are nondominated calculated vertices. Triangular faces connect
adjacent calculated cells and represent the discrete sampling topology. All eight
case-resolved plots and endpoint metadata are retained in the manuscript appendix.*

The following figures compare the four model families at fixed geometry; they are not
four strain-responsive models.

![Square-lattice results.](figures/square-2d-scientific-story.png)

*Square-lattice family. Withheld interpolation, external retained-subspace isolation,
hopping-tail power, withheld spectral consequence, and tail-power/consequence
comparison remain separate channels.*

![Graphene-inspired honeycomb results and matched Bravais controls.](figures/triangular-honeycomb-2d-scientific-story.png)

*Graphene-inspired family and matched Bravais controls. “Inspired” denotes geometry and
connectivity only, not a graphene parametrization or validation result.*

![Simple-cubic results.](figures/simple-cubic-3d-scientific-story.png)

*Simple-cubic family at two displayed mesh levels, with interpolation, external
isolation, tail power, and spectral consequence retained as distinct channels.*

![Silicon-inspired diamond results and matched FCC controls.](figures/fcc-diamond-3d-scientific-story.png)

*Silicon-inspired family and matched Bravais controls. “Inspired” denotes geometry and
connectivity rather than a silicon parametrization.*

The following refined-mesh figures show interpolation, deliberate-truncation, and total
errors separately. Near overlap of the latter two curves means interpolation is much
smaller at these sampled points; it does not make the channels definitionally identical.

![Square-lattice three-channel error decomposition.](figures/square-2d-three-channel-error-decomposition.png)

![Graphene-inspired-family three-channel error decomposition.](figures/triangular-honeycomb-2d-three-channel-error-decomposition.png)

![Simple-cubic three-channel error decomposition.](figures/simple-cubic-3d-three-channel-error-decomposition.png)

![Silicon-inspired-family three-channel error decomposition.](figures/fcc-diamond-3d-three-channel-error-decomposition.png)

**Bounded geometry-only control.** Separate frozen-parent geometry-stress diagnostics
use nine unit-area rhombic and unit-volume Bain metrics. The reduced-coordinate Hamiltonian,
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

![Two-dimensional frozen-gauge geometry-only result.](figures/rhombic-2d-geometry-only-control.png)

*The parent, gauge, Fourier
weights, and unit cell area remain fixed while the rhombic metric moves from triangular
to square. Tail-power thresholds are locality diagnostics, not universal spectral-error
bounds.*

![Three-dimensional frozen-gauge geometry-only result along the unit-volume FCC--BCC Bain path.](figures/bain-3d-geometry-only-control.png)

*The looser threshold shows that
first-passing physical radius and retained block count follow different trends along the
same metric path.*

**Frozen-parent and radial-response controls.** The response calculation uses the
four-state bipartite parent. The frozen-parent
null-response control holds its onsite and hopping matrices fixed; its pointwise
gauge-aligned strain difference remains below
$1.4\times10^{-15}E_{\mathrm{ref}}$ on both paths. The synthetic radial-response control
changes only the parent-bond amplitudes through the prescribed dimensionless
radial law

$$
\frac{t_j(s)}{t_j(0)}=
\exp\!\left[-\left(\frac{d_j(s)}{d_j(0)}-1\right)\right].
$$

At the final 2-D metric, the responses span 0.81758–1.27146 and the maximum aligned
retained-space perturbation is $0.063575E_{\mathrm{ref}}$. At the BCC endpoint, the
four selected bonds share response 0.97564 and the corresponding maximum is
$0.007289E_{\mathrm{ref}}$. The stored trace/traceless decomposition is dominated by the
traceless channel on both paths. At the $10^{-5}$ tail support, the 2-D endpoint
interpolation, deliberate-truncation, and total maximum matrix errors of $\Delta H_s$
are approximately $6.0\times10^{-8}$, $7.801\times10^{-4}$, and
$7.802\times10^{-4}$; the 3-D values are $9.36\times10^{-5}$,
$1.61\times10^{-4}$, and $1.89\times10^{-4}$. These channels are not added.

![Two-dimensional frozen-parent and radial-response controls.](figures/rhombic-2d-strain-response-controls.png)

*The frozen-parent control gives the null
aligned difference expected from the unchanged parent. The radial-response control
reports its synthetic aligned perturbation,
scalar/traceless split, locality cost, and three approximation channels.*

![Three-dimensional frozen-parent and radial-response Bain controls.](figures/bain-3d-strain-response-controls.png)

*The prescribed radial law generates a finite response while the frozen parent remains
a numerical null.*

**Pathwise qualification and approximation envelopes.** The 201-point sweeps retain the
external-gap, seed-overlap, frame-conditioning, approximation, and mechanism extrema and
the first strain where each occurs. For the radial control, the minimum external gaps
are $2.00708E_{\mathrm{ref}}$ in 2-D and $2.01305E_{\mathrm{ref}}$ in 3-D; minimum
seed overlaps are 0.998684 and 0.998687. Minimum frame-overlap singular values remain
above 0.9999998 and 0.999999996. The sampled response therefore does not coincide with
loss of the retained subspace or a rank-deficient frame overlap.

Maximum radial pointwise frame-alignment residuals are $8.27192\times10^{-4}$ in 2-D
and $9.64819\times10^{-5}$ in 3-D, both at $s=1$. At the $10^{-5}$ support, maximum
total aligned-difference Hamiltonian errors are $7.80164\times10^{-4}E_{\mathrm{ref}}$
and $1.89367\times10^{-4}E_{\mathrm{ref}}$. Frozen-parent envelopes remain at
binary64 roundoff. The maximum scalar/traceless response components are
$1.77497\times10^{-6}/0.0635748$ in 2-D and
$8.93927\times10^{-7}/0.00728904$ in 3-D. These are sampled extrema, not continuum
bounds.

![Two-dimensional strain qualification and response-mechanism scan.](figures/rhombic-2d-strain-qualification-response-scan.png)

*External gap, seed overlap, frame conditioning, response magnitude and mechanism split,
and tight-support approximation errors remain distinct 2-D sampled channels.*

![Three-dimensional strain qualification and response-mechanism scan.](figures/bain-3d-strain-qualification-response-scan.png)

*The 3-D synthetic diamond radial response remains separated from retained-subspace and
frame qualification throughout the sampled path.*

**Sampled witness and transition scan.** The 201-point base scan preserves normalized
cell measure to $4.5\times10^{-16}$ in 2-D and $1.3\times10^{-15}$ in 3-D; direct
sorted-band defects remain below $1.8\times10^{-15}$. In 2-D, the radial-response
pointwise requirement increases from 0.0810724 at $s=0$ to 0.0875414 at $s=1$, while
the fixed-$p_0$ requirement increases from 0.0835420 to 0.0907685. In 3-D, both radial
requirements attain their sampled maxima at $s=0$ and decrease slightly toward the BCC
endpoint. Geometry-only and frozen-parent requirement curves remain invariant. These
values are sampled coordinates of the decision landscape; no pass/fail classification
is intended.

The sampled 2-D locality envelopes are $(\widehat R,\widehat N)=(2.82843,25)$ at
$10^{-3}$ and $(4.24264,61)$ at $10^{-5}$, attained at $s=1$. In 3-D, the looser
tolerance has $\widehat R=2.24492$ at $s=0$ but $\widehat N=59$ first at $s=0.77$;
the tighter envelope is $(3.27337,169)$ at $s=1$. Five bisections localize seven
detected 2-D shell-count changes and six detected 3-D changes to widths no greater than
$1/6400$. Both endpoint bond-degeneracy changes lie in $[0,1/6400]$. Independent
test-only finite sums reconstruct the shells, and an independent harmonic calculation
reconstructs both operator-requirement channels. Hidden equal-endpoint transitions are
not excluded.

![Sampled two-dimensional rhombic strain scan.](figures/rhombic-2d-strain-scan.png)

*The pointwise and fixed-candidate requirements, geometry-only locality costs,
frozen-parent null response, and radial response remain separate across all 201 sampled
coordinates.*

![Sampled three-dimensional Bain strain scan.](figures/bain-3d-strain-scan.png)

*At the looser tail tolerance, maximum physical radius and maximum block count occur at
different sampled strains.*

Together, the scans establish the behavior of the declared finite synthetic models:
metric deformation reorganizes complete physical shells, an unchanged parent produces
no resolved Hamiltonian response, and the prescribed radial law produces a finite,
predominantly traceless response without loss of retained-subspace isolation. The
calculation contains no material strain potential and no continuum extrapolation.

## IX. Discussion

### 9.1 The three-way decision landscape

The central finding is that spectral fidelity, Hamiltonian fidelity, and hopping locality
form a genuine three-way trade-off once two practical restrictions are imposed:
alignment is limited to a single cell-local rotation, and hopping support is limited to
a finite set of complete metric shells. Exact gauge equivalence continues to hold in
the unrestricted setting; the incompatibility appears only after those restrictions are
added.

Consequently, a small sorted-band error is not by itself sufficient to establish the
operator fidelity or locality of a finite-range Hamiltonian representation. The sampled
Pareto fronts for all eight cases are nonempty and non-collapsed. In every geometry,
some calculated points improve locality only by degrading operator or spectral
agreement, and vice versa. The scientific output is therefore the set of available
nondominated compromises rather than a single preferred Hamiltonian.

### 9.2 Geometry dependence and the role of the comparison scale

The shape of the decision surface is strongly geometry dependent. The diamond-inspired
case is the most selective of the eight fronts examined: only 34 of 136 calculated
vertices are nondominated, whereas the triangular and FCC controls retain substantially
larger fractions of their sampled vertices. Similar retained-block counts can correspond
to different physical ranges once the metric changes, and equal shell indices have no
intrinsic cross-lattice meaning without the associated metric and orbit inventory.

The path from the optimized scale $\lambda_*$ to unit scale quantifies a concrete
compromise. At the largest sampled diamond shell, restoring unit scale increases the
normalized Hamiltonian mismatch by about 2.9% while reducing the sorted-band mismatch by
approximately 82%. Neither endpoint is universally preferred: $\lambda_*$ favors
restricted operator agreement, whereas unit scale recovers most of the original
spectral splitting at modest additional operator cost. The appropriate operating point
is application dependent and requires an external criterion.

### 9.3 Mechanism separation under synthetic strain

The three synthetic controls isolate distinct contributions to the observed trade-offs.
Geometry-only deformation leaves the reduced-coordinate Hamiltonian, gauge, and Fourier
weights invariant, yet reorders complete physical shells and changes both first-passing
radius and retained block count. At the looser three-dimensional tail tolerance, these
two locality costs move in opposite directions. Physical range and parameter count are
therefore independent locality costs.

The frozen-parent control returns a numerical null, with aligned differences at
binary64 roundoff. Coordinate deformation alone produces no Hamiltonian response when
the parent matrices are fixed. The prescribed radial-response control produces a finite,
predominantly traceless perturbation while preserving external isolation of the retained
subspace and full-rank frame conditioning. A finite response can therefore be introduced
without losing the spectral isolation required by the representation chain.

### 9.4 Implications and outlook

The rank-two benchmark supplies a controlled setting in which finite-range models are
assessed against an explicit three-objective surface rather than a single error metric.
In Wannier or machine-learned tight-binding workflows, an application can impose its own
Hamiltonian and spectral tolerances; the nondominated set then identifies the associated
locality choices.

Several extensions follow directly. Raising the retained rank above two will test how
the residual--locality identities and Pareto-front structure change beyond the simple
$U(2)$ gauge freedom used here. Direction-dependent coupling laws and material-specific
parent Hamiltonians can enter the same diagnostic channels without changing the
underlying state-space identifications. Repeating the shell--scale calculation along a
denser strain path or a lattice-relaxation trajectory would resolve the corresponding
motion of the decision landscape.

The essential distinction remains: exact spectral equivalence alone is insufficient;
restricted alignment and finite hopping support introduce the nontrivial representation
cost.

## X. Conclusions

We have separated exact spectral equivalence from the additional demands required of a
finite-range tight-binding representation. Spectral projection can generate infinite
support, and restricted global alignment exposes a residual exactly tied to non-onsite
Fourier weight in the orthogonal flat-parent family. Metric-complete shells and
bond-orbit identities extend the construction to non-orthogonal isotropic lattices.
Across eight calculated cases, locality, Hamiltonian fidelity, and sorted-band fidelity
form nontrivial sampled Pareto sets rather than sharing one optimum. Synthetic rhombic
and Bain controls further separate geometric reordering, a frozen-parent null response,
and a finite radial response. These results establish a controlled rank-two benchmark
for reduced Hamiltonians while preserving the distinctions among gauge equivalence,
operator agreement, spectral agreement, and real-space support.

## Appendix A. Proofs

The theorem and corollary statements remain in the main text. Their proofs are collected
here so that the main narrative can emphasize the representation chain, geometric
controls, and numerical evidence.

### A.1 Spectral projection and finite hopping support

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

### A.2 Flat-parent residual--locality identity

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

### A.3 Orthogonal shell coefficients and factorial tail

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

### A.4 Monotonicity and small-amplitude dimension law

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

### A.5 Bond-orbit flat-parent comparator

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

### A.6 Constrained-series complete-shell certificate

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

## Appendix B. Diagnostic definitions

Every discrepancy is defined only after both arguments have been represented on the
same reciprocal mesh, in the same retained state space, basis, gauge, energy reference,
units, and lattice geometry.

### B.1 Pointwise matrix and sorted-band errors

For Hermitian rank-$r$ fields $A_\ell$ and $B_\ell$ at $M$ common reciprocal points,
define

$$
d_{H,\ell}(A,B)=\frac{\lVert A_\ell-B_\ell\rVert_F}{\sqrt r}.
$$

The primary channels are

$$
\begin{aligned}
\epsilon_{H,\max}&=\max_\ell d_{H,\ell},&
\epsilon_{H,\mathrm{rms}}&=\left[\frac1M\sum_\ell d_{H,\ell}^2\right]^{1/2},\\
\epsilon_{b,\max}&=\max_{\ell,j}|\varepsilon_j^A(\mathbf q_\ell)-\varepsilon_j^B(\mathbf q_\ell)|,&
\epsilon_{b,\mathrm{rms}}&=\left[\frac1{Mr}\sum_{\ell,j}|\varepsilon_j^A(\mathbf q_\ell)-\varepsilon_j^B(\mathbf q_\ell)|^2\right]^{1/2}.
\end{aligned}
$$

They have energy units; displayed dimensionless values divide by the declared
$E_{\mathrm{ref}}$. Here $r=2$. The separately checked Weyl relation is
$\epsilon_{b,\max}\le\sqrt r\,\epsilon_{H,\max}$.

### B.2 Interpolation, deliberate truncation, and total error

With $H^{\mathrm{dir}}$ the direct withheld-mesh field,
$H_N^{\mathrm{ord}}$ the full ordinary Fourier interpolant, and
$H_{N,R}^{\mathrm{ord}}$ its complete-radius truncation,

$$
\begin{aligned}
\mathcal E_{\mathrm{interp}}&=\mathcal E(H_N^{\mathrm{ord}},H^{\mathrm{dir}}),\\
\mathcal E_{\mathrm{trunc}}&=\mathcal E(H_{N,R}^{\mathrm{ord}},H_N^{\mathrm{ord}}),\\
\mathcal E_{\mathrm{total}}&=\mathcal E(H_{N,R}^{\mathrm{ord}},H^{\mathrm{dir}}).
\end{aligned}
$$

Each uses all four primary channels. They are not added because interpolation and
truncation may reinforce or cancel. Strain-response channels are evaluated on the
aligned difference field $\Delta H_s$; the geometry-only control is not a
strain-potential calculation.

### B.3 Fourier power and first-passing support

For ordinary blocks $T_{\mathbf n}$ and complete physical-metric supports
$\mathcal S_s$,

$$
P_{\mathrm{omit}}(s)=\frac1r\sum_{\mathbf n\notin\mathcal S_s}
\lVert T_{\mathbf n}\rVert_F^2.
$$

Cyclic Nyquist power remains separate. For channel $X$ and tolerance $\tau$,

$$
\widehat s_X(\tau)=\min\{s:\epsilon_{X,\mathrm{total},\max}(s)\le\tau\}.
$$

The record retains physical radius, block count, passing error, and preceding error. No
passing shell at the declared cap is unresolved, not a pass at the cap.

### B.4 Alignment, reconstruction, and isolation

Parent Hermiticity, eigensystem and projector reconstruction, frame orthonormality,
parent--retained lifting, Fourier reconstruction, covariant equality, and restricted
global alignment remain separate. Restricted alignment records the global rotation,
optimized nonnegative splitting scale, finite-mesh correlation, minimum operator
threshold, and distinct unit-splitting exact-spectrum joint threshold. Sampled and
continuous external-gap quantities remain distinct.

### B.5 Strain candidates, sampled envelopes, and transition brackets

At sampled strain $s_i$, let $\kappa_i$ and $\mu_i$ be the restricted-alignment
splitting scale and maximum correlation. Then

$$
\tau_{o,\min}(s_i)=\sqrt{\kappa_i[1-\max(0,\mu_i)^2]},
\qquad
\tau_{o,p_0}(s_i)=\sqrt{2\kappa_i(1-\mu_i)},
\qquad p_0=(0,1).
$$

The first permits an independently optimized candidate at each sample; the second is a
prescribed parameter path. Neither is a common or continuum witness without frozen
limits and between-sample certification. The sampled maxima
$\widehat\tau_{o,\min}$, $\widehat\tau_{o,p_0}$,
$\widehat R_\varepsilon$, and $\widehat N_\varepsilon$ retain separate sample locations.

The qualification envelope also retains the sampled minimum external isolation gap,
minimum seed overlap, minimum frame-overlap singular value, and maximum pointwise and
restricted-global frame-alignment residuals. Separate approximation envelopes retain
all four matrix/band error reductions for the aligned response, interpolation,
truncation, and total channels, including the aligned difference field. Omitted and
Nyquist powers, hopping-response factors, scalar/traceless components, and onsite/offsite
response powers retain independent extrema and locations. None is a continuum bound.

A detected transition bracket has differing endpoint block counts or bond-orbit counts.
Five bisections reduce a base interval from at most $1/200$ to at most $1/6400$.
Equal endpoint values cannot exclude hidden transitions, so these brackets are not
continuum certificates.

### B.6 Transport and closure

For full-rank transport links, let $W_\alpha(\mathbf k_\perp)$ be the ordered closure
product and $\phi_{\alpha,j}$ its ordered principal eigenphases. The reported reduction
is

$$
\Phi_j=\max_{\alpha,\mathbf k_\perp}|\phi_{\alpha,j}(\mathbf k_\perp)|,
\qquad j\in\{0,1\}.
$$

It is accompanied by singular-value, Procrustes, rank-cutoff, roundoff, link-unitarity,
closure-unitarity, and plaquette channels. A rank-deficient link makes dependent closure
channels explicitly inapplicable. No topological meaning is asserted.

### B.7 Numerical validation boundary

The numerical checks retain mesh separation, metric covariance, basis-distance extrema
where applicable, refinement changes, exact identities, and independent reconstruction
defects. Agreement of these diagnostics verifies the declared finite calculation. It
does not supply a continuum limit, an externally chosen adequacy tolerance, or a
material-specific Hamiltonian.


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
