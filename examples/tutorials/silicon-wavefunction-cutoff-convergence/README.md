# Silicon wavefunction-cutoff convergence

**Status:** one six-point Quantum ESPRESSO 7.5 calculated tutorial observation retained; ABINIT realization not yet implemented.

## Learning objective

This tutorial studies the represented total energy of two-atom diamond silicon as the
plane-wave wavefunction cutoff changes while the structure, pseudopotential, k-point
mesh, occupations, and electronic-solver settings remain fixed.

The Quantum ESPRESSO realization belongs to
`quantumespresso.simulations.convergence-silicon-cutoff`. Its authoritative compact
result is a point-indexed table containing the cutoff, total energy when available,
process and calculator status, diagnostics, and runtime. A plot may be derived from the
table but does not define the Task boundary.

This tutorial is separate from k-point-density convergence and structural relaxation.
It does not select or validate a production cutoff.

## Backends

- [`qe/`](qe/) — one authorized six-point QE 7.5 attempt completed without retry; no production cutoff was selected.
- [`abinit/`](abinit/) — planned correspondence only; no execution is authorized.
