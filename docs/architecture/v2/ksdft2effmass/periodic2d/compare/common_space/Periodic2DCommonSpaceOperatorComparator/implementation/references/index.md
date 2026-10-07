# `Periodic2DCommonSpaceOperatorComparator` references and provenance

## Repository authority

The authoritative software and mathematical contract is
`specification/ksdft2Effmass.periodic2d-common-space-comparison.v1.md`. The exact
period-`2*pi` cell, reciprocal-index order, coordinate-grid order, sampling-map
orientation, normalization, transport direction, difference sign, diagnostics, range
failures, and claim boundaries are repository-defined conventions. They are not taken
verbatim from an external paper.

## Historical physics context

F. Bloch, “Über die Quantenmechanik der Elektronen in Kristallgittern,” *Zeitschrift
für Physik* **52**, 555–600 (1929), DOI
[10.1007/BF01339455](https://doi.org/10.1007/BF01339455), is cited for historical
context around Bloch-form states in periodic potentials. It does not specify this
finite cosine parent, the software's seam orientation, the map normalization, or any
numerical acceptance criterion.

The comparator uses one fixed reduced Bloch momentum and samples modes
$e^{i(\boldsymbol\kappa+\mathbf n)\cdot\mathbf r}$. The citation does not establish
that the toy model is physically adequate for a material or that a finite cutoff/grid
pair is converged.

## Discrete-Fourier context

J. W. Cooley and J. W. Tukey, “An Algorithm for the Machine Calculation of Complex
Fourier Series,” *Mathematics of Computation* **19**, 297–301 (1965), DOI
[10.1090/S0025-5718-1965-0178586-1](https://doi.org/10.1090/S0025-5718-1965-0178586-1),
is retained as historical discrete-Fourier context. This implementation does not use a
Cooley–Tukey FFT algorithm: it evaluates phases directly, forms a Kronecker product,
and performs dense matrix multiplication. The reference therefore does not validate
algorithmic complexity, rounding error, alias handling, or implementation correctness.

## Claim-to-source boundary

| Claim | Authority | Excluded inference |
|---|---|---|
| Exact sampling equation and ordering | Project specification | Not attributed to either historical paper |
| Bloch-momentum interpretation | Project specification, with Bloch paper as historical context | No material or convergence validation |
| DFT orthogonality, fixed-domain column isometry, and square unitarity | Project specification, finite scalar geometric sums, machine-readable qualified record, independently reviewed disposition, and fixed-domain qualification tests | Cooley–Tukey citation does not prove the implementation; rectangular domains claim only column isometry and no domain implies potential-transfer alias freedom |
| Centered-difference dispersion | Project specification, machine-readable qualified record, independently reviewed disposition, and direct-stencil qualification test | No continuum acceptance threshold or convergence claim |
| Resolved cosine Fourier transfers for `M=1,N=7` | Project specification, explicit harmonic expansion, machine-readable qualified record, independently reviewed disposition, and transfer/alias tests | Separate from column orthogonality; no arbitrary-potential or general alias-free claim |
| Software correctness | Mapped software tests | Software evidence is separate from bounded numerical consumers; the latter become accepted numerical-verification evidence only through effective reviewed-revision dispositions and the exact proposal acceptance gate |

## Navigation

- [Comparator contract](../../index.md)
- [Implementation](../index.md)
- [Mathematics and physics](../mathematics/index.md)
- [Verification strategy](../testing/index.md)
