# Simplify the durable project architecture role

Status: completed incremental refinement under `.pi/chains/harness-simplification.chain.json`

Task identity: `harness-simplification.agents.project-architecture`

Authority: the current human instruction authorizes this bounded incremental refinement without an additional checkpoint.

## Completed historical slice

The original task completed a bounded conversion of the project architecture-agent record from an OperatorRecord/CPN-specific checklist into an optional read-only architecture-decision capability. That completed slice and its completed predecessors remain historical; this refinement does not erase or reopen them.

## Current incremental refinement

Refine `.pi/agents/ksdft2effmass-architecture.md` into a concise durable role. Preserve explicit task authorization, read-only analysis by default, narrow documentation or decision-record writes only under exact task ownership, independence from implementation and human acceptance, proportional inspection, applicable cross-surface boundaries, evidence and claim separation, fail-closed authority behavior, and a concise handoff.

Use exactly three materially distinct alternatives only for a genuine human architecture choice, with a reasoned recommendation that does not make the decision. Remove fixed subsystem, tool, phase, path, command, and universal-checklist inventories; duplicated policy; universal ADR or three-option requirements; and mutable status snapshots. Keep `develop-architecture-decision` as the sole durable skill. Do not begin executable-tool migration.

## Authorized scope and ownership

The controlling ownership manifest is `.pi/task-ownership/harness-simplification.agents.project-architecture.json`.

`ksdft2effmass-harness-implementation` owns exactly the target agent record, this task record, the ownership manifest, the controlling chain, and the skill-capability inventory. The inventory is an allowed path only for a strictly necessary exact consumer correction; current registration is otherwise preserved.

`ksdft2effmass-harness-documentation` separately retains the four exact named harness documentation paths. `ksdft2effmass-harness-integration-reviewer` performs the required independent read-only review. Writer scopes are exact and non-overlapping.

## Boundaries and completion

Do not modify documentation, another agent record, a skill, harness implementation, tests, scientific source, schema, fixture, dependency, lockfile, checkpoint, or retained evidence. Preserve unrelated work. Do not activate successors, reopen completed predecessors, or enable automatic successor activation.

Completion requires valid ownership for the explicit harness chain, valid JSON and agent front matter, applicable skill-capability validation, whitespace-clean owned diffs, and one independent read-only integration review. During execution only this existing task is active. After accepted completion it may return to completed while every successor remains inactive; no successor or checkpoint is automatically created.
