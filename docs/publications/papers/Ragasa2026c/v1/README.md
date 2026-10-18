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
finite-family witness and separation statements.
[`Appendix A`](appendices/A-1-extracted-evidence-boundary.md) records the permitted role
of those extracted values together with the post-hoc M3 threshold and Wannier90
sensitivity records. [`Appendix B`](appendices/A-2-d1-p0-g0-isolation-gap-certificate.md)
gives the exact D1 exterior-isolation and attack-angle certificates together with a
finite-grid sanity check.

The publication-independent
[higher-rank protocol](../../../../../experiments/periodic-reduction/higher-rank-composite-band-alignment-and-locality/protocol.md)
now proposes a common analytic model for arbitrary finite retained rank and finite
Givens-circuit depth in one, two, and three spatial dimensions. Its first bounded 1-D
P0/G0 development tranche has selected parent coefficients, an analytic gap bound, real
Givens-angle law, rank/depth ladder, A0--A3 channels, and cross-rank normalizations.
Meshes, tolerances, supports, dimensional identities, schemas, implementation, and
evidence policy remain open. No new result or evidence status is established by this
README. Paper 3 must not inherit
rank-two formulas or Paper 2 numerical controls unless a reviewed specialization
establishes them.

Paper 3 deliberately supplies a topologically trivial synthetic baseline. Paper 5 owns
the downstream fail-closed pristine/defect compatibility decision, while Paper 6 owns
full topological and symmetry-obstruction studies. Paper 4 remains the non-SOC bulk-Si
reduction, and Paper 7 is the prospective matched SOC Si/Si:P/Si:B application. The
[current roadmap](../../../conferences/ICMSEP2026/paper-program-roadmap.md) records
these non-transfer boundaries.

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
calculation. The D1 P0/G0 development model is selected, but no new protocol result,
complete protocol freeze, retained run, evidence package, submission, or publication is
asserted or authorized.
