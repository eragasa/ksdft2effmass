# Harden task-state file inspection against symlink TOCTOU races

Status: proposed backlog candidate; inactive and not authorized for implementation

Task identity: `harness.task-state-symlink-toctou-hardening`

This record captures a pre-existing filesystem time-of-check/time-of-use (TOCTOU) limitation in bounded durable task-state inspection. It does not activate work, alter a controlling chain, or reopen an accepted harness task.

## Origin and affected surface

The general filesystem TOCTOU limitation is already retained in `.pi/evidence/pi-harness-incubation/H2/review-integration-initial.md`. The current affected implementation is `python/src/ksdft2effmass/harness/pi/_task_state_files.py`.

`_InspectionFiles.inspect` checks each path component for symlinks before reading the final path. A concurrent process could replace a checked component between the check and the read. Under the intended same-user, trusted-local-repository use, exploitation requires precisely timed concurrent mutation and is currently treated as defense-in-depth technical debt. The risk becomes material if inspection processes untrusted writable repositories, runs with elevated privileges, or supplies a security or authorization decision.

## Proposed outcome

When separately activated, determine and implement a portable filesystem access strategy that preserves the existing explicit-root and exact-declared-path contract while preventing symlink substitution between validation and file opening. Evaluate descriptor-relative traversal and no-follow facilities such as `openat` and `O_NOFOLLOW`, including Python and supported-platform behavior.

The implementation must preserve:

- the public `TaskStateInspectionRequest`, `TaskStateInspectionResult`, and `InspectTaskState` API;
- rejection of symlinked roots, files, and intermediate components;
- exact declared-path inspection without recursive discovery;
- deterministic inspected/read path reporting and validation issues; and
- ordinary trusted-repository behavior and packaging compatibility.

## Required verification when activated

Verification should include controlled tests for intermediate and final symlinks, component replacement where deterministic orchestration is feasible, regular-file behavior, missing and non-file paths, root confinement, and supported-platform fallback or fail-closed behavior. The activated task must explicitly define its platform contract before implementation.

## Boundaries

This proposal authorizes no source, test, dependency, platform-support, or public-contract change. It requires separate human activation and any ownership or review records applicable at that time. It does not justify elevated execution, external computation, dependency additions, or changes to completed H2 evidence.
