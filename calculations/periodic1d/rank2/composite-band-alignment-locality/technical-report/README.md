# Composite-band alignment and locality technical report

[`technical_report.tex`](technical_report.tex) is the comprehensive calculation-facing
scientific record for the direct rank-two finite control. It is intentionally broader
than publication prose. It records the literature position, exact parent and state
spaces, frame transport, Procrustes families, pointwise invariance results, Fourier
convolution mechanism, truncation noncommutation, cyclic-to-ordinary conversion,
separated interpolation/truncation/total Hamiltonian and spectral channels, Parseval
and spectral controls, seven complementary benchmarks, complete finite range study,
independent-verification scope,
historical M2 convention boundary, discussion, provenance, and explicit nonclaims.

Together with the rank-one Fourier-locality report, it supplies an upstream
mechanism-separation record for the scientific lineage surrounding Ragasa2026a: rank one
isolates spectral reduction without internal gauge action, while rank two activates a
momentum-dependent internal frame rotation at fixed retained projector and complete
spectrum. The current publication allocation ledger assigns this direct composite family
to Ragasa2026c rather than the active Ragasa2026a evidence graph. Changing that
allocation or binding these bytes into a publication manifest remains a separate
reviewed action.

The report embeds the authenticated review illustrations
[`rank2-composite-alignment.png`](rank2-composite-alignment.png) and
[`rank2-composite-locality.png`](rank2-composite-locality.png), and
[`rank2-composite-error-channels.png`](rank2-composite-error-channels.png).
[`render_review_figures.py`](render_review_figures.py) reproduces them by calculating the
frozen request in memory, independently verifying its exact typed result bytes, and
rendering only the authenticated projection. The script does not create an execution
directory or retained result.

## Regenerate review figures

From the repository Python environment:

```bash
cd python
uv run python \
  ../calculations/periodic1d/rank2/composite-band-alignment-locality/technical-report/render_review_figures.py
```

## Build

Build outside the source tree:

```bash
mkdir -p /tmp/ksd-rank2-composite-report
latexmk -pdf -interaction=nonstopmode -halt-on-error \
  -outdir=/tmp/ksd-rank2-composite-report technical_report.tex
```

The source uses [`references.bib`](references.bib). The selected
[`technical_report.pdf`](technical_report.pdf) is a review snapshot. The report, tables,
hashes, and figures remain provisional non-retained development material. They are not a
retained execution, sealed evidence package, continuum claim, uncertainty
quantification, material validation, publication artifact, or release.

Retained execution, publication-manifest changes, evidence promotion, and sealing each
require their own reviewed and authorized lifecycle actions.
