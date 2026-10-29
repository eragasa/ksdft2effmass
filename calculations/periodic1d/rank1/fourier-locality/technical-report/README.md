# Rank-one Fourier-locality technical report

[`technical_report.tex`](technical_report.tex) is the comprehensive calculation-facing
scientific record for the controlled rank-one family. It is intentionally broader than
a journal-paper treatment: it records the exact parent and state spaces, scalar gauge
invariance, finite Fourier identities, interpolation and truncation theory, direct-fit
route, five internal benchmarks, complete production range table, diagnostics,
independent-verification inventory, literature position, publication relationship,
provenance, and explicit nonclaims.

The report is upstream supporting material for the scalar-control argument in the
Ragasa2026a scientific program. Publication prose should distill this record rather than
serve as its only technical authority. This relationship does not by itself modify the
publication allocation ledger or bind these provisional bytes into an evidence manifest.

The report embeds the verifier-authenticated review illustrations
[`rank1-fourier-locality.png`](rank1-fourier-locality.png) and
[`rank1-fourier-route-agreement.png`](rank1-fourier-route-agreement.png). The numerical
tables and figures remain non-retained development material. They are not a retained
execution, sealed evidence package, continuum claim, scientific validation, or
publication artifact.

## Build

Build outside the source tree:

```bash
mkdir -p /tmp/ksd-rank1-fourier-locality-report
latexmk -pdf -interaction=nonstopmode -halt-on-error \
  -outdir=/tmp/ksd-rank1-fourier-locality-report technical_report.tex
```

The source uses [`references.bib`](references.bib). The selected compiled
[`technical_report.pdf`](technical_report.pdf) is retained only as a review snapshot;
LaTeX auxiliary products remain untracked.

Retained calculation outputs, publication-manifest changes, and evidence promotion each
require their own reviewed and authorized lifecycle actions.
