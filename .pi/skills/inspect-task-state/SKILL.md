---
name: inspect-task-state
description: Inspects the bounded durable repository state of one exact canonical HarnessTask using explicit Task and selection inputs and an optional operation-scoped ownership manifest.
---

# Inspect task state

Use this skill only after authority reconstruction has identified one exact Task
identity and canonical Task-record path. This procedure reports declared durable
repository state; it does not discover Tasks, resolve decisions, inspect interactive
sessions, infer ownership, or activate work.

## Required inputs

Require:

- an absolute repository root;
- the exact root-relative canonical Task JSON path;
- the root-relative ``harness/task-selection.json`` path; and
- the exact Task ID.

Supply an ownership-manifest path only when the inspected development operation
explicitly binds that manifest. Ownership is never discovered from the Task, selection,
a side registry, or historical control records.

## Invocation

```bash
python/.venv/bin/python python/src/cli/inspect_task_state.py \
  --root /absolute/path/to/repository \
  --task harness/tasks/exact.task.json \
  --selection harness/task-selection.json \
  --task-id exact.task.identity
```

For an operation that explicitly binds ownership, add:

```bash
  --ownership-manifest .pi/task-ownership/exact-operation.json
```

Do not add recursive discovery, SQLite, generated projection, Git-history, session-log,
or fallback inputs around this command.

## Interpret the result

- exit status ``0``: inspection completed without invalid durable references;
- exit status ``1``: an explicit durable input is invalid; retain the findings;
- exit status ``2``: request construction failed; correct only the invalid input; and
- exit status ``3``: unexpected command-boundary failure; report and stop.

Selection records requested work only and grant no authority. Ownership declarations
constrain an operation but do not prove execution, independence, acceptance, or
completion.

## Boundaries and stop

The command is read-only. It does not infer authorization, select a successor, resolve
a decision, mutate state, or establish software verification, numerical verification,
scientific validation, UQ, or human acceptance. Stop after returning the command,
status, exact paths, findings, and limitations needed by the caller.
