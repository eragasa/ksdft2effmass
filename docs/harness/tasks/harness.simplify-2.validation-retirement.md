<!-- Generated from SQLite control state; do not edit. -->
# Consolidate validation and retire replay machinery

[Task index](index.md) · [Previous](./harness.simplify-2.resource-decomposition.md) · [Next](./harness.simplify-2.wire-validation-decomposition.md)

## Status

`inactive`: corrected inactive R2.7 repository-validation composition and legacy-route retirement work package; separate explicit human activation required and no automatic successor activation

## Objective

Compose evidence, resource, Task, wire, and other repository validation results into one structured maintained result, invoke full reconstruction in check mode through the existing control owner, and retire replay, nested CLI validation, and duplicated cross-domain gates.

## Parent and prerequisites

- Parent: `harness.simplify-2`
- Depends on: `harness.simplify-2.cli-consolidation`

## Authority references

- AGENTS.md
- harness/intake/harness.simplify-2.md
- harness/tasks/harness.simplify-2.json

## Authorized scope

- Compose evidence, resource, Task, wire, and other domain validation results without absorbing their rule ownership into the repository-wide orchestration layer.
- Invoke the existing full reconstruction owner in check mode and consume its structured schema, relationship, SQLite, SQL-export, and projection-agreement result; R2.7 does not write SQLite directly and does not duplicate `HarnessControlMigrator`.
- Prove live-consumer obsolescence before retiring `replay_current_validators.py`, H3-era resource gates, nested CLI validation, or duplicated cross-domain validation paths.
- Provide one composable maintained validation Action returning structured named checks, statuses, findings, and durations, with one project-local renderer and no CLI-output parsing.
- Consume the completed R2.6 CLI inventory and command/API agreement without reopening CLI placement or reintroducing maintained wrappers outside `python/src/cli/`; expose integrated validation without parsing another CLI's output.
- Perform cross-package integration validation, synchronize directly affected documentation, and obtain one consolidated independent read-only compatibility review with at most one correction pass.
- Conclude the parent program pending explicit human acceptance with `active_task` restored to null and no successor activated.

## Completion criteria

- One maintained validation Action produces structured named checks, statuses, findings, and durations; one renderer exposes the result and no validator invokes another CLI and parses its output.
- Retired replay, H3-era, nested, and duplicated routes have no remaining live consumers; required historical records and compatibility remain preserved.
- The completed R2.6 command surface remains intact: every maintained live CLI script and entry point resides under `python/src/cli/`, no maintained executable wrapper elsewhere under `python/src/`, `harness/`, or `.pi/` becomes live again, and integrated validation requires no generated shell, inline-Python fragment, or nested CLI-output parsing.
- Full reconstruction in check mode is delegated to the existing control owner and contributes one structured result; R2.7 contains no direct SQLite write, second database-construction path, incremental mutation, or duplicated publication logic.
- Focused validation tests, complete resource and evidence conformance, deterministic full SQLite reconstruction and projection agreement, Sphinx warnings-as-errors, and dependency-lock nonmutation checks pass.
- One consolidated independent read-only compatibility review has no unresolved material findings after at most one consolidated correction pass.
- The parent is complete pending explicit human acceptance, `active_task` is null, and no telemetry, production-source refactor, scientific work, protected execution, or successor is activated.

## Exclusions

- Do not freeze a new public command grammar, import, or wire contract where the accepted parent authority leaves materially different defensible choices; stop for a human decision when required.
- Do not write SQLite directly, duplicate `HarnessControlMigrator`, create incremental SQL mutation or partial projection tracking, introduce another database or persistence framework, or infer authority from a watcher, daemon, event log, filesystem timing, current directory, or ambient discovery.
- Do not implement telemetry, observations collection, instrumentation, dashboards, tokens, costs, or effectiveness claims; bounded migration-performance measurements remain diagnostics only.
- Do not rewrite or delete retained `.pi` history or historical evidence scripts that record commands actually used; the `python/src/cli` location requirement applies to maintained live CLIs. Do not add dependencies, modify scientific/package-source modules, publish, release, or perform external, scientific, or other protected execution.

## Historical source

No archived source.
