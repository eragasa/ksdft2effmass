<!-- Generated from SQLite control state; do not edit. -->
# Extract the private control-generation builder

[Task index](index.md) · [Previous](./harness.simplify-2.validation-retirement.md) · [Next](./harness.simplify-2.validation-retirement.integration-closeout.md)

## Status

`active`: explicitly selected after inventory completion; automatic successor activation remains disabled

## Objective

Extract complete candidate control generation into one private local/control builder while preserving the migrator as sole publisher and all accepted public migration behavior.

## Parent and prerequisites

- Parent: `harness.simplify-2.validation-retirement`
- Depends on: `harness.simplify-2.validation-retirement.inventory`

## Authority references

- AGENTS.md
- harness/reports/validation-retirement-inventory.json
- harness/tasks/harness.simplify-2.validation-retirement.json

## Authorized scope

- Implement `_HarnessControlGenerationBuilder` and `_HarnessControlGeneration` under `python/src/ksdft2effmass/harness/pi/local/control/generation.py` using domain owners and local/dbcontrol persistence mechanics.
- Make `HarnessControlMigrator` perform candidate build, candidate validation, and sole publication through its retained `_publish_generation()` owner.
- Preserve noncanonical explicit requests, public identities and execute signature, schema, semantic content, SQL, and projection bytes.

## Completion criteria

- Exactly one private builder constructs the complete candidate without publishing maintained files.
- Semantic database, canonical SQL, and projection equivalence, noncanonical compatibility, validation-before-publication, and failure-safe publication tests pass.
- Control synchronization and affected deterministic validation pass.

## Exclusions

- Do not expose a public generation Action, create a second publisher, reverse the control-to-dbcontrol dependency, or add persistence machinery.
- Do not change dependencies, lockfiles, public wire kinds, scientific code, or historical records.

## Historical source

No archived source.
