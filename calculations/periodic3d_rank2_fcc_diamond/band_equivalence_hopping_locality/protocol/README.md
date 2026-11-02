# FCC/diamond band-equivalence and hopping-locality protocol

This directory is the authoritative research-protocol owner for the periodic-3D
rank-two FCC/diamond context. The protocol identity is

```text
ksdft2effmass.campaign.model-adequacy.periodic3d-nonorthogonal.band-equivalence-versus-hopping-locality
```

## Selected design

The protocol selects:

- an FCC nonorthogonal primitive metric with a two-site diamond basis;
- four equal-length tetrahedral $A$--$B$ bonds and a normalized diamond structure factor;
- a synthetic two-site, two-channel four-state parent with a conservative external
  rank-two gap bound;
- separate matched Hermitian-bond FCC and simple-cubic Bravais controls;
- the lowest two bands in a qualified periodic frame;
- equal reciprocal-torus RMS gauge amplitude;
- a constrained three-index FCC Bessel comparator;
- physical metric and complete lattice-point-group shells;
- equal-accuracy first-passing-shell and retained-block comparisons;
- a nontrivial unimodular primitive-basis covariance control; and
- separate reconstruction, alignment, conversion, interpolation, truncation, and total
  error channels.

The inspired parent is not an $sp^3s^*$ model, silicon parameterization, bulk-silicon
calculation, material validation, or effective-mass result. The matched simple-cubic
comparator is not the directed-hopping parent in the simple-cubic context, and their
results must not be pooled.

## Protocol files and boundary

- [`experimental-protocol.tex`](experimental-protocol.tex) is the authoritative
  prospective protocol.
- [`experimental-protocol.bib`](experimental-protocol.bib) is its bibliography.
- `experimental-protocol.pdf`, when built, is a replaceable working rendering and not
  retained evidence.

Build from this directory with:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error experimental-protocol.tex
```

The protocol and implementation must satisfy the calculation-owned
[cross-family parity contract](../../../periodic/multiband/band-equivalence-test-and-diagnostic-parity.md).
The bounded verifier reconstructs the sampled external gap on all three development
meshes, and sampled decisions were unchanged on both refinements. This does not establish
a formal mesh/shell convergence disposition. Constrained-series tail certification,
final tolerances, frozen revisions, retained-record policy, and evidence review remain
open. No Quantum ESPRESSO, Wannier90, remote, production, or retained calculation is
authorized by this protocol.

The neighboring [technical report](../technical-report/technical-report.md) records the
current calculation-facing evidence boundary. The distributed checklist is
[`../migration.md`](../migration.md).
