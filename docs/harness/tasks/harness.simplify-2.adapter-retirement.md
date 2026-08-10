<!-- Generated from SQLite control state; do not edit. -->
# Retire and decompose project-local adapters

[Task index](index.md) · [Previous](./harness.simplify-2.md) · [Next](./harness.simplify-2.control-decomposition.md)

## Status

`inactive`: decomposed work package R2.2; separate explicit human activation required and no automatic successor activation

## Objective

Remove obsolete project-local adapters and assign each surviving Task, ownership, resource, or legacy-compatibility translation to its owned contract without introducing a generic adapter framework.

## Parent and prerequisites

- Parent: `harness.simplify-2`
- Depends on: `harness.simplify-2.control-decomposition`

## Authority references

- AGENTS.md
- harness/intake/harness.simplify-2.md
- harness/tasks/harness.simplify-2.json

## Authorized scope

- Audit every live consumer of `python/src/ksdft2effmass/harness/pi/local/adapters.py` before moving or deleting behavior.
- Retire adapters with no live consumer, adapters translating only between generated projections, and compatibility readers whose archived-input requirement is proven absent.
- Split surviving behavior by Task, ownership, resource, and narrowly bounded legacy-Markdown contracts when those owners remain necessary.
- Preserve required historical traceability and supported compatibility behavior, public imports, and execute signatures.

## Completion criteria

- Every retained adapter has an identified live consumer and one explicit owned contract; obsolete adapters and generated-projection translations are removed.
- No generic adapter framework or reverse dependency from generic harness behavior to project-local state is introduced.
- Focused adapter and compatibility tests, the maintained harness software-verification suite, Ruff, mypy, documentation validation, and dependency-lock nonmutation checks pass.
- The work package completes without activating its successor.

## Exclusions

- Do not remove a compatibility reader without evidence that no live or required archived input consumes it.
- Do not rewrite or delete retained `.pi` history, exact human decisions, Tasks, chains, checkpoints, or evidence.
- Do not implement R2.3 through R2.6, activate another work package, add dependencies, modify scientific/package-source modules, or perform protected or release actions.

## Historical source

No archived source.
