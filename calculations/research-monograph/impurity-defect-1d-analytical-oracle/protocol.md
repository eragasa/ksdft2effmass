# Analytical finite-rank oracle protocol

## Status and scope

This deterministic experiment produces **synthetic test data** and software/numerical-verification evidence. It constructs finite-rank defects on the accepted two-orbital one-dimensional represented parent and compares a Bloch-resolvent oracle with an independently assembled site-space eigensolve. It does not establish an infinite-system or continuum limit, a silicon impurity model, scientific validation, transferability, or uncertainty quantification.

## Frozen parent and represented space

`input.json` SHA-256-identifies the accepted composite `low_pair` parent, the accepted defect-1D result, and the accepted independent-route result. The parent retains hopping blocks $h_R\in\mathbb C^{2\times2}$ for $|R|\leq4$ in a periodic $N$-cell supercell at $K=0$. The canonical ordering is site-major with two orbitals per site and energy unit $E_G$.

The normalized local orbital vector is fixed before evaluation:

$$
u=
\begin{pmatrix}
\cos(0.41)\\
e^{0.37i}\sin(0.41)
\end{pmatrix},
$$

and $v=|0\rangle\otimes u$ is supported on site zero.

## Rank-one oracle

For positive magnitude $g$, the attractive rank-one defect and physical finite operator are

$$
V_g=-g|v\rangle\langle v|,
\qquad
H_g=H_0+V_g.
$$

For $E$ below the finite-host lower edge $E_{\min}$, $H_0-EI$ is positive and invertible. The matrix determinant lemma gives the secular condition

$$
0=1-g\langle v|(H_0-EI)^{-1}|v\rangle.
$$

The oracle does not diagonalize $H_g$. It evaluates the local resolvent directly from the primitive $2\times2$ Bloch fibers,

$$
G_N(E)=\frac1N\sum_{j=0}^{N-1}
 u^\dagger[H(k_j)-EI]^{-1}u,
\qquad
k_j=\frac{j}{N},
$$

and resolves the unique sign-changing root of $1-gG_N(E)$ on $E<E_{\min}$ by deterministic bisection. The root bracket, iteration count, and secular residual are retained.

The corresponding oracle vector is reconstructed without a defect-Hamiltonian eigensolve:

$$
|\psi_{\mathrm{or}}\rangle
\propto(H_0-EI)^{-1}|v\rangle.
$$

## Independent numerical route

The comparison route independently assembles the finite site-space parent from $h_R$, constructs $H_g$, and diagonalizes that full Hermitian matrix. It does not call the root resolver. The calculation compares:

- the oracle root with the lowest numerical eigenvalue;
- the finite-host edge from Bloch fibers with the site-space host edge;
- the below-edge eigenvalue count;
- the oracle eigen-equation residual;
- equal-rank spectral projectors; and
- single-state fidelity only for the nondegenerate rank-one cases.

This separation avoids presenting a duplicate full diagonalization as an analytical oracle.

## Parameter and finite-size sequence

The frozen sequence uses

$$
N\in\{16,24,32,48,64\},
\qquad
g\in\{0.02,0.08,0.20,0.50\}E_G.
$$

Every attractive case must have exactly one state below the finite-host lower edge. The sequence records finite-size dependence of the binding but does not claim convergence to an infinite or continuum system.

## Special controls

Four controls preserve boundaries that a scalar energy comparison would miss:

1. **Zero-coupling threshold:** $g=0$ has no isolated state below the host edge; an edge state is not counted as bound.
2. **Repulsive defect:** $+0.20|v\rangle\langle v|$ has no state below the lower edge. Positivity of $(H_0-EI)^{-1}$ makes its below-edge secular expression $1+gG_N(E)$ strictly positive.
3. **Spin-degenerate rank two:** tensoring the parent and rank-one defect with the two-dimensional spin identity gives a two-dimensional bound eigenspace. Comparison uses the rank-two projector, not arbitrary individual eigenvectors.
4. **Unequal rank:** comparing that numerical rank-two eigenspace with a rank-one oracle stops with `ANALYTICAL_ORACLE.EIGENSPACE_RANK_MISMATCH`; no projector defect or state fidelity is returned.

Generic spin degeneracy here is not explicit spin-orbit coupling or a relativistic calculation.

## Frozen acceptance rules

The retained tolerances are:

- root interval: $10^{-13}E_G$;
- secular residual: $10^{-11}$;
- oracle/numerical energy agreement: $10^{-11}E_G$;
- oracle eigen residual: $10^{-10}E_G$;
- projector agreement: $10^{-9}$; and
- bound-state edge margin: $10^{-10}E_G$.

Wrong types, missing sources, changed hashes, incomplete hopping ranges, unbracketed roots, unexpected bound-state counts, failed tolerances, or unequal projector ranks produce explicit errors or stopping records. These thresholds verify the finite synthetic calculation only.

## Independent verification

`verify_result.py` does not import `run_experiment.py`. It separately reloads the identified parent, reconstructs the fibers and site-space operators, resolves every root, rebuilds every oracle state and digest, recalculates the threshold, repulsive, degenerate, and unequal-rank controls, and checks every retained record.

## Reproduction

From `python/`:

```bash
uv run python ../calculations/research-monograph/impurity-defect-1d-analytical-oracle/run_experiment.py \
  --input ../calculations/research-monograph/impurity-defect-1d-analytical-oracle/input.json \
  --output ../calculations/research-monograph/impurity-defect-1d-analytical-oracle/result.json

uv run python ../calculations/research-monograph/impurity-defect-1d-analytical-oracle/verify_result.py \
  --result ../calculations/research-monograph/impurity-defect-1d-analytical-oracle/result.json

uv run python ../calculations/research-monograph/impurity-defect-1d-analytical-oracle/plot_result.py \
  --result ../calculations/research-monograph/impurity-defect-1d-analytical-oracle/result.json \
  --output ../calculations/research-monograph/impurity-defect-1d-analytical-oracle/summary.png
```

Then run `sha256sum -c SHA256SUMS` from this directory.
