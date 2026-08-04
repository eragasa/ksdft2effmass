# Quantum ESPRESSO

Quantum ESPRESSO is the initial production backend for periodic KS/GKS electronic-structure calculations. The immediate scientific path is semilocal periodic KS for silicon. The project owns neutral periodic specifications/results and concrete QE adapters; it does not reimplement electronic-structure theory.

Prospective capabilities are selected individually:

- `pw.x` SCF;
- `pw.x` NSCF;
- `bands.x` when band ordering or symmetry output is required;
- `projwfc.x` when its specific projector diagnostics are required;
- `pw2wannier90.x` for the QE-to-Wannier90 interface.

Membership in the QE distribution does not make every executable required.

Input mapping, deterministic text serialization, mechanical output/save parsing, result adaptation, execution, and convergence analysis have separate owners. QE execution occurs outside CPN guards through immutable request/result tokens. A process exit, parsed result, converged SCF state, accepted numerical protocol, and scientifically validated result are distinct states.

The immediate path is `semilocal periodic specification -> QE -> PeriodicElectronicStructureDataset -> Wannier90`. Hybrid GKS mapping and execution are deferred; semilocal evidence cannot qualify a hybrid profile. A production QE run does not require a simultaneous ABINIT duplicate.

No QE executable or pseudopotential has been authorized by this architecture pass. Tutorial-derived future cases are interface and parser behavioral references, not numerical oracles. See [Periodic backends](dft-backends.md), [Cross-backend verification](cross-backend-verification.md), [External dependencies](external-dependencies.md), and [Troubleshooting](troubleshooting.md).
