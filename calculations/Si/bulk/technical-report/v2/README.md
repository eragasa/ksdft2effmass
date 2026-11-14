# Technical report v2

This version reorganizes the retained bulk-silicon Wannier reduction evidence into a
conventional scientific narrative:

1. introduction;
2. background;
3. methodology;
4. results; and
5. discussion.

Unlike the calculation-status report in the parent directory, v2 focuses on the actual
bounded result: gauge-dependent real-space locality, literal and refitted native-shell
compression, broader frozen-model fidelity, and conduction/degenerate-valence band-edge
consequences. It does not present the `C6-B20-W21` source as a validated silicon model.

Build outside the source tree with:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error \
  -outdir=/tmp/ksd-si-bulk-technical-report-v2 technical-report-v2.tex
```

The selected `technical-report-v2.pdf` is a review snapshot, not retained numerical
evidence or publication-qualified validation. Numerical provenance remains with the
calculation owners under `calculations/Si/bulk/analysis/`.
