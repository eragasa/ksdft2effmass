# KSDFT-to-effective-mass research monograph

## Status

This directory is a dissertation-style, long-form research-writing workspace. It
is not represented as an institutionally registered dissertation, submitted
manuscript, accepted publication, reviewed release, or completed research
output.

The monograph may expand freely enough to preserve derivations, alternatives,
negative results, workflow rationale, verification arguments, and limitations.
Shorter papers, conference material, and presentations may later extract a
bounded narrative from it. Extraction is an editorial operation, not automatic
synchronization, and does not transfer evidentiary status merely by copying
prose.

The current draft contains developed chapters on scope, the physical problem,
mathematical foundations, the proof and mechanization program, the
first-principles parent, representations and alignment, reduction, evidence,
present result boundaries, and outlook. It is a framework-rich pre-results
draft: chapter development does not imply completion of the proofs or
calculations described there.

## Authority and evidence boundary

The monograph is explanatory narrative. Applicable files under
`specification/`, proof packages under `docs/proofs/ksdft2effmass/`, theorem
contracts under `formal/theorem-catalog/`, retained calculation and provenance
records, software contracts, verification evidence, and durable human decisions
remain the owners
of scientific meaning and project state. The monograph must link those owners
rather than silently redefine them.

Every substantive result should retain one of the repository's declared
statuses: calculated result, literature value, expected behavior, illustrative
example, synthetic test data, placeholder, or proposed work. A chapter heading,
completed draft, successful build, or extraction into an article does not
establish numerical verification, scientific validation, uncertainty
quantification, publication, or human acceptance.

## Structure

- `manuscript.tex` — standard-LaTeX composition root;
- `chapters/` — independently maintainable long-form chapters;
- `appendices/` — shared notation, convention, and status reference material;
- `references.bib` — monograph-owned bibliography, independently maintained
  from article bibliographies;
- `extraction-map.md` — planned relationships between monograph material and
  shorter outputs;
- `build/` — ignored local LaTeX output.

P01 and other paper directories remain independently edited publication
surfaces. They may extract selected monograph material but are not generated
projections of this directory.

## Local build

With a local TeX distribution and `latexmk` available:

```bash
mkdir -p build/chapters build/appendices
latexmk -pdf -output-directory=build manuscript.tex
```

The build is formatting evidence only. Generated output remains local.
