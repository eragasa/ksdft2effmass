# Silicon k-point-density convergence

**Status:** one four-point Quantum ESPRESSO 7.5 calculated tutorial observation retained; ABINIT realization not yet implemented.

## Learning objective

This tutorial studies the represented total energy of two-atom diamond silicon as
Brillouin-zone sampling changes while the structure, pseudopotential, wavefunction
cutoff, occupations, and electronic-solver settings remain fixed.

The Quantum ESPRESSO realization belongs to
`quantumespresso.simulations.convergence-silicon-kpoint-density`. Its scalar abscissa is

$$
\rho_k = \frac{N_{\mathrm{full}}}{\Omega_{\mathrm{reciprocal}}},
$$

where $N_{\mathrm{full}}=n_1n_2n_3$ and the reciprocal primitive-cell volume uses the
project convention $A B^T=2\pi I$. The mesh tuple and shift remain explicit because a
scalar density does not encode anisotropy. The symmetry-reduced point count is retained
as backend-observed metadata rather than used to define $\rho_k$.

The authoritative compact result is a point-indexed table; a plot may be derived from
it. This tutorial is separate from wavefunction-cutoff convergence and structural
relaxation and does not select or validate a production mesh.

## Backends

- [`qe/`](qe/) — one authorized four-point QE 7.5 attempt completed without retry; no production mesh was selected.
- [`abinit/`](abinit/) — planned correspondence only; no execution is authorized.
