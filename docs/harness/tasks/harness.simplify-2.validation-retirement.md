<!-- Generated from SQLite control state; do not edit. -->
# Consolidate validation and retire replay machinery

[Task index](index.md) · [Previous](./harness.simplify-2.resource-decomposition.md) · [Next](./harness.simplify-2.wire-validation-decomposition.md)

## Status

`inactive`: corrected inactive R2.7 repository-validation composition, shared private compiler extraction, and legacy-route retirement work package; parent-authorized deterministic transition only, currently not activated, and no automatic successor activation

## Objective

Compose evidence, resource, Task, wire, and other repository validation results into one structured maintained result, extract one shared private control-generation compiler for candidate-based publication and nonmutating conformance, and retire replay, nested CLI validation, and duplicated cross-domain gates.

## Parent and prerequisites

- Parent: `harness.simplify-2`
- Depends on: `harness.simplify-2.cli-consolidation`

## Authority references

- AGENTS.md
- harness/intake/harness.simplify-2.md
- harness/tasks/harness.simplify-2.json

## Authorized scope

- Compose evidence, resource, Task, wire, and other domain validation results without absorbing their rule ownership into the repository-wide orchestration layer.
- Preserve the public responsibilities and current public imports and execute signatures: `HarnessControlMigrator` reconstructs, validates, and publishes maintained control state, while `HarnessControlVerifier` performs nonmutating conformance checks. Do not claim or add a migrator check mode.
- Extract exactly one private control-generation compiler with the boundary `authoritative repository inputs → private compiler → complete candidate SQLite and projection artifact set`. This compiler owns construction mechanics once and is consumed by both existing public Actions; introduce neither a second database-construction algorithm nor a public construction Action.
- Make `HarnessControlMigrator` consume the private compiler to compile, validate the complete candidate, and publish. The migrator remains the sole publisher of maintained SQLite, deterministic SQL export, projection manifest, and generated projections.
- Make `HarnessControlVerifier` consume the same private compiler to compile and compare a complete candidate against maintained state and report without publication or other maintained writes. Conformance covers authoritative source inputs versus maintained SQLite, deterministic SQL export, projection manifest, and generated projections; database-versus-SQL agreement alone is insufficient because both may be stale relative to source authority.
- Remove ordinary temporary candidate SQLite, SQL, projection, sidecar, and staging artifacts after verification on success or failure. R2.7 composes the verifier's structured source-aware result rather than invoking a CLI or parsing output.
- Prove live-consumer obsolescence before retiring `replay_current_validators.py`, H3-era resource gates, nested CLI validation, or duplicated cross-domain validation paths.
- Provide one composable maintained validation Action returning structured named checks, statuses, findings, and durations, with one project-local renderer and no CLI-output parsing.
- Consume the completed R2.6 CLI inventory and command/API agreement without reopening CLI placement or reintroducing maintained wrappers outside `python/src/cli/`; expose integrated validation without parsing another CLI's output.
- Perform cross-package integration validation, synchronize directly affected documentation, and obtain one consolidated independent read-only compatibility review with at most one correction pass.
- Implement R2.7 as a complete vertical replacement of its owned validation and control-generation internals: accepted end-state contract, isolated implementation, complete affected-data migration, controlled parity, one cutover, and removal of obsolete live validation and construction paths. Do not retain old and new operational authorities after cutover except for temporary compatibility required by an accepted public contract.
- Because the active parent authorizes the full round, R2.7 requires no separate human activation cycle once R2.6 is complete and the parent agent explicitly transitions to it with no unresolved checkpoint, human-owned material choice, protected action, or unresolved material review finding. Keep one active child, prohibit background activation, and keep automatic successor activation false.
- Internal implementation commits and deterministic child transitions require no separate checkpoint, acceptance packet, or human review cycle. Perform one consolidated independent compatibility review in R2.7, with at most one correction pass, before concluding the parent program pending final explicit human acceptance with `active_task` restored to null and no successor activated.

## Completion criteria

- One maintained validation Action produces structured named checks, statuses, findings, and durations; one renderer exposes the result and no validator invokes another CLI and parses its output.
- Retired replay, H3-era, nested, and duplicated routes have no remaining live consumers; required historical records and compatibility remain preserved.
- The completed R2.6 command surface remains intact: every maintained live CLI script and entry point resides under `python/src/cli/`, no maintained executable wrapper elsewhere under `python/src/`, `harness/`, or `.pi/` becomes live again, and integrated validation requires no generated shell, inline-Python fragment, or nested CLI-output parsing.
- Exactly one private compiler constructs complete candidate artifacts from authoritative inputs. `HarnessControlMigrator` alone validates and publishes a candidate; `HarnessControlVerifier` compiles and compares without maintained writes, checks source authority against SQLite, SQL export, and every projection, and removes ordinary temporary artifacts. No migrator check mode, second construction path, incremental mutation, public construction Action, or duplicated publication logic exists.
- Focused validation tests, complete resource and evidence conformance, deterministic full SQLite reconstruction and projection agreement, Sphinx warnings-as-errors, and dependency-lock nonmutation checks pass.
- One consolidated independent read-only compatibility review has no unresolved material findings after at most one consolidated correction pass.
- The parent is complete pending explicit human acceptance, `active_task` is null, and no telemetry, production-source refactor, scientific work, protected execution, or successor is activated.

## Exclusions

- Do not freeze a new public command grammar, import, or wire contract where the accepted parent authority leaves materially different defensible choices; stop for a human decision when required.
- Do not publish SQLite outside `HarnessControlMigrator`, duplicate the private compiler, create incremental SQL mutation or partial projection tracking, introduce another maintained database or persistence framework, expose a public construction Action, or infer authority from a watcher, daemon, event log, filesystem timing, current directory, or ambient discovery. Temporary verifier candidates are nonauthoritative and must be removed after use.
- Do not implement telemetry, observations collection, instrumentation, dashboards, tokens, costs, or effectiveness claims; bounded migration-performance measurements remain diagnostics only.
- Do not rewrite or delete retained `.pi` history or historical evidence scripts that record commands actually used; the `python/src/cli` location requirement applies to maintained live CLIs. Do not add dependencies, modify scientific/package-source modules, publish, release, or perform external, scientific, or other protected execution.

## Historical source

No archived source.
