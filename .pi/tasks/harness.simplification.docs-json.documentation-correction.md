# Correct documentation/control inconsistencies

Status: completed; three deterministic corrections independently reviewed on 2026-08-09

Task identity: `harness.simplification.docs-json.documentation-correction`

Parent task: `harness.simplification.docs-json`

## Objective

Consume `harness.simplification.docs-json.authority-catalog` and correct stale, duplicated, badly named, or misleading documentation when accepted authority determines one compatible correction. Preserve human intake and documentation-owned subject matter.

## Correction rule

Apply deterministic corrections directly, including:

- stale status, activation, prerequisite, successor, completion, or acceptance prose whose operational owner is a chain or Task record;
- obsolete names and links;
- manual restatements that will be replaced by generated control-reference pages;
- historical material that is not clearly labeled historical; and
- naming that violates an accepted convention.

Do not create a human checkpoint for these cases. Ask the human only when current applicable claims conflict, precedence does not resolve them, and materially different defensible corrections remain.

Documentation may locate or explain work, but it cannot activate a Task or supply executable scope. This rule already exists in repository policy; do not invent a new execution-target resolver unless an actual executable path violates it and a separate task authorizes that behavior.

## Method and completion

1. Apply the deterministic corrections from the reviewed mappings.
2. Resolve only the remaining ambiguity queue.
3. Validate links, names, historical/current labeling, and the absence of documentation-only activation paths.
4. Hand the remaining operational record families to `harness.simplification.docs-json.schema-projection`.

Completion requires corrected documentation, resolved links, preserved subject-matter contracts and human intake, an explicit unresolved list if any, and a bounded schema-projection handoff.

This Task does not change scientific meaning, activate work, resolve checkpoints, create runtime routing, or perform repository-wide rewriting beyond authorized paths.

## Result and schema-projection handoff

The reviewed `MAP-003`, `MAP-004`, and `MAP-005` corrections were applied to exactly three maintained harness pages. Mutable active-task and next-task snapshots now defer to the owning chain; obsolete `record: null` and unbegun successor claims were removed; and completed durable project-agent simplification and retirement from live discovery are distinguished from the 24 retained disabled historical records. No ambiguity remains.

Direct stale-phrase checks, relative-link checks, `git diff --check`, checkpoint validation, and a Sphinx warnings-as-errors build pass. Consolidated independent review returned no findings and confirmed that subject matter, historical attribution, non-activation boundaries, and protected/scientific claim boundaries are preserved.

The bounded pilot candidate for `harness.simplification.docs-json.schema-projection` is the Task control family: chain `task_sequence` references and active-task facts, transitional Markdown Task identity/status/authority/completion fields, the existing narrow `TaskReference` DataObject, and `TaskRecordAdapter`. The next Task must select exact authoritative JSON fields, fixtures, and one complete generated reference-page target before implementing a full public Task DataObject or serializer. This handoff does not select those contract semantics, implement a Task module, or activate schema projection.
