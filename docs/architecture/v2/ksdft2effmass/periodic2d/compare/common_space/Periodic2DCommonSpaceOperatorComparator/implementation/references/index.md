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
| Discrete orthogonality and alias prerequisite | Project specification and finite algebra | Cooley–Tukey citation does not prove this implementation |
| Centered-difference dispersion | Project specification and independent analytic test | No continuum acceptance threshold |
| Software correctness | Mapped software/numerical tests | Citations are not verification evidence |

## Navigation

- [Comparator contract](../../index.md)
- [Implementation](../index.md)
- [Mathematics and physics](../mathematics/index.md)
- [Verification strategy](../testing/index.md)
