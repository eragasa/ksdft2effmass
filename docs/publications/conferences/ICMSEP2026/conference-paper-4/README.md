# Conference paper 4: first-principles silicon application

This directory contains the pre-results working draft:

> *Compatibility of spectral and operator reductions of a first-principles silicon
> Hamiltonian*

The paper applies the framework from conference paper 1 to the planned PBE/Wannier and
orthogonal ten-orbital $sp^3s^\ast$ silicon hierarchy. The production parent,
Wannier validation, admissible-set searches, withheld checks, and model-selection
result are not yet available. Proposed work and empty result records remain in the
separate [`appendices/`](appendices/) directory until authenticated evidence exists.
Appendix D separately preserves bounded read-only Wannier90 silicon tutorial evidence
extracted from Paper 1 v2; it is excluded from the production admissible sets. Paper
2's separate silicon-inspired diamond-lattice parent is a synthetic structural control,
not silicon evidence or a substitute for this paper's specified material hierarchy.

When Paper 4 is converted to a rendered manuscript, planned production work, open
controls, pending records, and conditional conclusions must appear in red. Bounded
historical evidence such as Appendix D remains black and explicitly excluded from the
production admissible sets.

`manuscript.pdf` is the single rendered working paper and includes Appendices A--D.
Build it with:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error manuscript.tex
```

The draft must not be represented as a validated silicon Hamiltonian, a completed
compatibility test, or an accepted tight-binding model. It does not authorize Quantum
ESPRESSO, Wannier90, or other protected execution, submission, publication, or release.
