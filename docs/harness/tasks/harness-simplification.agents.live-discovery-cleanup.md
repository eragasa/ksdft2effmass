<!-- Generated from SQLite control state; do not edit. -->
# Retire historical phase agents from live discovery

[Task index](index.md) · [Previous](./harness-simplification.agents.executable-tool-placement-contract.md) · [Next](./harness-simplification.agents.project-architecture.md)

## Status

`completed`: completed under `.pi/chains/harness-simplification.chain.json`

## Objective

Task identity: `harness-simplification.agents.live-discovery-cleanup`

## Parent and prerequisites

- Depends on: `harness-simplification.execution.task-state-inspection-tool`

## Authority references

- .pi/agents/*.md
- .pi/chains/harness-simplification.chain.json
- .pi/settings.json
- harness/archive/task-control-v1/tasks/harness-simplification.agents.live-discovery-cleanup.md
- origin/dev

## Authorized scope

- Authority: the current human instruction authorized one bounded root-agent discovery cleanup, direct documentation and chain reconciliation, validation, commit, and push.

## Completion criteria

- The conceptual `harness-simplification.agents.live-discovery` and `harness-simplification.agents.historical-retirement` stages are retained and marked completed by this cleanup. Historical retirement means removal from selectable discovery, not repository deletion. Review-dispatch idempotency is `deferred_inactive`: PI already supplies run IDs, status, resume, and runtime artifacts; the duplicate cause has not been reconstructed; and repository SQLite would not intercept native `subagent(...)` dispatch. This deferral does not block unrelated cleanup.
- `active_task` remains `null` and automatic successor activation remains disabled. `harness-simplification.agents.delegation-validation` is the next inactive, unauthorized harness task. Evidence/SQLite, P3, and scientific or protected execution remain inactive and unauthorized.

## Exclusions

- It prohibited subagents, reviewers, historical-agent edits or deletion, new ownership/evidence/checkpoint artifacts, Python or scientific tests, and successor activation.

## Historical source

`harness/archive/task-control-v1/tasks/harness-simplification.agents.live-discovery-cleanup.md` (`sha256:70d2e307cbd44f2ff76ba492550c15aa066e7ae60a63691692aae94d1d41335a`)
