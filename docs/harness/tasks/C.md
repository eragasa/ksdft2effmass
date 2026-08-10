<!-- Generated from SQLite control state; do not edit. -->
# Task C — Backend-neutral DFT DataObjects and ResultObjects

[Task index](index.md) · [Previous](./B.md) · [Next](./D.md)

## Status

`superseded`: prospectively superseded for workflow sequencing by P4; never launched

## Objective

Implement the neutral scientific records and compact Kohn–Sham calculation ResultObject without importing a backend.

## Parent and prerequisites

None.

## Authority references

- dft/paw.py
- harness/archive/task-control-v1/tasks/C.md

## Authorized scope

- structure, site, species, pseudopotential, sampling, and calculation-specification DataObjects;
- `PseudopotentialFormalism` representation without execution-support claims;
- `KPointSet`, `KohnShamBandStructure`, and `KohnShamArtifactSet` DataObjects;
- immutable `KohnShamDataset` ResultObject.

## Completion criteria

- Implementation, software and applicable numerical verification, documentation, independent read-only review, parent verification, and human acceptance are required. Acceptance unlocks E and contributes to G and H; it launches none.

## Exclusions

- No `dft/paw.py`, generic operator/projector payload, QE import, file parsing, unit conversion policy, serializer method on a DataObject, or large embedded production payload is permitted.

## Historical source

`harness/archive/task-control-v1/tasks/C.md` (`sha256:2c23d6ffe7b3ddf2599b61439982531be4e8be4729b5f5c31f676d6b096fb1d0`)
