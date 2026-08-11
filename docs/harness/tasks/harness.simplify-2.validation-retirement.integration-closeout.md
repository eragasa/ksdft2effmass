<!-- Generated from SQLite control state; do not edit. -->
# Integrate and close R2.7

[Task index](index.md) · [Previous](./harness.simplify-2.validation-retirement.generation-builder.md) · [Next](./harness.simplify-2.validation-retirement.inventory.md)

## Status

`active`: explicitly selected after legacy-route retirement completion; automatic successor activation remains disabled

## Objective

Synchronize current documentation, execute the complete R2.7 integration gates, obtain one independent read-only review, and close R2.7 without successor activation or human-acceptance claims.

## Parent and prerequisites

- Parent: `harness.simplify-2.validation-retirement`
- Depends on: `harness.simplify-2.validation-retirement.legacy-route-retirement`

## Authority references

- AGENTS.md
- harness/reports/validation-retirement-inventory.json
- harness/tasks/harness.simplify-2.validation-retirement.json

## Authorized scope

- Update current architecture, API, operational, and Task documentation without rewriting historical evidence.
- Run the exact focused and repository-wide software, harness, documentation, control, cleanup, dependency-lock, and Git gates required by the current human instruction.
- Launch exactly one durable read-only harness integration reviewer and permit the original writer at most one bounded correction pass for material findings.

## Completion criteria

- All required deterministic and external final gates pass on one exact candidate tree and one independent integration review is complete.
- R2.7 and this child are completed, `harness.simplify-2` is selected as coordinating parent without human acceptance, automatic successor activation remains disabled, and no successor is active.
- The final boundary is committed and pushed with HEAD equal to origin/dev and a clean working tree.

## Exclusions

- Do not launch additional reviewers, perform more than one correction pass, rewrite historical evidence, activate a successor, or claim human acceptance.
- Do not add dependencies or lockfile changes, scientific or numerical work, protected execution, publication, or release work.

## Historical source

No archived source.
