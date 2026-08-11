<!-- Generated from SQLite control state; do not edit. -->
# Compose deterministic repository validation

[Task index](index.md) · [Previous](./harness.simplify-2.validation-retirement.legacy-route-retirement.md) · [Next](./harness.simplify-2.validation-retirement.source-aware-verification.md)

## Status

`active`: explicitly selected after source-aware verification completion; automatic successor activation remains disabled

## Objective

Compose existing project-local domain validation owners into one deterministic structured repository-validation result and one thin maintained CLI without duplicating domain rules or executing development tools.

## Parent and prerequisites

- Parent: `harness.simplify-2.validation-retirement`
- Depends on: `harness.simplify-2.validation-retirement.source-aware-verification`

## Authority references

- AGENTS.md
- harness/reports/validation-retirement-inventory.json
- harness/tasks/harness.simplify-2.validation-retirement.json

## Authorized scope

- Reuse sufficient existing validation records and add at most the project-local Harness validation request, check, result, and ActionObject surface under local/validation.py.
- Compose executable domain owners directly with stable check and finding ordering, deterministic PASS/WARN/FAIL aggregation, and explicit structural claim boundaries.
- Add `python/src/cli/validate_harness.py` and its thin reusable command owner with exact exit statuses zero through three.

## Completion criteria

- One project-local Action returns stable named checks, statuses, and structured findings without durations, nested CLI execution, CLI-output parsing, or development-tool execution.
- The CLI and API agree, expected findings exit one, invalid construction exits two, and unexpected boundary failures exit three.
- Control synchronization and affected deterministic validation pass.

## Exclusions

- Do not duplicate domain rules, turn programming exceptions into findings, invent production validators for test-only assertions, or claim pytest, lint, type, documentation-build, numerical, scientific, UQ, protected, or human acceptance.
- Do not add generic public APIs, public wire kinds, dependencies, telemetry, or scientific work.

## Historical source

No archived source.
