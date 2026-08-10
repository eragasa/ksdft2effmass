<!-- Generated from SQLite control state; do not edit. -->
# Decompose canonical JSON and domain wire codecs

[Task index](index.md) · [Previous](./harness.simplify-2.validation-retirement.md) · [Next](./harness.telemetry.md)

## Status

`inactive`: corrected inactive R2.5 wire-codec decomposition with unchanged persistence ownership; parent-authorized deterministic transition only, currently not activated, and no automatic successor activation

## Objective

Decompose `python/src/ksdft2effmass/harness/pi/validation.py` into canonical JSON support, explicit domain codecs, and thin wire-kind dispatch without changing database construction, publication, or synchronization ownership.

## Parent and prerequisites

- Parent: `harness.simplify-2`
- Depends on: `harness.simplify-2.resource-decomposition`

## Authority references

- AGENTS.md
- harness/intake/harness.simplify-2.md
- harness/tasks/harness.simplify-2.json

## Authorized scope

- Separate canonical JSON mechanics from explicit checkpoint, Task, resource, human-review, and other currently supported harness-domain codecs.
- Keep domain field mappings and construction in their domain codec; keep dispatch limited to explicit wire-kind routing.
- Avoid magical registration, implicit discovery, and unnecessary public exposure of internal codecs.
- Preserve existing supported public wire contracts, canonical bytes, imports, ActionObject names, and execute signatures unless a separately resolved human decision authorizes a change.
- Keep persistence ownership unchanged: wire codecs may prepare or decode explicit records but do not construct, mutate, publish, or synchronize SQLite and do not duplicate the full `HarnessControlMigrator`.
- Use the existing `HarnessControlMigrator` throughout R2.5; private compiler extraction and full source-aware verifier integration belong only to R2.7.
- Implement R2.5 as a complete vertical replacement of its owned wire-codec subsystem: accepted end-state contract, isolated implementation, complete affected-data migration, controlled parity, one cutover, and removal of the obsolete live path. Do not retain old and new operational codec authorities after cutover except for temporary compatibility required by an accepted public contract.
- Because the active parent authorizes the full round, R2.5 requires no separate human activation cycle once R2.4 is complete and the parent agent explicitly transitions to it with no unresolved checkpoint, human-owned material choice, protected action, or unresolved material review finding. Keep one active child, prohibit background activation, and keep automatic successor activation false.

## Completion criteria

- Canonical JSON, domain mappings, and dispatch have explicit owners; dispatch contains no domain construction or field-mapping mechanism.
- All supported wire kinds retain accepted structural and runtime behavior, canonical serialization, deterministic diagnostics, public imports, and compatibility behavior.
- No wire codec or dispatch path writes SQLite, performs synchronization, or creates a second database-construction path; `HarnessControlMigrator` remains the sole maintained construction and publication Action.
- Focused codec and canonical-vector tests, complete wire-contract tests, documentation validation, and dependency-lock nonmutation checks pass.
- The work package completes without self-activating its successor. A prerequisite-satisfied R2.6 transition is performed explicitly by the parent agent under the parent-authorized deterministic rule, not by an automatic successor mechanism.

## Exclusions

- Do not refactor `operators/serialization.py`, `workflows/cpn/execution.py`, `provenance/serialization.py`, or another production or scientific codec.
- Do not add magical registration, plugin discovery, a generic codec framework, new public wire kinds, or compatibility changes without separate authority.
- Do not introduce incremental SQL mutation, another database writer, partial projection tracking, a watcher, daemon, event log, ambient discovery, or another persistence framework.
- Do not implement R2.6 CLI consolidation or R2.7 validation retirement, activate another work package, add dependencies, or perform protected or release actions.

## Historical source

No archived source.
