# Conference paper 1: controlled-model methodology

This directory contains the working conference-paper draft:

> *Compatibility of spectral and operator reductions of periodic Hamiltonians:
> controlled one- and two-dimensional benchmarks*

## Files

- `manuscript.tex` — primary LaTeX manuscript source.
- `references.bib` — authoritative BibTeX database used by `manuscript.tex`.
- `manuscript.bbl` — generated numbered bibliography retained as a build fallback.
- `manuscript.pdf` — compiled working draft.
- `supplementary-material.tex`, `supplementary-material.bbl`, and
  `supplementary-material.pdf` — appendix-only extract containing Appendices S1,
  S2, S3, and S4.
- `appendices/*.tex` — separately maintained LaTeX appendices; the complete
  `manuscript.pdf` includes Appendices A, B, S1, S2, S3, and S4.
- `manuscript.md` and `appendices/*.md` — source-first Markdown counterparts.
- `evidence-ledger.md` — numerical-statement and figure-provenance crosswalk.

Build from this directory with:

```bash
latexmk -pdf manuscript.tex
latexmk -pdf supplementary-material.tex
```

The paper presents the general admissible-set framework and retained illustrative
numerical-verification results from the controlled 1D and 2D periodic programs. Those
results establish bounded software and numerical behavior only. They do not validate a
material, establish uncertainty quantification, or demonstrate transferability to
silicon.

The draft now includes a prospectively frozen isolated-band package at
[`calculations/ICMSEP2026/conference/paper_1/isolated-band/`](../../../../../calculations/ICMSEP2026/conference/paper_1/isolated-band/).
Its independent retained verification passes; this establishes bounded synthetic
numerical consistency only.

A second prospectively frozen synthetic package at
[`calculations/ICMSEP2026/conference/paper_1/multiband-alignment/`](../../../../../calculations/ICMSEP2026/conference/paper_1/multiband-alignment/)
adds a gapped rank-two parent, known nonidentity gauge attack, separate pointwise and
global-unitary alignment channels, gauge-resolved block hoppings, and disjoint withheld
diagnostics. Its independent reconstruction passes the frozen tolerance; it does not
establish a general alignment optimizer or material validity.

Supplementary Appendix S4 is a separate bridge to already retained synthetic
Wannier90 3.1.0 evidence. It is not part of M2, was not rerun for this paper, and does
not establish first-principles, material, optimizer, or convergence validity.

The draft also includes a direct low-dimensional admissible-set demonstration with an
exact common witness and a certified separated case. Its retained calculation package
is [`calculations/ICMSEP2026/conference/paper_1/`](../../../../../calculations/ICMSEP2026/conference/paper_1/),
and its bounded interpretation is documented in
[`appendices/B-direct-admissible-set-demonstration.md`](appendices/B-direct-admissible-set-demonstration.md).
The separate appendix index is [`appendices/README.md`](appendices/README.md).

No submission, publication, release, or protected calculation is authorized by this
working package.
