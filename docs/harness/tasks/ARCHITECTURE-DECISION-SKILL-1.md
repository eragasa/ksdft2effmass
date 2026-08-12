<!-- Generated from SQLite control state; do not edit. -->
# ARCHITECTURE-DECISION-SKILL-1 — develop-architecture-decision harness resource

[Task index](index.md) · [Previous](./A.md) · [Next](./B.md)

## Status

`closed_human_accepted_pass`: closed as human-accepted PASS at `ARCHITECTURE-DECISION-SKILL-1-HC01` on 2026-08-07 from starting revision `3927d41b93e6be480e9c29013984b9385808ad4c`

## Objective

It creates and activates the read-only `develop-architecture-decision` skill, canonical/reference/descriptor resources, byte-identical live resources, controlled H6-only fixtures and validator, generic/local manifest and profile synchronization, eight-skill inventory/validation, current local replay, selected local route, maintained harness documentation, and task evidence.

## Parent and prerequisites

- External prerequisite: `explicit_human_authorization`

## Authority references

- .pi/agents
- .pi/chains/develop-architecture-decision-skill.chain.json
- harness/archive/task-control-v1/tasks/ARCHITECTURE-DECISION-SKILL-1.md

## Authorized scope

- It creates and activates the read-only `develop-architecture-decision` skill, canonical/reference/descriptor resources, byte-identical live resources, controlled H6-only fixtures and validator, generic/local manifest and profile synchronization, eight-skill inventory/validation, current local replay, selected local route, maintained harness documentation, and task evidence.

## Completion criteria

- Run ownership preflight with the task-specific chain:
- ```text
python .pi/task-ownership/validate_task_ownership.py --task ARCHITECTURE-DECISION-SKILL-1 --chain .pi/chains/develop-architecture-decision-skill.chain.json
```
- Then run task completion, current H3 resource validation, eight-skill capability validation, selected local route, controlled architecture cases, JSON/link checks, and diff/protected-nonmutation checks. Reviewer gate is required after deterministic completion. One consolidated correction pass is permitted after that review. Final output is one pending skill-acceptance checkpoint; acceptance must not invoke the skill, initialize H6, or activate a successor.

## Exclusions

- The current human instruction authorizes this bounded one-writer harness resource task. It creates and activates the read-only `develop-architecture-decision` skill, canonical/reference/descriptor resources, byte-identical live resources, controlled H6-only fixtures and validator, generic/local manifest and profile synchronization, eight-skill inventory/validation, current local replay, selected local route, maintained harness documentation, and task evidence.
- Historical implementation and review assignments are retained only in Git; current work routes through durable harness roles.
- No `.pi/agents/`, real H6 work, dispatch, ownership semantics, P2/P3/H5 surfaces, production/project tests or schemas, dependencies, locks, SQLite, replay redesign, execution/release, historical catalogs, final checkpoint, commit, or push may be changed. Canonical generic resources remain authoritative; local depends on generic and live resources are synchronized from canonical. The selected route remains `local`.

## Historical source

`harness/archive/task-control-v1/tasks/ARCHITECTURE-DECISION-SKILL-1.md` (`sha256:eee17615b5e4b4120ffb64dda283e6b74cd2cb7c985ac56fecd5739b0dee187a`)
