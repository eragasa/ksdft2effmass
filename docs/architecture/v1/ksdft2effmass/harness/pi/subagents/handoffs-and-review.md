# Pi subagent handoffs and review in v1

## Writer handoffs

Enabled writer descriptors request concise results containing some or all of:

- Task and assignment identity;
- workspace and base/result revision or uncommitted state;
- owned and changed paths;
- commands and observed results;
- relevant contract or evidence references;
- activation and successor state; and
- unresolved findings and risks.

A delegated writer outside the parent checkout must report its workspace, base and resulting state, changed paths, checks, and unresolved risks. A formal durable handoff is required only when managed-task policy or later integration requires one. Managed-worktree runs can provide Pi-owned artifact paths and a handoff manifest containing patch and cleanup information.

The exact handoff fields are enforced primarily by descriptor prompts and parent review. There is no single project-local handoff schema shared by every role.

## Reviewer results

Enabled integration-review descriptors are read-only. They request exact review scope, subject revision, inspected evidence, material findings with severity and references, authority assessment, and residual limitations.

Reviewers do not mutate the reviewed scope, resolve human decisions, authorize protected execution, accept the work, or approve their own review. A reviewer result is evidence returned to the parent.

## Parent verification

The parent checks the actual workspace, changed paths, diff, commands, ownership, and unresolved findings before integration. Child-reported command success remains reported evidence unless the parent or host acceptance gate independently runs the command.

Independent review is optional and risk-based for ordinary direct work. When a managed Task or current human instruction requires consolidated review and a bounded correction pass, the parent coordinates that procedure; it is not Pi runtime lifecycle.

## Known limitations

- Writer handoff wording varies across descriptors.
- No common finding-code or handoff wire contract exists.
- Parent disposition of reviewer findings is not represented by one dedicated V1 object.
- A clean child result does not automatically update canonical Task JSON, `harness/task-selection.json`, transitional chain projections, or checkpoints.
