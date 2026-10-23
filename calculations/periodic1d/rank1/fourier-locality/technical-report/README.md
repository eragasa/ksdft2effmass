# Technical report

[`technical_report.tex`](technical_report.tex) is the pre-execution calculation-facing design note. It contains no numerical result or evidence claim.

Build outside the source tree with:

```bash
mkdir -p /tmp/ksd-rank1-fourier-locality-report
latexmk -pdf -interaction=nonstopmode -halt-on-error \\
  -outdir=/tmp/ksd-rank1-fourier-locality-report technical_report.tex
```
