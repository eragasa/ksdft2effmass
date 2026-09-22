# Composite projected-gauge deterministic correction

## Disposition

During independent reconstruction of the corrected Wannier90 comparison, a
deterministic implementation error was found in the provisional direct
rank-three composite result. The previously generated composite result and
figure were not human accepted or committed. They are superseded by the
regenerated `composite-result.json` and `composite-summary.png`.

## Error

Let $A_{mn}(\mathbf k)=\langle\psi_{m\mathbf k}|g_{n\mathbf k}\rangle$ be the
square, full-rank trial-overlap matrix. The provisional runner formed

$$
|u^{\mathrm{old}}\rangle
 = |\psi\rangle A A^{-1}=|\psi\rangle,
$$

because it multiplied the projected trials by the full inverse of $A$. The
result therefore returned the raw eigengauge rather than the declared
symmetrically orthonormalized projected gauge. The first verifier repeated the
same algebra, so agreement between those two implementations did not expose the
semantic error.

## Correction

For an SVD $A=L\Sigma R^\dagger$, the corrected projected frame is the polar
factor

$$
|u^{\mathrm{proj}}\rangle
 = |\psi\rangle A(A^\dagger A)^{-1/2}
 = |\psi\rangle LR^\dagger.
$$

The runner now uses the SVD polar factor. The independent verifier reconstructs
$(A^\dagger A)^{-1/2}$ through a Hermitian eigendecomposition rather than
copying the runner route. Probability content identities are rounded to 12
binary64 decimal digits so route-level roundoff does not create false digest
mismatches; centers, norms, and spreads remain checked numerically.

## Effect on calculated diagnostics

The parent spectrum, minimum exterior gap, projection singular values,
projectors, zero total Chern diagnostic, and gauge-invariant Wilson spectra are
unchanged within their retained tolerances. Gauge-coordinate diagnostics change
materially:

- direct projected total spread: $90.87a^2 \rightarrow 24.90a^2$;
- rough-gauge total spread: $103.01a^2 \rightarrow 67.70a^2$;
- direct radius-18 omitted hopping norm:
  $1.26\times10^{-2}E_G \rightarrow 1.38\times10^{-2}E_G$; and
- rough radius-18 omitted hopping norm:
  $4.87\times10^{-1}E_G \rightarrow 5.25\times10^{-1}E_G$.

The corrected result still demonstrates the intended distinction: invariant
subspace and Wilson diagnostics survive the internal gauge attack, while spread
and hopping locality worsen. The correction also provides the proper direct
projected baseline for the independent Wannier90 comparison.
