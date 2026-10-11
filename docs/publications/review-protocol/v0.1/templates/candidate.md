# Candidate version `<CAMPAIGN>-C<N>`

## Identity

| Field | Value |
|---|---|
| Campaign | `<campaign identifier>` |
| Candidate version | `<candidate identifier>` |
| Predecessor | `<identifier or none>` |
| Protocol | `v0.1` |
| Protocol Git revision | `<full commit>` |
| Candidate Git revision | `<full commit>` |
| Worktree clean | `<yes/no with command evidence>` |
| Candidate state | `<proposed/frozen/superseded/final>` |

## Intended review scope

- Publication purpose: `<purpose>`
- Intended audience: `<audience>`
- Definition of done: `<bounded definition>`
- Included supplements and appendices: `<paths>`
- Explicit exclusions: `<paths and reasons>`
- Current evidence boundary: `<owning sources>`
- Known unavailable evidence: `<evidence and consequence>`

## Composition and source binding

- Composition root: `<path>`
- Ordered source manifest: `<path or table>`
- Bibliography paths: `<paths>`
- Evidence or calculation indexes: `<paths and revisions>`
- Source SHA-256 manifest: `<path and digest>`

A branch name is not a revision. A dirty worktree cannot be marked frozen unless
all consumed bytes are separately retained and bound by the campaign.

## Rendered artifact

| Field | Value |
|---|---|
| Artifact | `<path or retained review attachment>` |
| SHA-256 | `<digest>` |
| Page count | `<count>` |
| Build command | `<exact command>` |
| Tool versions | `<relevant versions>` |
| Build result | `<result and log owner>` |

## Mechanical checks

| Check | Command | Result | Evidence |
|---|---|---|---|
| Source audit | `<command>` | `<result>` | `<path or output>` |
| Citation audit | `<command>` | `<result>` | `<path or output>` |
| Document build | `<command>` | `<result>` | `<path or output>` |
| Other | `<command>` | `<result>` | `<path or output>` |

Passing checks establish only the behavior named by those checks.

## Roles at freeze

| Role | Human or agent | Independence or qualification note |
|---|---|---|
| Lead editor | `<name>` | `<note>` |
| Review orchestrator | `<name/system>` | `<note>` |
| Initial human reviewers | `<names>` | `<roles>` |

## Change from predecessor

`<Required for C1 and later: exact diff, affected packets, and impact decision.>`

## Human freeze confirmation

- Decision record: `<decision identifier>`
- Human decision owner: `<name>`
- Confirmation date: `<date>`
- Confirmed scope: `<summary>`

Until this section is complete, the candidate remains proposed rather than
frozen.
