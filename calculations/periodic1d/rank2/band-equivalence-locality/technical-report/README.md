# Technical report

This directory owns the calculation-facing technical report for the periodic-1D
rank-two band-equivalence/locality study. It separates model definition, simulation,
verification, analysis, limitations, and provenance from the shorter publication
narrative in `Ragasa2026a`.

The report is a migration draft. It does not establish retained evidence, scientific
validation, submission, publication, or priority.

Build from this directory with:

```console
latexmk -pdf -interaction=nonstopmode -halt-on-error technical-report.tex
```

The selected compiled `technical-report.pdf` is retained as a review snapshot. It is
not evidence, scientific validation, or a publication; all LaTeX auxiliary products
remain untracked.
