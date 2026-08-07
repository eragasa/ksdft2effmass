---
document_id: ksdft2effmass.harness.010.030.000
task_id: harness-simplification.agents
parent: ksdft2effmass.harness.010.000.000
status: proposed
sphinx: excluded
---

# Durable agent architecture

> **Incremental architecture.** The five durable project roles and five durable
> harness roles exist. The durable harness-role creation and the bounded
> `ksdft2effmass-tests` simplification are current; all later migration steps
> remain proposed and require separate authorization.

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

These agents continue to load project specifications and domain skills. They do
not acquire generic harness implementation authority merely because a task uses
the harness.

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
completes only the concise stable capability definition for
`ksdft2effmass-tests`; the other four durable project roles are unchanged.
Live-discovery changes, historical-agent retirement, and delegation and handoff
validation remain proposed and unauthorized. Existing historical identities
remain present and retained evidence remains historically accurate.

See [current agents and ownership](./ksdft2effmass.harness.001.050.000.md) and the
[simplification overview](./ksdft2effmass.harness.010.000.000.md).
