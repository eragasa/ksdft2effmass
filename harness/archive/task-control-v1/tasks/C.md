# Task C — Backend-neutral DFT DataObjects and ResultObjects

Status: prospectively superseded for workflow sequencing by P4; never launched

The neutral DFT content remains preserved. See `.pi/tasks/backend-neutral-cpn-workflow-architecture.md`.

## Objective

Implement the neutral scientific records and compact Kohn–Sham calculation ResultObject without importing a backend.

## Prerequisites

- human acceptance of Tasks A and B.

## Owned objects

- structure, site, species, pseudopotential, sampling, and calculation-specification DataObjects;
- `PseudopotentialFormalism` representation without execution-support claims;
- `KPointSet`, `KohnShamBandStructure`, and `KohnShamArtifactSet` DataObjects;
- immutable `KohnShamDataset` ResultObject.

No `dft/paw.py`, generic operator/projector payload, QE import, file parsing, unit conversion policy, serializer method on a DataObject, or large embedded production payload is permitted.

## Completion sequence

Implementation, software and applicable numerical verification, documentation, independent read-only review, parent verification, and human acceptance are required. Acceptance unlocks E and contributes to G and H; it launches none.
