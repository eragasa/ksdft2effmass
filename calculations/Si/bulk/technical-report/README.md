# Technical report

[`technical-report.tex`](technical-report.tex) is the calculation-facing status and
design report for the bulk-silicon parent and reduction program. Its bibliography is
maintained in [`references.bib`](references.bib). The report is publication-independent
and may be cited by Paper D without transferring calculation identity.

Build outside the source tree with:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error \
  -outdir=/tmp/ksd-si-bulk-technical-report technical-report.tex
```

The selected compiled `technical-report.pdf` is retained as a review snapshot. It is
not retained calculation evidence, scientific validation, or a publication; LaTeX
auxiliary products remain untracked.

The detailed production-parent audit remains in
[`docs/computational/bulk-silicon-production-convergence-design.md`](../../../../docs/computational/bulk-silicon-production-convergence-design.md).
The separate external empirical development control and its source boundary are under
[`analysis/controls/vogl-sp3s-star/`](../analysis/controls/vogl-sp3s-star/). The report
does not duplicate retained result payloads, ingested source bytes, or historical
provenance bytes.
