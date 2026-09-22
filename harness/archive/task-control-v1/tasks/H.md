# Task H — Wannier specification and QE–Wannier bridge

Status: prospectively superseded for workflow sequencing by P8/P9; never launched

The Wannier specification/bridge content remains preserved. See `.pi/tasks/backend-neutral-cpn-workflow-architecture.md`.

## Objective

Implement neutral Wannier input specifications and the explicit QE-to-Wannier bridge without collapsing QE and Wannier90 into one backend.

## Prerequisites

- human acceptance of Tasks B, C, D, and E;
- before a real Stage 03 run, accepted G02 SCF parent manifest and separately approved target bands, windows, projections, and uniform grid.

## Owned objects and actions

- Wannierization specification and input-set objects;
- `WannierizationInputBuilder`;
- `QuantumEspressoWannier90Bridge`;
- typed references for `.nnkp`, `.amn`, `.mmn`, `.eig`, and approved optional bridge artifacts;
- explicit lineage from the Stage 03 uniform-grid NSCF child to the accepted G02 SCF parent.

Wannier90 execution remains a separate backend. This task does not implement localization, run QE/Wannier90 without authorization, treat `projwfc.x` output as `.amn`, or place bridge filenames in the neutral Kohn–Sham core.

## Completion sequence

Implementation, tests, documentation, independent read-only review, parent verification, and human acceptance are required. Real execution additionally requires the production authorization checkpoint.
