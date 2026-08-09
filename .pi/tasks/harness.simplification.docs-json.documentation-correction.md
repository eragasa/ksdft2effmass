# Correct documentation/control inconsistencies

Status: active; authorized by the human PI on 2026-08-09 after the completed comparison baseline

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
