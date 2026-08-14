# Pi parent orchestration

## Parent responsibility

The parent Pi session is the sole orchestrator for ordinary project subagents. Before execution it:

1. reconstructs the exact selected Harness Task context;
2. inspects the repository and current uncommitted state;
3. determines whether delegation is materially useful;
4. lists available agents and selects only an executable, non-disabled role;
5. defines the child’s goal, target revision, authority boundary, success criteria, validation, output, and stop rules; and
6. chooses context, isolation, and runtime controls appropriate to the work.

The parent does not delegate human-owned decisions, protected-action authority, Task activation, final synthesis, or acceptance.

## Execution surface

All execution uses `workflowScript`:

```text
one child       runs.run(stableKey, assignment)
parallel lanes  runs.all(distinctAssignments)
sequence        ordinary JavaScript over runs.run results
```

A one-child delegation is still a workflow. Saved chains may remain as durable historical state, but new orchestration is authored through `workflowScript` rather than a duplicate chain or workflow language.

## Assignment contract

A strong child assignment contains only the context needed by that role:

- concrete goal;
- repository, `cwd`, starting revision, and relevant source seam;
- selected Task and approved scope;
- exact read/write and protected-action boundary;
- relevant decisions and evidence;
- success criteria and focused validation;
- expected result or artifact shape; and
- conditions requiring supervisor escalation or immediate stop.

The assignment narrows authority inherited from the Task. It cannot expand it. Fresh-context reviewers inspect authoritative files and diffs directly rather than relying on the writer’s reasoning. Forked context is used only when inherited parent history is intentionally part of the child contract.

## Orchestration shape

The default bounded shape is:

```text
parent inspection
→ one writer when delegation is useful
→ fresh-context read-only review when materially useful or required
→ parent synthesis
→ at most one correction writer
→ parent final verification
```

This is guidance for coordinating actual work, not a Harness Task state machine. Routine work need not launch a subagent merely to satisfy the diagram.

## Child delegation

Ordinary children must not launch their own subagents. Only an explicitly configured fanout child whose resolved tools include `subagent` may delegate, and only within its assigned fanout. The parent retains orchestration authority and the configured nesting ceiling still applies.

## Unresolved issues

- Whether project policy should forbid fanout children entirely.
- Which tasks justify forked context rather than fresh context.
- Whether parent assignments need a project-local structured schema or remain concise prompt contracts.
- Default review fanout for broad public-contract changes.
- When a mission is required for recovery across parent-session boundaries.
