# QHO1D technical report

`technical_report.tex` is the maintained calculation-facing report source. Its
bibliography and three figure inputs are report-local, so the report builds without
files outside this directory:

```console
latexmk -pdf -interaction=nonstopmode -halt-on-error technical_report.tex
```

`technical_report.pdf` is a retained review snapshot, not a sealed evidence package,
scientific validation, or a publication. LaTeX auxiliary products remain ignored.

The local figures were copied from the independently verified unsealed execution
`../executions/direct-spatial-truncation-3x3x3/`, whose result SHA-256 is
`83c420ccd365bfba23401b98069566625049bd18dfac47568b006e848176993b`:

| figure | SHA-256 |
|---|---|
| `qho1d-eigenstates.png` | `d016e16a6ecc2eea216a8e329347f1c878febb7839c096384e2009c5cb328ca7` |
| `qho1d-eigenstate-distortion.png` | `792b8a6b80806f62efd1b6f18562d7fa21d9b76792b15c97725e744076508a66` |
| `qho1d-diagnostics.png` | `47fc9084f3c409506befc847fbdce752f31452cdd5df8cd58b5fcf19a4cc5441` |

The retained PDF SHA-256 is
`6289bdd96c873ef9c8bea9d6159fafa4790d2e8462510fa59391556bbed9bb78`.

The predecessor under `../development_report/` remains unchanged as a retained review
snapshot. Its generated development result is not the source contract for the direct
successor lifecycle.
