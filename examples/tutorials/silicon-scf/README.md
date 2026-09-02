# Silicon self-consistent-field tutorial

This project tutorial introduces a ground-state self-consistent-field calculation for
diamond silicon and the preprocessing → simulation → postprocessing stage boundary.

## Backend status

| Backend | Status | Scope |
|---|---|---|
| [Quantum ESPRESSO](qe/README.md) | Implemented software example | Portable `pw.x` input construction; the test does not invoke QE. |
| [ABINIT](abinit/README.md) | Planned; execution blocked | The corresponding basic3 source and project-owned portable input have not been selected and ABINIT execution is not authorized. |

The paired directories share a learning objective only. They do not establish aligned
pseudopotentials, cutoffs, sampling, energy references, numerical equivalence, or
scientific validation.
