# Optional evidence-branch orchestration profile

## Decision

- Decision ID: `EBOV1-AUTH-2026-08-03`
- Profile: `evidence-branches-v1`
- Authority: explicit human authorization in the 2026-08-03 conversation that
  requested the bounded initial implementation and authorized this single
  correction cycle after independent review.
- Status: authorized non-production repository control-plane maintenance.

<!-- evidence-branch-authorization {"profile":"evidence-branches-v1","decision_id":"EBOV1-AUTH-2026-08-03","authorized":true} -->

## Scope and ownership

The authorized scope is the reusable optional ownership-manifest version 2 and
`evidence-branches-v1` matrix schemas, their fail-closed validator, focused
control-plane tests and fixtures, and concise corresponding repository guidance.
One generic sole writer works in the current shared worktree. That description
records the execution mode without assigning the historical control-plane writer
to a production implementation, test, or documentation agent role.

An independent read-only reviewer reviewed the initial implementation. The human
authorized exactly one consolidated writer correction cycle for the resulting
findings. After its correction review found a context-free authorization check,
the human separately authorized one final parent-applied correction; no further
writer/reviewer loop is authorized.

## Exclusions

This maintenance task does not authorize or modify Python production code,
scientific schemas or fixtures, P1 test modules, the P1 ownership manifest, the
P1 test completeness or ownership matrices, scientific execution, a scientific
Workflow, a workflow engine, a new skill, or a new scientific-chain task. The
optional profile does not become mandatory for ordinary version-2 tasks and does
not itself execute or orchestrate branches.

The production-task ownership launch preflight applies prospectively to
production tasks. It does not apply retrospectively to this explicitly authorized
non-production control-plane maintenance task, and this record does not invent a
production ownership manifest for work already performed.

## Validation and claim boundary

The correction is validated with focused pytest coverage, the unchanged P1
version-1 ownership preflight, Draft 2020-12 schema compilation, Ruff check and
format, checkpoint validation, a Sphinx warnings-as-errors build, and a Git diff
and staging check. These checks establish only control-plane contract behavior;
they do not establish production correctness, scientific validity, or human final
acceptance. Direct tool invocation can technically bypass the preflight and
remains unauthorized.
