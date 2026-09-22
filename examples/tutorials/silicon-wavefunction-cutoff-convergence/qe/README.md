# Quantum ESPRESSO wavefunction-cutoff convergence

**Status:** one exact six-point QE 7.5 attempt completed under resolved protected-execution checkpoint `QE-SILICON-CUTOFF-CONVERGENCE-RUN-HC01`.

The tutorial contains six independent `pw.x` SCF points with `ecutwfc` values 12,
16, 20, 24, 28, and 32 Ry. Every other represented scientific setting remained fixed.
Each point used its own isolated runtime workspace, streams, snapshots, process record,
native-state identity, and result status.

No PWTK installation or invocation is planned. The exact operational inputs are staged
in the external run identified by the
[silicon cutoff-convergence preflight](../../../../docs/computational/silicon-wavefunction-cutoff-convergence-preflight.md);
they are not maintained here because upstream redistribution terms are unresolved.
Generated run state remains in that external run root.

The compact calculated observation is retained at
[`expected/qe75-calculated-observation.json`](expected/qe75-calculated-observation.json).
The authoritative total-energy table is:

| `ecutwfc` (Ry) | Total energy (Ry) | QE SCF iterations | Process result |
|---:|---:|---:|---|
| 12 | -15.80599058 | 4 | exit 0; `JOB DONE.` |
| 16 | -15.83735595 | 4 | exit 0; `JOB DONE.` |
| 20 | -15.84571802 | 4 | exit 0; `JOB DONE.` |
| 24 | -15.84907010 | 4 | exit 0; `JOB DONE.` |
| 28 | -15.85008691 | 4 | exit 0; `JOB DONE.` |
| 32 | -15.85064840 | 4 | exit 0; `JOB DONE.` |

QEXSD 25.05.21 reported exit status 0 for every point and its Hartree energies agree
with the printed Rydberg energies after the exact factor-of-two unit conversion at the
retained precision. The represented total energy is successively lower at every point
in this finite ordered sequence; no tolerance or cutoff-selection rule was applied.
Every stderr stream contains the same 139-byte floating-point
exception note; it is retained as an uncharacterized diagnostic rather than classified
as harmless or fatal. Peak resident memory was not captured.

These passing tutorial points do not select a production cutoff, establish an
infinite-basis limit, provide numerical verification, or establish scientific
validation or acceptance.
