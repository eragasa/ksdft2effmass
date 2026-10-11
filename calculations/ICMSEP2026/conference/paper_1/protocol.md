# Direct admissible-set demonstration protocol

## Evidence boundary

This protocol governs a calculated, controlled one-dimensional demonstration for
Conference Paper 1 at ICMSEP 2026. It uses an analytically tractable synthetic scalar
periodic Hamiltonian. It is not a material calculation, uncertainty quantification,
semiconductor validation, or evidence about silicon. It does not execute Quantum
ESPRESSO, Wannier90, VASP, or ABINIT.

## Frozen parent and candidate class

The unit convention is a lattice period of $2\pi$, reciprocal period one, and
$E_G=1$. The represented parent is

$$
E_{\rm ref}(k)=a+2b\cos k+2c\cos 2k,
\qquad (a,b,c)=\left(1,-\frac14,\frac1{10}\right).
$$

Its real-space coefficients are $h_0=a$, $h_{\pm1}=b$, and $h_{\pm2}=c$.
The deliberately restricted candidate class is

$$
E_{\boldsymbol\theta}(k)=\theta_0+2\theta_1\cos k,
$$

with $0\leq\theta_0\leq3/2$ and $-3/4\leq\theta_1\leq1/2$. Canonical parameter
scales and weights are both one, so the declared reduced-parameter metric is ordinary
Euclidean distance in $(\theta_0,\theta_1)$ coordinates. The omitted second-neighbor
coefficient makes model-class error explicit.

## Losses, alignment, and thresholds

The spectral loss is the equal-weight mean squared energy residual on the declared
training points. Weights sum to one and the normalization scale is $E_G=1$; it is a
frozen nondimensionalization, not an estimated standard deviation or uncertainty.

The operator domain is $\mathcal S_H=\{-2,-1,0,1,2\}$ with unit shell weights. The
alignment family is the singleton identity because the model is scalar with one fixed
orbital coordinate. Therefore this controlled calculation does not invoke or test a
nonconvex gauge-alignment optimizer. The globally normalized operator loss is

$$
\mathcal L_H(\boldsymbol\theta)=
\frac{(\theta_0-a)^2+2(\theta_1-b)^2+2c^2}
{a^2+2b^2+2c^2}.
$$

The global loss is accompanied by translation-resolved residuals so that small blocks
cannot disappear behind the aggregate normalization.

The exact analytic minimum of each frozen loss is derived before either set is mapped.
Each admissibility threshold is that minimum plus the fixed excess-loss budget
$\epsilon=10^{-4}$. This is a benchmark-design resolution, not a confidence level or
physical uncertainty. The input file freezes the rule and all model data.

## Compatible complete-mesh case

The spectral training mesh is
$k\in\{0,\pi/3,2\pi/3,\pi,4\pi/3,5\pi/3\}$ with equal weights. On this
complete six-point mesh, the represented translations $R=0,\pm1,\pm2$ are distinct,
and the first- and second-neighbor Fourier columns are orthogonal. The spectral set and operator set therefore have the common
center $(a,b)=(1,-1/4)$. The calculation must retain that point as an exact common
feasible witness. This establishes compatibility only for the frozen class, losses,
thresholds, alignment family, and finite domains; it does not establish uniqueness or
operator equivalence.

## Separated restricted-training case

The spectral training points are $k\in\{-\pi/3,0,\pi/3\}$. The two-parameter
candidate can absorb the omitted second-neighbor term exactly on these restricted
points, moving the spectral-loss center to $(3/5,1/20)$. The operator-loss center
remains $(1,-1/4)$.

The separation certificate uses exact rational inequalities, not failed numerical
search:

1. the center distance is exactly $1/2$;
2. the restricted spectral quadratic has minimum eigenvalue
   $(9-\sqrt{73})/6>91/1200$ because $(1709/200)^2>73$;
3. the spectral set lies within radius $37/1000$ of its center;
4. the operator set lies within radius $11/1000$ of its center; and
5. the reverse triangle inequality gives
   $\delta^\ast\geq1/2-37/1000-11/1000=113/250=0.452$.

The two centers are feasible and are separated by $1/2$, giving the feasible upper
bound $\delta^\ast\leq0.500$. A positive lower bound therefore certifies separation
for this frozen case.

## Withheld role

Both cases use $k\in\{-5\pi/6,-\pi/6,\pi/6,5\pi/6\}$ only as withheld diagnostics.
These points do not define either admissible set, do not change a threshold, and do not
update a witness or certificate. The separated case is expected to show that an exact
fit on a restricted training set need not generalize.

## Reproduction and independent verification

Run from the repository root:

```bash
python/.venv/bin/python calculations/ICMSEP2026/conference/paper_1/run.py
python/.venv/bin/python calculations/ICMSEP2026/conference/paper_1/verify_result.py
```

`verify_result.py` does not import `run.py`. It reconstructs the exact quadratic forms,
centers, thresholds, witness losses, rational radius inequalities, and separation
bounds from `input.json` and compares them with `result.json`. The plotted boundary
samples are illustrative only; the intersection and separation dispositions come from
the exact witness and rational certificate.
