<!-- Generated from SQLite control state; do not edit. -->
# Task B — Provenance foundation

[Task index](index.md) · [Previous](./ARCHITECTURE-DECISION-SKILL-1.md) · [Next](./C.md)

## Status

`superseded`: prospectively superseded for workflow sequencing by P2/P3; never launched

## Objective

Implement the approved portable provenance foundation without coupling it to DFT, QE, TB, Wannier, or operators.

## Parent and prerequisites

None.

## Authority references

- harness/archive/task-control-v1/tasks/B.md

## Authorized scope

- immutable `ArtifactReference`;
- separately owned `ArtifactLocation` or explicit resolver contract;
- immutable `RunManifest`;
- deterministic serializers/deserializers;
- checksum and directory-index verification actions;
- structured partial, interrupted, resumed, missing, and checksum-mismatch states.

## Completion criteria

- Implementation, software-verification tests, documentation, independent read-only review, parent verification, and human acceptance are all required. Acceptance contributes to G01a and unlocks C, E, F, and H according to their remaining prerequisites; it launches none.

## Exclusions

- No `logical_path_or_uri` field is permitted. Storage technology, deletion, unrestricted environment capture, production manifests, and real execution are excluded.

## Historical source

`harness/archive/task-control-v1/tasks/B.md` (`sha256:49c3dd593d56607de9ff2ca88ea9ccebc9fc660e38a4947db8a997f15e57e85b`)
