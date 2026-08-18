# From Kohn–Sham Operators to Effective-Mass Models

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

The current draft has four main divisions: criteria for a good reduced model;
the bulk-silicon representation program; the doped-silicon representation
program; and the mathematical and proof program. A substantial appendix
collection owns detailed notation, derivations, controlled examples, route
comparisons, and analytical warmups. It is a framework-rich pre-results draft:
chapter development does not imply completion of the proofs or calculations
described there.

Red boxes headed **Prospective citation note** are unresolved editorial prompts.
They record candidate sources and claim checks from the citation audit; they do
not assert that the sources have been read or that the proposed attribution is
correct. Candidate bibliography records may be present solely so the red box
can render a citation number; that presence does not resolve the note or accept
the record's metadata.

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
- `chapters/` — independently maintainable chapters organized into the four
  main divisions and final synthesis;
- `figures/` — editable diagram sources and their manuscript-ready renderings;
- `appendices/` — notation, derivations, controlled examples, route
  comparisons, and analytical warmups supporting the main narrative;
- `references.bib` — monograph-owned bibliography, independently maintained
  from article bibliographies;
- `navigation-index.md` — machine-readable concept map from scientific terms to
  their primary and supporting manuscript sources;
- `citation-audit.md` — conservative full-manuscript audit of missing, weak, and
  proposed scholarly citations;
- `extraction-map.md` — planned relationships between monograph material and
  shorter outputs;
- `build/` — ignored local LaTeX output.

P01 and other paper directories remain independently edited publication
surfaces. They may extract selected monograph material but are not generated
projections of this directory.

## Local build

With a local TeX distribution, LuaLaTeX, Biber, and `latexmk` available:

```bash
mkdir -p build/chapters build/appendices
latexmk -lualatex -output-directory=build manuscript.tex
```

The manuscript uses `fontspec`, so the pdfLaTeX-oriented `-pdf` mode is not
supported. `latexmk` also runs `makeindex` for the curated back-of-book index.
Legacy BibTeX-generated `manuscript.bbl` files must not be reused by the Biber
build. The build is formatting evidence only. Generated output remains local.
