# Pi subagent descriptors

## Authority and location

Canonical project agent descriptors live under `.pi/agents/**/*.md`. User agents and Pi built-ins may also be discovered, but project descriptors win on runtime-name conflicts. Legacy `.agents/**/*.md` discovery is compatibility behavior and is not the V2 project-authoring location.

A descriptor defines a role and capability ceiling. It does not assign work or grant Harness Task authority.

## Descriptor contract

A project descriptor may declare:

- canonical name and optional package;
- concise role description;
- strict child tool allowlist;
- project-context and skill inheritance policy;
- selected skills and extension providers when needed;
- system-prompt composition mode and role instructions;
- default context, model, thinking, output, or runtime limits when justified; and
- `acceptanceRole` as `writer` or `read-only` for acceptance inference.

`tools` is a child allowlist, not an extension loader. A named extension tool must also have an explicitly available provider. `acceptanceRole` influences runtime acceptance inference; it does not grant tools, repository authority, or permission to edit.

## Role families

The maintained project descriptors currently demonstrate these role families:

| Family | Intended use | Typical capability |
|---|---|---|
| Architecture specialist | Read-only analysis of a genuine architecture decision | `read`, `bash` |
| Implementation writer | Task-assigned source and directly affected documentation | `read`, `bash`, `edit`, `write` |
| Documentation writer | Task-assigned maintained documentation | `read`, `bash`, `edit`, `write` |
| Test writer | Task-assigned software-verification evidence | `read`, `bash`, `edit`, `write` |
| Integration reviewer | Independent cross-surface review | `read`, `bash` |

A role describes reusable behavior. It must not duplicate mutable Task scope, current selection, exact owned paths, or one-run instructions. Those belong in the parent’s assignment prompt and any required ownership record.

## Validation

A descriptor validator should check structural and project policy rules without executing the agent:

- canonical name and discovery location;
- required role description;
- known tool names and strict allowlist syntax;
- writer versus read-only role consistency;
- inheritance and skill references;
- absence of embedded credentials or mutable Task status; and
- required stop and escalation boundaries for project roles.

Validation establishes descriptor conformance only. Runtime discovery and launch preflight remain Pi responsibilities.

## Unresolved issues

- Closed project role-family vocabulary.
- Which legacy task-specific descriptors should be retired after their Tasks close.
- Whether project descriptors should use qualified runtime package names.
- Minimum required frontmatter across all project roles.
- Whether role-specific durable memory is ever justified for this project.
