# Conference paper 6: topological and symmetry obstructions to multiband alignment

This directory contains the synchronized pre-results sources
[`manuscript.md`](manuscript.md) and [`manuscript.tex`](manuscript.tex). The manuscript
formalizes relative bundle alignment, qualified complex and symmetry obstruction
diagnostics, patchwise operator comparison, staged controlled-model roles, and the
current evidence boundary without asserting a topological classification.

## Prospective role

Paper 6 is reserved for the conditions under which a retained periodic multiband space
cannot be represented by the global smooth periodic frame, or by the
symmetry-compatible frame, required by an operator-comparison protocol.

Its proposed scope includes:

- vector bundles defined by periodic projector fields;
- local frames, gauge patches, transition functions, and reciprocal-boundary sewing;
- obstruction to a global complex periodic frame;
- Chern diagnostics in two dimensions and on qualified two-dimensional slices in three
  dimensions;
- time-reversal/Kramers-compatible framing and $\mathbb Z_2$-aware diagnostics when that
  symmetry is an explicit requirement;
- real or orientation-preserving frame restrictions when an $SO(r)$ rather than $U(r)$
  alignment is scientifically required;
- relative bundle compatibility for two operators that are candidates for global
  alignment;
- Wilson-loop flow as a qualified diagnostic rather than automatic evidence of topology;
- patchwise operator comparison when a global representation is unavailable; and
- fail-closed dispositions for obstructed, rank-changing, and numerically unresolved
  cases.

A nonidentity Wilson loop is not by itself an obstruction. Finite-mesh winding or
plaquette values do not establish continuum invariants without a reviewed convergence
and certification protocol.

## Relationship to the silicon sequence

Paper 6 is not required merely because Paper 4 studies ordinary non-SOC bulk silicon.
It supplies an escalation path for Paper 5 and Paper 7 when a global or required
symmetry-compatible pristine/defect alignment cannot be constructively qualified. It
must not relabel ordinary frame-sewing defects as topological results.

Material-Si, Si:P, and Si:B conclusions remain outside Paper 6 unless a separately
reviewed material specialization and authenticated evidence are later added. The initial
study should use controlled models whose topological class and transition functions are
known independently.

## Experiment-tree status

No maintained experiment family under `experiments/` currently supplies Paper 6
obstruction evidence; the program-wide
[allocation ledger](../../experiment-to-paper-allocation.md) records this empty boundary.
Closure phases, Wilson loops, and plaquette diagnostics in Papers
2 and 3 remain finite transport/sewing controls and must not be relabeled as continuum
topological classifications. Historical topological calculations under `calculations/`
require a separate evidence review and maintained successor before publication use.

## Current evidence status

A pre-results manuscript now exists, but no model family, immutable invariant protocol,
implementation, numerical result, material classification, or retained evidence has
been selected. No protected execution, submission, publication, release, or promotion
is authorized.

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
