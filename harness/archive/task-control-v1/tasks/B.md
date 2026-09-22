# Task B — Provenance foundation

Status: prospectively superseded for workflow sequencing by P2/P3; never launched

The provenance content remains preserved. See `.pi/tasks/backend-neutral-cpn-workflow-architecture.md`.

## Objective

Implement the approved portable provenance foundation without coupling it to DFT, QE, TB, Wannier, or operators.

## Prerequisites

- human acceptance of Task A.

## Owned objects and actions

- immutable `ArtifactReference`;
- separately owned `ArtifactLocation` or explicit resolver contract;
- immutable `RunManifest`;
- deterministic serializers/deserializers;
- checksum and directory-index verification actions;
- structured partial, interrupted, resumed, missing, and checksum-mismatch states.

No `logical_path_or_uri` field is permitted. Storage technology, deletion, unrestricted environment capture, production manifests, and real execution are excluded.

## Completion sequence

Implementation, software-verification tests, documentation, independent read-only review, parent verification, and human acceptance are all required. Acceptance contributes to G01a and unlocks C, E, F, and H according to their remaining prerequisites; it launches none.
