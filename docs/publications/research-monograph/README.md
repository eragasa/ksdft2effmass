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

The current draft has five main divisions, arranged from lower to higher
conceptual load: computational foundations; criteria for a good reduced model;
the bulk-silicon representation program; the doped-silicon representation
program; and the mathematical and proof program. Part I proceeds from
quantities, units, coordinates, and metadata through finite representations,
Hermitian eigensystems and spectral subspaces, quantum operators and the
one-dimensional box, two- and three-dimensional box
models with Kronecker products, periodic geometry, Bloch-periodic finite
differences, retained spaces, isolated-band Fourier reduction to finite-range
lattice Hamiltonians, composite Bloch frames, the Bloch--Wannier bridge, gauge
transport and alignment, block locality, and evidence vocabulary. Part II then
moves from the scientific adequacy question through common-space operator
comparison to weighted spectral and operator losses, with fitting and
model-class-expressivity precedents integrated where the corresponding concepts
enter, followed by admissible sets, common witnesses,
quadratic-loss geometry, separation certificates, and evidence discipline. A
substantial appendix collection owns detailed notation, derivations,
controlled examples, route comparisons, and analytical warmups. It is a framework-rich pre-results draft: chapter
development does not imply completion of the proofs or calculations described
there.

Red boxes headed **Prospective citation note** are unresolved editorial prompts.
They record candidate sources and claim checks from the citation audit; they do
not assert that the sources have been read or that the proposed attribution is
correct. Candidate bibliography records may be present solely so the red box
can render a citation number; that presence does not resolve the note or accept
the record's metadata.

## Authority and evidence boundary

The monograph is explanatory narrative. Applicable files under
`specification/`, proof packages under `docs/research/proofs/ksdft2effmass/`, theorem
contracts under `docs/research/proofs/formal/theorem-catalog/`, retained calculation and provenance
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

- `manuscript/manuscript.tex` — standard-LaTeX composition root;
- `chapters/` — independently maintainable, semantically named lecture sources;
  filenames carry no sequence numbers, and `manuscript/manuscript.tex` alone
  determines their current pedagogical order;
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
- `current-library-capability-crosswalk.md` — architecture-linked map from maintained
  public APIs and extraction gaps to new controlled calculations and the staged
  manuscript rewrite;
- `build/` — ignored local LaTeX output.

P01 and other paper directories remain independently edited publication
surfaces. They may extract selected monograph material but are not generated
projections of this directory.

## Planned Part I notebooks

**To do:** create the following pedagogical notebooks under
`examples/tutorials/research-monograph/foundations/` only after their lecture
contracts are stable:

- `computational_quantities.ipynb`;
- `finite_representations.ipynb`;
- `hermitian_eigensystems.ipynb`;
- `quantum_operators.ipynb`;
- `particle_in_box_dimensions.ipynb`;
- `periodic_geometry.ipynb`;
- `bloch_periodic_finite_differences.ipynb`;
- `isolated_band_fourier_reduction.ipynb`; and
- `composite_band_gauge_alignment.ipynb`.

Each notebook must show its imports, use explanatory inline comments, avoid
hidden state, and keep synthetic examples distinct from calculated material
results. Sparse operators must remain sparse in diagnostics; a check must not
call `toarray()` merely to compare an operator with its adjoint. Notebook files
and outputs are not present yet, and this to-do list makes no execution or
verification claim.

## Local build

With a local TeX distribution, LuaLaTeX, Biber, and `latexmk` available:

```bash
cd docs/publications/research-monograph
mkdir -p build/chapters build/appendices
latexmk -lualatex -output-directory=build manuscript/manuscript.tex
```

The manuscript uses `fontspec`, so the pdfLaTeX-oriented `-pdf` mode is not
supported. `latexmk` also runs `makeindex` for the curated back-of-book index.
Legacy BibTeX-generated `manuscript.bbl` files must not be reused by the Biber
build. The build is formatting evidence only. Generated output remains local.

## Maintained source audit

`ksdft2effmass.publications.manuscript.LatexManuscriptAuditor` provides a typed,
deterministic audit of the LaTeX composition graph. It checks that included
sources and declared BibLaTeX resources exist and remain beneath the monograph
root, labels and bibliography keys are unique, and internal references and
literal citation keys resolve. Selected equation-intensive sources can use the
stricter `equationterms` contract: every display-math environment has one unique
stable label and must be followed immediately by a rendered term list bound to
that exact label. Every `equationterm` entry must contain one nonempty symbol and
one nonempty definition, and duplicate symbols within a term list are rejected.
The semantically named `impurity-operator-extraction.tex` chapter and Appendix J
currently use this contract.

Run the focused maintained audit from `python/`:

```bash
uv run pytest -q \
  tests/software_verification/ksdft2effmass/publications/test__LatexManuscriptAuditor.py
```

The same test is collected by the repository's ordinary deterministic
`uv run pytest` verification command; no separate manuscript-only CI path is
required.

The structural audit does not parse mathematical semantics. A structurally
complete symbol list can still omit a mathematical variable or give a wrong
definition, so scientific review remains required. Citation-key resolution
establishes only that a literal key names one bibliography entry; it does not
verify metadata, source quality, claim support, or citation suitability. The
audit also does not replace the LuaLaTeX build, citation review, numerical
verification, scientific validation, uncertainty quantification, or human
acceptance.
