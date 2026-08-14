# Pi subagent runtime state and artifacts

## Separate state spaces

Pi runtime state and Harness Task state are independent.

| Pi concept | Meaning | Harness authority |
|---|---|---|
| Agent descriptor | Reusable child role and capability configuration | None |
| Workflow | Parent-authored orchestration through `workflowScript` | None by itself |
| Run | One actual Pi subagent execution | Execution fact only |
| Child session | Runtime conversation and tool state | None |
| Mission | Durable reason and recovery context for delegated work | Does not select or close a Task |
| Receipt | Evidence or link for an external outcome | Evidence only |
| Runtime status | Queued, running, paused, complete, stopped, failed, or rejected | Not Task lifecycle state |
| Handoff artifact | Child output and workspace recovery data | Provisional integration evidence |

The harness may reference immutable Pi run, mission, artifact, or handoff identities when they support a required development claim. It must not import Pi lifecycle state as Task authority.

## Runtime artifacts

Pi may retain status, event, output, session, mission, and managed-worktree handoff artifacts. Consumers use documented status and artifact surfaces rather than scraping terminal rendering. Runtime artifacts remain outside human-authored architecture documentation.

Large child output is stored in distinct durable artifact paths when a later workflow step or parent session must consume it. Parallel children never share output paths.

## Missions

Ordinary substantial delegated work may use the Pi default mission so its objective, linked runs, decisions, artifacts, and receipts survive compaction or parent-session replacement. Trivial lookups and disposable probes may be intentionally missionless.

Mission decisions and receipts are recovery and evidence records. They do not resolve project checkpoints, authorize protected actions, merge code, publish results, or close Harness Tasks. Project checkpoint and Task repositories remain authoritative for those conclusions.

## Retention and privacy

Retained runtime data excludes credentials, private keys, scheduler secrets, restricted scientific data, and unnecessary environment content. External transmission is prohibited unless explicitly authorized. Ephemeral reasoning and scratch state are not promoted to maintained project records merely because Pi can retain a session.

## Recovery

After interruption or context compaction, the parent recovers in this order:

1. authoritative Harness Task context;
2. current Git and workspace state;
3. applicable ownership records;
4. Pi mission and run status when delegation was active;
5. child handoff and output artifacts; and
6. parent verification against authoritative repository state.

Runtime recovery never silently resumes a stopped child, discards a preserved worktree, or assumes that a completed run delivered acceptable work.

## Unresolved issues

- Which Pi artifacts are maintained project evidence versus transient runtime data.
- Mission retention and closure policy for project work.
- Whether Pi run identities appear in Task closure evidence references.
- Sanitization and size limits for retained child outputs.
- Recovery behavior when runtime artifacts and repository state disagree.
