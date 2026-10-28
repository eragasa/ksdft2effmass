# PIAB1D technical report

`technical_report.tex` is the maintained calculation-facing report source. Its
bibliography, review record, figure-generation sources, and retained static figures are
report-local.

The source was promoted from the historical duplicate development report. That
duplicate was removed after promotion; its exact tree identity and recovery revision are
recorded in `../legacy-retirement.md`. The maintained report is now authoritative.

Build the maintained report from this directory:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error technical_report.tex
```

The report-local ladder generator reads only the direct result after checking its
retained typed verification; the retained-dimension generator owns its explicitly
illustrative report calculation. Report-local figures are presentation copies and do not
create new independent scientific evidence. The compiled `technical_report.pdf` is a
review snapshot. It and ignored LaTeX intermediates are not retained calculation
evidence unless a later execution contract explicitly admits and checksums them.
