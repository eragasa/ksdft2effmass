---
name: inspect-task-state
description: Inspects the bounded durable repository state of one exact task selected by a known chain path and task ID. Use when an agent must read declared task, ownership, completion, artifact, run, or handoff records without recursive discovery or inference from prose.
---

# Inspect task state

Use this skill only after authority reconstruction has identified one exact chain path and task identity. This procedure reports declared durable repository state; it does not discover the controlling chain, resolve checkpoints, inspect interactive sessions, infer undeclared artifacts, or activate work.

## Required inputs

Require all three inputs explicitly:

- an absolute repository root;
- a root-relative chain path; and
- the exact task ID selected from that chain.

If the controlling chain or task identity is unknown or conflicting, stop and reconstruct authority from the applicable checkpoints, human decisions, chains, and task records. Do not search for a convenient substitute.

## Invocation

From the repository environment, run:

```bash
python/.venv/bin/python python/src/cli/inspect_task_state.py \
  --root /absolute/path/to/repository \
  --chain .pi/chains/example.chain.json \
  --task-id exact.task.identity
```

Substitute only the three explicit inputs. Do not add recursive discovery, Git-history inspection, session-log inspection, or fallback paths around this command.

## Interpret the result

The command emits deterministic JSON:

- exit status `0`: inspection completed without invalid durable references;
- exit status `1`: declared repository state is invalid or unresolved; retain and report the structured findings;
- exit status `2`: request construction failed; correct only the explicit input that is invalid; and
- exit status `3`: unexpected command-boundary failure; report the failure and stop.

Treat `not_declared`, `declared_missing`, and `inspected` as distinct states. Empty or undeclared run and handoff paths do not establish that no interactive execution occurred. The reported writers and reviewers are declarations, not proof of execution, independence, acceptance, or completion.

## Boundaries and stop

The command is read-only and must not be used to infer authorization, select a successor, resolve a checkpoint, mutate repository state, or claim software verification, numerical verification, scientific validation, uncertainty quantification, or human acceptance beyond the structured result. Stop after returning the exact command, status, declared paths, findings, and limitations needed by the calling task.
