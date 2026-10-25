# Technical report

[`technical_report.tex`](technical_report.tex) is the pre-execution calculation-facing design note. It contains no numerical result or evidence claim.

Build outside the source tree with:

```bash
mkdir -p /tmp/ksd-rank1-fourier-locality-report
latexmk -pdf -interaction=nonstopmode -halt-on-error \\
  -outdir=/tmp/ksd-rank1-fourier-locality-report technical_report.tex
```

The selected compiled `technical_report.pdf` is retained as a review snapshot. It
remains a pre-execution design note, not numerical evidence, scientific validation, or
a publication; LaTeX auxiliary products remain untracked.
