# Quantum ESPRESSO realization

One exact Quantum ESPRESSO 7.5 `pw.x` variable-cell-relaxation Task was authorized by
checkpoint `QE-SILICON-VCRELAX-RUN-HC01` and executed once without retry. The pinned
input used a 30 Ry cutoff, shifted $6\times6\times6$ mesh, fixed atomic positions, an
initial 14 Bohr lattice parameter, and `cell_dofree='ibrav'`.

The process exited with status 0 and printed `JOB DONE.`. Quantum ESPRESSO reported
BFGS convergence after 14 SCF cycles and 12 BFGS steps. The printed final-coordinate
cell corresponds to a derived conventional cubic lattice constant of
`10.207479548` Bohr; QEXSD gives `10.207479550732002` Bohr from its final cell vectors.
The BFGS final enthalpy was `-15.8536258899` Ry.

QE then performed its distinct final SCF calculation after recalculating G-vectors. It
reported convergence in six iterations, total energy `-15.85238670` Ry, and pressure
`-1.22` kbar. These values are not substituted for the preceding BFGS enthalpy and
terminal optimization pressure. Intermediate stdout also contained six BFGS curvature
warnings and fourteen `c_bands` messages reporting one unconverged eigenvalue; they are
retained alongside the later convergence reports rather than silently discarded.

The compact calculated observation is
[qe75-calculated-observation.json](expected/qe75-calculated-observation.json). Native
QEXSD, charge density, wavefunctions, complete streams, and snapshots remain in the
identified external run. The source input and pseudopotential are not redistributed
here.

This is a calculated tutorial observation, not a cutoff, mesh, pseudopotential, or
convergence study; numerical verification; scientific validation; uncertainty
quantification; or a project lattice reference. A later human decision selected its
QEXSD-derived geometry only for the bounded tutorial DOS Workflow. See the
[exact preflight](../../../../docs/computational/silicon-structure-optimization-preflight.md).
