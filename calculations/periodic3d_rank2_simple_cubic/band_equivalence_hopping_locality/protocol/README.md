# Simple-cubic band-equivalence and hopping-locality protocol

This directory is the authoritative research-protocol owner for the periodic-3D
rank-two simple-cubic context. The protocol identity is

```text
ksdft2effmass.campaign.model-adequacy.periodic3d.band-equivalence-versus-hopping-locality
```

The scientific system is a synthetic simple-cubic rank-two retained Hamiltonian obtained
from an exact four-state parent. The finite parent is stated on the complete
cell--orbital space; eigenvalue lists are never used as Hamiltonian operands.
Three-dimensional space does not change the retained rank.

## Selected design

The protocol selects:

- the direct axis-permutation-symmetric extension of the one-dimensional four-state
  directed-hopping parent;
- an explicit Kronecker lattice construction with four orbitals per cell;
- exact unitary relations among cell--orbital, Bloch, retained-frame, and Wannier/TB
  representations;
- the two lowest bands in a qualified periodic rank-two frame;
- the smooth sine-rotation family with amplitudes through `pi/4`;
- the analytic flat-parent correlation `J_0(2*a/3)^3`;
- complete cubic signed-permutation displacement orbits ordered by squared radius;
- equal-accuracy first-passing-shell and retained-block comparisons; and
- separate reconstruction, alignment, conversion, interpolation, truncation, total
  matrix-error, and spectral-error channels.

Signed-permutation-complete support does not imply equality of hopping coefficients over
an orbit or a cubic material model.

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
The bounded `8`, `16`, and `32` construction meshes and associated resource observations
are development controls. They do not establish convergence, uncertainty quantification,
material validity, or publication acceptance. No Quantum ESPRESSO, Wannier90, remote,
production, or retained calculation is authorized by this protocol.

The neighboring [technical report](../technical-report/technical-report.md) records the
current calculation-facing evidence boundary. The distributed checklist is
[`../migration.md`](../migration.md).
