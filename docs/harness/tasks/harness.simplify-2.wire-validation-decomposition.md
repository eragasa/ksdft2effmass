<!-- Generated from SQLite control state; do not edit. -->
# Decompose canonical JSON and domain wire codecs

[Task index](index.md) · [Previous](./harness.simplify-2.validation-retirement.md) · [Next](./harness.telemetry.md)

## Status

`inactive`: decomposed work package R2.5; separate explicit human activation required and no automatic successor activation

## Objective

Decompose `python/src/ksdft2effmass/harness/pi/validation.py` into canonical JSON support, explicit domain codecs, and a thin dispatch layer that routes wire kinds without owning domain mappings.

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

## Completion criteria

- Canonical JSON, domain mappings, and dispatch have explicit owners; dispatch contains no domain construction or field-mapping mechanism.
- All supported wire kinds retain accepted structural and runtime behavior, canonical serialization, deterministic diagnostics, public imports, and compatibility behavior.
- Focused codec and canonical-vector tests, complete wire-contract tests, the maintained harness software-verification suite, Ruff, mypy, documentation validation, and dependency-lock nonmutation checks pass.
- The work package completes without activating its successor.

## Exclusions

- Do not refactor `operators/serialization.py`, `workflows/cpn/execution.py`, `provenance/serialization.py`, or another production or scientific codec.
- Do not add magical registration, plugin discovery, a generic codec framework, new public wire kinds, or compatibility changes without separate authority.
- Do not implement R2.6, activate another work package, add dependencies, or perform protected or release actions.

## Historical source

No archived source.
