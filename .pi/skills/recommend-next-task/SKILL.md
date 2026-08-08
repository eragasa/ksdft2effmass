---
name: recommend-next-task
description: Recommend exactly one currently eligible next task when the human asks what should follow or how the project should continue. Do not use for ordinary task implementation, checkpoint resolution, material architecture review, or status inspection alone.
---

# Recommend next task

## Purpose and trigger

Use this read-only decision procedure when the human asks what is next, what to
work on now, which task should follow, what the smallest useful next step is, or
which currently eligible task should be selected.

The skill identifies the project frontier, recommends exactly one proposed task,
and stops for human selection. It never creates, edits, activates, assigns,
accepts, implements, or launches a task, and it never claims human authorization.

## Authority and state gate

Apply authority in this order:

1. current human instruction;
2. applicable repository policy;
3. unresolved human checkpoints;
4. active chain and task state;
5. durable human decisions and accepted task records;
6. implemented source, tests, specifications, and maintained documentation; and
7. derived or historical evidence only as supporting context.

Do not infer current authority from an agent summary, filename, timestamp,
historical evidence record, chat memory, or apparent implementation state.

Inspect only the authoritative control-plane indexes needed to determine whether
work is active, blocked, awaiting a human decision, or complete. Before
recommending new work, determine whether a task is active, a checkpoint awaits
human disposition, an accepted correction or closeout remains incomplete, a
prerequisite remains blocked, or durable state is insufficient or conflicting.

| State | Required response |
|---|---|
| Active authorized work exists | Report that work instead of recommending a new task. |
| Human checkpoint is pending | Route to `resolve-human-checkpoint` and stop. |
| Required correction or closeout remains incomplete | Recommend completing that bounded work. |
| A prerequisite is blocked | Exclude dependent candidates and report the blocker. |
| Durable state conflicts | Report the exact conflict and stop. |
| State is sufficient and no work is active | Evaluate next-task candidates. |

When the exact chain path and task ID are known, use the maintained
`InspectTaskState` ActionObject through the stable command documented by
[inspect-task-state](../inspect-task-state/SKILL.md). Do not reconstruct the
same state with broad searches, inline scripts, session memory, or historical
evidence. If the identity is unknown, inspect only the small authoritative chain
or task indexes needed to identify it; do not recursively search task or evidence
files. This skill does not replace or duplicate task-state inspection.

## Candidate-selection rule

Consider only serious unblocked candidates. A recommended task must:

- follow from completed prerequisites;
- produce a concrete artifact or capability from explicit inputs;
- expose or resolve an important software, numerical, or scientific boundary;
- have verification or validation appropriate to its claim;
- advance the central research or infrastructure objective;
- be small enough for human review; and
- avoid speculative framework expansion.

Prefer a vertical slice with complete behavior and evidence over a broad
framework. Classify serious candidates compactly as `core scientific capability`,
`publishable scientific claim`, `validation or reproducibility infrastructure`,
`general engineering infrastructure`, `premature branch`, or `deferred work`.
Do not require a fixed analysis table for weak candidates.

## Recommendation shape

Return:

1. verified current state;
2. exactly one recommended task;
3. why it is next;
4. expected inputs;
5. expected output;
6. applicable verification or validation;
7. any material human decision;
8. one or two serious alternatives and why they are not next; and
9. an explicit stop for human selection.

Do not design the complete implementation or control plane.

If durable state is insufficient, report what was verified, the exact missing or
conflicting record, and one focused human question when human input can resolve
it. Do not create state to fill the gap.

## Routing

- Exact bounded task-state inspection belongs to `InspectTaskState` and the
  [inspect-task-state](../inspect-task-state/SKILL.md) usage skill.
- Human checkpoint interpretation belongs to
  [resolve-human-checkpoint](../../../.agents/skills/resolve-human-checkpoint/SKILL.md).
- Material architecture alternatives belong to
  [develop-architecture-decision](../develop-architecture-decision/SKILL.md).
- Object architecture belongs to
  [design-data-action-objects](../design-data-action-objects/SKILL.md).
- Test-evidence design belongs to
  [develop-python-test-evidence](../develop-python-test-evidence/SKILL.md).
- Implementation belongs to the task-selected durable writer.

This skill proposes which task should be selected; it performs none of those
other capabilities.

## Stop conditions

Stop after one recommendation and the human-selection notice. Also stop on a
pending checkpoint, active authorized task, unresolved durable conflict, or
insufficient durable basis. Do not modify roadmaps, task or checkpoint records,
source, tests, documentation, specifications, assignments, acceptance state, or
successor state.
