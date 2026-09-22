# GaAs non-SOC bands

**Status:** one authorized Quantum ESPRESSO 7.5 attempt completed with a retained bands-stage failure observation; ABINIT realization not implemented.

## Learning objective

This tutorial probes how a generic calculator and Workflow interface represents a
compound semiconductor with two atomic species, two pseudopotentials, an SCF state
admitted into a fixed-path bands calculation, and symmetry-aware band postprocessing.

The smallest proposed QE realization explicitly defers the source's `vc-relax` branch
and DOS-only NSCF branch. It uses the source-recorded fixed lattice parameter and runs
SCF, bands, and `bands.x` as three isolated stages with content-identity-checked native
state transfer.

GaAs is outside the project's supported material scope. Any calculated result will be
software-workflow evidence, not a validated GaAs geometry, band structure, gap, or
controlled baseline for spin-orbit coupling.

## Backends

- [`qe/`](qe/) — exact QE 7.5 attempt complete; SCF admitted, bands failed, and dependent `bands.x` remained unattempted under the no-retry policy.
- [`abinit/`](abinit/) — correspondence placeholder only; no implementation or execution is authorized.
