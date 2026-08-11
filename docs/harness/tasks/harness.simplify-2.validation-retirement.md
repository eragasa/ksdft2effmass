<!-- Generated from SQLite control state; do not edit. -->
# Consolidate validation and retire replay machinery

[Task index](index.md) · [Previous](./harness.simplify-2.resource-decomposition.md) · [Next](./harness.simplify-2.validation-retirement.generation-builder.md)

## Status

`completed`: completed after the single bounded post-review correction with one live Task schema, one Python evidence route, one repository validator, no live shadow or routing compatibility, and no human-acceptance claim

## Objective

Compose evidence, resource, Task, wire, and other repository validation results into one structured maintained result, extract one narrow private control-generation builder for candidate-based publication and nonmutating conformance, and retire replay, nested CLI validation, and duplicated cross-domain gates.

## Parent and prerequisites

- Parent: `harness.simplify-2`
- Depends on: `harness.simplify-2.cli-consolidation`

## Authority references

- AGENTS.md
- harness/intake/harness.simplify-2.md
- harness/tasks/harness.simplify-2.json

## Authorized scope

- Compose evidence, resource, Task, wire, and other domain validation results without absorbing their rule ownership into the repository-wide orchestration layer.
- Preserve the public responsibilities and current public imports and execute signatures: `HarnessControlMigrator` reconstructs, validates, and publishes maintained control state, while `HarnessControlVerifier` performs nonmutating conformance checks. There is no migrator check mode.
- Extract exactly one narrow private control-generation builder with the boundary `authoritative repository inputs → private builder → complete candidate SQLite, SQL, manifest, and projection artifacts`. The implementation may use a private stateless builder and immutable result, but it introduces no second construction algorithm and no public builder Action or frozen public interface.
- Make `HarnessControlMigrator` use the private builder, validate the complete candidate, and remain the sole publisher of maintained SQLite, deterministic SQL export, projection manifest, and generated projections.
- Make `HarnessControlVerifier` derive the canonical maintained evidence, resource, Task, and graph input set from repository-owned configuration, use the same private builder, compare the candidate with maintained artifacts, report differences, and perform no maintained writes. Verification detects authoritative-source drift even when maintained SQLite and maintained SQL agree with each other.
- Limit the source-aware guarantee to maintained canonical control state. Do not claim that `HarnessControlVerifier.execute(repository_root)` reproduces arbitrary noncanonical migration requests or alternate output locations, and preserve bounded compatibility for nondefault `HarnessControlMigrationRequest` inputs unless separately authorized.
- Remove temporary candidate SQLite, SQL, manifest, projection, sidecar, and staging artifacts after verification on success or failure. Compose the verifier's structured source-aware result without invoking a CLI or parsing output.
- Prove live-consumer obsolescence before retiring `replay_current_validators.py`, H3-era resource gates, nested CLI validation, or duplicated cross-domain validation paths.
- Provide one composable maintained validation Action returning deterministic structured named checks, statuses, and findings without durations, with one project-local renderer and no CLI-output parsing.
- Consume the completed R2.6 CLI inventory and command/API agreement without reopening CLI placement or reintroducing maintained wrappers outside `python/src/cli/`; expose integrated validation without parsing another CLI's output.
- Perform cross-package integration validation and synchronize directly affected documentation.

## Completion criteria

- One maintained validation Action produces deterministic structured named checks, statuses, and findings without durations; one renderer exposes the result and no validator invokes another CLI or parses CLI output.
- Retired replay, H3-era, nested, and duplicated routes have no remaining live consumers; required historical records and compatibility remain preserved.
- The completed R2.6 command surface remains intact: every maintained live CLI script and entry point resides under `python/src/cli/`, no maintained executable wrapper elsewhere under `python/src/`, `harness/`, or `.pi/` becomes live again, and integrated validation requires no generated shell, inline-Python fragment, or nested CLI-output parsing.
- Exactly one private builder constructs complete candidate SQLite, SQL, manifest, and projection artifacts from canonical maintained inputs. `HarnessControlMigrator` validates and is the sole publisher; `HarnessControlVerifier` derives the canonical inputs, compares without maintained writes, detects authoritative-source drift, and removes temporary artifacts. No migrator check mode, second construction path, incremental mutation, public builder Action, or duplicated publication logic exists.
- Focused validation tests, complete resource and evidence conformance, deterministic full SQLite reconstruction and projection agreement, Sphinx warnings-as-errors, and dependency-lock nonmutation checks pass.

## Exclusions

- Do not freeze a new public command grammar, import, or wire contract where the accepted parent authority leaves materially different defensible choices; stop for a human decision when required.
- Do not publish maintained control artifacts outside `HarnessControlMigrator`, duplicate the private builder, create incremental SQL mutation or partial projection tracking, introduce another maintained database or persistence framework, expose a public builder Action, or infer authority from a watcher, daemon, event log, filesystem timing, current directory, or ambient discovery. Temporary verifier candidates are nonauthoritative and must be removed after use.
- Do not implement telemetry, observations collection, instrumentation, dashboards, tokens, costs, or effectiveness claims; bounded migration-performance measurements remain diagnostics only.
- Do not rewrite or delete retained `.pi` history or historical evidence scripts that record commands actually used; the `python/src/cli` location requirement applies to maintained live CLIs. Do not add dependencies, modify scientific/package-source modules, publish, release, or perform external, scientific, or other protected execution.

## Historical source

No archived source.
