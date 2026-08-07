# Task-ownership launch preflight

Task-specific writers and independent reviewers must be declared when an
accepted task requires a manifest, multiple agents write concurrently, protected
source and independent verification must be separated, or conflicting or
high-risk path ownership exists. Ordinary bounded work may use one writer for
source, tests, and documentation without a manifest. When required, the
declaration is a fail-closed launch prerequisite, not retrospective review
evidence. The controlling record names an `ownership_manifest`. Run:

```bash
python/.venv/bin/python .pi/task-ownership/validate_task_ownership.py --task <TASK_ID>
```

Run the command from the repository root. If the canonical interpreter is
missing, stop and synchronize it with `cd python && uv sync --locked --all-extras`;
do not fall back to an activated environment or system Python.

## Manifest versions

`ownership.schema.json` is the version-1 compatibility contract. Its P1 object
inventory, test filename rules, exception classes, and string completion command
remain unchanged.

`ownership-v2.schema.json` is the generic contract. It declares role-labelled
writers, independent reviewers, non-overlapping repository-relative scopes, and
a completion validator. Its command is exactly `[path]` or
`[python-like, path]`; a wrapper must own any additional arguments. Version-2
agent records validate agent identity and writer/read-only role only. Structured
manifest `owned_paths`, not agent-record prose, authorizes paths. Version 2
intentionally has no P1-specific object-kind or test-filename convention.

The bounded maintenance authorization for this reusable profile is recorded in
`.pi/tasks/evidence-branch-orchestration-profile.md`; it is not a scientific-chain
task or a retrospective production manifest.

A version-2 manifest may select the exact optional profile
`evidence-branches-v1` by declaring a repository-relative `branch_matrix` and
`correction_cycle_limit` equal to `1`. The matrix conforms to
`evidence-branch-matrix.schema.json`. Its structured authorization names the
same durable task record as the manifest, a stable decision ID, and a rationale.
The record must contain exactly one affirmative machine-readable marker whose
JSON object contains only the declared `profile`, `decision_id`, and
`"authorized": true`; prose mentions, including negations, do not authorize the
profile. Activation requires at least two branches and either two writer roles or both
deterministic and protected-checkpoint classifications.

Every validation stage declares a writer role, structured command, evidence
paths, and requirements. All stages are referenced. Exactly one completion stage
matches the manifest completion command and includes its validator path as owned
evidence. The matrix is reusable control-plane input: execution results do not
belong in it.

For the optional profile, dispatch all matrix branches assigned to one writer
role as one batch. After all writer batches and declared validation stages,
perform one consolidated independent review. At most one consolidated correction
cycle may follow; unresolved findings are escalated instead of starting another
writer/reviewer loop. Ordinary version-2 tasks need not enable this profile.
The schema and validator authorize and validate declarations; they do not
execute, dispatch, or otherwise orchestrate branches.

The validator fully applies the selected Draft 2020-12 JSON Schema and then
checks task identity, agent records, path containment and ownership, role
independence, branch identity and acyclicity, validation-stage references, and
unresolved same-task checkpoint bindings. Missing or invalid declarations fail
the preflight. Passing establishes control-plane ownership only; it does not
validate implementation, tests, scientific claims, or human acceptance. A
direct tool or agent invocation can still bypass this script technically; such a
bypass remains unauthorized and is not evidence that the preflight passed.
