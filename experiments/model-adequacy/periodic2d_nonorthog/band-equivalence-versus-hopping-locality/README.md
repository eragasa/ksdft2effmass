# Graphene-inspired Band Equivalence versus Hopping Locality

## Identity and status

This directory is the prospective experiment home for

```text
ksdft2effmass.campaign.model-adequacy.periodic2d-nonorthogonal.band-equivalence-versus-hopping-locality
```

It is a separate family from the orthogonal periodic-2D experiment. Bounded,
independently verified `16 x 16`, `32 x 32`, and `64 x 64` Monkhorst--Pack development
composition and plots are maintained by the
[calculation owner](../../../../calculations/periodic2d/rank2/nonorthogonal/band-equivalence-locality/).
They remain replaceable development artifacts, not an immutable version, convergence
result, retained run, evidence package, or qualified scientific result. This experiment
directory retains the prospective protocol and bibliography rather than a second
executable composition.

## Selected design

The protocol selects:

- a triangular primitive metric with a two-site honeycomb basis;
- three equal-length $A$--$B$ bonds and a normalized honeycomb structure factor;
- a synthetic two-sublattice, two-channel four-state parent with a certified external
  rank-two gap;
- separate matched Hermitian-bond triangular and square Bravais controls;
- the lowest two bands in a qualified periodic frame;
- equal reciprocal-torus RMS gauge amplitude;
- the constrained triangular comparator
  `sum_l (-1)^l J_l(2*g*sqrt(2/3))^3`;
- physical metric and complete lattice-point-group shells;
- equal-accuracy first-passing-shell and retained-block comparisons;
- a nontrivial unimodular primitive-basis covariance control; and
- separate reconstruction, alignment, conversion, interpolation, truncation, and total
  error channels.

The inspired parent is not a carbon $p_z$ model or graphene parametrization. The matched
square comparator is not the directed-hopping parent in the orthogonal family, and their
eventual results must not be pooled.

## Files and build

- [`experimental-protocol.tex`](experimental-protocol.tex) — authoritative prospective
  protocol.
- [`experimental-protocol.bib`](experimental-protocol.bib) — protocol bibliography.
- `experimental-protocol.pdf` — generated working rendering.

Build with:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error experimental-protocol.tex
```

## Cross-family parity

Implementation and analysis must satisfy the shared
[test and diagnostic parity contract](../../band-equivalence-test-and-diagnostic-parity.md).
Geometry-specific additions include honeycomb-basis, structure-factor, external-isolation-gap,
basis-aware-distance, metric-shell, constrained-comparator, and primitive-basis
covariance tests and diagnostics.

## Boundary

The inspired parent has an analytic conservative gap bound, and the bounded verifier
reconstructs the sampled gap on all three development meshes. Every sampled decision is
unchanged between `N=32` and `N=64`. Row-level Paper 1 software parity is complete for
every applicable or explicitly inapplicable catalog quantity, including independent
finite-sum reconstruction, but a formal mesh/shell convergence disposition remains open.
Bessel-tail certification, final tolerances and
retained-record schemas, frozen revisions, and evidence policy remain open. No
Quantum ESPRESSO, Wannier90, remote, production, or retained calculation is authorized
by this development package.

## Distributed migration ledger

The complete cross-surface inventory and authoritative checklist are maintained with the
calculation owner in
[`calculations/periodic2d/rank2/nonorthogonal/band-equivalence-locality/README.md`](../../../../calculations/periodic2d/rank2/nonorthogonal/band-equivalence-locality/README.md)
and [`migration.md`](../../../../calculations/periodic2d/rank2/nonorthogonal/band-equivalence-locality/migration.md).
