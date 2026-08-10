---
document_id: ksdft2effmass.harness.002.002.005
task_record: harness/tasks/harness.simplification.docs-json.documentation-correction.json
parent: ksdft2effmass.harness.002.001.000
sphinx: excluded
---

# Documentation/control consistency correction

> **Operational authority:**
> [the version-3 JSON Task record](../../harness/tasks/harness.simplification.docs-json.documentation-correction.json)
> owns Task identity, lifecycle status, hierarchy, prerequisites, supersession, activation policy,
> scope, completion criteria, exclusions, authority references, intake path, and
> documentation path. This page is maintained explanation only. The
> [harness-simplification chain](../../.pi/chains/harness-simplification.chain.json)
> owns ordering and activation.

## Rationale

The correction separated durable control facts from human-facing documentation.
Stale snapshots of active work, prerequisites, successors, completion, or
acceptance become misleading when copied into narrative pages. Likewise, obsolete
names and links, unlabeled historical material, and manual control-reference
restatements obscure the owning records.

A deterministic correction was appropriate when accepted authority allowed only
one compatible result. Human review remained appropriate only for a genuine
conflict that precedence could not resolve and that left materially different
defensible choices. Documentation can locate and explain work, but it cannot
activate a Task or supply executable scope.

## Historical result

The reviewed `MAP-003`, `MAP-004`, and `MAP-005` corrections changed exactly
three maintained harness pages:

- mutable active-Task and next-Task snapshots were replaced by references to the
  owning chain;
- obsolete `record: null` and unbegun-successor claims were removed; and
- completed durable project-agent simplification and retirement from live
  discovery were distinguished from the 24 retained disabled historical records.

No ambiguity remained. The focused checks covered stale phrases, relative links,
Git whitespace, checkpoint validity, and a Sphinx warnings-as-errors build. A
consolidated independent review reported no findings and confirmed preservation
of subject matter, historical attribution, non-activation boundaries, and
scientific and protected-action boundaries.

## Handoff context

The resulting bounded schema-projection candidate was the Task control family:
chain `task_sequence` references and active-Task facts, transitional Markdown
Task identity/status/authority/completion fields, the existing narrow
`TaskReference` DataObject, and `TaskRecordAdapter`. The next Task had to select
exact authoritative JSON fields, fixtures, and one complete generated
reference-page target before implementing a full public Task DataObject or
serializer. This handoff did not itself select contract semantics, implement the
Task model, or activate schema projection.

## Preservation and condensation

Operational fields were extracted into JSON. Remaining narrative was condensed
while preserving the identified rationale, reviewed result, authority boundary,
contributor guidance, and schema-projection handoff. This first real migration
also exposed and corrected the version-2 Task contract: `intake_path` changed from
mandatory `ResourcePath` to `ResourcePath | None`, with JSON `null` representing
that no separate intake artifact exists. That is a Task-contract correction, not
merely a data migration.

Intentionally omitted presentation-only material consists of the old operational
labels, duplicated section framing, list numbering, and wording now represented
by JSON fields. No identified substantive narrative was omitted.

## Contributor guidance

When correcting similar documentation, consult the operational record instead of
copying mutable control state into prose. Preserve useful rationale, historical
context, and subject-matter guidance. Escalate only unresolved human-owned choices;
do not introduce an execution-target resolver merely to synchronize narrative
text.

## Navigation

- **Index:** [Harness documentation](ksdft2effmass.harness.000.000.000.md)
- **Parent:** [First harness simplification round](ksdft2effmass.harness.002.001.000.md)
- **Task-model context:** [Retained HarnessTask model](ksdft2effmass.harness.002.001.011.md)
