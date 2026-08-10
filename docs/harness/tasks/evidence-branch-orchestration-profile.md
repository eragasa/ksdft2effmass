<!-- Generated from SQLite control state; do not edit. -->
# Optional evidence-branch orchestration profile

[Task index](index.md) · [Previous](./deferred-harness-current-phase-history.md) · [Next](./graphify-integration.md)

## Status

`legacy_recorded`

## Objective

- Decision ID: `EBOV1-AUTH-2026-08-03`
- Profile: `evidence-branches-v1`
- Authority: explicit human authorization in the 2026-08-03 conversation that
  requested the bounded initial implementation and authorized this single
  correction cycle after independent review.
- Status: authorized non-production repository control-plane maintenance.

## Parent and prerequisites

None.

## Authority references

- harness/archive/task-control-v1/tasks/evidence-branch-orchestration-profile.md

## Authorized scope

- The authorized scope is the reusable optional ownership-manifest version 2 and
`evidence-branches-v1` matrix schemas, their fail-closed validator, focused
control-plane tests and fixtures, and concise corresponding repository guidance.
One generic sole writer works in the current shared worktree. That description
records the execution mode without assigning the historical control-plane writer
to a production implementation, test, or documentation agent role.
- An independent read-only reviewer reviewed the initial implementation. The human
authorized exactly one consolidated writer correction cycle for the resulting
findings. After its correction review found a context-free authorization check,
the human separately authorized one final parent-applied correction; no further
writer/reviewer loop is authorized.

## Completion criteria

- The correction is validated with focused pytest coverage, the unchanged P1
version-1 ownership preflight, Draft 2020-12 schema compilation, Ruff check and
format, checkpoint validation, a Sphinx warnings-as-errors build, and a Git diff
and staging check. These checks establish only control-plane contract behavior;
they do not establish production correctness, scientific validity, or human final
acceptance. Direct tool invocation can technically bypass the preflight and
remains unauthorized.

## Exclusions

- This maintenance task does not authorize or modify Python production code,
scientific schemas or fixtures, P1 test modules, the P1 ownership manifest, the
P1 test completeness or ownership matrices, scientific execution, a scientific
Workflow, a workflow engine, a new skill, or a new scientific-chain task. The
optional profile does not become mandatory for ordinary version-2 tasks and does
not itself execute or orchestrate branches.
- The production-task ownership launch preflight applies prospectively to
production tasks. It does not apply retrospectively to this explicitly authorized
non-production control-plane maintenance task, and this record does not invent a
production ownership manifest for work already performed.
- The correction is validated with focused pytest coverage, the unchanged P1
version-1 ownership preflight, Draft 2020-12 schema compilation, Ruff check and
format, checkpoint validation, a Sphinx warnings-as-errors build, and a Git diff
and staging check. These checks establish only control-plane contract behavior;
they do not establish production correctness, scientific validity, or human final
acceptance. Direct tool invocation can technically bypass the preflight and
remains unauthorized.

## Historical source

`harness/archive/task-control-v1/tasks/evidence-branch-orchestration-profile.md` (`sha256:496cd13a74d8c3a2d64f7a44dfe24fa4f23a2005d0a0e2b9a99350b8bfc5243f`)
