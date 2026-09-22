# Computational Materials Science LaTeX package

Working pre-results manuscript package for:

> Compatibility of spectral and operator-preserving tight-binding reductions
> of a first-principles silicon Hamiltonian

## Files

- `manuscript.tex` — Elsevier `elsarticle` manuscript source.
- `references.bib` — BibTeX database using DOI-backed references.
- `manuscript.bbl` — generated bibliography for submission-system fallback.
- `highlights.txt` — required journal highlights; each is at most 85 characters.
- `elsarticle.cls` — Elsevier document class vendored for reproducible builds.
- `elsarticle-num.bst` — Elsevier numbered-reference BibTeX style.
- `manuscript.pdf` — compiled working draft, generated during package validation.

## Build

The project requires a TeX distribution containing `elsarticle`, BibTeX, and
the standard AMS packages. Build with:

```bash
latexmk -pdf manuscript.tex
```

Clean generated intermediate files with:

```bash
latexmk -c manuscript.tex
```

## Submission notes

The manuscript remains a pre-results draft. Before journal submission:

1. Replace future-tense methodology and expected-result statements with the
   completed calculations and conclusions.
2. Insert all figures, tables, numerical results, and uncertainty analyses.
3. Replace the data-and-code placeholders with permanent repository DOIs.
4. Complete the acknowledgments and funding declarations.
5. Verify the CRediT statement with both authors.
6. Review the generative-AI declaration against the actual tools and uses.
7. Update the highlights so that every bullet states a demonstrated result.
8. Follow the current journal guide at the date of submission.

Elsevier Editorial Manager may require all submission-source files to be
uploaded at one folder level. This package therefore uses a flat layout.
