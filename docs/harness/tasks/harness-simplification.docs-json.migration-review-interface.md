<!-- Generated from SQLite control state; do not edit. -->
# Serial HarnessTask migration-review operational interface

[Task index](index.md) · [Previous](./harness-simplification.checkpoints.resolve-checkpoint-decision.md) · [Next](./harness-simplification.evidence.audit-action-conformance.md)

## Status

`completed`: completed under `.pi/chains/harness-simplification.chain.json`

## Objective

Task identity: `harness-simplification.docs-json.migration-review-interface`

## Parent and prerequisites

None.

## Authority references

- .pi/chains/harness-simplification.chain.json
- .pi/skills/mediate-harness-task-migration/SKILL.md
- .pi/task-ownership/README.md
- harness/archive/task-control-v1/tasks/harness-simplification.docs-json.migration-review-interface.md
- harness/local/skills/mediate-harness-task-migration/SKILL.md
- origin/dev

## Authorized scope

- The canonical skill is `harness/local/skills/mediate-harness-task-migration/SKILL.md`; the live synchronized route is `.pi/skills/mediate-harness-task-migration/SKILL.md`. The stable commands are:
- ```text
python/.venv/bin/python -m ksdft2effmass.harness.pi.local.prepare_harness_task_migration_review
python/.venv/bin/python -m ksdft2effmass.harness.pi.local.record_harness_task_migration_disposition
```
- Both require explicit roots, paths, and identities. Preparation writes one complete deterministic review document atomically. Disposition reconstructs the same packet, invokes `HumanReviewDecisionRecorder` and `HarnessTaskMigrationFileDispositionRecorder`, binds the exact review document, and writes one canonical project-local disposition record atomically. No packet envelope was added because exact reconstruction from the original explicit inputs is lossless. Existing public Python interfaces remain unchanged.
- Focused maintained evidence uses only synthetic files and establishes software verification, not semantic migration correctness or human acceptance. The commands perform no Git discovery, source inference, migration application, activation, checkpoint mutation, or next-file preparation.

## Completion criteria

- Stage 2A remains pending explicit human acceptance at `.pi/checkpoints/harness.simplification.docs-json.task-implementation-hardening.human-review-boundary-acceptance.json`. Stage 2B remains inactive and blocked. The chain retains `active_task: null` and `automatic_successor_activation: false`. All six authoritative Markdown Tasks remain byte-identical to `.pi/evidence/docs-json/task-model-contract/source-inventory.json`.

## Exclusions

- The canonical skill is `harness/local/skills/mediate-harness-task-migration/SKILL.md`; the live synchronized route is `.pi/skills/mediate-harness-task-migration/SKILL.md`. The stable commands are:
- ```text
python/.venv/bin/python -m ksdft2effmass.harness.pi.local.prepare_harness_task_migration_review
python/.venv/bin/python -m ksdft2effmass.harness.pi.local.record_harness_task_migration_disposition
```
- Both require explicit roots, paths, and identities. Preparation writes one complete deterministic review document atomically. Disposition reconstructs the same packet, invokes `HumanReviewDecisionRecorder` and `HarnessTaskMigrationFileDispositionRecorder`, binds the exact review document, and writes one canonical project-local disposition record atomically. No packet envelope was added because exact reconstruction from the original explicit inputs is lossless. Existing public Python interfaces remain unchanged.
- Focused maintained evidence uses only synthetic files and establishes software verification, not semantic migration correctness or human acceptance. The commands perform no Git discovery, source inference, migration application, activation, checkpoint mutation, or next-file preparation.

## Historical source

`harness/archive/task-control-v1/tasks/harness-simplification.docs-json.migration-review-interface.md` (`sha256:6f202ac4850706beb6fb1e7c86834b9b2b2a61221c8ca87ff9522b9b4e9e0d30`)
