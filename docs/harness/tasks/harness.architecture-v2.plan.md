<!-- Generated from SQLite control state; do not edit. -->
# Plan harness Architecture v2

[Task index](index.md) · [Previous](./harness-task-state-symlink-toctou-hardening.md) · [Next](./harness.architecture-v2.simulation-execution.md)

## Status

`inactive`: Planning-only and inactive. Architecture documentation is version-isolated: v1 is one implemented-system snapshot, v2 contains normative target architecture only, and the migration page contains all cross-version comparison. This Task authorizes no implementation or scientific execution.

## Objective

Maintain strict version isolation between the self-contained implemented Architecture v1 snapshot, the normative Architecture v2 target, and the explicit v1-to-v2 migration crosswalk without authorizing implementation.

## Parent and prerequisites

None.

## Authority references

- docs/architecture/index.md
- docs/architecture/migration-v1-to-v2.md
- docs/architecture/v1/index.md
- docs/architecture/v2/index.md

## Authorized scope

- Maintain a self-contained v1 architecture tree that mirrors the v2 subject structure while describing only implemented behavior, generated state, documented intention, known limitations, and historical execution.
- Maintain normative v2 pages containing only the selected development-harness, scientific-workflow, simulation, Campaign/CPN, artifact, calculator, analysis, control, compiler, validation, persistence, projection, composition, and package target responsibilities.
- Maintain all current-to-target responsibility maps, implementation status, cutover conditions, migration order, and unresolved extraction/import decisions only in the v1-to-v2 migration page.
- Keep ProjectKoios Bootstrap and Workflows as conceptual target ownership boundaries without claiming current package integration.
- Repair maintained architecture navigation and remove duplicate unversioned or harness-local Architecture v2 authority without creating an archive or ADR.

## Completion criteria

- docs/architecture has indexed v1 and v2 trees plus one migration page; docs/harness/architecture-v2 no longer exists, and page counts are not part of the architecture contract.
- The v1 tree is self-contained and accurately records implemented repository, harness, CPN, scientific-record, validation, calculator-execution, historical-execution, and limitation boundaries while mirroring v2 subjects.
- V2 pages use target terminology and contain no v1 implementation narrative or cross-version chronology; the required two-harness and lifecycle diagrams are preserved.
- The migration page contains the complete responsibility crosswalk, ProjectKoios ownership status, ordered cutover, direct-execution fixture disposition, and unresolved target import/package decisions.
- Maintained links, Mermaid blocks, Task/graph state, synchronized control projections, source-aware verification, SQLite integrity, dependency immutability, and git diff checks pass without implementation or scientific execution.

## Exclusions

- Do not implement Architecture v2, change Python source or tests, alter CPN behavior, integrate ProjectKoios packages, add dependencies, or begin a simulation-execution slice.
- Do not modify scientific results, calculation inputs, pseudopotentials, external artifacts, scientific settings, publication or release state, or any protected execution boundary.
- Do not create ADRs, compatibility documentation trees, archive copies of removed architecture pages, additional Tasks, checkpoints, successor activations, plugin frameworks, or mutable registries.

## Historical source

No archived source.
