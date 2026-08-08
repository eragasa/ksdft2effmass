---
document_id: ksdft2effmass.harness.010.030.000
task_id: harness-simplification.agents
parent: ksdft2effmass.harness.010.000.000
status: proposed
sphinx: excluded
---

# Durable agent architecture

> **Incremental architecture.** Five durable project roles and five durable
> harness roles exist. Their bounded simplification and the executable harness-tool
> placement contract are complete. One validator migration pilot remains the next
> ordered `inactive_unauthorized` proposal and has not begun.

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

These agents retain stable capability rather than task-specific paths,
deliverables, commands, or permissions. A task and its ownership assignment
supply those details and may select supported subject-specific skills when
needed. The architecture role's sole durable skill routing is
`develop-architecture-decision`. Neither routing nor use of the harness expands
an agent's authority or grants generic harness implementation authority.

## Harness-agent set

The five durable harness roles cover reusable control-plane work:

- generic harness implementation;
- project-local harness composition;
- resource, schema, profile, and skill maintenance;
- evidence and test-evidence maintenance;
- control-plane documentation;
- independent architecture, evidence, and integration review.

## Request-time specialization

Durable records supply capability, access mode, stable responsibility, and
authority boundaries. A task request or ownership manifest supplies:

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

[harness.010.030.010](./ksdft2effmass.harness.010.030.010.md) created the five
durable harness roles. [harness.010.030.020](./ksdft2effmass.harness.010.030.020.md)
records the completed simplification of all five durable project roles,
including the final architecture responsibility, proportional analysis, and
conditional exactly-three-alternative rule. That work changed no executable
harness behavior and performed no executable migration.

[harness.010.030.030](./ksdft2effmass.harness.010.030.030.md) records the
completed executable harness-tool placement contract, maintained-tool object
model, thin-wrapper boundary, and proportional execution and delegation rules.
It changes no executable harness behavior and migrates no script.

The chain retains `harness-simplification.agents.validator-migration-pilot` as
the next `inactive_unauthorized` entry with `record: null`; it is not activated
or begun. Live discovery, historical retirement, broader delegation validation,
SQLite or evidence-storage work, and later protected work remain inactive and
proposed. Existing historical identities remain present and retained evidence
remains historically accurate.

See [harness.001.050.000](./ksdft2effmass.harness.001.050.000.md) and
[harness.010.000.000](./ksdft2effmass.harness.010.000.000.md).
