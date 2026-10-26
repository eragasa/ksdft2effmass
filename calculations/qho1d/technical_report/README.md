# QHO1D technical report

`technical_report.tex` is the maintained calculation-facing report source. Its
bibliography and three figure inputs are report-local, so the report builds without
files outside this directory:

```console
latexmk -pdf -interaction=nonstopmode -halt-on-error technical_report.tex
```

`technical_report.pdf` is a retained review snapshot, not a sealed evidence package,
scientific validation, or a publication. LaTeX auxiliary products remain ignored.

The local figure bytes are exact copies from the independently verified unsealed
semantic-section execution
`../executions/direct-spatial-truncation-3x3x3-sections/`, whose result SHA-256 is
`df3fd9f9cccf1f2cdcde200537a22064e6925498da7c738ffbfbc4bd5205e1b0`:

| figure | SHA-256 |
|---|---|
| `qho1d-eigenstates.png` | `c204502198311b93afd1d608732d2d4cfae8322b6da657a17acfab3cda1eca4e` |
| `qho1d-eigenstate-distortion.png` | `85d6ee44da149d4f10f84ed89f1875899a1df770790ec139fe214646b0ff6fbf` |
| `qho1d-diagnostics.png` | `e52b4c85edad2f2c6073924afd00e68a5f07f5fe1e72b082da885b98e5aac5fb` |

The maintained report now uses the semantic-section successor result
`../executions/direct-spatial-truncation-3x3x3-sections/results/result.json`, SHA-256
`df3fd9f9cccf1f2cdcde200537a22064e6925498da7c738ffbfbc4bd5205e1b0`. Its
scientific fields are exactly equal to the earlier result; the JSON identity differs
because cases are grouped into representation, alignment, Hamiltonian-comparison, and
residual sections.

The report also evaluates the direct typed result with
`Qho1dCrossGridAnalyzer` and `Qho1dCrossGridVerifier`. The resulting 18
adjacent-grid comparisons and 90 passing derivation checks are post-analysis of the
retained case matrices. They are not embedded in or used to rewrite either execution,
and they are not continuum-error estimates.

The retained nine-page PDF SHA-256 is
`80e71530cf54f897a39c30b34ef75603029aa2dad23a86f0ab582736eed9a9b0`.

The earlier flat-case direct execution and its report snapshot beneath
`../executions/direct-spatial-truncation-3x3x3/` remain byte-exact because the research
monograph consumes them. The older JSON-authored development implementation and report
were removed after migration; their Git-history locator and qualification are recorded
in the Architecture v3 QHO1D legacy-disposition page.
