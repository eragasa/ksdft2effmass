# Silicon-inspired Diamond-lattice Band Equivalence versus Hopping Locality

## Identity and status

This directory is the prospective experiment home for

```text
ksdft2effmass.campaign.model-adequacy.periodic3d-nonorthogonal.band-equivalence-versus-hopping-locality
```

It is a separate family from the orthogonal periodic-3D experiment. A bounded
implementation and independently verified `8 x 8 x 8`, `16 x 16 x 16`, and
`32 x 32 x 32` Monkhorst--Pack calculations exist under
[`analysis/development/`](analysis/development/) and
[`analysis/development-refinement/`](analysis/development-refinement/). They are
replaceable development artifacts, not an immutable version, convergence result,
retained run, evidence package, or qualified scientific result. Family-owned vector PDF
and 600-dpi PNG diagnostics are cataloged in
[`analysis/README.md`](analysis/README.md).

## Selected design

The protocol selects:

- an FCC non-orthogonal primitive metric with a two-site diamond basis;
- four equal-length tetrahedral $A$--$B$ bonds and a normalized diamond structure factor;
- a synthetic two-site, two-channel four-state parent with a certified external rank-two
  gap;
- separate matched Hermitian-bond FCC and simple-cubic Bravais controls;
- the lowest two bands in a qualified periodic frame;
- equal reciprocal-torus RMS gauge amplitude;
- a constrained three-index FCC Bessel comparator;
- physical metric and complete lattice-point-group shells;
- equal-accuracy first-passing-shell and retained-block comparisons;
- a nontrivial unimodular primitive-basis covariance control; and
- separate reconstruction, alignment, conversion, interpolation, truncation, and total
  error channels.

The inspired parent is not an $sp^3s^*$ model or silicon parametrization. The matched
simple-cubic comparator is not the directed-hopping parent in the orthogonal family, and
their eventual results must not be pooled.

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
Geometry-specific additions include diamond-basis, structure-factor, external-isolation-gap,
basis-aware-distance, metric-shell, constrained-comparator, primitive-basis covariance,
and resource tests and diagnostics.

## Boundary

The inspired parent has an analytic conservative gap bound, and the bounded verifier
reconstructs the sampled gap on all three development meshes. Every sampled decision is
unchanged on both refinements. Row-level Paper 1 software parity is complete for every
applicable or explicitly inapplicable catalog quantity, including independent finite-sum
reconstruction, but a formal mesh/shell convergence disposition remains open.
Constrained-series tail certification,
final tolerances and retained-record schemas, frozen revisions, and evidence policy
remain open. The measured `N=32` action stayed below about 740 MB peak memory; it does
not authorize larger or retained actions. No
Quantum ESPRESSO, Wannier90, remote, production, or retained calculation is authorized
by this development package.
