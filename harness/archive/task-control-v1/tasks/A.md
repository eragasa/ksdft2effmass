# Task A — Control-plane and language-neutral specification contract

Status: prospectively superseded for workflow sequencing by P1/P4; never launched

The scientific contract content remains preserved. See `.pi/tasks/backend-neutral-cpn-workflow-architecture.md`.

## Objective

Turn the approved architecture into versioned language-neutral scientific, numerical, array, error, and serialization contracts before production source implementation. This task may create approved schemas and fixtures only after explicit launch; this architecture-recording turn creates none.

## Prerequisites

- approved `.pi/tasks/backend-neutral-kohn-sham-qe-architecture.md`;
- accepted physical and numerical specification records;
- accepted operator-record foundation.

## Owned contract

- approved units, reciprocal/Fourier conventions, axis ordering, spin/occupation metadata, and compact-versus-external boundary;
- DataObject/ResultObject/ActionObject inventory;
- fixed field names and Rust-translatable tagged states;
- public structured errors;
- valid/invalid and numerical fixture design;
- G01a/G01b supersession cross-references.

It must not select a pseudopotential or production environment, implement Python production modules, copy PhysKit, or run QE.

## Completion sequence

1. implementation of the specification artifacts;
2. software/numerical fixture evidence as applicable;
3. documentation synchronization;
4. independent read-only architecture/integration review;
5. parent verification;
6. human acceptance.

Acceptance unlocks B and D. It does not launch either task.
