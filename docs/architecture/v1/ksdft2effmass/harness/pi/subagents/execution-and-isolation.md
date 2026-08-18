# Pi subagent execution and isolation in v1

## Pi-owned runtime

The installed `pi-subagents` extension implements discovery, launch preflight, child sessions, context forking, asynchronous execution, supervision, status, steering, interruption, stopping, resumption, managed worktrees, missions, and artifact capture.

The repository does not reimplement these functions in `ksdft2effmass` Python source.

## Context

- **Fresh context** creates a new child session with the resolved role, project context, and explicit assignment.
- **Forked context** branches from a persisted parent session and inherits a filtered transcript. Pi removes parent-only orchestration tool traffic and instructions, slash/status/control messages, and provider-private thinking content.

Project descriptors set `inheritProjectContext: true`. They do not currently declare `defaultContext`; the effective context therefore comes from the launch or runtime defaults.

## Tools and skills

Descriptor `tools` fields are strict child allowlists. Read-only project roles use `read` and `bash`. Writers additionally receive `edit` and `write`. Most descriptors disable ambient skill inheritance and select required skills explicitly. Three retained H2/H4 descriptors use inherited skills but are disabled in project settings.

Tool availability does not grant Task, path, scientific, protected-execution, or acceptance authority.

## Asynchronous control

The parent can launch children asynchronously and inspect documented status or transcript surfaces. Runtime states such as queued, running, paused, complete, stopped, failed, and rejected describe Pi execution only. `needs_attention` indicates lack of observed activity rather than Task failure.

Children may request parent input through the native supervisor bridge when supplied by the runtime. The repository contains no separate project implementation of that channel.

## Managed worktrees

A launch with `worktree: true` asks Pi to create an isolated Git worktree and durable handoff metadata. This supports parallel independent writers only when the source worktree and ownership constraints permit it. Pi may preserve dirty or divergent child work for recovery.

A delegated writer outside the parent checkout reports its workspace, base and resulting state, changed paths, checks, and unresolved risks. The parent verifies the report before integration; a formal durable handoff is retained only when managed-task policy or later integration requires it.

## Known limitations

- Project settings do not establish a project-wide default context, model, thinking level, or worktree policy.
- Runtime capability ceilings are Pi session configuration rather than durable Harness Task fields.
- Managed-worktree setup requires suitable Git state and may not include ignored dependency state.
- Pi runtime lifecycle and project authority remain separately represented.
