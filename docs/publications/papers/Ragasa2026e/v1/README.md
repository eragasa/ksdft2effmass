# Conference paper 5: common-space defect-operator construction

This directory contains the synchronized pre-results sources
[`manuscript.md`](manuscript.md) and [`manuscript.tex`](manuscript.tex). The manuscript
formalizes matched comparison geometry, rank and bundle admission, constrained alignment,
energy referencing, gauge-covariant subtraction, failure dispositions, and the current
evidence boundary without asserting a production defect result.

## Prospective role

Paper 5 is reserved for the methodology that makes a periodic defect-induced operator
difference mathematically defined. Its central object is

\[
\Delta H_{\mathrm{imp}}=H_{\mathrm{defect}}^{\mathrm{aligned}}
-H_{\mathrm{pristine}}^{\mathrm{matched}},
\]

formed only after the two represented operators act on an explicitly identified common
retained space and share lattice, units, scalar energy reference, coordinate ordering,
and compatible boundary sewing.

The proposed scope includes:

- matched pristine and doped supercells rather than primitive-cell/doped-cell subtraction;
- explicit Brillouin-zone folding and translation correspondence;
- equal-rank bundle compatibility or a separately justified projection/embedding;
- projector principal angles, cross-overlap singular values, and fail-closed rank gates;
- common reciprocal-face sewing and a constructible global periodic alignment;
- orbital-semantic, center, site, and surviving-symmetry constraints;
- scalar energy-reference alignment with retained uncertainty;
- separate treatment of defect-localized states that change the retained-space content;
- impurity-operator Hermiticity, spatial-shell, and reconstruction diagnostics; and
- distinct P:Si and B:Si specialization contracts.

Paper 5 may use a minimal topological-obstruction screen, but it does not own a general
Chern, $\mathbb Z_2$, crystalline, or real-bundle classification. Those methods belong
to Paper 6. An obstruction or unresolved compatibility gate blocks subtraction rather
than authorizing a post-hoc gauge or rank change.

## Separation from Papers 4 and 7

Paper 4 owns the scalar-relativistic, non-spin-polarized, non-SOC pristine bulk-Si
reduction. Paper 5 owns common-space defect methodology and may define spinor-capable
contracts, but it does not report production P:Si or B:Si operators. Paper 7 owns the
separately qualified SOC material application.

The Paper 4 ten-spatial-orbital operator is not a direct subtraction reference for an SOC
defect branch. A later SOC branch requires its own matched pristine-Si SOC supercell and
spinorial retained representation.

## Experiment-tree status

No maintained experiment family under `experiments/` currently implements the common-
space defect contract or supplies Paper 5 execution evidence; the program-wide
[allocation ledger](../../experiment-to-paper-allocation.md) records this empty boundary.
Paper 1--3 synthetic
experiments may motivate alignment and locality diagnostics, but their identities,
tolerances, and evidence cannot be transferred to pristine/defect subtraction.

## Current evidence status

A pre-results manuscript now exists, but no immutable protocol, implementation,
production calculation, retained run, defect operator, or material conclusion exists.
The proposed SOC P:Si specialization differs from the current physical-specification v1
primary P:Si branch and requires a reviewed specification amendment or successor before
execution.

This README authorizes no Quantum ESPRESSO or Wannier90 execution, retained evidence,
submission, publication, release, or promotion.

## Working-color convention

Red text in the rendered manuscript marks proposed methods, unselected controls, and
conditional future decisions. The introduction, current evidence boundary, and disclosed
blockers remain black. Color does not confer evidence status.

## Rendering

Build the LaTeX manuscript locally with:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error manuscript.tex
```

The literature bibliography in [`references.bib`](references.bib) is combined with the
shared unpublished-paper identities. A successful build verifies document mechanics
only.
