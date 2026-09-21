# Wannier90 3.1.0 example08: Iron states around the Fermi level

> Human-readable companion to the authoritative adjacent JSON Task record.

## Task metadata

- **Schema version:** `3`
- **Task ID:** `wannier90.tutorials.v3_1_0.example08`
- **Status:** `deferred`
- **Status detail:** Deliberately deferred inventory Task for Wannier90 3.1.0 `examples/example08`. It is not selected for execution; no workspace has been created and no command has been invoked by this Task.
- **Parent Task:** `wannier90.tutorials.v3_1_0`
- **Explicit activation required:** `true`
- **Intake path:** None.
- **Archived source:** None.

## Objective

Preflight and, only after exact protected-execution authorization, execute or deliberately defer the bundled Wannier90 3.1.0 `examples/example08` tutorial on iron states around the fermi level.

## Relationships

### Task prerequisites

- `P2`
- `quantumespresso.simulations.integration`

### External prerequisites

- `local_execution_resource_authorization`
- `pseudopotential_selection_and_license`
- `qe_tutorial_execution_authorization`
- `tutorial_input_terms_accepted`
- `wannier90_tutorial_execution_authorization`
- `wannier90_tutorial_preflight_completed`

### Superseded by

- None.

## Authorized scope

- Inventory the exact `examples/example08` source directory: 6 files with canonical path-and-content manifest SHA-256 `9b2062a0125408ca7851b79c7e13ce7a6c507e7bd604ee3c86a41f63a1161f9e`.
- Inspect the tutorial inputs, required executables and interfaces, pseudopotentials or supplied matrices, terms, environment assumptions, expected cost, stage order, warnings, and output behavior without executing them.
- If separately authorized, copy only the exact preflighted minimum assets into a new isolated ignored run workspace and invoke only the declared bounded stage sequence without automatic retries.
- Retain exact source and executable identities, inputs, pseudopotential or matrix identities and terms, commands, attempts, streams, runtimes, exit states, warnings, and compact artifact inventories.
- Record a completed, completed-with-warning, failed, unsupported, or deliberately deferred learning disposition without automatically activating another tutorial or production work.

## Completion criteria

- The source-directory Task has an explicit evidence-backed execution or deliberate-deferral disposition.
- Any invocation is covered by exact protected-execution authorization and remains within its declared stage, resource, retry, and warning-handling envelope.
- Retained evidence distinguishes tutorial behavior from project production convergence, numerical verification, scientific validation, and human acceptance.
- No large native output, restart state, wavefunction, charge density, dense matrix, or mutable tutorial workspace is committed to Git.

## Exclusions

- This Task record does not authorize execution, dependency installation, pseudopotential download, network access, remote computation, workspace creation, or source-tree mutation.
- Bundled settings and outputs do not override project specifications or become production defaults.
- A successful tutorial does not establish scientific correctness, cross-version equivalence, production suitability, or support for its material system.
- Automatic retries, successor activation, and unbounded execution are prohibited.

## Authority references

- `docs/computational/wannier90.tutorials.v3_1_0.md`
