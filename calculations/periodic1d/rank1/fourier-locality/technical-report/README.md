# Technical report

[`technical_report.tex`](technical_report.tex) records the frozen finite control and a
provisional, non-retained local calculate → independently verify → authenticated render
result. It embeds the authenticated review illustrations
[`rank1-fourier-locality.png`](rank1-fourier-locality.png) and
[`rank1-fourier-route-agreement.png`](rank1-fourier-route-agreement.png). The numerical
tables and figures are not a retained execution, sealed evidence package, continuum
claim, scientific validation, or publication artifact.

Build outside the source tree with:

```bash
mkdir -p /tmp/ksd-rank1-fourier-locality-report
latexmk -pdf -interaction=nonstopmode -halt-on-error \
  -outdir=/tmp/ksd-rank1-fourier-locality-report technical_report.tex
```

The selected compiled `technical_report.pdf` is retained only as a review snapshot.
LaTeX auxiliary products remain untracked. Retained calculation outputs require a
separately authorized direct execution and the repository's provenance gates.
