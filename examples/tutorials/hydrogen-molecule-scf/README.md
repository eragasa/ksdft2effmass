# Hydrogen-molecule self-consistent-field tutorial

This project tutorial introduces one ground-state self-consistent-field calculation for
an isolated H$_2$ molecule and exercises the preprocessing → simulation →
postprocessing boundary with calculator-native outputs.

## Backend status

| Backend | Status | Scope |
|---|---|---|
| [ABINIT](abinit/README.md) | Partially materialized; one execution observed | An authorized ABINIT 10.8.3 run exercised exact external input staging, direct serial execution, and useful `.abo` and NetCDF processing. A reusable project input is still blocked by source-term disposition. |
| [Quantum ESPRESSO](qe/README.md) | Planned | No same-system QE input, pseudopotential, or execution has been selected. |

The observed ABINIT run emitted the main text result, separate log and error streams,
GSR/EIG/OUT NetCDF records, density and wavefunction state, a derivative database, and
plain-text eigenvalue/band data. Postprocessing extracted the SCF history, total energy,
forces, eigenvalues, diagnostics, and selected NetCDF metadata. Native state remains
external.

This tutorial does not align ABINIT and QE pseudopotentials, exchange-correlation
implementations, cutoffs, geometry conventions, or energy references. It supports no
cross-backend numerical comparison or scientific-validation claim.
