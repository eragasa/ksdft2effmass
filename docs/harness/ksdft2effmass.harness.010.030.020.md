---
document_id: ksdft2effmass.harness.010.030.020
task_id: harness-simplification.agents.project-integration-review
parent: ksdft2effmass.harness.010.030.000
status: current
sphinx: excluded
---

# Simplify durable project roles

## Capability boundary

Durable project roles describe reusable capability rather than the history or
file layout of a particular task. The completed test-agent, implementation-agent,
and documentation-agent slices removed subsystem names, exact paths, migration
state, and procedural mechanics from their durable records. The current
integration-review-agent slice applies the same boundary to independent review:
the durable role no longer embeds historical OperatorRecord and CPN subjects,
fixed paths or commands, correction-cycle procedure, or checkpoint
specialization.

The concise [`ksdft2effmass-integration-reviewer`](../../.pi/agents/ksdft2effmass-integration-reviewer.md)
role remains independent and read-only. Its proportional-review rule is to
review only surfaces materially affected by the assigned change and the
interfaces connecting them. Within that scope it checks applicable agreement
among accepted contracts, production source, tests, maintained documentation,
schemas and fixtures, exports and imports, dependency and packaging declarations,
and task ownership and completion surfaces. It also verifies that evidence
classes and scientific claims do not exceed demonstrated evidence or review
authority.

The role reports material findings with severity and exact file and line evidence
when practical, classifies them as deterministic defects, architectural
conflicts, unsupported claims, or residual limitations, and never repairs or
accepts reviewed work. It fails closed on missing or conflicting authority,
incomplete material inputs, writer-independence conflicts, unresolved scientific
or mathematical meaning, public-contract or compatibility conflicts, ownership
conflicts, unsupported claims, and required human decisions.

It retains the broadly reusable `develop-python-test-evidence` and
`document-python-research-software` skills. Universal
`design-data-action-objects` and `develop-operator-records` specialization is
removed. A future authorized task may select a supported subject-specific skill
when required; a routing limitation must be reported rather than embedded as
durable specialization, and task routing cannot expand authority or scope.

## Completed and current slices

The completed slices simplified
[`ksdft2effmass-tests`](../../.pi/agents/ksdft2effmass-tests.md),
[`ksdft2effmass-implementation`](../../.pi/agents/ksdft2effmass-implementation.md),
and [`ksdft2effmass-documentation`](../../.pi/agents/ksdft2effmass-documentation.md).
The current slice simplifies only `ksdft2effmass-integration-reviewer`.
`ksdft2effmass-architecture` remains unchanged and inactive.

These slices do not change agent population, role identity, access, lifecycle,
historical attribution, discovery, routing, harness behavior, tests, retained
evidence, scientific source, dependencies, or protected-execution authority.
Architecture simplification, live discovery, historical retirement, and
delegation validation remain proposed and unauthorized.

## Validation and rollback

Focused validation checks the ownership manifest, agent and skill-capability
agreement, exact front matter, the
[self](./ksdft2effmass.harness.010.030.020.md) and
[parent](./ksdft2effmass.harness.010.030.000.md) links, relative links on the
owned pages, unchanged inventory totals, absence of links to nonexistent planned
children, and whitespace errors. These structural checks do not establish
scientific validity or human acceptance.

Rollback for the current slice restores the prior
`ksdft2effmass-integration-reviewer` record and any required capability
registration, then restores this page and the
[current inventory](./ksdft2effmass.harness.001.050.000.md) descriptions. It
does not undo the completed test-agent, implementation-agent, or
documentation-agent slices, rewrite historical agents or retained evidence, or
affect the unchanged architecture role.
