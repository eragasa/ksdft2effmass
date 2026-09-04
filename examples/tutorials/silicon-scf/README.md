# Silicon self-consistent-field tutorial

This project tutorial introduces a ground-state self-consistent-field calculation for
diamond silicon and the preprocessing → simulation → postprocessing stage boundary.

## Backend status

| Backend | Status | Scope |
|---|---|---|
| [Quantum ESPRESSO](qe/README.md) | Implemented software example | Portable `pw.x` input construction; the test does not invoke QE. |
| [ABINIT](abinit/README.md) | Calculated tutorial observation; portable example planned | Basic3 dataset 1 was executed as the SCF producer for the paired silicon-bands workflow; no project-owned portable input is committed here. |

The backend directories share a learning objective only. They do not establish aligned
pseudopotentials, cutoffs, sampling, energy references, numerical equivalence, or
scientific validation.
