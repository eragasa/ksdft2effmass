# Conference paper 3: multiband representation and locality

## Prospective role

Paper 3 is reserved for the multiband extension of the band-equivalence versus hopping-
locality program. It follows the rank-two `SO(2)` benchmark of Paper 1 and the spatial-
dimension/general-lattice study of Paper 2.

Before the higher-rank extension, the manuscript extracts the controlled M2 rank-two
pointwise/global-alignment control and the M3 common-witness/separated-set demonstration
from Paper 1 v2. These examples introduce alignment-family and bounded-decision logic
without being presented as higher-rank or material evidence. The authoritative figures
and verification records remain in their calculation-owned source packages rather than
being copied here.

Its prospective scope includes:

- retained rank greater than two;
- real `SO(N)` and, when scientifically selected, complex `U(N)` gauge classes;
- non-Abelian periodic-frame transport and sewing;
- multiband alignment with explicit rank and singular-value qualification;
- complete matrix-valued hopping representations and symmetry-complete truncation;
- operator subtraction only after state-space, basis, gauge, energy-reference, unit, and
  geometry alignment; and
- separate projection, disentanglement, gauge-restriction, conversion, interpolation,
  truncation, and total consequences.

The working [`manuscript.md`](manuscript.md) extracts M2 and M3 rank-two precursors,
bounded rank-three synthetic evidence, and Wannier90 bridge evidence from Paper 1 v2 and
separates them from the prospective higher-rank study. M2 compares pointwise and global
alignment families; M3 uses nine frozen constant rotations and supports only its
finite-family witness and separation statements. [`Appendix A`](appendices/A-extracted-evidence-boundary.md) records the
permitted role of those extracted values together with the post-hoc M3 threshold and
Wannier90 sensitivity records. No new parent family, rank, lattice, gauge class, numerical controls,
experiment identity, result, or evidence status is selected by this README. Those choices require a separate
scientific protocol and review. Paper 3 must not inherit rank-two formulas or Paper 2
numerical controls unless a reviewed specialization establishes them.

## Working-color convention

Red text in the working manuscript identifies prospective multiband work, open controls,
unexecuted calculations, or conditional conclusions. Extracted historical controls are
kept black and retain their original finite-mesh scope.

## Rendering

`manuscript.pdf` is the single rendered working paper and includes Appendix A. Build it
with:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error manuscript.tex
```

## Status

Pre-results publication package. Historical extracted controls are not a new Paper 3
calculation. No new protocol result, protocol freeze, retained run, evidence package,
submission, or publication is asserted or authorized.
