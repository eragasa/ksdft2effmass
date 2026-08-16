# Pi subagent runtime state and artifacts in v1

## Runtime records

Pi may retain:

- child session JSONL;
- workflow and async status;
- event logs;
- child input and output artifacts;
- transcripts and metadata;
- mission records;
- external receipts; and
- managed-worktree handoff manifests and patches.

These are Pi runtime and recovery records. They are not canonical Harness Task, chain, checkpoint, ownership, scientific workflow, or human-acceptance records.

## Missions and runs

A mission records why delegated work exists and links its runs, decisions, artifacts, and receipts. A run records one actual subagent execution. Ordinary launches may create missions by default; trivial runs can be explicitly missionless.

The repository’s current projection compiler and private projection verifier do not import mission or run lifecycle as development authority. A parent may cite a runtime artifact as evidence or a recovery location.

## Status and control

Pi exposes runtime status, fleet, transcript, steering, interruption, stop, resume, and wait surfaces. Runtime completion reports that the child process returned; it does not establish that requested repository work is correct, integrated, complete, or accepted.

## Retention

Subagent artifacts may be written under `.pi/subagents/`, a session location, or temporary storage according to runtime configuration. The repository does not currently define one complete project retention policy covering all Pi session, mission, transcript, and handoff artifacts.

Repository policy prohibits retaining credentials, private keys, scheduler secrets, private data, or restricted data in source, logs, documentation, manifests, or commits.

## Recovery

Current recovery requires the parent to reconcile several surfaces:

1. Harness Task, chain, checkpoint, and ownership records;
2. Git branch, revision, and working-tree state;
3. Pi mission and run status when applicable;
4. child output and handoff artifacts; and
5. actual changed files and validation evidence.

No runtime artifact silently authorizes resumption, destructive cleanup, publication, or Task completion.

## Known limitations

- Artifact retention and sanitization are not represented by one project contract.
- Pi run identities are not first-class fields in V1 Task records.
- Saved sessions and missions can outlive the parent conversation without becoming part of the harness compiler input.
- Runtime and project-state reconciliation remains a parent procedure.
