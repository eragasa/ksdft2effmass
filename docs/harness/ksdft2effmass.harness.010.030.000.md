---
document_id: ksdft2effmass.harness.010.030.000
task_id: harness-simplification.agents
parent: ksdft2effmass.harness.010.000.000
status: proposed
sphinx: excluded
---

# Durable agent architecture

> **Incremental architecture.** The first bounded child creates durable harness
> capability roles. Project-role simplification, discovery changes, and historical
> retirement remain proposed and require separate authorization.

The proposal replaces repeated phase-numbered role files with two small durable
sets. Task scope, owned paths, evidence requirements, and completion commands
would remain in task and ownership data rather than being copied into agent
prompts.

## Project-agent set

Durable project agents would cover domain-facing work:

- architecture and scientific-boundary review;
- production implementation;
- test and numerical-evidence development;
- maintained documentation;
- independent integration review.

These agents would continue to load project specifications and domain skills.
They would not acquire generic harness implementation authority merely because a
task uses the harness.

## Harness-agent set

Durable harness agents would cover reusable control-plane work:

- generic harness implementation;
- project-local harness composition;
- resource, schema, profile, and skill maintenance;
- evidence and test-evidence maintenance;
- control-plane documentation;
- independent architecture, evidence, and integration review.

## Request-time specialization

A task request or ownership manifest would supply:

- immutable task and attempt identities;
- exact input artifacts;
- writer and reviewer roles;
- explicit paths and protected exclusions;
- expected output shape;
- focused validation and full reconciliation commands;
- stop and correction-cycle policy.

This keeps durable role meaning stable while preserving narrow task authority.
An agent file still would not activate work or provide acceptance.

## Migration requirement

Existing agents should be mapped to durable roles before any retirement. During
the transition, old and new role resolution would be compared on representative
requests. Historical agent identities remain in retained evidence.

The implemented first child is [Create durable harness roles](./ksdft2effmass.harness.010.030.010.md).
It creates only reusable future assignment targets; the remaining migration
children stay proposed and unauthorized.

See [current agents and ownership](./ksdft2effmass.harness.001.050.000.md) and the
[simplification overview](./ksdft2effmass.harness.010.000.000.md).
