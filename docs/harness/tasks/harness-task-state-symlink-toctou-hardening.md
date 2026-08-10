<!-- Generated from SQLite control state; do not edit. -->
# Harden task-state file inspection against symlink TOCTOU races

[Task index](index.md) · [Previous](./harness-simplification.resources.manifest-refresh.md) · [Next](./harness.simplification.agents.delegation-validation.md)

## Status

`inactive`: proposed backlog candidate; inactive and not authorized for implementation

## Objective

When separately activated, determine and implement a portable filesystem access strategy that preserves the existing explicit-root and exact-declared-path contract while preventing symlink substitution between validation and file opening. Evaluate descriptor-relative traversal and no-follow facilities such as `openat` and `O_NOFOLLOW`, including Python and supported-platform behavior.

## Parent and prerequisites

None.

## Authority references

- .pi/evidence/pi-harness-incubation/H2/review-integration-initial.md
- harness/archive/task-control-v1/tasks/harness-task-state-symlink-toctou-hardening.md
- python/src/ksdft2effmass/harness/pi/_task_state_files.py

## Authorized scope

- the public `TaskStateInspectionRequest`, `TaskStateInspectionResult`, and `InspectTaskState` API;
- rejection of symlinked roots, files, and intermediate components;
- exact declared-path inspection without recursive discovery;
- deterministic inspected/read path reporting and validation issues; and
- ordinary trusted-repository behavior and packaging compatibility.

## Completion criteria

- Verification should include controlled tests for intermediate and final symlinks, component replacement where deterministic orchestration is feasible, regular-file behavior, missing and non-file paths, root confinement, and supported-platform fallback or fail-closed behavior. The activated task must explicitly define its platform contract before implementation.

## Exclusions

- This proposal authorizes no source, test, dependency, platform-support, or public-contract change. It requires separate human activation and any ownership or review records applicable at that time. It does not justify elevated execution, external computation, dependency additions, or changes to completed H2 evidence.

## Historical source

`harness/archive/task-control-v1/tasks/harness-task-state-symlink-toctou-hardening.md` (`sha256:d5c4a542aa04b0ac86b2dce634590157a0db59a17caf39f2fc9ea661e0cfb306`)
