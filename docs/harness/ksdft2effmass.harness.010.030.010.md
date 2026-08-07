---
document_id: ksdft2effmass.harness.010.030.010
task_id: harness-simplification.agents.durable-roles
parent: ksdft2effmass.harness.010.030.000
status: current
sphinx: excluded
---

# Create durable harness roles

## Baseline and result

The pre-migration population contained 29 agent records: five durable project
roles and 24 historical-reference-only phase-specific harness roles. No durable
harness-agent record existed, no phase-specific role had a live assignment, and
no active task or unresolved checkpoint conflicted with this bounded action.

This slice creates five available durable capability roles. Their records do not
activate work, grant path ownership, replace historical identity, or provide
acceptance.

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
| [harness.010.030.010](./ksdft2effmass.harness.010.030.010.md) | `harness-simplification.agents.durable-roles` | Create durable harness roles | Current | Excluded |
| harness.010.030.020 | `harness-simplification.agents.project-role-simplification` | Simplify durable project roles | Proposed | Excluded |
| harness.010.030.030 | `harness-simplification.agents.live-discovery` | Remove historical roles from live discovery | Proposed | Excluded |
| harness.010.030.040 | `harness-simplification.agents.historical-retirement` | Retire obsolete phase-agent files | Proposed | Excluded |
| harness.010.030.050 | `harness-simplification.agents.delegation-validation` | Validate delegation and handoffs | Proposed | Excluded |

Only the first row is implemented. The plain coordinates reserve possible
future children without linking to files that do not exist.

## Implementation scope and validation

Implementation is limited to the five new agent records, this plan, its parent
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

Project-role simplification, live-discovery changes, historical-agent retirement,
delegation and handoff validation, harness behavior changes, SQLite or evidence
subsystem implementation, dependency changes, protected execution, and release
work remain unauthorized.
