# Gauge-Constrained Locality

> Status: Proposed proof material. Structural decomposition does not establish mathematical correctness, numerical verification, scientific validation, or human acceptance.

## 7. The next genuinely nontrivial issue: locality is not gauge invariant

After establishing diagram-level equivariance, the next important result concerns localization and truncation.

A real-space truncation operator might be written as

$$
\mathcal T_R[H](\mathbf R')

\begin{cases}
H(\mathbf R'), & |\mathbf R'|\leq R,\
0, & |\mathbf R'|>R.
\end{cases}
$$

Under a general $\mathbf k$-dependent gauge,

$$
H'(\mathbf k)

G^\dagger(\mathbf k)H(\mathbf k)G(\mathbf k),
$$

the Fourier-transformed operator may mix different lattice vectors. Therefore, in general,

$$
\mathcal T_R!\left[\rho_G(H)\right]
\neq
\rho_G!\left(\mathcal T_R[H]\right).
$$

Real-space truncation is not equivariant under arbitrary $\mathbf k$-dependent gauges.

This is likely the first result in the sequence that is scientifically substantive rather than merely formal.

It implies that quantities such as

- hopping range;

- neighbor-shell weight;

- orbital-block locality;

- apparent decay length;

- truncation error;


are properties of an operator **together with a chosen localized gauge**, not of the abstract operator alone.

## 8. This motivates a gauge-constrained locality theorem

The next publishable proposition could take the form:

> Real-space locality diagnostics are invariant under site-local, lattice-periodic orbital rotations, but not under arbitrary $\mathbf k$-dependent gauge transformations.

For a $\mathbf k$-independent unitary $G$,

$$
H'(\mathbf R)

G^\dagger H(\mathbf R)G.
$$

Then each lattice vector remains separate, and

$$
|H'(\mathbf R)|_F

|H(\mathbf R)|_F.
$$

Therefore shell-resolved Frobenius weights such as

$$
w_n

\left(
\sum_{\mathbf R\in\mathcal S_n}
|H(\mathbf R)|_F^2
\right)^{1/2}
$$

are invariant under a global orbital rotation.

By contrast, for $\mathbf k$-dependent $G(\mathbf k)$, different $\mathbf R$ blocks mix, and $w_n$ is not invariant.

This gives a precise boundary between:

- acceptable residual diagnostics after Wannier-gauge alignment; and

- quantities that cannot be claimed as intrinsic operator observables.


## 9. The best immediate proof sequence

The most coherent continuation is:

### Proposition 1 — Gauge equivariance of aligned subtraction

Prove that projection, identification, pullback, and subtraction yield a covariant impurity operator.

### Proposition 2 — Gauge invariance of the path residual

Prove that the norm of the difference between two equivariant reduction paths is independent of the initial retained-basis gauges.

### Proposition 3 — Non-equivariance of real-space truncation

Show that arbitrary $\mathbf k$-dependent gauges generally do not commute with truncation by neighbor shell or spatial range.

### Proposition 4 — Restricted invariance under lattice-local rotations

Show that shell-resolved Frobenius diagnostics remain invariant under $\mathbf k$-independent unitary rotations of the local orbital basis.

### Theorem — Well-posed operator-path comparison

State that the operator-path consistency test is coordinate independent provided:

1. retained spaces are identified covariantly;

2. compared outputs are placed in a common gauge;

3. residuals use unitarily invariant norms;

4. locality diagnostics are evaluated only after fixing an admissible localized gauge.


## 10. The resulting scientific claim

The line of reasoning then supports a stronger claim than simply “the matrices are gauge covariant”:

> Operator-level comparisons between first-principles, Wannier, and parameterized tight-binding reductions are well posed only after separating coordinate-invariant operator discrepancies from gauge-dependent localization and truncation effects.

That is the right bridge from elementary gauge bookkeeping to the substantive issue in your program:

$$
\boxed{
\text{Is disagreement caused by physics/model reduction,}
\quad
\text{or merely by representation?}
}
$$

The most valuable next section is therefore **“Gauge equivariance of the reduction diagram and the gauge dependence of locality.”**
