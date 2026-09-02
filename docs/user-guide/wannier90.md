# Wannier90

Wannier90 remains a separate external backend responsible for disentanglement, gauge construction, localization, interpolation, and related outputs. The QE bridge and Wannier90 execution are not one interchangeable backend.

Prospective capabilities are selected individually:

- `wannier90.x -pp` preprocessing and `.nnkp` generation;
- `wannier90.x` localization/interpolation;
- `postw90.x` only when a declared downstream observable requires it.

Stage 03 owns the Wannier-compatible uniform-grid NSCF child. It must reference the accepted G02 SCF parent manifest and consume declared capabilities of the neutral `PeriodicElectronicStructureDataset`. The QE-to-Wannier bridge retains typed references to `.nnkp`, `.amn`, `.mmn`, `.eig`, and separately approved optional artifacts. Wannier overlap and projection matrices are distinct semantic products, not interchangeable wavefunction representations.

Wannier90 execution uses the same pure-guard, two-phase request/result CPN boundary as
QE. Wannier90 3.1.0 is installed and has completed version and linkage probes only;
ABINIT 10.8.3 reports its connector enabled. No scientific input, tutorial, or test
suite has run, so this installation does not establish localization behavior,
QE–Wannier90 or ABINIT–Wannier90 interface compatibility, numerical verification, or
scientific validation. Exact installation identity is retained in
`docs/computational/wannier90-3.1.0-installation.md`.
