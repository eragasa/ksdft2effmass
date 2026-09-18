# Corrected independent Wannier90 rank-three comparison

## Status

This is a calculated illustrative synthetic comparison. The first authorized
preprocessing attempt failed and remains retained in `wannier90-execution.json`.
The separately authorized balanced-embedding attempt completed under
`RM-PERIODIC-2D-WANNIER90-EMBEDDING-RETRY-HC04`. It is not a material
calculation, production workflow, scientific validation, or uncertainty
quantification.

## Input and execution

The represented parent is

$$
H=-\nabla^2+0.5\cos x+0.5\cos y+0.15\cos x\cos y
$$

with $a=2\pi$, $G=1$, plane-wave cutoff $P=3$, a
$15\times15\times1$ reciprocal mesh, and the isolated lowest three bands. The
centered Gaussian $s$, $p_x$, and $p_y$ projections have minimum retained
singular value 0.886. No disentanglement is used.

The corrected auxiliary cell changes only the inactive lattice length from 1 to
15. Wannier90 3.1.0 then identifies six axial neighbors. Preprocessing completes
in 0.28 s with 22.6 MB maximum resident memory. Localization completes in
0.47 s with 27.3 MB and satisfies the $10^{-12}$ spread criterion over five
iterations at iteration 94. Total external output is 1.40 MB.

## Deterministic direct-gauge correction

Independent comparison exposed a provisional direct-gauge error: multiplying
the square projected-trial overlap by its full inverse returned the raw
eigengauge. The corrected direct frame uses the polar factor
$A(A^\dagger A)^{-1/2}$. The primary direct runner evaluates it by SVD; its
independent verifier uses a Hermitian eigendecomposition. The full disposition
is retained in `composite-projected-gauge-correction.md`.

## Calculated comparison

Wannier90 reports native active-plane centers modulo one cell of approximately
$(0.366,0.367)$, $(0.673,0.463)$, and $(0.463,0.673)$. Its native Berry-link
spreads are $0.2072a^2$, $0.2509a^2$, and $0.2513a^2$, totaling
$0.7094a^2$. These native values are not directly substituted for the
finite-supercell estimator used by the direct route. Reconstructing the
Wannier90 frame on the same $128^2$ FFT grid gives spreads $0.2358a^2$,
$2.9532a^2$, and $2.9469a^2$, totaling $6.1359a^2$. Reconstructing the corrected
direct projected frame from the same external mesh gives $24.5163a^2$ under
that estimator, so the commensurate optimized-to-direct ratio is 25.03%. The
separate centered-mesh direct route gives $24.8951a^2$. The difference between
the
native $0.7094a^2$ and common-estimator $6.1359a^2$ values is retained as an
estimator/discretization difference, not a localization gain.

The frames span the same retained subspace within
$2.65\times10^{-10}$. Their raw represented Hamiltonians differ by
$1.14E_G$, but exact $k$-dependent unitary alignment reduces the operator defect
to $3.57\times10^{-10}E_G$. A bounded search over independent integer orbital
translations in $[-1,1]^2$ and one constant orbital unitary leaves a per-orbital
frame RMS defect of 1.188. Thus the optimized gauge is not merely a translated
or constantly rotated direct projected gauge.

At squared-radius shell 18, the omitted matrix-hopping norm is
$9.92\times10^{-3}E_G$ for Wannier90 versus $1.38\times10^{-2}E_G$ for the
direct projected gauge. At shell 50, the corresponding values are
$2.72\times10^{-4}E_G$ and $5.90\times10^{-3}E_G$. Native `_hr.dat` blocks
reconstruct the external mesh within $3.06\times10^{-5}E_G$ in maximum
Frobenius norm and $2.23\times10^{-5}E_G$ spectrally; this is retained as
six-decimal serialization error, not hopping truncation.

![Corrected external localization and hopping comparison.](wannier90-balanced-summary.png)

## Independent verification

`verify_wannier90_balanced.py` does not import the extractor. In native mode it
verifies all external file identities; in portable mode it consumes the compact
extracted fixture retained in the result. Both modes independently reconstruct:

- the plane-wave parent through explicit reciprocal-index loops;
- the direct polar frame through a Hermitian inverse square root;
- subspace and represented-operator defects;
- the bounded translation-plus-constant alignment search;
- native hopping blocks and mesh reconstruction;
- shell-tail norms;
- native convergence and active-plane spread; and
- the common-grid finite-supercell densities, centers, and spreads.

It reports `periodic_2d_wannier90_balanced_verification=PASS`.

## Limitations

The auxiliary third direction exists only to satisfy Wannier90's
three-dimensional interface. Its overlap is fixed to one, and only active-plane
centers and spreads are interpreted. The calculation covers one finite parent,
one reciprocal mesh, one isolated rank-three group, and one trial family. The
later bounded study in `wannier90-study-report.md` finds nonmonotone cutoff and
mesh behavior and an alternative basin at auxiliary length $c=18$; therefore
no converged or embedding-independent localization claim is supported. Neither
record establishes a general localization theorem, material adequacy, or
transferability.

## Verification

From `python/`, the repository-only portable verification is:

```bash
uv run python \
  ../calculations/research-monograph/periodic-2d/verify_wannier90_balanced.py \
  ../calculations/research-monograph/periodic-2d/wannier90-balanced-result.json \
  --portable

uv run --extra notebooks python \
  ../calculations/research-monograph/periodic-2d/plot_wannier90_balanced.py \
  ../calculations/research-monograph/periodic-2d/wannier90-balanced-result.json \
  --output ../calculations/research-monograph/periodic-2d/wannier90-balanced-summary.png
```

The protected executable stages are not repeated by these commands. Portable
mode reproduces the numerical comparisons but does not re-parse native formats
or execution logs. With the retained external run at its recorded path,
omitting `--portable` adds those identity, format, and log checks.
