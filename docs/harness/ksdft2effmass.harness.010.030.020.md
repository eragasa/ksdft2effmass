---
document_id: ksdft2effmass.harness.010.030.020
task_id: harness-simplification.agents.project-role-simplification
parent: ksdft2effmass.harness.010.030.000
status: current
sphinx: excluded
---

# Simplify durable project roles

## Capability boundary

The durable project roles describe reusable capability rather than the history
or file layout of a particular task. Project tests is the first role simplified
because its former record contained the largest concentration of subsystem
names, exact test paths, per-object inventories, naming rules, migration state,
and command procedure. That detail duplicated skills and ownership records and
could drift as the test suite evolved.

The concise `ksdft2effmass-tests` role retains the stable responsibility to
independently test accepted public contracts and documented invariants on
explicitly assigned test-evidence paths. It preserves supported-public-import
and integration-boundary coverage when assigned, independent oracles (or a
report that no independent oracle is available), precise evidence-class
separation, limits on what passing tests establish, scientific-integrity and
human-authority boundaries, fail-closed stop conditions, and a concise handoff.

Detailed organization, naming, documentation, helper, parameterization,
evidence-identifier, migration, validation, invocation, and reporting mechanics
belong to `develop-python-test-evidence`. Scientific or architecture skills are
loaded only when the assigned subject requires them. Exact paths, commands, and
task scope belong to the active task and validated ownership manifest, not the
durable role.

## Current slice

This slice simplifies only [`ksdft2effmass-tests`](../../.pi/agents/ksdft2effmass-tests.md).
The four later project roles are unchanged:

- `ksdft2effmass-implementation`;
- `ksdft2effmass-documentation`;
- `ksdft2effmass-integration-reviewer`; and
- `ksdft2effmass-architecture`.

It does not change agent population, role identity, access, lifecycle,
historical attribution, discovery, routing, harness behavior, tests, retained
evidence, scientific source, dependencies, or protected-execution authority.
The later live-discovery, historical-retirement, and delegation-validation
stages remain proposed and unauthorized.

## Validation and rollback

Focused validation checks the ownership manifest, exact front matter, the
[self](./ksdft2effmass.harness.010.030.020.md) and
[parent](./ksdft2effmass.harness.010.030.000.md) links, relative links on the
owned pages, unchanged inventory totals, absence of links to nonexistent planned
children, capability registration, and whitespace errors. These structural
checks do not establish scientific validity or human acceptance.

Rollback restores the prior `ksdft2effmass-tests` record, removes this page, and
restores the [parent](./ksdft2effmass.harness.010.030.000.md) and
[current inventory](./ksdft2effmass.harness.001.050.000.md) descriptions. It
does not rewrite historical agents or retained evidence and does not affect the
four unchanged project roles.
