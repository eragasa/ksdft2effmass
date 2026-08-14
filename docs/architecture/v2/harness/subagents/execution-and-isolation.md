# Pi subagent execution and isolation

## Runtime boundary

The `pi-subagents` extension owns child-process launch, child-session construction, model and tool resolution, context mode, asynchronous control, managed worktrees, artifacts, and runtime lifecycle. The project owns descriptors, assignments, repository policy, and interpretation of returned work.

Project architecture does not reimplement the Pi supervisor or persist a competing run state.

## Context modes

| Mode | Meaning | Preferred use |
|---|---|---|
| Fresh | New child context containing explicit project and assignment inputs | Independent review, validation, bounded inspection |
| Fork | Branched child session inheriting Pi's filtered form of the persisted parent transcript | Advisory work or execution where parent history is intentionally relevant |

Forked context is not a purpose-built minimal context. Pi removes parent-only orchestration traffic and instructions, control messages, and provider-private thinking content, but the child still receives relevant inherited conversation history. A fresh reviewer should inspect the actual repository revision and diff rather than receive the writer’s chain of reasoning.

## Asynchronous execution

Subagent work is asynchronous by default. The parent may continue read-only inspection, validation preparation, or synthesis while a child runs. It must not perform conflicting writes in the child’s active workspace.

The parent uses supervisor status, transcript, steering, interrupt, stop, resume, and wait surfaces rather than polling files or inferring state from silence. A `needs_attention` signal reports lack of observed activity; it is not failure or Harness Task state.

## Managed worktrees

`worktree: true` creates a managed isolated Git worktree for a child. It requires a suitable clean source state and produces a handoff manifest containing status, patch references, statistics, and cleanup information. Preserved dirty or divergent work is not discarded without explicit authority.

Managed worktrees are required for parallel writers. They are optional for one isolated writer and unnecessary for read-only children unless a clean independent subject is useful.

## Capability controls

Effective child capability is the intersection of:

- the selected Task and parent assignment;
- the resolved agent descriptor;
- project and user settings;
- session-scoped capability ceilings;
- runtime tool and extension availability; and
- host safety and authority policy.

A prompt cannot widen a tool allowlist or capability ceiling. Protected execution, destructive cleanup, external transmission, dependency changes, and release actions remain governed by repository authority even when a runtime tool could technically perform them.

## Supervision

A child requests clarification or a human-owned decision through the injected supervisor channel when available. The parent replies through the native supervisor surface. Progress messages are reserved for meaningful discoveries, requested updates, or blockers; routine completion returns through the normal result.

## Unresolved issues

- Project defaults for fresh versus forked context by role.
- Whether project settings should enforce a session-wide agent allowlist.
- Default asynchronous time and attention thresholds for long validation commands.
- Whether managed worktrees should be mandatory for every delegated writer.
- Recovery contract for a child that terminates after mutating an unmanaged checkout.
