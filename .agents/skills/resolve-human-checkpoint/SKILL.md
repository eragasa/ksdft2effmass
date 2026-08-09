---
name: resolve-human-checkpoint
description: Interpret a current human answer only when it appears to answer a durably represented unresolved checkpoint; preserve the response verbatim, normalize one defensible decision, or ask for clarification without mutating state.
---

# Resolve human checkpoint

## Trigger
Use this skill only when both are true:

1. at least one unresolved checkpoint is durably represented; and
2. the current human message appears to answer its question or select an option.

Do not use it for ordinary conversation, general approval, routine software
corrections, next-task recommendations, architecture analysis, task activation
without a checkpoint, or acceptance unrelated to a durable unresolved checkpoint.
If no unresolved checkpoint exists, return control to ordinary task policy.

## Interpretation inputs
Require:

- the current human message;
- the unresolved checkpoint record or records;
- each checkpoint ID, question, option labels, and option meanings;
- its recommendation, when present;
- its blocked scope or decision boundary; and
- its related task identity, when declared.

Do not require special wording such as `record this decision`, `resume the task`,
`update the checkpoint`, or `continue the chain`.

Checkpoint parsing and lifecycle validation belong to the maintained
[`CheckpointRecord` and `CheckpointSetValidator`](../../../python/src/ksdft2effmass/harness/pi/checkpoints.py)
contract, not this skill.

## Matching rules
Return `unambiguous` only when the current response supports exactly one
checkpoint and exactly one checkpoint-defined normalized decision. Accept:

- an exact option label;
- an option letter clearly associated with one checkpoint;
- explicit prose selecting one option; or
- explicit rejection or deferral when the checkpoint provides that disposition.

Do not infer a decision from tone, prior preference, a recommendation alone, or
an unrelated statement.

A short affirmative such as `yes`, `accept`, or `proceed` is unambiguous only
when exactly one unresolved checkpoint and one approval proposition are pending,
the recommendation clearly identifies the approval option, and no competing
interpretation is plausible. Otherwise return `ambiguous`.

## Ambiguity behavior
If multiple checkpoints or normalized decisions are plausible:

1. identify the ambiguity;
2. ask one concise clarification question;
3. present only the relevant checkpoint options; and
4. stop without modifying state or activating or resuming work.

Return `no_matching_checkpoint` when no unresolved checkpoint is answered. Return
`conflict` with the exact durable-state conflict when the records cannot support
one valid interpretation.

## Preserved response and normalized decision
Preserve the human's decision-bearing text verbatim as `human_response`. Keep it
distinct from the checkpoint-defined `normalized_decision` and the
`authorized_scope` explicitly resulting from that option. Never rewrite cleaner
prose and represent it as verbatim, invent a decision, or broaden scope.

Return only the checkpoint ID, declared task ID, preserved human response,
normalized decision, resulting authorized scope, interpretation status
(`unambiguous`, `ambiguous`, `no_matching_checkpoint`, or `conflict`), one
clarification question when ambiguous, and any exact durable-state conflict.

The human response supplies decision authority. A recommendation, validator
result, or reviewer agreement does not. The skill must not decide scientific
meaning for the human or resolve a different checkpoint.

## Deterministic-action boundary
This skill interprets intent; it does not transform checkpoint records.
Deterministic generic record transformation belongs to
`CheckpointDecisionResolver`. Checkpoint validation remains with the maintained
validator, while project-local writing remains outside this skill.

Current task-state inspection belongs to `TaskStateInspector` via
[inspect-task-state](../../../.pi/skills/inspect-task-state/SKILL.md). Next-task
selection belongs to
[recommend-next-task](../../../.pi/skills/recommend-next-task/SKILL.md), and
material architecture alternatives belong to
[develop-architecture-decision](../../../.pi/skills/develop-architecture-decision/SKILL.md).
Git persistence and task resumption belong to a separately authorized root
operational workflow.

## Stop conditions
Stop after the concise interpretation result or one clarification question. Do
not mutate checkpoints or tasks, validate a transformed record, create commits,
push, activate successors, resume work, or perform external effects.
