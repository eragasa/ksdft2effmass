# Pi parent orchestration in v1

## Implemented execution surface

The parent Pi session invokes the installed `subagent` tool and launches one or more children through `workflowScript` using stable run keys. Repository procedure requires listing executable, non-disabled agents before project delegation, although Pi can technically resolve a named role directly.

```text
runs.run(key, {agent, task, ...})
runs.all([{key, agent, task, ...}, ...])
```

The parent may choose fresh or forked context, asynchronous execution, managed worktrees, output paths, validation gates, and runtime controls. Project descriptors do not select those values automatically unless their frontmatter supplies a default.

## Parent responsibility

The parent first determines whether the request is ordinary direct work or managed work. For direct work it inspects the relevant files, branch, and working tree without reconstructing unrelated control state. For managed work it inspects only the applicable canonical Task, `harness/task-selection.json`, checkpoint, ownership, workspace, and handoff records. The parent supplies the child’s exact assignment and retains responsibility for:

- role selection;
- scope and path boundary;
- orchestration order;
- human-decision escalation;
- synthesis of reviewer findings;
- integration of writer output;
- final repository verification; and
- user reporting.

Ordinary child roles are not orchestrators. The parent may use read-only children for advice or review and one writer for mutation. Parallel writers require deliberate isolation and ownership separation.

## Assignment representation

V1 assignments are prompt text plus runtime launch parameters. There is no project-local serialized assignment contract. Managed Task and ownership records may be referenced by path and identity, but Pi does not compile them into the child assignment automatically. `DevelopmentTaskSelection` identifies current managed selection only; it is not a launch request or delegation grant.

The parent relies on project-context inheritance, the child role prompt, and explicit assignment text. Fresh-context children receive project context but not the parent’s complete reasoning history. Forked children inherit a filtered form of the persisted parent transcript. Pi removes parent-only subagent tool calls and results, orchestration instructions, slash/status/control messages, and provider-private thinking content before child construction.

## Review flow

The default direct-work flow is implementation, proportionate checks, and a concise report. Independent review, a correction pass, retained evidence, and formal handoff are added only when risk, a current human request, protected boundaries, concurrent ownership, or an explicitly managed Task requires them. Pi supplies execution primitives but does not infer either flow from the Harness Task model.

## Known limitations

- Parent classification of direct versus managed work and inspection of only applicable authority is procedural rather than enforced by a typed launch request.
- No project-local operation derives a minimal child context from authoritative records.
- Harness `.pi/chains/*.chain.json` share a discovery namespace with Pi chain compatibility behavior even though they are development-control records, not subagent workflow definitions.
- Child prompts may repeat policy already present in inherited project context.
