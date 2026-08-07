# Implement bounded task-state inspection

Status: completed under `.pi/chains/harness-simplification.chain.json`

Task identity: `harness-simplification.execution.task-state-inspection-tool`

Starting revision: `f3c7886430b6d03e1b5595135560acd31a3bc63e` (`origin/dev` at task start).

Authority: the current human instruction authorized one root-agent implementation of `TaskStateInspectionRequest`, `InspectTaskState`, `TaskStateInspectionResult`, proportional software-verification tests, one thin project-local module command, the smallest maintained harness documentation update, chain closeout, commit, and push. It prohibited subagents, reviewers, recursive repository inspection, review-dispatch idempotency implementation, broader discovery, SQLite, scientific work, and protected execution.

## Maintained operation

The public immutable request accepts an explicit absolute repository root, one root-relative chain path, and one exact task identity. The fieldless ActionObject reads that chain and only exact task-record, ownership-manifest, completion-validator, artifact, run-record, and handoff-record paths declared by the selected task or ownership manifest. Every path is checked against the existing lexical path policy and a nonsymlink root-confined filesystem boundary. The action performs no recursive directory search, Git command, subprocess, network access, temporary-log or session inspection, repository mutation, or inference from prose.

The immutable result reports task and active state, declared paths and roles, completion command, inspected and read paths, deterministic validation issues, durable run/handoff declaration status, and explicit limitations. Undeclared runtime state is represented as `not_declared`; a declared missing record is `declared_missing`; a declared readable record is `inspected`.

The thin invocation is:

```text
python/.venv/bin/python -m ksdft2effmass.harness.pi.local.inspect_task_state \
  --root . \
  --chain .pi/chains/harness-simplification.chain.json \
  --task-id harness-simplification.agents.validator-migration-pilot
```

## Validator-pilot inspection

The maintained command returned `PASS`, task status `completed`, `active_task: null`, the exact task and ownership paths, the pytest completion path and command, three sorted writer assignments, and one declared reviewer assignment. The selected chain entry declares no artifact, run-record, or handoff-record paths, so durable run and handoff status are both `not_declared`.

The intended policy remains one final review. The human-observed four duplicate completed reviewer assignments are interactive runtime observations outside declared repository state. The tool does not inspect or infer session history, cannot reconstruct the exact reviewer-launch count, and does not reinterpret duplicate assignments as independent evidence.

## Boundary

Reviewer dispatch remains owned by the inactive `harness-simplification.execution.review-dispatch-idempotency` successor. Live discovery, historical retirement, delegation validation, evidence/SQLite, scientific work, and protected work remain inactive and unauthorized.
