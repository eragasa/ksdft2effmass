<!-- Generated from SQLite control state; do not edit. -->
# Consolidate validation and retire replay machinery

[Task index](index.md) · [Previous](./harness.simplify-2.resource-decomposition.md) · [Next](./harness.simplify-2.wire-validation-decomposition.md)

## Status

`inactive`: decomposed work package R2.6; separate explicit human activation required and no automatic successor activation

## Objective

Replace replay, H3-era gates, nested CLI validation, and duplicated live control routes with one composable maintained validation Action and one renderer, then verify the integrated round-two result.

## Parent and prerequisites

- Parent: `harness.simplify-2`
- Depends on: `harness.simplify-2.wire-validation-decomposition`

## Authority references

- AGENTS.md
- harness/intake/harness.simplify-2.md
- harness/tasks/harness.simplify-2.json

## Authorized scope

- Prove live-consumer obsolescence before retiring `replay_current_validators.py`, H3-era resource gates, nested CLI validation, or duplicated live control paths.
- Provide one composable maintained validation Action returning structured named checks, statuses, findings, and durations, with one project-local renderer and no CLI-output parsing.
- Consolidate routine inspect, validate, project, Task, and evidence operations behind a small maintained Action-backed command surface; normalize maintained examples and entry points on `python/.venv/bin/python`.
- Perform cross-package integration validation, synchronize directly affected documentation, and obtain one consolidated independent read-only compatibility review with at most one correction pass.
- Conclude the parent program pending explicit human acceptance with `active_task` restored to null and no successor activated.

## Completion criteria

- One maintained validation Action produces structured named checks, statuses, findings, and durations; one renderer exposes the result and no validator invokes another CLI and parses its output.
- Retired replay, H3-era, nested, and duplicated routes have no remaining live consumers; required historical records and compatibility remain preserved.
- Routine maintained command examples use `python/.venv/bin/python` and do not require generated shell or inline-Python fragments.
- Focused validation tests, the complete maintained harness software-verification suite, Ruff, mypy, resource and evidence conformance, deterministic SQLite reconstruction, projection agreement, Sphinx warnings-as-errors, and dependency-lock nonmutation checks pass.
- One consolidated independent read-only compatibility review has no unresolved material findings after at most one consolidated correction pass.
- The parent is complete pending explicit human acceptance, `active_task` is null, and no telemetry, production-source refactor, scientific work, protected execution, or successor is activated.

## Exclusions

- Do not freeze a new public command grammar, import, or wire contract where the accepted parent authority leaves materially different defensible choices; stop for a human decision when required.
- Do not implement telemetry, observations collection, instrumentation, benchmarks, dashboards, tokens, costs, or effectiveness claims.
- Do not rewrite or delete retained `.pi` history, add dependencies, modify scientific/package-source modules, publish, release, or perform external, scientific, or other protected execution.

## Historical source

No archived source.
