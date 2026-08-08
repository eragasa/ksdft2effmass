---
document_id: ksdft2effmass.harness.002.001.004
task_id: harness-simplification.agents.durable-roles
parent: ksdft2effmass.harness.002.001.000
status: current
sphinx: excluded
---

# Create durable harness roles

## Baseline and result

The pre-migration population contained 29 agent records: five durable project
roles and 24 historical-reference-only phase-specific harness roles. No durable
harness-agent record existed, no phase-specific role had a live assignment, and
no active task or unresolved checkpoint conflicted with this bounded action.

This completed slice created five available durable capability roles. Their
records do not activate work, grant path ownership, replace historical identity,
or provide acceptance.

| Role | Access | Stable responsibility and authority boundary |
|---|---|---|
| `ksdft2effmass-harness-implementation` | Writer | Assigned generic and project-local harness source, textual resources, and directly affected source documentation; no normal test, narrative-documentation, scientific-source, or decision ownership. |
| `ksdft2effmass-harness-tests` | Writer | Assigned harness software-verification tests and independent contract oracles; reports production defects instead of repairing source. |
| `ksdft2effmass-harness-documentation` | Writer | Assigned maintained harness architecture, API, resource, profile, agent, ownership, migration, and operational documentation; source and tests remain read-only unless separately assigned. |
| `ksdft2effmass-harness-integration-reviewer` | Read-only | Final cross-surface agreement and exact material findings; cannot accept or repair the reviewed work. |
| `ksdft2effmass-harness-architecture` | Read-only | Optional specialist for genuine architecture alternatives and recommendations; not a routine-work participant and cannot select its recommendation. |

## Boundaries

Project-local harness may depend on generic harness. Generic harness must not
depend on project-local code or scientific semantics. Generic capabilities
therefore remain free of project task identities, CPN scientific workflow
semantics, electronic-structure tools, semiconductor physics, provenance-domain
scientific meaning, and scientific-validation conclusions. Explicit repository
roots, profiles, manifests, policy extensions, compatibility adapters, and
selected routing configuration enter only through project-local composition.

Agent records own reusable capability, access mode, stable boundaries, and
applicable skills. Task-specific paths and permissions belong in explicit
ownership assignments so the same identity remains stable across bounded work.
No role may activate its task, expand assigned paths, make a human-owned
decision, authorize protected execution, approve its own work, or modify
unrelated scientific code.

The new identities are future assignment targets. They do not retroactively
replace, alias, rename, or claim work performed by the 24 retained phase agents;
those records remain `historical-reference-only`.

## Decomposition

| Document | Task identity | Title | Status | Sphinx |
|---|---|---|---|---|
| [harness.002.001.004](./ksdft2effmass.harness.002.001.004.md) | `harness-simplification.agents.durable-roles` | Create durable harness roles | Current | Excluded |
| [harness.002.001.005](./ksdft2effmass.harness.002.001.005.md) | `harness-simplification.agents.project-role-simplification` | Simplify durable project roles | Current | Excluded |
| [harness.002.001.006](./ksdft2effmass.harness.002.001.006.md) | `harness-simplification.agents.executable-tool-placement-contract` | Establish executable-code and maintained-agent-tool placement contract | Current | Excluded |
| No document assigned | `harness-simplification.agents.validator-migration-pilot` | Pilot migration of one validator under the accepted placement contract | `inactive_unauthorized` | Excluded |
| No document assigned | Not created | Remove historical roles from live discovery | Proposed | Excluded |
| No document assigned | Not created | Retire obsolete phase-agent files | Proposed | Excluded |
| No document assigned | Not created | Validate delegation and handoffs | Proposed | Excluded |
| No document assigned | Not created | Evaluate SQLite or evidence-storage work | Proposed | Excluded |

The first three rows are current. The project-role page records the completed
simplification of all five durable project roles, and the placement-contract page
records the completed executable-tool architecture. The validator pilot remains
the next ordered `inactive_unauthorized` chain entry with `record: null`; it has
no task record or child page and is not activated or begun. The remaining
unassigned rows identify later proposals without linking to nonexistent files;
broader discovery, retirement, delegation, storage, and protected work remain
later proposals.

## Implementation scope and validation

Implementation was limited to the five new agent records, this plan, its parent
link, the complete agent inventory, and any minimum deterministic capability
registration required by existing validators. Existing agents, assignments,
control records, retained evidence, harness behavior, tests, dependencies,
lockfiles, and scientific source remain unchanged by this slice.

Focused validation parses all records, checks filename/identity and access-mode
agreement, resolves referenced skills and documentation links, reconciles every
agent exactly once with inventory totals, runs existing agent and skill-capability
validators, confirms protected surfaces are unchanged, and runs
`git diff --check`. These checks establish bounded structural consistency only.

## Rollback and stop conditions

Rollback removes the five new records and this page, then restores the parent,
inventory, and any minimum capability registration to their pre-migration
content. Historical agents and retained evidence require no rewrite.

Stop rather than broaden the change if an active assignment or unresolved
checkpoint conflicts, an applicable skill is missing, generic/local direction
cannot be preserved, a validator requires behavioral or historical rewrites, an
unrelated working-tree change cannot be preserved, or a human-owned decision is
required.

## Unauthorized later work

The executable-code and maintained-agent-tool placement contract is completed.
The following validator migration pilot remains `inactive_unauthorized`, has no
task record or child page, and is not activated or begun. This page migrates no
executable. Live-discovery changes, historical-agent retirement, delegation and
handoff validation, wider harness behavior changes, SQLite or evidence-storage
implementation, dependency changes, protected execution, and release work
remain inactive and proposed.

## Navigation

- **Index:** [Harness documentation](ksdft2effmass.harness.000.000.000.md)
- **Parent:** [First harness simplification round](ksdft2effmass.harness.002.001.000.md)
- **Previous:** [Durable agent architecture](ksdft2effmass.harness.002.001.003.md)
- **Next:** [Simplify durable project roles](ksdft2effmass.harness.002.001.005.md)
