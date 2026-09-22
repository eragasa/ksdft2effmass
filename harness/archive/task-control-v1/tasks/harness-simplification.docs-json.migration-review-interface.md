# Serial HarnessTask migration-review operational interface

Status: completed under `.pi/chains/harness-simplification.chain.json`

Task identity: `harness-simplification.docs-json.migration-review-interface`

Starting revision: `5d0d3dd7b1433ca1fd1ddf9f9da3db49ad5c4f44` (`origin/dev` after explicit fetch).

Authority: the current human instruction authorized one bounded pre-Stage-2B tooling slice connecting the accepted deterministic HarnessTask ActionObjects to a project-local mediation skill and maintained preparation/disposition commands. It explicitly prohibited Stage-2A acceptance, Stage-2B activation, any real Task packet or migration, successor activation, dependencies, persistence frameworks, and unrelated work.

## Ownership

One root-session writer directly owned the bounded skill/resource, project-local command, focused synthetic test, routing, documentation, task, and chain paths changed by this slice. No concurrent writer was used, so a task-ownership manifest was not required by `.pi/task-ownership/README.md`. At most one durable harness integration reviewer is read-only over the resulting diff. The reviewer owns findings only and cannot mutate, accept Stage 2A, activate Stage 2B, or provide human acceptance.

## Delivered boundary

The canonical skill is `harness/local/skills/mediate-harness-task-migration/SKILL.md`; the live synchronized route is `.pi/skills/mediate-harness-task-migration/SKILL.md`. The stable commands are:

```text
python/.venv/bin/python -m ksdft2effmass.harness.pi.local.prepare_harness_task_migration_review
python/.venv/bin/python -m ksdft2effmass.harness.pi.local.record_harness_task_migration_disposition
```

Both require explicit roots, paths, and identities. Preparation writes one complete deterministic review document atomically. Disposition reconstructs the same packet, invokes `HumanReviewDecisionRecorder` and `HarnessTaskMigrationFileDispositionRecorder`, binds the exact review document, and writes one canonical project-local disposition record atomically. No packet envelope was added because exact reconstruction from the original explicit inputs is lossless. Existing public Python interfaces remain unchanged.

Focused maintained evidence uses only synthetic files and establishes software verification, not semantic migration correctness or human acceptance. The commands perform no Git discovery, source inference, migration application, activation, checkpoint mutation, or next-file preparation.

## Review and correction

The single bounded read-only integration review reported two high findings and one medium limitation. The correction pass bound the explicit output review path into the packet identity and added focused path-substitution evidence. It also changed output handling from silent replacement to atomic fail-if-present creation for both review and disposition records, with focused repeated-write evidence. The medium parent-component symlink TOCTOU limitation is retained explicitly under the trusted-local threat model; no claim of adversarial filesystem race hardening is made.

A final bounded Stage-2A operational recovery correction makes preparation idempotent. An absent review document is atomically created without replacement. An existing confined byte-identical regular file is accepted without mutation and emits the same stable `result: available` receipt, allowing a later session to recover the exact packet binding. Differing, symlinked, nonregular, stale, or drifting outputs fail closed. Disposition output remains immutable and nonreplaceable. The existing observation-construction duplication is deferred maintainability debt and continues to fail closed through packet-preparer equality.

## Administrative state

Stage 2A remains pending explicit human acceptance at `.pi/checkpoints/harness.simplification.docs-json.task-implementation-hardening.human-review-boundary-acceptance.json`. Stage 2B remains inactive and blocked. The chain retains `active_task: null` and `automatic_successor_activation: false`. All six authoritative Markdown Tasks remain byte-identical to `.pi/evidence/docs-json/task-model-contract/source-inventory.json`.
