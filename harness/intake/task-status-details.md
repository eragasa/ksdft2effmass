# List-valued Task status details

## Human request

While Task catalog configuration implementation was in progress, the human asked:

> i feel status detail should be a list and not just a string, what do you think?

The assistant recommended an ordered list of short, single-purpose current-status
entries, rather than one paragraph combining decisions, progress, blockers and
exclusions. The existing `status` value remains the lifecycle label. Detailed
history belongs in linked intake and evidence records, not an accumulating status
log. The assistant identified the need for coordinated Task-schema, serializer,
validator and existing-record changes.

The human instructed:

> let's add this as a task

## Recording authority and boundary

This instruction authorizes recording `harness.task-status-details` as a separate,
unactivated software Task, with this intake and necessary generated projections.
It does not authorize implementation or select a Task-schema version, legacy-read
policy, empty-list/null policy, or lossy migration of existing prose.

The canonical Task remains under the currently configured `harness/tasks/` root.
Its prospective catalog destination is the configured software root. Include it
when the catalog migration inventory is next refreshed; the earlier 216-Task
planning inventory predates this addition and is not an exhaustive cutover map
for the enlarged catalog.

`harness.task-catalog-configuration` remains selected. This new concern does not
expand that Task's implementation scope, block it through an invented dependency,
or automatically activate a successor. No source, schema, live configuration,
existing status field, scientific setting, dependency or Git closeout change is
included in this recording operation.

## Proposed work after explicit activation

- Define ordered JSON string-list status details and their immutable Python
  representation, retaining `status` as the lifecycle label.
- Specify entry validity, ordering, duplicate handling, empty/null behavior and
  compatibility/versioning before changing the public representation. Resolve
  any material remaining contract choice using the applicable human boundary.
- Integrate the owning Task model, serializers, schema, validation, SQL/control
  persistence and projections, plus affected tests and documentation. The current
  owning surfaces include `python/src/ksdft2effmass/harness/task.py`,
  `_compiler_serialization.py` in the same package, and
  `harness/local/schemas/task-record-v3.schema.json`; record the actual affected
  consumers at implementation time rather than assume this list is exhaustive.
- Migrate maintained current summaries without losing meaning or changing Task
  IDs, lifecycle, relationships or authority. Do not split prose mechanically on
  punctuation or rewrite retained historical/checksummed evidence as if it had
  always used the new representation.
- Verify exact ordered round trips, positive and negative input behavior, legacy
  disposition, migration preservation and source/projection agreement.

This is proposed software work, not an implemented capability, scientific result,
Task acceptance or authorization to execute the Tasks whose summaries it records.
