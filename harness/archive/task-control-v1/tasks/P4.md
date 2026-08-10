# P4 — Neutral periodic electronic-structure structures, specifications, and datasets

Status: blocked by accepted P1 and P2

## Objective

Implement the approved periodic electronic-structure DataObjects and immutable `PeriodicElectronicStructureDataset`/`SCFConvergenceResult` ResultObjects as project-owned CPN payloads without importing workflows.cpn, SNAKES, or a backend.

The domain is periodic KS/GKS electronic structure for crystalline solids organized in Bloch fibers. Preserve direct/reciprocal lattice, Brillouin-zone, $k$-point, band, unit, reciprocal/Fourier, spin/occupation, energy-reference, convergence, pseudopotential/PAW provenance, downstream-capability, and compact/external-artifact contracts. Keep theory, core treatment, numerical representation, backend, and available-product axes independent. Do not introduce molecular coverage, a universal DFT API, generic operator reconstruction from eigenvalues, a generic wavefunction object, a `PAWCalculator`, hybrid runtime support, or ABINIT implementation. This task preserves A/C content as prospectively corrected by `docs/architecture/periodic-electronic-structure-integration.md`.

Completion requires implementation, tests, documentation, independent review, parent verification, and human acceptance.