# E01 checkpoint 02: Codex skill-surface correction

## Finding identifier

`E01-F01`

## Category and severity

- Category: `I` -- Integration defect
- Severity: `material`
- Stage: `final_human_review`

## Finding

Graphify 0.9.2 installed its project Codex skill under `.codex/skills`, while
current official Codex documentation specifies `.agents/skills` for
repository-local skill discovery.

## Official Codex evidence

Authoritative reference inspected on 2026-07-30:

<https://learn.chatgpt.com/docs/build-skills>

The documentation states that Codex reads repository-local skills from
`.agents/skills` in every directory from the current working directory up to the
repository root. It also states that Codex explicit invocation can use `/skills`
or `$` skill mention and that the Codex initial skills list includes each
skill's file path.

## Root cause

The Graphify installer source was treated as authoritative for Codex discovery,
and validation checked file presence at `.codex/skills/graphify/SKILL.md`
instead of actual discovery by a fresh Codex session.

## Consequence

The repository could report a completed Codex integration even though Codex
might not expose or invoke the Graphify skill.

## Human corrective approval

The human approved Checkpoint 3 corrective work for this material finding on
2026-07-30. Final human acceptance remains blocked until the skill location is
corrected and actual Codex discovery is verified.

## Affected files

Planned affected files and directories:

- `.agents/skills/graphify/`
- `.codex/skills/graphify/`
- `AGENTS.md`
- `.pi/tasks/graphify-integration.md`
- `.pi/skills/choose-next-task/SKILL.md`
- `.pi/skills/use-graphify/SKILL.md`
- `docs/development/agent-control-plane.rst`
- `docs/research/agentic-development-case-study.rst`
- `docs/research/agentic-development-case-study/`
- `docs/architecture/repository-layout.md`
- `docs/architecture/repository-layout.rst`

## Planned correction

Move the manually installed Graphify skill from `.codex/skills/graphify/` to
`.agents/skills/graphify/`, preserving Graphify version `0.9.2`, frontmatter,
references, and provenance. Remove the obsolete repository copy under
`.codex/skills/graphify/` and do not leave duplicate Graphify skills in both
locations. Do not create `.codex/hooks.json`, install hooks, modify global
skills, or enable external semantic processing.

Update control-plane and documentation references so the separation is:

```text
.pi/skills/      repository-local pi skill surface
.agents/skills/  repository-local Codex skill surface
.codex/          Codex configuration or hooks only when explicitly approved
```

## Verification required

A file-presence check is insufficient. Verification must start a fresh Codex
session from the repository root and verify that `graphify` appears in available
project skills and resolves to `<repository-root>/.agents/skills/graphify/SKILL.md`.
The validation must not run graph generation, modify repository files, install
hooks, enable external semantic processing, or configure API keys.
