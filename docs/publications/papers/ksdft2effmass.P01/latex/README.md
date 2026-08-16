# P01 LaTeX source

This folder owns the independently authored LaTeX manuscript-preparation surface for P01. [`../manuscript.md`](../manuscript.md) remains a repository working projection, not the source document for mechanical synchronization with LaTeX. The two forms may organize and develop their prose independently.

Both forms remain subordinate to the applicable scientific specifications, retained evidence, and publication record. Neither form overrides the other, authorizes protected execution, or turns expected work into a calculated, verified, validated, or accepted result. Material disagreements in scientific meaning or evidentiary status must be resolved against those owning records rather than by preferring one manuscript format.

P01 remains in the `Waiting` publication state. No LaTeX manuscript, generated PDF, submission artifact, or publication claim is represented as complete.

## Working files

- `manuscript.tex` is the independently authored pre-results article draft.
- `references.bib` is a candidate bibliography. Inclusion does not record that
  every entry or its use in the manuscript has completed primary-source review.
- `highlights.txt` contains working placeholders, not demonstrated results or a
  submission-ready highlights file.
- `elsarticle.cls` and `elsarticle-num.bst` are vendored under the license and
  provenance recorded in `THIRD_PARTY_NOTICES.md`.

Generated `.bbl`, PDF, HTML, and HTML-asset output remains local and ignored.
Build the local draft from this directory with:

```bash
latexmk -pdf manuscript.tex
```

A successful build establishes formatting only. It does not establish the
manuscript's scientific correctness, evidentiary completeness, author approval,
or readiness for submission.
