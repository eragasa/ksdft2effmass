<!-- Generated from SQLite control state; do not edit. -->
# Implement bounded task-state inspection

[Task index](index.md) · [Previous](./harness-simplification.evidence.audit-action-conformance.md) · [Next](./harness-simplification.execution.validator-pilot-stabilization.md)

## Status

`completed`: completed under `.pi/chains/harness-simplification.chain.json`

## Objective

Task identity: `harness-simplification.execution.task-state-inspection-tool`

## Parent and prerequisites

- Depends on: `harness-simplification.execution.validator-pilot-stabilization`

## Authority references

- .pi/chains/harness-simplification.chain.json
- harness/archive/task-control-v1/tasks/harness-simplification.execution.task-state-inspection-tool.md
- origin/dev

## Authorized scope

- The public immutable request accepts an explicit absolute repository root, one root-relative chain path, and one exact task identity. The fieldless ActionObject reads that chain and only exact task-record, ownership-manifest, completion-validator, artifact, run-record, and handoff-record paths declared by the selected task or ownership manifest. Every path is checked against the existing lexical path policy and a nonsymlink root-confined filesystem boundary. The action performs no recursive directory search, Git command, subprocess, network access, temporary-log or session inspection, repository mutation, or inference from prose.
- The immutable result reports task and active state, declared paths and roles, completion command, inspected and read paths, deterministic validation issues, durable run/handoff declaration status, and explicit limitations. Undeclared runtime state is represented as `not_declared`; a declared missing record is `declared_missing`; a declared readable record is `inspected`.
- The thin invocation is:
- ```text
python/.venv/bin/python -m ksdft2effmass.harness.pi.local.inspect_task_state \
  --root . \
  --chain .pi/chains/harness-simplification.chain.json \
  --task-id harness-simplification.agents.validator-migration-pilot
```

## Completion criteria

- Reviewer dispatch remains owned by the inactive `harness-simplification.execution.review-dispatch-idempotency` successor. Live discovery, historical retirement, delegation validation, evidence/SQLite, scientific work, and protected work remain inactive and unauthorized.

## Exclusions

- Reviewer dispatch remains owned by the inactive `harness-simplification.execution.review-dispatch-idempotency` successor. Live discovery, historical retirement, delegation validation, evidence/SQLite, scientific work, and protected work remain inactive and unauthorized.

## Historical source

`harness/archive/task-control-v1/tasks/harness-simplification.execution.task-state-inspection-tool.md` (`sha256:b28eb94cbb97e8333b8a54cdf2f6fadc4e48db8ec1fa02c8aed4779471cb8b8f`)
