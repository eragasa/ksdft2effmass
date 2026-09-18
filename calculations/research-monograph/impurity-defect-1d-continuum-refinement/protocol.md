# Continuum-refinement protocol for the synthetic 1D defect

## Evidence status and question

This deterministic experiment produces **synthetic test data** and software/numerical-verification evidence. It asks whether the accepted scalar lattice parent and a parabolic comparator approach a stable bounded comparison when continuum discretization, finite domain, lattice supercell, represented lattice scale, and defect width are varied independently.

The exercise does not establish an asymptotic theorem, a silicon impurity model, scientific validation, transferability, or uncertainty quantification.

## Why this is a follow-on rather than a repeated calculation

The accepted defect-1D package compared lattice and parabolic dispersions on one fixed 128-point band-limited grid while changing Gaussian width. It explicitly declined a continuum-crossover claim because grid, domain, image, and profile effects were not independently refined. This package retains that scan as provenance but introduces four separate refinement axes and a frozen multi-metric crossover rule.

## Frozen represented parent

`input.json` identifies the accepted periodic-1D, defect-1D, and analytical-oracle results by SHA-256. The scalar hopping coefficients $t_R$ define

$$
E_{\mathrm{lat}}(k)=\sum_R t_R e^{2\pi i kR},
$$

with lower edge $E_0=\sum_R t_R$ and parabolic coefficient

$$
\alpha=-\frac12\sum_R(2\pi R)^2t_R
       =0.6519378386943853\,E_G a_{\mathrm{ref}}^2.
$$

Every comparison uses centered periodic Fourier modes ordered by increasing integer label. Energy is measured in $E_G$ and length in the reference period $a_{\mathrm{ref}}$.

## Continuum and scaled-lattice operators

On a periodic physical domain of length $L$, Fourier mode $m$ has physical reduced wave number $q_m=m/L$. The continuum parent is

$$
E_{\mathrm{cont}}(q_m)=E_0+\alpha q_m^2.
$$

For represented lattice spacing $a$, the parent is scaled while preserving the same band-edge curvature:

$$
E_a(q_m)=E_0+
\frac{E_{\mathrm{lat}}(a q_m)-E_0}{a^2}.
$$

Thus $a\to0$ changes the represented lattice scale at fixed physical domain and profile rather than merely widening the defect on one lattice.

The periodized fixed-integrated Gaussian has magnitude $g=0.30E_Ga_{\mathrm{ref}}$ and Fourier coefficients

$$
V_\ell=-\frac{g}{L}
\exp\!\left[-2\pi^2\sigma^2\left(\frac{\ell}{L}\right)^2\right].
$$

The fixed-peak family replaces $g$ with
$V_0\sqrt{2\pi}\sigma$, where $V_0=0.12E_G$. The two normalizations remain separate because changing $\sigma$ changes their integrated strengths differently.

The continuum runner uses the analytical Fourier coefficients. The lattice route samples the periodized profile on its sites and transforms the diagonal site potential to Fourier coordinates. Comparisons therefore occur in the declared common Fourier ordering without silently identifying unequal spaces.

## Independent refinement axes

1. **Continuum mesh:** mode counts $64,96,128,192,256$ at fixed $L=64a_{\mathrm{ref}}$, $\sigma=2a_{\mathrm{ref}}$, and fixed-integrated normalization.
2. **Continuum domain:** $L/a_{\mathrm{ref}}=32,48,64,96,128$ at fixed spectral spacing $L/M=0.25a_{\mathrm{ref}}$ and fixed profile.
3. **Lattice supercell:** $N=32,48,64,96,128$ at fixed $a=a_{\mathrm{ref}}$ and fixed profile.
4. **Lattice scale:** $a/a_{\mathrm{ref}}=1,1/2,1/4,1/8$ at fixed $L=64a_{\mathrm{ref}}$, $\sigma=2a_{\mathrm{ref}}$, and fixed-integrated normalization.
5. **Profile width:** $\sigma/a_{\mathrm{ref}}=0.5,1,2,4,8,12$ at fixed $a=a_{\mathrm{ref}}$ and $L=128a_{\mathrm{ref}}$, with fixed-integrated and fixed-peak families evaluated separately.

No axis is used as a substitute for another.

## Separate metrics

For compatible lattice and continuum matrices, define

$$
D=H_a-H_{\mathrm{cont}},
$$

and let $P$ retain the physical low-momentum sector $|q|\leq0.25/a_{\mathrm{ref}}$. The experiment reports separately:

- relative lowest-state binding error;
- below-edge bound-state count;
- lowest-state projector Frobenius defect;
- compressed residual $\|PDP\|_2$;
- cross residual $\|PD(I-P)\|_2$; and
- lattice-state weight in the outer Brillouin region $|aq|\geq0.25$.

A small binding error cannot replace an operator, state, count, or high-momentum criterion.

## Frozen decisions

Numerical support passes require:

- final continuum-mesh binding change at most $10^{-10}E_G$;
- final continuum-mesh projector defect at most $10^{-6}$;
- final continuum-domain binding change and boundary probability at most $10^{-8}$; and
- final lattice-supercell binding change and boundary probability at most $10^{-8}$.

A lattice/continuum comparison passes only if all of the following hold:

- relative binding error $\leq10^{-3}$;
- projector defect $\leq10^{-2}$;
- compressed residual $\leq10^{-3}E_G$;
- cross residual $\leq10^{-3}E_G$;
- Brillouin-edge weight $\leq10^{-4}$; and
- below-edge bound-state counts agree.

A lattice-scale boundary is the largest tested spacing for which that point and every finer point pass. A profile-width crossover is the smallest tested width for which that point and every broader point pass. Failure of any criterion retains a no-crossover outcome; tolerances are not changed after evaluation.

## Independent implementation

`run_experiment.py` constructs the lattice matrix directly in Fourier coordinates. `verify_result.py` does not import the runner: it independently assembles the scaled hopping operator and sampled defect in site space, transforms that complete matrix into centered Fourier coordinates, reconstructs the continuum matrix entry by entry, and recalculates every spectrum, metric, criterion, boundary, and canonical matrix digest.

Canonical matrix digests round real and imaginary coordinates to $10^{-9}E_G$ solely so independently ordered floating-point constructions have the same content identity. Numerical comparisons retain unrounded matrices.

## Literature relationship

The calculation keeps distinct the finite-rank impurity method of Koster and Slater, weak band-edge homogenization studied by Hoefer--Weinstein and Duchêne--Vukićević--Weinstein, discrete-to-continuum operator convergence studied by Nakamura--Tadano, finite-volume bound-state precedents, and semiconductor central-cell or multivalley limitations. It does not claim that this finite represented parent satisfies the hypotheses of those theorems.

## Reproduction

From `python/`:

```bash
uv run python ../calculations/research-monograph/impurity-defect-1d-continuum-refinement/run_experiment.py \
  --input ../calculations/research-monograph/impurity-defect-1d-continuum-refinement/input.json \
  --output ../calculations/research-monograph/impurity-defect-1d-continuum-refinement/result.json

uv run python ../calculations/research-monograph/impurity-defect-1d-continuum-refinement/verify_result.py \
  --result ../calculations/research-monograph/impurity-defect-1d-continuum-refinement/result.json

uv run python ../calculations/research-monograph/impurity-defect-1d-continuum-refinement/plot_result.py \
  --result ../calculations/research-monograph/impurity-defect-1d-continuum-refinement/result.json \
  --output ../calculations/research-monograph/impurity-defect-1d-continuum-refinement/summary.png
```

Then run `sha256sum -c SHA256SUMS` from this directory.
