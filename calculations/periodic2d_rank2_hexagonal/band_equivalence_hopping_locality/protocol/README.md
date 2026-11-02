# Hexagonal-metric band-equivalence and hopping-locality protocol

This directory is the authoritative research-protocol owner for the periodic-2D
rank-two hexagonal-metric context. The protocol identity is

```text
ksdft2effmass.campaign.model-adequacy.periodic2d-nonorthogonal.band-equivalence-versus-hopping-locality
```

The calculation is a separate family from the retained orthogonal periodic-2D package.
Its bounded `16 x 16`, `32 x 32`, and `64 x 64` Monkhorst--Pack calculations remain
replaceable development artifacts, not an immutable version, convergence result,
retained run, evidence package, or qualified scientific result.

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
results must not be pooled.

## Protocol files and build

- [`experimental-protocol.tex`](experimental-protocol.tex) is the authoritative
  prospective protocol.
- [`experimental-protocol.bib`](experimental-protocol.bib) is its bibliography.
- `experimental-protocol.pdf`, when built, is a replaceable working rendering and is not
  retained evidence.

Build from this directory with:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error experimental-protocol.tex
```

## Diagnostic parity and boundary

Implementation and analysis must satisfy the calculation-owned
[periodic-2D rank-two diagnostic-parity catalog](../../../periodic2d/rank2/diagnostic-parity.md).
Geometry-specific additions include honeycomb-basis, structure-factor,
external-isolation-gap, basis-aware-distance, metric-shell, constrained-comparator, and
primitive-basis covariance tests and diagnostics.

The inspired parent has an analytic conservative gap bound, and the bounded verifier
reconstructs the sampled gap on all three development meshes. Every sampled decision is
unchanged between `N=32` and `N=64`. Row-level software parity is complete for every
applicable or explicitly inapplicable catalog quantity, including independent finite-sum
reconstruction, but a formal mesh/shell convergence disposition remains open.
Bessel-tail certification, final tolerances, retained-record schemas, frozen revisions,
and evidence policy remain open. No Quantum ESPRESSO, Wannier90, remote, production, or
retained calculation is authorized by this protocol.

The neighboring [technical report](../technical-report/technical-report.md) records the
calculation-facing interpretation and current evidence boundary. The distributed
migration checklist is [`../migration.md`](../migration.md).
