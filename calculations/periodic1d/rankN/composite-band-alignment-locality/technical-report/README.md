# Technical report

[`technical_report.tex`](technical_report.tex) is the calculation-facing development report.

Build outside the source tree with:

```bash
mkdir -p /tmp/ksd-higher-rank-d1-report
latexmk -pdf -interaction=nonstopmode -halt-on-error \
  -outdir=/tmp/ksd-higher-rank-d1-report technical_report.tex
```

The selected compiled `technical_report.pdf` is retained as a review snapshot. It is
not retained numerical evidence, scientific validation, or a publication; LaTeX
auxiliary products remain untracked.
