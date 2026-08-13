<!-- Generated from SQLite control state; do not edit. -->
# Plan harness Architecture v2

[Task index](index.md) · [Previous](./harness-task-state-symlink-toctou-hardening.md) · [Next](./harness.architecture-v2.simulation-execution.md)

## Status

`inactive`: Proposed architecture; inactive; not implemented; not accepted. Separate explicit human activation is required before any implementation Task may be created or executed.

## Objective

Plan a second-generation harness architecture from observed repository operation while leaving the accepted periodic-extraction implementation unchanged.

## Parent and prerequisites

None.

## Authority references

- docs/harness/architecture-v2/index.md
- harness/reports/control-plane-cleanup-slice-b.md
- harness/reports/control-plane-cleanup-slice-c-dispositions.md
- harness/tasks/harness.control-plane-cleanup.json

## Authorized scope

- Document an inactive compiler-style harness architecture separating control, compilation, validation, projection, synchronization, execution, evidence, telemetry, and Git-history planes.
- Map current origin/dev responsibilities to proposed target owners and dispositions without changing current source, schemas, CLIs, SQLite behavior, agents, skills, or scientific workflows.
- Propose a bounded eleven-slice migration beginning with a governed-operation lifecycle and explicit repository-context preflight before any telemetry implementation, plus governed action execution, an immutable SQLite projection lifecycle, extension boundaries, and effectiveness criteria using the completed QE tutorial as the primary acceptance scenario.
- Distinguish deterministic operation-specific execution-context validation from optional session observation; propose RepositoryContext, RepositoryContextRequirement, ObserveRepositoryContext, ValidateRepositoryContext, and deferred operation receipts without implementing them.
- Formalize policy-selected preflight, implementation, verification, conditional read-only review, and conditional human-acceptance stages; minimum request/result responsibilities; current single-writer limitations; deferred restricted-dispatch enforcement; and the non-authoritative relationship from operation transitions through optional receipts to later telemetry.

## Completion criteria

- All nine Architecture v2 Markdown pages exist, agree, and identify themselves as proposed, inactive, not implemented, and not accepted.
- Current authority and proposed target state are distinct; current responsibilities and migration slices are mapped; operation lifecycle, extension, SQLite, governed-execution, explicit-root repository-context, optional-observation, and scientific-fast-path boundaries are explicit.
- Lifecycle documentation preserves the required state diagram and distinguishes preflight, implementation, verification, conditional read-only review, and conditional human acceptance without making stages automatic Tasks, agents, checkpoints, commits, or human decisions.
- The generated Task page and maintained harness-index link exist; current control synchronization, source-aware validation, documentation links, applicable Sphinx build, dependency immutability, and git diff checks pass.
- No implementation occurs, no child implementation Task is created, the accepted bulk-silicon.records.periodic.extraction implementation remains unchanged, no successor is activated, and automatic successor activation remains disabled.

## Exclusions

- Do not implement Architecture v2, repository-context objects, receipts, telemetry stores, failure catalogs, source or test refactors, SQLite schemas or lifecycle, control migration, CLIs, Pi extension code, agents or skills, CPN behavior, or dependencies.
- Do not modify periodic-record extraction, simulations, pseudopotentials, scientific settings, dependency or lock files, publication or release state, or any protected execution boundary.
- Do not create ADRs, child implementation Tasks, plugin frameworks, service locators, mutable global registries, speculative abstract bases, pre-alpha compatibility layers, or successor activations.

## Historical source

No archived source.
