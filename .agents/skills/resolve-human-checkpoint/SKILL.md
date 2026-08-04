---
name: resolve-human-checkpoint
description: "Resolve a persisted repository human checkpoint only when an unresolved .pi/checkpoints record exists and the current human message unambiguously answers it; record the decision, resume only authorized work, and validate without requiring special wording."
---

# Resolve Human Checkpoint

Use this shared repository-local skill whenever both conditions hold:

1. at least one unresolved checkpoint exists under `.pi/checkpoints/`; and
2. the current human message appears to answer a checkpoint question.

This skill is an operational control-plane skill. It does not decide scientific
meaning by itself; it records and applies a human decision that has already been
provided, or asks one concise clarification when the response is ambiguous.

## Required inputs

- the current human message;
- unresolved checkpoint JSON files under `.pi/checkpoints/`;
- the checkpoint schema at `.pi/checkpoints/checkpoint.schema.json`;
- related task and episode records referenced by the checkpoint;
- the pending checkpoint commit identity and active task branch; and
- the expected remote containing the durable checkpoint boundary.

A genuine pending checkpoint should already be committed and pushed with its
validated pre-checkpoint state. If it is not, report the missing durable boundary
and remain blocked rather than treating local-only state as a shared rollback
anchor.

Do not require the human to say `record this decision`, `resume the task`,
`update the task file`, or `continue the chain`.

## Resolution procedure

1. Validate checkpoint files against `.pi/checkpoints/checkpoint.schema.json`.
2. Locate unresolved checkpoints where `status` is `pending` or `blocked`.
3. If no unresolved checkpoint exists, stop and let ordinary task/session policy
   continue.
4. Match the current human message against each checkpoint's `question`,
   `options`, `recommendation`, and `blocked_scope`.
5. If exactly one checkpoint has exactly one unambiguous interpretation:
   - preserve the decision-bearing human text in `human_response`;
   - normalize the decision in `normalized_decision`;
   - set `status` to `resolved`;
   - set `resolved_at` to the current timestamp;
   - set `authorized_scope` to the work now authorized by the decision;
   - update `record_paths` with the task, episode, and evidence files changed;
   - update the linked task and episode records;
   - set `resumption_status` to the current resumption state;
   - rerun required resolution validation;
   - commit the coherent resolution as a separate task/checkpoint decision
     boundary and push it to the active task branch;
   - resume the blocked task automatically only after that push succeeds; and
   - report the outcome and remaining unresolved decisions.
   If commit or push fails, preserve the written resolution records, report the
   partial failure and commit/push status, and do not resume authorized work.
6. If a bare `yes` or equivalent is the current response, resolve only when
   exactly one unresolved (`pending` or `blocked`) checkpoint exists and exactly
   one proposed approval is awaiting confirmation.
7. If multiple checkpoints or multiple interpretations remain plausible, ask one
   concise clarifying question and do not mutate checkpoint records.

## Decision classes

Use the repository decision-class policy in `AGENTS.md` and
`docs/development/agent-control-plane.rst`.

- `deterministic_agent_correction`: no human checkpoint is needed. Correct,
  record as an agent-resolved corrective finding, revalidate, and continue.
- `standing_delegated_decision`: cite the durable human policy that already
  resolves the choice, act, record, revalidate, and continue.
- `genuine_human_decision`: create or keep a checkpoint only when materially
  different defensible options remain and the choice affects protected human
  authority such as scientific meaning, public contracts, scope, privacy,
  external transmission, destructive action, resource-intensive computation, or
  conflicting authoritative instructions.

## Output

Report:

- checkpoint id and task id;
- original question;
- preserved human response;
- normalized decision;
- authorized scope;
- task/episode/checkpoint files updated;
- validation rerun;
- pending-boundary and resolution commit identities;
- branch, remote, and push status;
- resumed or still-blocked status;
- remaining genuine human decisions, if any.

## CPN invocation, replay, and partial-failure boundary

This skill records an already supplied human decision; it does not create the
decision or act as a CPN guard. The external agent/harness invokes it outside
guard evaluation from an immutable request containing the checkpoint identity
and expected current status/content hash, task/episode identities, preserved
human response, expected normalized option, parent-workflow and attempt
identities, permitted control-plane paths, and validation/stop policy.

Before mutation, compare the current checkpoint identity and status with the
request. If it is already resolved with the same normalized decision, report an
idempotent no-op and do not resume work twice. If it is resolved differently,
has changed identity, or the human response is ambiguous, return a structured
conflict/ambiguity failure and stop. Record checkpoint, task, and episode updates
before any separately authorized resumption; report every path successfully
written if a later write, validation, commit, or push fails. The validated
resolution commit must be pushed before resumption. Resumption is a distinct
external operation and must not occur when the normalized decision does not
authorize it or when the durable push failed.

Retries require an immutable parent authorization identity or a request's
pre-authorized retry policy, use new attempt identities, and retain earlier
failure/results. The result records skill identity/content hash; request, task,
parent-workflow, and attempt identities; input identities; changed paths; normalized
decision, validation commands/results, resumption status, warnings, and any
partial-failure classification. Only the preserved human response supplies human
acceptance authority; skill execution, validation, commit, and push do not.

## Incremental human-acceptance boundary

When the human explicitly accepts a coherent incremental change outside a formal
checkpoint, apply the same durability rule after validation: commit and push that
accepted increment before continuing with unaccepted work. Do not invoke this
skill merely for routine conversation, but preserve the accepted boundary under
the standing policy in `AGENTS.md` and
`docs/development/agent-control-plane.rst`. Do not amend or rewrite a pushed
decision-boundary commit; use revert or a new branch for restoration unless the
human explicitly authorizes destructive history rewriting.
