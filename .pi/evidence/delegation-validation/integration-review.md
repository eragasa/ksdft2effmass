# Final independent integration review

**Result: FAIL**

## Reviewed scope

- `.pi/evidence/delegation-validation/runtime-probes.md`
- Active Task JSON
- `.pi/settings.json`
- Ten named durable agent records
- Output and metadata artifacts for all ten listed run IDs
- Git and dependency/lockfile status

## Material findings

1. **Unsupported runtime-inventory claim**
   `runtime-probes.md` states that supported runtime discovery returned exactly ten executable identities and excluded all 24 disabled identities. None of the retained raw artifacts reviewed contains the runtime inventory/status output supporting that assertion. Repository records and settings support the expected 34 − 24 = 10 configuration relationship, but configuration agreement does not independently establish runtime discoverability.

2. **Unsupported exact terminal-state claim**
   The report states that every run reached terminal state `completed`. Each metadata artifact establishes the correct run ID, agent identity, exit code `0`, `acceptance: not-required`, and a produced output, but it contains no `completed` status field. Each metadata record also reports `processSignal: SIGTERM`. This does not contradict successful output, but the claimed exact supported-runtime terminal status is not independently retained.

These omissions are material because the active Task explicitly requires exact runtime identities and terminal statuses and makes runtime discovery/delegation behavior the subject of verification.

## Agreements observed

- All ten run IDs map one-to-one to the ten reported durable identities.
- Roles, tools, and skills agree among the report, agent front matter, outputs, and metadata.
- Each output preserves its assigned nonmutation, fail-closed, authority, and claim boundaries.
- Harness outputs preserve the required project-local-to-generic dependency direction.
- Disabled identities were appropriately checked by configuration/set comparison rather than launched.
- The aggregation-expression error and its claim limitation are explicitly disclosed.
- No scientific validity, protected-action authority, Task acceptance, or human acceptance is claimed.
- Git status showed only the untracked `.pi/evidence/delegation-validation/` report directory.
- No dependency declaration or lockfile change was present.

## Residual limitations

- No probes or runtime inventory commands were rerun, as required.
- Probe nonmutation is supported by outputs and current repository status, but pre-probe cleanliness cannot be independently reconstructed from the reviewed artifacts.
- The disclosed aggregation failure means general aggregation correctness remains unverified.
- Passing these probes would establish only the recorded discovery/delegation transport behavior, not future availability or broader agent correctness.
