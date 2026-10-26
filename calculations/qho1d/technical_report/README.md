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
PhysKit-norm execution
`../executions/direct-spatial-truncation-3x3x3-physkit-norms/`, whose result SHA-256 is
`cb5469d2c4959dd6d7a9474d12252f0a32469abfbf2b54667a03bc9ab6e62e18`:

| figure | SHA-256 |
|---|---|
| `qho1d-eigenstates.png` | `c204502198311b93afd1d608732d2d4cfae8322b6da657a17acfab3cda1eca4e` |
| `qho1d-eigenstate-distortion.png` | `85d6ee44da149d4f10f84ed89f1875899a1df770790ec139fe214646b0ff6fbf` |
| `qho1d-diagnostics.png` | `e52b4c85edad2f2c6073924afd00e68a5f07f5fe1e72b082da885b98e5aac5fb` |

The maintained report uses the semantic-section result
`../executions/direct-spatial-truncation-3x3x3-physkit-norms/results/result.json`,
SHA-256
`cb5469d2c4959dd6d7a9474d12252f0a32469abfbf2b54667a03bc9ab6e62e18`.
Its production Frobenius diagnostics use the canonical PhysKit owner. Relative to the
prior semantic-section execution, every non-norm case array and selected-state value is
exactly equal. Reduction-order differences affect 31 stored case metrics across seven
fields; the largest absolute difference is `4.440892098500626e-16`.

The report also evaluates the direct typed result with
`Qho1dCrossGridAnalyzer` and `Qho1dCrossGridVerifier`. The resulting 18
adjacent-grid comparisons and 90 passing derivation checks are post-analysis of the
retained case matrices. They are not embedded in or used to rewrite either execution,
and they are not continuum-error estimates.

The retained ten-page PDF SHA-256 is
`7acd12af1ed1fd170ed423049ac191a0bbffb71f9e4a13c45eadf98cac900633`.

The earlier flat-case direct execution and its report snapshot beneath
`../executions/direct-spatial-truncation-3x3x3/` remain byte-exact because the research
monograph consumes them. The older JSON-authored development implementation and report
were removed after migration; their Git-history locator and qualification are recorded
in the Architecture v3 QHO1D legacy-disposition page.
