# PIAB1D technical report

`technical_report.tex` is the maintained calculation-facing report source. Its
bibliography, review record, figure-generation sources, and retained static figures are
report-local.

The source is initially byte-identical to the historical
`development_report/development_report.tex`; only the destination filename differs.
The historical report directory remains unchanged for retained provenance.

Build the maintained report from this directory:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error technical_report.tex
```

The generated PDF and LaTeX intermediates are not retained evidence unless a later
execution contract explicitly admits and checksums them.
