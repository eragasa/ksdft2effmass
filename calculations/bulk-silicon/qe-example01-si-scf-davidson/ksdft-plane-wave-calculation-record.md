# Kohn–Sham plane-wave calculation record

**Status:** retained software-verification record; not numerical verification,
scientific validation, convergence acceptance, uncertainty quantification, or
human acceptance.

The canonical JSON was constructed from the exact external QEXSD artifact
`/Users/eugene/projects/q-e-qe-7.2/tempdir/silicon.save/data-file-schema.xml`
(SHA-256 `2ad68bf1f16d6fda3873f5967677a81e81f16a9f88a797701134c0e5fecdd1d9`,
55,068 bytes) through the explicit parse-then-construct boundary.

Direct lattice vectors and Cartesian atomic positions are in bohr. The raw
reciprocal coefficients and raw Cartesian $k$-point coordinates are
dimensionless coefficients in units of $2\pi/a_{\mathrm{lat}}$, with
$a_{\mathrm{lat}}=10.2$ bohr; physical values are retained in bohr$^{-1}$.
The direct and physical reciprocal matrices satisfy
$A B_{\mathrm{physical}}^{\mathsf T}=2\pi I$ with the deterministic absolute
componentwise residual bound $10^{-12}$. The retained irreducible-zone weights
sum to 2.0 and are marked `sum_to_two`.

Eigenvalues and total energy use the concrete unit hartree. Spin-resolved arrays,
energy reference, basis identity, retained subspace, gauge, and phase convention
remain explicitly unavailable. Kohn–Sham eigenvalues are observations, not a
complete many-body spectrum or a uniquely identified basis-independent operator.
