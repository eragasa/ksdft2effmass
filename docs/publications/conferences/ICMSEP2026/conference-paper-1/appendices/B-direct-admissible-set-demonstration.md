# Appendix B. Direct Admissible-Set Demonstration

The completed controlled calculation is retained under
[`calculations/ICMSEP2026/conference/paper_1/`](../../../../../../calculations/ICMSEP2026/conference/paper_1/).
It freezes the scalar 1D parent

$$
E_{\rm ref}(k)=1-\frac12\cos k+\frac15\cos 2k
$$

and the two-parameter nearest-neighbor candidate family

$$
E_{\boldsymbol\theta}(k)=\theta_0+2\theta_1\cos k.
$$

The parameter box is $0\leq\theta_0\leq3/2$ and
$-3/4\leq\theta_1\leq1/2$. Both canonical scales and weights are one. The
operator domain is $R=-2,\ldots,2$ with unit shell weights, and the scalar
alignment family is the singleton identity.

## Frozen threshold rule

For each quadratic loss, the exact analytic minimum is derived from the frozen parent
and sampling design. The admissibility threshold is that minimum plus the common
excess-loss budget $\epsilon=10^{-4}$. This is a controlled map resolution, not a
statistical uncertainty. The operator normalization is global over the five
translations; translation-resolved residuals and the omitted second-neighbor tail
remain separate records.

## Witness and feasible-pair certificates

Let $\mathfrak A_E$ and $\mathfrak A_H$ denote the two frozen admissible parameter
sets and let $d$ be the declared parameter metric. If a point
$\boldsymbol\theta^\star$ satisfies both threshold inequalities, then
$\boldsymbol\theta^\star\in\mathfrak A_E\cap\mathfrak A_H$. The pair
$(\boldsymbol\theta^\star,\boldsymbol\theta^\star)$ is feasible in the definition of
set separation and has distance zero; nonnegativity of $d$ therefore proves
$\delta^\star=0$. Membership in a sampled Pareto set is neither necessary nor
sufficient for this certificate; the two threshold inequalities are the operative
hypotheses.

More generally, every feasible pair
$\boldsymbol\theta_E\in\mathfrak A_E$ and
$\boldsymbol\theta_H\in\mathfrak A_H$ gives

$$
\delta^\star\leq d(\boldsymbol\theta_E,\boldsymbol\theta_H).
$$

Thus a sampled nondominated calculation supplies a certified upper bound only when it
supplies such a feasible pair. A distance from one sampled point to
$\mathfrak A_E\cap\mathfrak A_H$ is not a separation certificate and, when the
intersection is empty, is not the relevant quantity.

## Quadratic enclosure and separation lemma

Suppose a frozen quadratic loss has the exact form

$$
\mathcal L(\boldsymbol\theta)=\mathcal L_{\min}+Q(\boldsymbol\theta),\qquad
Q(\boldsymbol\theta)=
(\boldsymbol\theta-\boldsymbol\theta^\star)^{\mathsf T}
\mathbf G(\boldsymbol\theta-\boldsymbol\theta^\star),
$$

where $\mathbf G$ is positive definite and a certified lower eigenvalue bound
$\lambda_{\min}>0$ satisfies

$$
Q(\boldsymbol\theta)\geq\lambda_{\min}
\|\boldsymbol\theta-\boldsymbol\theta^\star\|_2^2.
$$

Then $\mathcal L(\boldsymbol\theta)\leq\mathcal L_{\min}+\epsilon$ implies

$$
\|\boldsymbol\theta-\boldsymbol\theta^\star\|_2
\leq r=\sqrt{\epsilon/\lambda_{\min}}.
$$

Intersecting the quadratic sublevel set with the frozen parameter box can only shrink
it, so the same enclosing ball remains valid. Apply this result to centers
$\boldsymbol\theta_E^\star$ and $\boldsymbol\theta_H^\star$ with radii $r_E$ and
$r_H$. For every feasible pair, the triangle inequality gives

$$
D=\|\boldsymbol\theta_E^\star-\boldsymbol\theta_H^\star\|_2
\leq r_E+\|\boldsymbol\theta_E-\boldsymbol\theta_H\|_2+r_H.
$$

Rearrangement followed by the infimum over feasible pairs proves

$$
\delta^\star\geq D-r_E-r_H.
$$

Consequently $D>r_E+r_H$ is a sufficient certificate of positive separation; it does
not rely on a failed search.

## Constructive compatibility case

Equal spectral weights on the complete six-point mesh
$k\in\{0,\pi/3,2\pi/3,\pi,4\pi/3,5\pi/3\}$ keep the represented
$R=0,\pm1,\pm2$ translations distinct and make the retained first-neighbor and
omitted second-neighbor Fourier columns orthogonal. The spectral and
operator sets both contain $(\theta_0,\theta_1)=(1,-1/4)$. This exact common witness
establishes $\delta^\ast=0$ for the frozen contract. It does not establish uniqueness,
equivalence of the losses, or compatibility under another threshold or model class.

## Certified separation case

Changing only the spectral training domain to
$k\in\{-\pi/3,0,\pi/3\}$ moves the exact spectral center to $(3/5,1/20)$ while
leaving the operator center at $(1,-1/4)$. Their distance is $1/2$. The restricted
spectral quadratic has minimum eigenvalue $(9-\sqrt{73})/6>91/1200$. The
corresponding admissible set lies within radius $37/1000$ of its center, while the
operator set lies within radius $11/1000$ of its center. Therefore

$$
\frac{113}{250}=0.452\leq\delta^\ast\leq\frac12=0.500.
$$

The upper bound is supplied by the feasible pair of centers. The lower bound is an
exact rational enclosure, not a conclusion drawn from optimization failure or plot
resolution.

## Evidence and limitations

The retained package contains the frozen input, protocol, result record, independent
verifier, boundary samples, figure, report, and checksum manifest. The verifier does
not import the result constructor and reconstructs the quadratic forms, thresholds,
common witness, radius inequalities, and separation bounds. Four disjoint reciprocal
points are withheld from both training sets; they diagnose generalization and do not
update either admissible set.

This demonstration is synthetic, scalar, one-dimensional, and restricted to a
singleton alignment family. It establishes both a compatible case and a certified
separated case only relative to their frozen contracts. It supplies no 3D or
material-specific evidence.
