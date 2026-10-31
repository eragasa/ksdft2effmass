# Technical report

This directory owns the calculation-facing technical report for the periodic-1D
rank-two band-equivalence-versus-hopping-locality study. The report deliberately gives
an extensive mathematical account of the model, state spaces, homotopy, frame transport,
restricted alignment, Fourier conventions, refinement rules, truncation errors,
independent verification, closed outcomes, evidence boundary, and provenance. It is
more detailed than the shorter publication narrative in `Ragasa2026a`.

The report is a migration draft and review document. It does not establish sealed
evidence, material validation, submission, publication, or priority.

The first authorized unsealed execution,
`direct-embedded-rank2-controlled-v1`, completed calculation but failed aggregate
independent verification because the independent route did not encode the exact
zero-amplitude identity. Its failing artifacts are preserved and it has no figures.
Its metadata retain the historical calculation- and verification-script digests, but
separate byte copies of those two pre-remediation producer scripts are not retained in
the current checkout; this provenance limitation is stated in the report.

The separately authorized no-overwrite successor,
`direct-embedded-rank2-controlled-v2`, retains byte-identical calculation JSON, passes
all four aggregate verification components at the unchanged installed tolerance, and
contains the closed six-figure authenticated inventory. The report includes those six
figures while preserving the distinction between bounded software-route agreement and
scientific validation.

Build from this directory with:

```console
latexmk -pdf -interaction=nonstopmode -halt-on-error technical-report.tex
```

The selected compiled `technical-report.pdf` is retained as a review snapshot. It is
not sealed evidence, scientific validation, or a publication; all LaTeX auxiliary
products remain untracked.
