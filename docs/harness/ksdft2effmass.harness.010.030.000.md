---
document_id: ksdft2effmass.harness.010.030.000
task_id: harness-simplification.agents
parent: ksdft2effmass.harness.010.000.000
status: proposed
sphinx: excluded
---

# Durable agent architecture

> **Incremental architecture.** The five durable project roles and five durable
> harness roles exist. The bounded test, implementation, documentation, and
> integration-review simplifications are current. Architecture simplification,
> live discovery, historical retirement, and delegation validation remain
> proposed and require separate authorization.

The implemented durable sets provide stable capability identities. They are
available for explicit assignment but do not activate themselves, grant path
ownership, or provide acceptance. Task scope, owned paths, evidence requirements,
and completion commands remain external task and ownership data rather than
being copied into durable agent records.

## Project-agent set

The five existing durable project agents cover domain-facing work:

- architecture and scientific-boundary review;
- production implementation;
- test and numerical-evidence development;
- maintained documentation;
- independent integration review.

These agents retain only their stable broadly reusable skills. A task selects
supported subject-specific skills when needed; neither task routing nor use of
the harness expands an agent's authority or grants generic harness
implementation authority.

## Harness-agent set

The five durable harness roles cover reusable control-plane work:

- generic harness implementation;
- project-local harness composition;
- resource, schema, profile, and skill maintenance;
- evidence and test-evidence maintenance;
- control-plane documentation;
- independent architecture, evidence, and integration review.

## Request-time specialization

A task request or ownership manifest supplies:

- immutable task and attempt identities;
- exact input artifacts;
- writer and reviewer roles;
- explicit paths and protected exclusions;
- expected output shape;
- focused validation and full reconciliation commands;
- stop and correction-cycle policy.

This keeps durable role meaning stable while preserving narrow task authority.
An agent file still would not activate work or provide acceptance.

## Migration status

The first child, [Create durable harness roles](./ksdft2effmass.harness.010.030.010.md),
is complete. The second child, [Simplify durable project roles](./ksdft2effmass.harness.010.030.020.md),
records the current concise capability definitions for the test,
implementation, documentation, and integration-review roles. The architecture
role is unchanged. Architecture simplification, live-discovery changes,
historical-agent retirement, and delegation and handoff validation remain
proposed and unauthorized. Existing historical identities remain present and
retained evidence remains historically accurate.

See [current agents and ownership](./ksdft2effmass.harness.001.050.000.md) and the
[simplification overview](./ksdft2effmass.harness.010.000.000.md).
