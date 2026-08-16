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

## Authority and evidence boundary

The monograph is explanatory narrative. Applicable files under
`specification/`, retained calculation and provenance records, software
contracts, verification evidence, and durable human decisions remain the owners
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
- `chapters/` — independently maintainable long-form chapter skeletons;
- `notes/` — explicitly labelled working fragments that are not included in the
  composed manuscript until corrected and reviewed;
- `extraction-map.md` — planned relationships between monograph material and
  shorter outputs;
- `build/` — ignored local LaTeX output.

P01 and other paper directories remain independently edited publication
surfaces. They may extract selected monograph material but are not generated
projections of this directory.

## Local build

With a local TeX distribution and `latexmk` available:

```bash
mkdir -p build/chapters
latexmk -pdf -output-directory=build manuscript.tex
```

The build is formatting evidence only. Generated output remains local.
