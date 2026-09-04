# ABINIT silicon SCF backend

**Status: calculated tutorial observation; portable example planned.**

ABINIT 10.8.3 basic3 dataset 1 was executed as the self-consistent-density
producer for the paired silicon SCF-to-bands tutorial. The exact single-shot
process exited 0, and ABINIT reported energy convergence at SCF step 5 with a
total energy of `-8.52502677067667 Ha`. This is a calculated tutorial
observation, not production convergence, numerical verification, scientific
validation, or acceptance.

The calculated settings and result identities are retained in the
[ABINIT bands-workflow observation](../../silicon-bands/abinit/expected/abinit1083-calculated-observation.json).
Native input, PseudoDojo pseudopotential, density, wavefunctions, NetCDF, and
streams remain external.

This directory still contains no project-owned portable ABINIT input. A future
portable implementation must preserve the silicon-SCF learning objective and
document backend-specific units, pseudopotential representation, cutoff,
sampling, and output semantics. Numerical comparison with the QE backend
requires a separate explicit alignment contract.
